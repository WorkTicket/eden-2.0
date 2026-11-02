---
description: Run the mock simulation and summarize behavior
argument-hint: [ticks] [seed]
---
Run `python -m engine.sim.runner --ticks ${1:-100} --llm mock --seed ${2:-0}` then `make eval`.
Summarize per-inhabitant metrics in a short table. Flag degenerate behavior (action entropy near 0, tiny cells_visited, no reflections). Do NOT run with `--llm anthropic` unless the user explicitly asks.
