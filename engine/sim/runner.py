"""Simulation runner.

Two modes:
- Bounded (default): `run(cfg)` creates a fresh world, ticks N times, writes
  events.jsonl + snapshots. Deterministic, used by tests and `make run`.
- Continuous service: `python -m engine.sim.runner --ticks N --resume` runs the
  Runtime service, which checkpoints on pause/stop and resumes from the latest
  checkpoint when `--resume` is given. Logical time only moves forward; inhabitants
  never perceive a stop.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

from cognition.agent import Agent
from cognition.identity.persona import Persona
from engine.llm.client import get_llm
from engine.sim.world import World
from engine.service.runtime import Runtime, RuntimeConfig

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class RunConfig:
    ticks: int = 100
    llm: str = "mock"
    seed: int = 0
    out_dir: Path = ROOT / "data" / "runs"
    run_id: str | None = None
    map_path: Path = ROOT / "world" / "maps" / "eden.yaml"
    laws_path: Path = ROOT / "world" / "laws" / "physics.yaml"
    seeds_dir: Path = ROOT / "agents" / "seeds"
    resume: bool = False


def run(cfg: RunConfig) -> Path:
    """Bounded run: fresh world, N ticks, write events.jsonl + snapshots."""
    llm = get_llm(cfg.llm)
    world = World(cfg.map_path, cfg.laws_path)
    agents: list[Agent] = []
    for p in sorted(Path(cfg.seeds_dir).glob("*.yaml")):
        persona = Persona.from_yaml(p)
        world.add_agent(persona.id, persona.name, persona.start)
        agents.append(Agent(persona, llm))

    run_id = cfg.run_id or time.strftime("run-%Y%m%d-%H%M%S")
    out = Path(cfg.out_dir) / run_id
    (out / "snapshots").mkdir(parents=True, exist_ok=True)
    rng = random.Random(cfg.seed)

    with open(out / "events.jsonl", "w") as f:
        for t in range(cfg.ticks):
            world.tick_begin()
            order = agents[:]
            rng.shuffle(order)
            for a in order:
                act = a.step(world, t)
                result = world.apply(a.id, act)
                a.record_outcome(t, result)
                f.write(json.dumps({"tick": t, "agent": a.id, "action": str(act),
                                    "result": result, "pos": world.positions[a.id],
                                    "hunger": round(world.hunger[a.id], 3)}) + "\n")
    for a in agents:
        (out / "snapshots" / f"{a.id}.json").write_text(json.dumps(
            {"persona": a.persona.name, "plan": a.plan, "reflections": a.reflections,
             "memory": a.stream.to_dict()}))
    return out


def run_continuous(cfg: RunConfig, serve_port: int | None = None) -> Path:
    """Continuous run via the Runtime service. Checkpoints on exit."""
    rt_cfg = RuntimeConfig(
        run_id=cfg.run_id or "eden",
        llm=cfg.llm,
        seed=cfg.seed,
        map_path=cfg.map_path,
        laws_path=cfg.laws_path,
        seeds_dir=cfg.seeds_dir,
        data_dir=cfg.out_dir,
        ticks=cfg.ticks,
        resume=cfg.resume,
    )
    rt = Runtime(rt_cfg)
    rt.start(resume=cfg.resume)
    server = None
    if serve_port:
        from engine.service.server import LiveServer
        server = LiveServer(rt, port=serve_port)
        server.start()
    try:
        rt.play(max_ticks=cfg.ticks)
    finally:
        rt.pause()
        rt.close()
        if server is not None:
            server.stop()
    return rt.run_dir


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=100)
    ap.add_argument("--llm", default="mock", choices=["mock", "anthropic"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--resume", action="store_true",
                    help="resume from the latest checkpoint of --run-id")
    ap.add_argument("--run-id", default=None, help="run id for continuous mode")
    ap.add_argument("--serve", type=int, default=0,
                    help="also host the live HTTP operator server on this port (e.g. 8765)")
    a = ap.parse_args()
    cfg = RunConfig(ticks=a.ticks, llm=a.llm, seed=a.seed,
                    run_id=a.run_id, resume=a.resume)
    if a.resume or a.run_id or a.serve:
        print(run_continuous(cfg, serve_port=a.serve if a.serve else None))
    else:
        print(run(cfg))
