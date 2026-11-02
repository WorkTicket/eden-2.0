# TASKS

Status: `todo` | `in progress (who, date)` | `done`. Lanes: ENG, COG, WORLD, EVAL, DOCS. Update in the same change as the work.

## M1 — Real minds
| ID | Lane | Task | Status | Notes |
|---|---|---|---|---|
| T-101 | ENG | Run `make run-live` for 50 ticks, record token usage + cost per agent-tick in `07-EVALUATION.md` | todo | needs human with API key |
| T-102 | ENG | Log token usage per run to `data/runs/<id>/usage.json` | todo | |
| T-103 | COG | Replace hash embeddings with a real embedder behind `LLM.embed` (write ADR-0004) | todo | Anthropic has no embeddings endpoint; pick provider/local model |
| T-104 | COG | LLM-based importance scoring with heuristic fallback + caching | todo | |
| T-105 | COG | Conversation module: multi-turn dialogue, summarized into memory | todo | |
| T-106 | EVAL | Memory-recall eval (ask in-world questions; score vs event log) | todo | |
| T-107 | EVAL | Retrieval recall@k labeled set + weight tuning | todo | |
| T-108 | ENG | Snapshot **load** path: resume a run from `snapshots/` | todo | prerequisite for M3 |
| T-109 | COG | Mock LLM: make less degenerate (vary by observations/state) so mock runs exercise more code | todo | |

## M2 — Social world
| ID | Lane | Task | Status |
|---|---|---|---|
| T-201 | WORLD | Objects: carry/drop/give; gifts between inhabitants | todo |
| T-202 | WORLD | Day/night cycle and light-aware observations | todo |
| T-203 | COG | Hierarchical plans + surprise-driven re-planning | todo |
| T-204 | COG | Relationship memory (trust/liking per other) | todo |
| T-205 | ENG | Replay viewer in `engine/viz/` reading `events.jsonl` | todo |
| T-206 | EVAL | Welfare monitors (distress, isolation, loops) per `06` | todo |
| T-207 | WORLD | Scale to 5–10 seeds; add `tools/new_agent.py` coordinate picker | todo |

## M2.5 — Civilization and graphics (see `docs/10`, `docs/11`, ADR-0006 proposed)
| ID | Lane | Task | Status |
|---|---|---|---|
| T-301 | ENG | Load `world/resources/*.yaml` into the engine; items on tiles, inventory, carry/drop/give | todo |
| T-302 | WORLD | `gather` and `craft` actions + regrowth timers; add stone/clay/fiber/reeds sources to a new map region | todo |
| T-303 | ENG | Structures (placed, persistent, stations/shelter) | todo |
| T-304 | ENG | Log fruit/objects/structures per tick; viewer draws them | todo |
| T-305 | COG | Game Master + persistent inventions registry (needs ADR-0006 approved) | todo |
| T-306 | WORLD | Richer senses in observations (sound, smell, touch, taste) | todo |
| T-307 | WORLD | Records: clay tablets/paper as persistent in-world text; teaching/skill transfer | todo |
| T-308 | EVAL | Civilization metrics (recipes used, structures, techs reached, inventions, norms) | todo |
| T-309 | WORLD | Regions + biomes + exploration (world -> region -> chunk) | todo |
| T-310 | ENG | Viewer: live feed, sprites/tileset, world-map layer, heatmaps, welfare overlay | todo |

## Open questions (humans answer)
- Q5: Approve ADR-0006 (invention, senses, sealed boundary, amends ADR-0005)?
- Q6: Is population growth ever allowed (see `docs/10`), and under what conditions?
- ~~Q1~~ ANSWERED 2026-11-02: the project owner signs off on ethics (ADR-0005). Add legal name to ADR-0005.
- Q2: Which embedding provider is acceptable (cost, privacy, offline)?
- ~~Q3~~ ANSWERED 2026-11-02: inhabitants must not be able to learn the nature of their world (ADR-0005). No active cover stories; sincere questioning is logged and escalated.
- Q4: 2D grid viewer first, or jump to a 3D backend?

## Done
- T-001 Skeleton, mock LLM, tests, eval, docs (M0)
- T-109 (partial) Mock LLM no longer loops on identical prompts (call counter); 300-tick runs now show varied movement
- T-205 (v1) Replay viewer: sun, planet, Eden, close-up; `make viewer` (see `docs/11`)
- Civilization data seed: resources, recipes, tech tree + integrity tests
