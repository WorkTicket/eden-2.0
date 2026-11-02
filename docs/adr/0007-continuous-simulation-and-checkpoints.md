# ADR-0007: Continuous simulation with play/pause and checkpoint persistence

- **Status:** accepted
- **Date:** 2026-11-02

## Context
The original `run()` executes a bounded number of ticks in one process then exits; there is no way to pause and later resume a continuing world. Inhabitants must never perceive time going backward or a gap when the runtime is stopped and restarted.

## Decision
Introduce a `Runtime` service (`engine/service/runtime.py`) owning the world, agents, logical clock (`engine/sim/clock.py`), RNG and LLM. Logical time advances only while playing; `pause()` checkpoints atomically and `resume()` loads the latest checkpoint and continues exactly where it left off. Time only moves forward.

Persistence uses SQLite (`engine/persistence/store.py`) with:
- an append-only `events` table (authoritative log, JSONL export remains available),
- versioned `checkpoints` that are archived rather than overwritten (previous live checkpoint archived on each save),
- a `meta` table recording schema version (mismatch rejected).

`World` and `Agent` gained `to_dict`/`from_dict` so full state (positions, hunger, fruit, regrow, speech buffer, memory stream, plans, reflections, previous observations) round-trips. The runner keeps bounded mode (`run()`) unchanged and adds continuous mode (`run_continuous`, `--resume`) plus an optional live HTTP operator server (`engine/service/server.py`, `/state`, `/events`, `/control`, `/export`).

## Consequences
+ Pause/resume preserves the complete world and unfinished work; mock determinism is preserved via seeded RNG state saved in checkpoints.
+ Inhabitants never observe a stop; no rewinding.
+ Checkpoints are archived, enabling recovery from a corrupt latest checkpoint.
- A resume is only as faithful as the serialized state; any new mutable field must be added to `to_dict`/`from_dict` or it will be lost on restore.
- Schema changes require a migration path or a new schema version.

## Alternatives
- Rebuild a continuing person from the seed persona alone (rejected: loses memory, beliefs, goals, and unfinished work; violates plan section 5).
- JSONL-only persistence (rejected: no atomic, random-access checkpoints; slower restore).
