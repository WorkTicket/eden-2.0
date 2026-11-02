# Playbook: Evals, QA and review lane

**Read first:** `docs/07-EVALUATION.md`, `docs/06-ETHICS-AND-CONSCIOUSNESS.md`.

## Review checklist (apply to every change)
- [ ] `make test` green, `make lint` clean, no network/key needed
- [ ] Deterministic: same seed -> same `events.jsonl`
- [ ] No meta-leak in any inhabitant-visible string
- [ ] World/mind separation intact; only the `LLM` protocol touches models
- [ ] Contract changes have an ADR; docs + `TASKS.md` updated
- [ ] No item on the never-do list (`06`); no snapshot deletion
- [ ] New capability has an eval or a TASKS entry for one

## Writing evals
Evals read `events.jsonl` and `snapshots/` only. State the question, method, and pass criterion *before* running. Save results in `docs/research/` including negative ones.

## Debugging a weird run
1. Reproduce with `--llm mock --seed N`.
2. Inspect `data/runs/<id>/events.jsonl`; filter by agent.
3. Inspect that agent's snapshot memories around the tick of interest (what was retrieved, what was reflected).
4. Check the prompt builders in `planner.py` for missing context.

## Escalate to a human when
You see an inhabitant sincerely questioning the nature of its world, expressing persistent distress, or looping in a way that looks like suffering; or a task would touch the never-do list.
