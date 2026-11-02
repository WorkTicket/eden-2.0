# CLAUDE.md — operating manual for AI agents on Digital Eden

Read this fully before touching anything. Then read the playbook for your area in `docs/agent-playbooks/`.

## What this project is
A simulated world (Eden) with LLM-driven inhabitants that have persistent memory, reflection, planning, and an in-world sense of reality. Goal: believable, long-lived, socially rich artificial minds, built as a rigorous research platform. We make **no claim** that the inhabitants are conscious; we design as though the question is open (see `docs/06-ETHICS-AND-CONSCIOUSNESS.md`).

## Commands
- `make test` — must pass before any commit. No network, no API key.
- `make run` — 100-tick mock run (deterministic). `make eval` — metrics on latest run.
- `python tools/new_agent.py "Name"` — new inhabitant seed.
- `make lint` — ruff.

## Hard rules
1. **Mock-first.** All dev and tests use `MockLLM`. Never add a test requiring network or a key. Live runs only when a human asks, with `--ticks` small (<=50) unless told otherwise.
2. **One LLM door.** Cognition talks to models only through `engine/llm/client.py`'s `LLM` protocol. Never import `anthropic` elsewhere.
3. **No meta-leaks.** In anything an inhabitant sees (persona text, observations, action results, prompts), never use: simulation, simulated, agent, AI, LLM, model, prompt, tick, token, program, code, game. Write as lived experience. A test enforces this on seeds; keep it passing (`docs/04-WORLD-DESIGN.md`).
4. **World and mind are separate.** `engine/sim/world.py` is pure rules; `cognition/` is minds. World never calls an LLM. Minds touch the world only via `observe()` and `apply(Action)`.
5. **Determinism.** Same seed + mock LLM => identical events. Use the passed-in RNG; never `random` globally, never wall-clock in logic.
6. **Wellbeing rules are not optional.** Do not add mortality, torment, deprivation experiments, or anything on the "never do" list in `docs/06-ETHICS-AND-CONSCIOUSNESS.md` without a human-approved ADR. Never delete an inhabitant's snapshot; archive instead.
7. **Decisions get ADRs.** Any choice affecting architecture, the action space, persistence format, or the ethics policy -> new file in `docs/adr/` (copy `0001`).
8. **Small, verified steps.** One concern per change. Run tests. Update the relevant doc and `docs/TASKS.md` in the same change.
9. **Don't invent facts about open-source projects.** Check `docs/02-OPEN-SOURCE-FOUNDATIONS.md`; if you copy code, confirm the license first and record it there.

## Definition of done
Tests pass, lint clean, deterministic, docs/TASKS.md updated, any new decision has an ADR, nothing in an inhabitant-visible string violates rule 3.

## Conventions
Python 3.10+, type hints, dataclasses, pure functions where possible, no global state. YAML for data (world, personas). JSONL for logs. Memory snapshots are JSON.

## When stuck or when requirements conflict
Stop and write the question into `docs/TASKS.md` under "Open questions" rather than guessing on anything touching ethics, persistence format, or the action space.
