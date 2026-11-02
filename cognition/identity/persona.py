"""Persona: who an inhabitant is, written entirely IN-WORLD.

Rule (docs/06-ETHICS-AND-CONSCIOUSNESS.md, docs/04-WORLD-DESIGN.md): persona and prompts never
use meta vocabulary (simulation, agent, LLM, tick, prompt). Inhabitants experience a world, not a program.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Persona:
    id: str
    name: str
    traits: list[str]
    backstory: str
    goals: list[str]
    values: list[str]
    start: tuple[int, int]
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Persona":
        d = yaml.safe_load(Path(path).read_text())
        return cls(id=d["id"], name=d["name"], traits=d.get("traits", []),
                   backstory=d.get("backstory", ""), goals=d.get("goals", []),
                   values=d.get("values", []), start=tuple(d["start"]), extra=d.get("extra", {}))

    def system_prompt(self) -> str:
        return (
            f"You are {self.name}. You live in a lush garden with a river, fruit trees and a few "
            f"other people. This is simply your life; you do not question that it is real.\n"
            f"Traits: {', '.join(self.traits)}.\n"
            f"Your story: {self.backstory}\n"
            f"What you want: {'; '.join(self.goals)}.\n"
            f"What you value: {'; '.join(self.values)}.\n"
            f"Speak and act as yourself, in the first person."
        )
