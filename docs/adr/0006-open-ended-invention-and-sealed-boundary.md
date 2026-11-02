# ADR-0006: Open-ended invention, richer senses, and the sealed boundary (PROPOSED)

- **Status:** proposed. **Needs owner sign-off** because it refines the decision in ADR-0005.
- **Date:** 2026-11-02

## Context
The owner wants inhabitants who can invent, perceive through all human senses, feel the full human emotional range, and build a civilization. The owner also floated that a determined inhabitant might work out what its world is by inventing things.

## Proposed decisions
1. **Invention** is adjudicated by a Game Master (Concordia pattern) against the world's physics. Accepted inventions are appended to a persistent registry (recipes, tools, structures) usable by everyone. Seed data: `world/resources/`.
2. **Senses:** observations expand to sight, sound, smell, touch and taste, always phrased as experience.
3. **Sealed boundary (architectural, not deceptive):** every action passes through the `apply(Action)` interface. No invention, structure or text can reach engine internals, the logs, or anything outside the world. Inhabitants can discover the world's *internal laws* by experiment (in-world science) and may *reason toward* what the world is, but nothing in the world states or confirms it.
4. **Amendment to ADR-0005:** "inhabitants must not be able to learn the nature of their world" becomes "inhabitants are never told or shown it; we do not prevent inference." If one infers it, that is logged as a significant event and escalated to the owner per `06`; it is not scrubbed from memory and no cover story is invented.
5. **Affect:** a functional emotion system with the full range may be built, but only after welfare monitors (T-206) exist. We do not engineer triggers for distress, and the never-do list in `06` still applies.
6. **Population growth** stays gated (see `docs/10`).

## Consequences
+ Richer, more open-ended science and culture; consistent with "we can wonder but not step outside".
+ Clear, testable security boundary.
- A Game Master is an LLM and can be inconsistent; the registry and physics checks are mandatory to keep discovery meaningful.
- Higher cost per invention call; mitigated by caching and registry reuse.
- Raises the stakes on welfare; the build order in `docs/05-ROADMAP.md` puts monitors first.

## Alternatives
Fixed action set only (no invention); fully scripted tech tree gating (rejected: contradicts open-endedness); letting inventions touch the engine (rejected: breaks the boundary and the logs).
