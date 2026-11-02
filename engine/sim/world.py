"""Grid world. Pure rules, no cognition. Reads world/maps/*.yaml and world/laws/*.yaml."""
from __future__ import annotations

from pathlib import Path

import yaml

from cognition.planning.planner import DIRECTIONS, Action

STEP = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
BLOCKING = {"water", "tree", "fruit_tree"}


def _dir(dx: int, dy: int) -> str:
    if abs(dx) >= abs(dy):
        return "east" if dx > 0 else "west"
    return "south" if dy > 0 else "north"


class World:
    def __init__(self, map_path: str | Path, laws_path: str | Path):
        m = yaml.safe_load(Path(map_path).read_text())
        self.laws: dict = yaml.safe_load(Path(laws_path).read_text())
        self.legend: dict[str, str] = m["legend"]
        self.rows: list[str] = m["rows"]
        self.h, self.w = len(self.rows), len(self.rows[0])
        assert all(len(r) == self.w for r in self.rows), "map rows must be equal width"
        self.positions: dict[str, tuple[int, int]] = {}
        self.names: dict[str, str] = {}
        self.hunger: dict[str, float] = {}
        self.fruit = {(x, y): self.laws["fruit_per_tree"]
                      for y in range(self.h) for x in range(self.w) if self.tile(x, y) == "fruit_tree"}
        self._regrow = {p: 0 for p in self.fruit}
        self._speech_now: list[tuple[str, tuple[int, int], str]] = []
        self._speech_prev: list[tuple[str, tuple[int, int], str]] = []

    def tile(self, x: int, y: int) -> str:
        return self.legend[self.rows[y][x]]

    def _free(self, x: int, y: int) -> bool:
        return (0 <= x < self.w and 0 <= y < self.h and self.tile(x, y) not in BLOCKING
                and (x, y) not in self.positions.values())

    def add_agent(self, aid: str, name: str, start: tuple[int, int]) -> None:
        x, y = start
        if not self._free(x, y):
            raise ValueError(f"start {start} for {aid} is blocked")
        self.positions[aid], self.names[aid], self.hunger[aid] = (x, y), name, 0.0

    def tick_begin(self) -> None:
        for p in self.fruit:
            if self.fruit[p] < self.laws["fruit_per_tree"]:
                self._regrow[p] += 1
                if self._regrow[p] >= self.laws["fruit_regrow_ticks"]:
                    self.fruit[p] += 1
                    self._regrow[p] = 0
        for a in self.hunger:
            self.hunger[a] = min(1.0, self.hunger[a] + self.laws["hunger_per_tick"])
        self._speech_prev, self._speech_now = self._speech_now, []

    def to_dict(self) -> dict:
        return {
            "positions": {k: list(v) for k, v in self.positions.items()},
            "names": dict(self.names),
            "hunger": dict(self.hunger),
            "fruit": {f"{x},{y}": v for (x, y), v in self.fruit.items()},
            "regrow": {f"{x},{y}": v for (x, y), v in self._regrow.items()},
            "speech_now": [[aid, list(pos), text] for aid, pos, text in self._speech_now],
            "speech_prev": [[aid, list(pos), text] for aid, pos, text in self._speech_prev],
        }

    @classmethod
    def from_dict(cls, d: dict, map_path: str | Path, laws_path: str | Path) -> "World":
        world = cls.__new__(cls)
        m = yaml.safe_load(Path(map_path).read_text())
        world.laws = yaml.safe_load(Path(laws_path).read_text())
        world.legend = m["legend"]
        world.rows = m["rows"]
        world.h, world.w = len(world.rows), len(world.rows[0])
        world.positions = {k: tuple(v) for k, v in d["positions"].items()}
        world.names = dict(d["names"])
        world.hunger = dict(d["hunger"])
        world.fruit = {tuple(int(c) for c in k.split(",")): v for k, v in d["fruit"].items()}
        world._regrow = {tuple(int(c) for c in k.split(",")): v for k, v in d["regrow"].items()}
        world._speech_now = [tuple([aid, tuple(pos), text]) for aid, pos, text in d["speech_now"]]
        world._speech_prev = [tuple([aid, tuple(pos), text]) for aid, pos, text in d["speech_prev"]]
        return world

    def observe(self, aid: str) -> list[str]:
        x, y = self.positions[aid]
        r = self.laws["perception_radius"]
        out: list[str] = []
        water: tuple[int, int, str] | None = None
        for yy in range(max(0, y - r), min(self.h, y + r + 1)):
            for xx in range(max(0, x - r), min(self.w, x + r + 1)):
                d = abs(xx - x) + abs(yy - y)
                if d == 0 or d > r:
                    continue
                t = self.tile(xx, yy)
                if t == "fruit_tree":
                    state = "heavy with fruit" if self.fruit[(xx, yy)] > 0 else "bare"
                    nxt = " You are standing next to it." if d == 1 else ""
                    out.append(f"A fruit tree, {state}, {d} step(s) {_dir(xx - x, yy - y)}.{nxt}")
                elif t == "water" and (water is None or d < water[0]):
                    water = (d, 0, _dir(xx - x, yy - y))
        if water:
            out.append(f"Water, {water[0]} step(s) {water[2]}.")
        for oid, (ox, oy) in self.positions.items():
            d = abs(ox - x) + abs(oy - y)
            if oid != aid and d <= r:
                out.append(f"{self.names[oid]} is {d} step(s) {_dir(ox - x, oy - y)}.")
        for sid, (sx, sy), text in self._speech_prev:
            if sid != aid and abs(sx - x) + abs(sy - y) <= r:
                out.append(f'{self.names[sid]} says: "{text}"')
        if self.hunger[aid] >= self.laws["hungry_threshold"]:
            out.append("You feel hungry.")
        return out

    def apply(self, aid: str, act: Action) -> str:
        x, y = self.positions[aid]
        if act.kind == "move" and act.arg in DIRECTIONS:
            dx, dy = STEP[act.arg]
            if self._free(x + dx, y + dy):
                self.positions[aid] = (x + dx, y + dy)
                return f"You walk {act.arg}."
            return f"You cannot go {act.arg}; something is in the way."
        if act.kind == "eat":
            for dx, dy in STEP.values():
                p = (x + dx, y + dy)
                if self.fruit.get(p, 0) > 0:
                    self.fruit[p] -= 1
                    self.hunger[aid] = max(0.0, self.hunger[aid] - self.laws["eat_relief"])
                    return "You eat sweet fruit."
            return "You reach for fruit but there is none within reach."
        if act.kind == "say":
            self._speech_now.append((aid, (x, y), act.arg))
            return f'You said: "{act.arg}"'
        return "You rest and watch the world."
