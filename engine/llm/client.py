"""LLM abstraction. ALL cognition code talks to this interface only (see ADR-0003).

MockLLM is deterministic and free: use it for tests, CI, and engine development.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from typing import Protocol

EMBED_DIM = 128
_WORD = re.compile(r"[a-z']+")


def hash_embed(text: str, dim: int = EMBED_DIM) -> list[float]:
    """Cheap bag-of-words hashing embedding. Placeholder until a real embedder is chosen."""
    vec = [0.0] * dim
    for w in _WORD.findall(text.lower()):
        vec[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class LLM(Protocol):
    def complete(self, system: str, prompt: str, max_tokens: int = 200, task: str = "act") -> str: ...
    def embed(self, text: str) -> list[float]: ...


class MockLLM:
    ACTIONS = [
        "move east", "move south", "say Hello, friend.", "eat", "wait",
        "move north", "move west", "say The fruit here is sweet.",
    ]

    def __init__(self) -> None:
        self._n = 0  # call counter: keeps runs deterministic but stops identical prompts looping forever

    def complete(self, system: str, prompt: str, max_tokens: int = 200, task: str = "act") -> str:
        self._n += 1
        h = int(hashlib.md5(f"{self._n}|{system}|{prompt}".encode()).hexdigest(), 16)
        if task == "rate":
            return str(1 + h % 10)
        if task == "reflect":
            return "I notice my days follow a gentle pattern.\nI value the company of others."
        if task == "plan":
            return "wake and look around\nforage for fruit\nfind someone to talk to\nrest"
        return self.ACTIONS[h % len(self.ACTIONS)]

    def embed(self, text: str) -> list[float]:
        return hash_embed(text)


class AnthropicLLM:
    def __init__(self, model: str | None = None):
        import anthropic  # optional dependency

        self.client = anthropic.Anthropic()
        self.model = model or os.environ.get("EDEN_MODEL", "claude-haiku-5-5")

    def complete(self, system: str, prompt: str, max_tokens: int = 200, task: str = "act") -> str:
        r = self.client.messages.create(
            model=self.model, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")

    def embed(self, text: str) -> list[float]:
        return hash_embed(text)  # TODO(ADR-0004): replace with a real embedding provider


def get_llm(name: str) -> LLM:
    if name == "mock":
        return MockLLM()
    if name == "anthropic":
        return AnthropicLLM()
    raise ValueError(f"unknown llm backend: {name}")
