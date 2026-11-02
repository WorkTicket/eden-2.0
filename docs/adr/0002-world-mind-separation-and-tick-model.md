# ADR-0002: World/mind separation and a synchronous tick model

- **Status:** accepted
- **Date:** 2026-11-02

## Context
We want to swap worlds (grid -> 3D) and minds independently, and to debug deterministically.

## Decision
`engine/sim/world.py` is pure rules and never calls an LLM. Minds interact only via `observe(aid) -> list[str]` and `apply(aid, Action) -> str`. The loop is synchronous: per tick, shuffle agents with the seeded RNG, each observes, decides, acts.

## Consequences
+ Deterministic replay with the mock LLM; simple tests.
+ Backend swaps (Luanti/Godot) need only an adapter implementing the two methods.
- Real-time/concurrent cognition (Project Sid style) needs a new ADR.

## Alternatives
Async per-agent loops (harder to debug); shared mutable world accessed by minds directly (couples everything).
