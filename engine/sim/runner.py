"""Simulation runner. `python -m engine.sim.runner --ticks 100 --llm mock`"""
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


def run(cfg: RunConfig) -> Path:
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=100)
    ap.add_argument("--llm", default="mock", choices=["mock", "anthropic"])
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    print(run(RunConfig(ticks=a.ticks, llm=a.llm, seed=a.seed)))
