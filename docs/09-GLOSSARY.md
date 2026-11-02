# 09 — Glossary

- **Inhabitant / agent:** an LLM-driven character with persona, memory, plans. ("Agent" is a builders' word; inhabitants never see it.)
- **Tick:** one simulation step. Builders' word; inhabitants experience time as days and moments.
- **Persona:** in-world identity text (traits, backstory, goals, values).
- **Memory stream:** append-only record of experiences, reflections, actions.
- **Reflection:** synthesized higher-level belief derived from memories.
- **Importance / recency / relevance:** the three retrieval signals.
- **Observation:** in-world sentence the world gives an inhabitant about what they perceive.
- **Action:** structured thing an inhabitant does: `move`, `say`, `eat`, `wait`.
- **Mock LLM:** deterministic, free stand-in model for tests and development.
- **Game Master:** (Concordia) a model that adjudicates free-form actions in the world.
- **ADR:** architecture decision record in `docs/adr/`.
- **Meta-leak:** inhabitant-visible text that references the machinery. Forbidden.
- **Snapshot:** serialized full state of an inhabitant; never deleted, only archived.
- **Moral patient:** a being whose experiences matter morally; whether inhabitants qualify is unknown.
