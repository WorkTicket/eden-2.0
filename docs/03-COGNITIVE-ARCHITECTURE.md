# 03 — Cognitive architecture

## Implemented (v0.1)
**Perception** (`cognition/perception`): world observations are deduplicated against the last tick so only *changes* become memories.

**Memory stream** (`cognition/memory/stream.py`): append-only list of `Memory(kind, text, importance 1–10, embedding, last_access)`. Retrieval score = `1.0*recency + 1.0*importance/10 + 2.0*relevance`, where recency = `0.995^(ticks since last access)` and relevance = cosine similarity of embeddings. (Lesson learned: min-max normalizing recency over-weights tiny tick gaps.)

**Reflection** (`cognition/reflection`): when summed importance since the last reflection >= 40, ask the persona for 2–3 higher-level realizations over recent memories; store as `kind="reflection"` (importance 7). Reflections are retrievable like any memory, so beliefs compound.

**Planning** (`cognition/planning`): at the start of each in-world day (`day_length_ticks`), produce 3–5 intentions from retrieved memories. Each tick `decide()` picks one structured action given plan + memories + current observations.

**Identity** (`cognition/identity`): `Persona` renders an in-world system prompt (never meta vocabulary).

## Planned modules (see roadmap)
| Module | Purpose | Design sketch |
|---|---|---|
| Hierarchical plans | Day -> hour -> action, with re-planning on surprise | Plan tree stored as memories; interrupt when an observation contradicts the plan |
| Conversation | Multi-turn dialogue with shared context | Dialogue state per pair; summarize to memory at end |
| Relationships | Who do I trust / like / owe | Per-other semantic memory updated by reflection |
| Self-model | What I believe about my own traits, habits, history | Periodic "who am I" reflection; consistency check vs persona; allowed to *drift* (log drift) |
| Emotion/affect | Valence/arousal state biasing retrieval and action | Small state vector updated by events; included in prompts |
| Skill library | Reusable procedures (Voyager-style) | Named routines stored and retrieved |
| Consolidation/forgetting | Keep memory bounded and meaningful | Merge low-importance old observations into summaries; never delete reflections |
| Global-workspace style attention | A bottleneck that selects what is "in mind" | Top-k retrieval + current percepts -> single working context (this is what `decide` already approximates) |

## Why these? (and a caution)
Several scientific theories of consciousness (global workspace, higher-order, predictive processing, attention schema) emphasize things like a limited-capacity workspace, self-modeling, and prediction. Building toward them makes the system a *useful testbed*; it does **not** show consciousness. Document which theory-inspired feature each module implements so results can be compared honestly (`06-ETHICS-AND-CONSCIOUSNESS.md`).

## Prompting rules
- System prompt = persona only. Situation goes in the user prompt.
- Keep action prompts short; reply format strictly parsed, with safe fallback to `wait`.
- Everything the inhabitant reads is in-world. Test it.
- Temperature/model choices live in the LLM client, not in cognition.
