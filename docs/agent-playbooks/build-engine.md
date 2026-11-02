# Playbook: Engine lane (`engine/sim`, `engine/llm`)

**Read first:** `CLAUDE.md`, `docs/01-ARCHITECTURE.md`, ADR-0002, ADR-0003.

## You own
Runner loop, world rules plumbing, LLM client/backends, logging, snapshots, (later) viewer.

## Checklist for any change
1. Does it alter a contract (`observe`, `apply`, `Action`, `LLM`, log/snapshot format)? -> ADR first.
2. Keep determinism: seeded RNG only, no wall-clock in logic (run ids may use time).
3. Keep `MockLLM` working for every new `task=` kind you add (return something parseable).
4. Add/adjust tests in `tests/`; `make test`, `make run`, `make eval`.
5. Update `docs/01-ARCHITECTURE.md` if the diagram changes and `docs/TASKS.md`.

## Recipes
**Add an LLM backend:** new class in `engine/llm/client.py` implementing `complete` + `embed`, lazy import, register in `get_llm`, add to `--llm` choices in `runner.py`. Never import the SDK at module top level.

**Add a log field:** extend the event dict in `runner.py`, update `evals/eval_basic.py` if needed, keep old fields (evals and the future viewer read them).

**Add snapshot loading (T-108):** `Agent.from_snapshot(path, llm)` using `MemoryStream.from_dict`; runner flag `--resume <run_id>`; test that resumed + continued == uninterrupted for N ticks under the mock.

**Track usage (T-102):** wrap the client to count input/output tokens per `task`; write `usage.json`.
