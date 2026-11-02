"""Reflection: periodically synthesize higher-level beliefs from recent experience."""
from __future__ import annotations

from cognition.identity.persona import Persona
from cognition.memory.stream import MemoryStream
from engine.llm.client import LLM

REFLECTION_THRESHOLD = 40.0  # summed importance since last reflection


def should_reflect(stream: MemoryStream, threshold: float = REFLECTION_THRESHOLD) -> bool:
    return stream.importance_since_reflection >= threshold


def reflect(llm: LLM, persona: Persona, stream: MemoryStream, tick: int, k: int = 12) -> int:
    recent = "\n".join(f"- {m.text}" for m in stream.recent(k))
    prompt = (f"Your recent experiences:\n{recent}\n\n"
              "What two or three deeper things do you realize about your life, yourself or the "
              "others? One short sentence per line.")
    text = llm.complete(persona.system_prompt(), prompt, max_tokens=200, task="reflect")
    lines = [ln.strip("-• ").strip() for ln in text.splitlines() if ln.strip()][:3]
    for ln in lines:
        stream.add(tick, "reflection", ln, importance=7)
    stream.reset_reflection_counter()
    return len(lines)
