# 05 — Roadmap

Each milestone has an exit test so AI workers know when to stop. Tasks live in `TASKS.md`.

## M0 — Skeleton (DONE)
Runnable sim, mock LLM, memory/reflection/planning, tests, eval script, docs.
**Exit:** `make test` green; `make run` produces events + snapshots.

## M1 — Real minds (next)
- Anthropic backend verified on a 50-tick run; cost logged per run
- Real embeddings (ADR-0004), retrieval weight tuning against a small recall test set
- LLM importance scoring (with heuristic fallback); batch/caching to cut cost
- Conversation module (multi-turn, summarized to memory)
**Exit:** two agents hold a coherent conversation across 200 ticks and later recall it when asked (interview eval passes).

## M2 — Social world
- 5–10 agents; relationships; objects (carry/drop/give); day/night
- Hierarchical planning with surprise-driven re-planning
- Replay viewer in `engine/viz/` reading `events.jsonl`
**Exit:** observable emergent behavior (sharing, routines, gossip) quantified by evals; viewer replays a run.

## M2.5 — Civilization and graphics (proposed; ADR-0006)
Order matters: (1) richer senses, (2) objects/gather/craft/structures from `world/resources/`, (3) Game Master + inventions registry, (4) welfare monitors, (5) affect system. Viewer grows with each (fruit/objects/structures drawn, sprites, world map). Details: `docs/10`, `docs/11`, tasks T-301..T-310.
**Exit:** inhabitants craft a tool chain from raw resources unaided, one invention is accepted into the registry and used by a second inhabitant, and the viewer shows it.

## M3 — Identity and self-model
- Self-model reflection; drift logging; persona-consistency eval
- Consolidation/forgetting; resumable snapshots across process restarts
**Exit:** 1000-tick run resumed from snapshot is behaviorally continuous; persona consistency score above threshold in `07-EVALUATION.md`.

## M4 — Scale and richness
- 25+ agents, Game-Master adjudication for free-form actions, crafting, seasons
- 3D backend adapter prototype (Luanti or Godot)
**Exit:** 25 agents x 1000 ticks within the cost budget; world adapter swap does not touch `cognition/`.

## M5 — Long-lived Eden
Multi-week persistent run, welfare monitoring dashboard, visitor protocol, public write-up of methods and negative results.

## Standing work
Ethics review at each milestone boundary (`06`). Open-source license audit (`02`). Eval suite grows with every capability.
