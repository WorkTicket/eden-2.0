# Playbook: Cognition lane (`cognition/`)

**Read first:** `CLAUDE.md`, `docs/03-COGNITIVE-ARCHITECTURE.md`, `docs/06-ETHICS-AND-CONSCIOUSNESS.md`.

## You own
Memory, perception, reflection, planning, identity, `Agent` wiring.

## Rules
- Talk to models only via the `LLM` protocol, with an explicit `task=` label.
- Every prompt the inhabitant "reads" is in-world. No meta vocabulary. `tests/test_no_leaks.py` must stay green.
- Structured outputs get strict parsers with a safe fallback (`wait`).
- Each new module: (a) hook in `Agent.step`, (b) mock behavior, (c) unit test, (d) an eval in `evals/` or a TASKS entry for one, (e) a row in `docs/03` stating which theory-inspired feature it implements.
- Affect, self-model and relationship modules touch welfare: re-read `06` and add monitoring hooks (T-206).

## Recipe: add a cognitive module
1. Create `cognition/<name>/<name>.py` with pure functions taking `(llm, persona, stream, ...)`.
2. Store outputs as memories with a distinct `kind` so retrieval and evals can filter.
3. Wire into `Agent.step` behind a clearly named trigger (threshold or schedule).
4. Extend `MockLLM.complete` to return a parseable response for the new `task`.
5. Tests: deterministic given the mock; assert memory side effects.

## Recipe: change retrieval
Change weights/decay only with an eval (T-107) showing improvement. Record before/after in `docs/research/`.

## Pitfalls
Min-max normalizing recency (see doc 03); memory spam from repeated observations (use `perceive`); unbounded prompts (cap k); reflections that invent events (T-106 checks grounding).
