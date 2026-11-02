"""Cheap behavioral metrics over a run: python evals/eval_basic.py data/runs/<run_id>

These are SANITY metrics (is anything alive-looking happening?), not evidence of consciousness.
See docs/07-EVALUATION.md for the real eval plan.
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

run = Path(sys.argv[1])
events = [json.loads(line) for line in open(run / "events.jsonl")]
by_agent = defaultdict(list)
for e in events:
    by_agent[e["agent"]].append(e)

for aid, evs in by_agent.items():
    kinds = Counter(e["action"].split()[0] for e in evs)
    total = sum(kinds.values())
    entropy = -sum(c / total * math.log2(c / total) for c in kinds.values())
    cells = {tuple(e["pos"]) for e in evs}
    snap = json.loads((run / "snapshots" / f"{aid}.json").read_text())
    print(f"{aid}: action_entropy={entropy:.2f} bits  cells_visited={len(cells)}  "
          f"memories={len(snap['memory']['items'])}  reflections={snap['reflections']}  "
          f"says={kinds.get('say', 0)}  eats={kinds.get('eat', 0)}")
