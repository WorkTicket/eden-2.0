"""Planning + action selection. Action space is small and structured on purpose (see world/laws)."""
from __future__ import annotations

import re
from dataclasses import dataclass

from cognition.identity.persona import Persona
from engine.llm.client import LLM

DIRECTIONS = ("north", "south", "east", "west")


@dataclass
class Action:
    kind: str  # move | say | eat | wait
    arg: str = ""

    def __str__(self) -> str:
        return f"{self.kind} {self.arg}".strip()


def parse_action(text: str) -> Action:
    line = (text.strip().splitlines() or [""])[0].strip().lower()
    m = re.match(r"move\s+(north|south|east|west)", line)
    if m:
        return Action("move", m.group(1))
    if line.startswith("say"):
        raw = text.strip().splitlines()[0].strip()[3:].strip().strip('"\'')
        return Action("say", raw[:200]) if raw else Action("wait")
    if line.startswith("eat"):
        return Action("eat")
    return Action("wait")


def plan_day(llm: LLM, persona: Persona, memories: list[str]) -> list[str]:
    mem = "\n".join(f"- {m}" for m in memories) or "- (a fresh morning)"
    prompt = f"What you remember:\n{mem}\n\nList 3-5 things you intend to do today, one per line."
    text = llm.complete(persona.system_prompt(), prompt, max_tokens=150, task="plan")
    return [ln.strip("-• 0123456789.").strip() for ln in text.splitlines() if ln.strip()][:5]


def decide(llm: LLM, persona: Persona, plan: list[str], memories: list[str],
           observations: list[str]) -> Action:
    prompt = (
        f"Today's intentions: {'; '.join(plan) or 'none yet'}\n"
        f"Relevant memories:\n" + "\n".join(f"- {m}" for m in memories) + "\n"
        "Right now:\n" + "\n".join(f"- {o}" for o in observations) + "\n\n"
        "Choose ONE action. Reply with only the action:\n"
        "move <north|south|east|west>\nsay <what you say aloud>\neat   (only next to a fruit tree with fruit)\nwait"
    )
    return parse_action(llm.complete(persona.system_prompt(), prompt, max_tokens=60, task="act"))
