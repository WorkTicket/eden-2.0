"""Perception filter: only genuinely new observations become memories (prevents memory spam)."""
from __future__ import annotations


def new_observations(previous: set[str], current: list[str]) -> list[str]:
    return [o for o in current if o not in previous]


def importance_heuristic(text: str) -> float:
    """Free, deterministic stand-in for LLM importance rating (1..10)."""
    t = text.lower()
    if "says:" in t:
        return 6
    if "hungry" in t:
        return 5
    if "you eat" in t or "you said" in t:
        return 4
    return 2
