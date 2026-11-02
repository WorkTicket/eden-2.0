# Playbook: World lane (`world/`, `agents/`, world rules in `engine/sim/world.py`)

**Read first:** `docs/04-WORLD-DESIGN.md`, `world/laws/rules.md`, `docs/06-ETHICS-AND-CONSCIOUSNESS.md`.

## Rules
- The world is pure rules; it never calls an LLM.
- Observations and results are experiential, in-world sentences. Run `make test` (leak test).
- No new hardship (death, pain-analogues, deprivation) without an approved ADR.
- Keep maps backward compatible with existing snapshots (agents remember places).

## Recipe: add an action
1. Add the kind to `parse_action` (`cognition/planning/planner.py`) and to the action prompt in `decide`.
2. Implement in `World.apply`, returning an experiential sentence.
3. Update `docs/01-ARCHITECTURE.md` contracts table (this is an ADR-worthy change).
4. Tests: success and failure paths; leak test still passes.

## Recipe: add a map or new tile
New YAML in `world/maps/`; add the glyph to `legend`; mark blocking tiles in `BLOCKING` if needed; add a runner `--map` option; test that all seeds start on free tiles.

## Recipe: add an inhabitant
`python tools/new_agent.py "Name"`, then fill the YAML **in-world** (no meta words) and set `start` to a free tile. Run `make test`.

## Recipe: tune the laws
Edit `world/laws/physics.yaml`; record the reason in the commit and, if agent-visible, an ADR. Re-run `make run` + `make eval` and compare.
