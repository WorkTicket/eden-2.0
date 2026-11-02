"""Integrity of the civilization data: every reference resolves, nothing is unobtainable, tech tree is acyclic."""
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[1] / "world" / "resources"


def _load():
    res = yaml.safe_load((R / "resources.yaml").read_text())
    rec = yaml.safe_load((R / "recipes.yaml").read_text())["recipes"]
    tech = yaml.safe_load((R / "tech_tree.yaml").read_text())["techs"]
    natural = {r["id"] for r in res["natural"]}
    made = {r["id"] for r in res["made"]}
    return natural, made, rec, tech


def test_recipe_references_resolve():
    natural, made, rec, _ = _load()
    known = natural | made
    for r in rec:
        for k in list(r["inputs"]) + list(r["output"]):
            assert k in known, f"{r['id']}: unknown item {k}"
        for k in (r.get("tool"), r.get("station")):
            assert k is None or k in known, f"{r['id']}: unknown tool/station {k}"


def test_every_made_item_is_producible_from_natural_items():
    natural, made, rec, _ = _load()
    producers = {}
    for r in rec:
        for out in r["output"]:
            producers.setdefault(out, []).append(r)
    assert made <= set(producers), f"no recipe for: {made - set(producers)}"
    obtainable = set(natural)
    changed = True
    while changed:
        changed = False
        for r in rec:
            needs = set(r["inputs"]) | {x for x in (r.get("tool"), r.get("station")) if x}
            if needs <= obtainable and not set(r["output"]) <= obtainable:
                obtainable |= set(r["output"])
                changed = True
    assert made <= obtainable, f"unreachable from raw resources: {made - obtainable}"


def test_tech_tree_is_valid_and_acyclic():
    _, made, rec, tech = _load()
    ids = {t["id"] for t in tech}
    rec_ids = {r["id"] for r in rec}
    for t in tech:
        assert set(t["requires"]) <= ids
        assert set(t["unlocks"]) <= (rec_ids | made), t["id"]
    seen, stack = set(), set()

    def visit(i):
        assert i not in stack, f"cycle at {i}"
        if i in seen:
            return
        stack.add(i)
        for p in next(t for t in tech if t["id"] == i)["requires"]:
            visit(p)
        stack.discard(i)
        seen.add(i)

    for i in ids:
        visit(i)
