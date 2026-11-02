"""Agent: wires perception -> memory -> (reflection, planning) -> action."""
from __future__ import annotations

from cognition.identity.persona import Persona
from cognition.memory.stream import MemoryStream
from cognition.perception.perceive import importance_heuristic, new_observations
from cognition.planning.planner import Action, decide, plan_day
from cognition.reflection.reflect import reflect, should_reflect
from engine.llm.client import LLM


class Agent:
    def __init__(self, persona: Persona, llm: LLM):
        self.persona = persona
        self.llm = llm
        self.id = persona.id
        self.stream = MemoryStream(llm)
        self.plan: list[str] = []
        self._prev_obs: set[str] = set()
        self.reflections = 0

    def step(self, world, tick: int) -> Action:
        obs = world.observe(self.id)
        for o in new_observations(self._prev_obs, obs):
            self.stream.add(tick, "observation", o, importance_heuristic(o))
        self._prev_obs = set(obs)

        day = world.laws.get("day_length_ticks", 48)
        query = " ".join(obs) or "my day"
        if tick % day == 0:
            self.plan = plan_day(self.llm, self.persona,
                                 [m.text for m in self.stream.retrieve(query, tick, k=6)])
        if should_reflect(self.stream):
            reflect(self.llm, self.persona, self.stream, tick)
            self.reflections += 1

        mems = [m.text for m in self.stream.retrieve(query, tick, k=8)]
        return decide(self.llm, self.persona, self.plan, mems, obs)

    def record_outcome(self, tick: int, result: str) -> None:
        self.stream.add(tick, "action", result, importance_heuristic(result))
