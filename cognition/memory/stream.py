"""Memory stream: append-only record of experience with recency/importance/relevance retrieval.

Design follows Park et al. 2023 (Generative Agents). See docs/03-COGNITIVE-ARCHITECTURE.md.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from engine.llm.client import LLM, cosine


@dataclass
class Memory:
    id: int
    tick: int
    kind: str  # observation | reflection | plan | action
    text: str
    importance: float  # 1..10
    embedding: list[float]
    last_access: int


def _norm(xs: list[float]) -> list[float]:
    lo, hi = min(xs), max(xs)
    return [0.5] * len(xs) if hi == lo else [(x - lo) / (hi - lo) for x in xs]


class MemoryStream:
    def __init__(self, llm: LLM, decay: float = 0.995):
        self.llm = llm
        self.decay = decay
        self.items: list[Memory] = []
        self.importance_since_reflection = 0.0

    def add(self, tick: int, kind: str, text: str, importance: float) -> Memory:
        m = Memory(len(self.items), tick, kind, text, float(importance), self.llm.embed(text), tick)
        self.items.append(m)
        if kind != "reflection":
            self.importance_since_reflection += importance
        return m

    def retrieve(self, query: str, now: int, k: int = 8) -> list[Memory]:
        if not self.items:
            return []
        q = self.llm.embed(query)
        # Raw 0..1 components. (Min-max normalizing recency exaggerates tiny tick gaps.)
        rec = [self.decay ** (now - m.last_access) for m in self.items]
        imp = [m.importance / 10 for m in self.items]
        rel = [cosine(q, m.embedding) for m in self.items]
        w_rec, w_imp, w_rel = 1.0, 1.0, 2.0
        scored = sorted(
            zip((w_rec * r + w_imp * i + w_rel * v for r, i, v in zip(rec, imp, rel)), self.items),
            key=lambda p: (-p[0], -p[1].id))
        top = [m for _, m in scored[:k]]
        for m in top:
            m.last_access = now
        return top

    def recent(self, n: int) -> list[Memory]:
        return self.items[-n:]

    def reset_reflection_counter(self) -> None:
        self.importance_since_reflection = 0.0

    def to_dict(self) -> dict:
        return {"decay": self.decay, "items": [asdict(m) for m in self.items],
                "importance_since_reflection": self.importance_since_reflection}

    @classmethod
    def from_dict(cls, llm: LLM, d: dict) -> "MemoryStream":
        s = cls(llm, d["decay"])
        s.items = [Memory(**m) for m in d["items"]]
        s.importance_since_reflection = d["importance_since_reflection"]
        return s
