"""Continuous simulation runtime service.

Play / pause model:
- The runtime owns the world, agents, logical clock, RNG, and LLM.
- `play()` ticks forward until paused, a tick budget is exhausted, or a stop is requested.
- `pause()` checkpoints atomically and stops. Logical time freezes; wall-clock keeps moving.
- `resume()` loads the latest checkpoint and continues exactly where it left off.
- Inhabitants never perceive a gap: time only ever moves forward.

The runner supports both bounded experiments (fixed tick count, fresh world) and the
live service (resume from checkpoint, run until paused).
"""
from __future__ import annotations

import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from cognition.agent import Agent
from cognition.identity.persona import Persona
from engine.llm.client import get_llm
from engine.persistence import CheckpointStore
from engine.sim.clock import Clock
from engine.sim.world import World

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class RuntimeConfig:
    run_id: str = "eden"
    llm: str = "mock"
    seed: int = 0
    map_path: Path = ROOT / "world" / "maps" / "eden.yaml"
    laws_path: Path = ROOT / "world" / "laws" / "physics.yaml"
    seeds_dir: Path = ROOT / "agents" / "seeds"
    data_dir: Path = ROOT / "data" / "runs"
    # Bounded mode: run N ticks then stop (fresh world unless resume=True).
    ticks: int | None = None
    resume: bool = False


class Runtime:
    """Authoritative simulation runtime with play/pause and checkpoint persistence."""

    def __init__(self, cfg: RuntimeConfig) -> None:
        self.cfg = cfg
        self.run_dir = cfg.data_dir / cfg.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.store = CheckpointStore(self.run_dir)
        self.llm = get_llm(cfg.llm)
        self.clock = Clock()
        self.rng = random.Random(cfg.seed)
        self.world: World | None = None
        self.agents: dict[str, Agent] = {}
        self.personas: dict[str, Persona] = {}
        self.seed_files: dict[str, Path] = {}
        self._playing = False
        self._stop = False
        self._seq = self.store.last_seq()
        self._initialized = False

    # ------------------------------------------------------------------ setup

    def _fresh_world(self) -> None:
        self.world = World(self.cfg.map_path, self.cfg.laws_path)
        self.agents = {}
        self.personas = {}
        for p in sorted(Path(self.cfg.seeds_dir).glob("*.yaml")):
            persona = Persona.from_yaml(p)
            self.world.add_agent(persona.id, persona.name, persona.start)
            self.personas[persona.id] = persona
            self.seed_files[persona.id] = p
            self.agents[persona.id] = Agent(persona, self.llm)
        self.clock = Clock()
        self.rng = random.Random(self.cfg.seed)
        self._seq = self.store.last_seq()
        self._initialized = True

    def _load_checkpoint(self, payload: dict[str, Any]) -> None:
        self.world = World.from_dict(payload["world"], self.cfg.map_path, self.cfg.laws_path)
        self.clock = Clock(tick=int(payload["clock"]["tick"]),
                           played_seconds=float(payload["clock"].get("played_seconds", 0.0)))
        seed = int(payload.get("seed", self.cfg.seed))
        self.rng = random.Random(seed)
        self.agents = {}
        self.personas = {}
        self.seed_files = {}
        for aid, ap in payload["agents"].items():
            sf = payload.get("seed_files", {}).get(aid) or Path(self.cfg.seeds_dir) / f"{aid}.yaml"
            persona = Persona.from_yaml(Path(sf))
            self.personas[aid] = persona
            self.seed_files[aid] = Path(sf)
            self.agents[aid] = Agent.from_dict(ap, persona, self.llm)
        self._seq = int(payload.get("seq", self.store.last_seq()))
        self._initialized = True

    # ---------------------------------------------------------------- control

    def start(self, resume: bool | None = None) -> None:
        """Begin or resume a run. If resume and a checkpoint exists, load it."""
        should_resume = self.cfg.resume if resume is None else resume
        if should_resume:
            cp = self.store.load_latest_checkpoint()
            if cp is not None:
                self._load_checkpoint(cp)
                return
        self._fresh_world()

    def playing(self) -> bool:
        return self._playing

    def tick(self, steps: int = 1) -> int:
        """Advance logical time by `steps` ticks. Returns ticks actually advanced."""
        if not self._initialized:
            self.start()
        advanced = 0
        for _ in range(steps):
            if self._stop:
                break
            self._tick_once()
            advanced += 1
        return advanced

    def _tick_once(self) -> None:
        t = self.clock.tick
        self.world.tick_begin()
        order = list(self.agents.values())
        self.rng.shuffle(order)
        for a in order:
            act = a.step(self.world, t)
            result = self.world.apply(a.id, act)
            a.record_outcome(t, result)
            pos = self.world.positions[a.id]
            hunger = self.world.hunger[a.id]
            self._seq += 1
            self.store.append_event(
                t, a.id, str(act), result, pos, hunger,
                {"plan": list(a.plan), "reflections": a.reflections},
            )
        self.clock.advance()

    def play(self, max_ticks: int | None = None, on_tick=None) -> int:
        """Play until paused, stopped, or max_ticks reached. Returns ticks advanced."""
        if not self._initialized:
            self.start()
        self._playing = True
        self._stop = False
        budget = max_ticks if max_ticks is not None else self.cfg.ticks
        advanced = 0
        start_wall = time.perf_counter()
        try:
            while self._playing and not self._stop:
                if budget is not None and advanced >= budget:
                    break
                self._tick_once()
                advanced += 1
                elapsed = time.perf_counter() - start_wall
                self.clock.played_seconds += elapsed
                start_wall = time.perf_counter()
                if on_tick is not None:
                    on_tick(self.clock.tick, self)
        finally:
            self._playing = False
        return advanced

    def pause(self) -> dict[str, Any] | None:
        """Checkpoint atomically and stop. Returns the checkpoint payload or None."""
        if not self._initialized:
            return None
        payload = self.snapshot()
        self.store.save_checkpoint(
            self.clock.tick, self._seq, payload, archive_previous=True
        )
        self._playing = False
        return payload

    def stop(self) -> None:
        self._stop = True
        self._playing = False

    # ---------------------------------------------------------------- introspection

    def snapshot(self) -> dict[str, Any]:
        """Full serializable state for checkpointing or read-only inspection."""
        if not self._initialized:
            return {}
        return {
            "schema_version": 1,
            "seed": self.cfg.seed,
            "clock": asdict(self.clock),
            "seq": self._seq,
            "world": self.world.to_dict(),
            "agents": {aid: a.to_dict() for aid, a in self.agents.items()},
            "seed_files": {aid: str(p) for aid, p in self.seed_files.items()},
        }

    def current_state(self) -> dict[str, Any]:
        """Read-only view of the current runtime (for the live viewer)."""
        if not self._initialized:
            return {"running": False, "tick": 0}
        return {
            "running": self._playing,
            "tick": self.clock.tick,
            "day": self.clock.day,
            "world": {
                "w": self.world.w, "h": self.world.h,
                "positions": {k: list(v) for k, v in self.world.positions.items()},
                "names": dict(self.world.names),
                "hunger": dict(self.world.hunger),
                "fruit": {f"{x},{y}": v for (x, y), v in self.world.fruit.items()},
            },
            "agents": {aid: {"plan": list(a.plan), "reflections": a.reflections}
                       for aid, a in self.agents.items()},
        }

    def recent_events(self, n: int = 50) -> list[dict[str, Any]]:
        """Most recent committed events (read-only)."""
        return self.store.load_events_after(max(0, self._seq - n))

    def close(self) -> None:
        self.store.close()
