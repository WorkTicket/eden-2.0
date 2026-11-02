# 07 — Evaluation

Evals answer "is it working?" with numbers. Each capability gets one before it ships. Cheap evals run on the mock LLM in CI; expensive ones are human-triggered.

## Tier 1 — Sanity metrics (exist now: `evals/eval_basic.py`)
Action entropy, cells visited, memory count, reflections, speech/eat counts. Detects dead or degenerate agents (the mock deliberately shows a degenerate case).

## Tier 2 — Capability evals (build in M1–M2)
| Eval | Method | Pass signal |
|---|---|---|
| Memory recall | After N ticks, ask the agent (in-world) about specific past events; score vs event log | >= 80% of salient events recalled correctly |
| Retrieval quality | Labeled set of (query, relevant memory); recall@k | recall@8 >= 0.8, tune weights |
| Reflection grounding | Each reflection must cite/relate to real memories; LLM or rubric judge | no fabricated events |
| Planning follow-through | Fraction of plan items attempted | > 60% without being rigid |
| Social diffusion | Seed one fact with one agent; measure spread through conversation | spreads, with realistic distortion |

## Tier 3 — Identity and believability (M3+)
| Eval | Method |
|---|---|
| Persona consistency | Interview at ticks 100/500/1000, judge traits/values stability vs justified change |
| Interview believability | Blind raters or judge-model rank agent answers vs human-written controls |
| Continuity across restart | Resume from snapshot; compare behavior distribution before/after |

## Tier 4 — Welfare monitors (M2+, see `06`)
Negative-valence persistence, distress expressions, isolation, loop detection. These are **safety instruments**, not benchmarks.

## Rules
- Pre-register: write the eval and pass criteria in the PR before running it.
- Evals read `events.jsonl` and `snapshots/`; they must not require changes to the sim.
- Report null and negative results in `docs/research/`.

## Cost budget (fill in with real numbers after the first live run)
Estimate = agents x ticks x (calls per tick) x tokens x price. Starting guidance: live runs <= 2 agents x 50 ticks until the cost per agent-tick is measured and recorded here. Log token usage per run in `data/runs/<id>/`.
