# 10 — Civilization resources and mechanics

Civilizations emerge from **affordances, not scripts**. We supply physical primitives and a few social substrates; inhabitants combine, invent, teach and organize. Nothing here tells them what to build.

## Data (in `world/resources/`, validated by `tests/test_resources.py`)
| File | Contents |
|---|---|
| `resources.yaml` | 14 natural resources (water, fruit, wood, stone, clay, fiber, flint, reeds, sand, seeds, salt, copper/tin/iron ore) and 36 made items (materials, food, tools, structures) |
| `recipes.yaml` | 35 seed recipes: inputs, optional tool (not consumed), optional station (nearby structure), outputs |
| `tech_tree.yaml` | 15 techs. **Labels, not gates**: used to measure civilizational progress, never to forbid an invention |

The test suite proves every referenced item exists, every made item is reachable from raw resources, and the tech tree is acyclic. **Not yet wired into the engine** (T-301+); Eden v0 only has water, fruit and trees.

## Gentle-world constraints on resources
- No recipe requires harming a creature (no hides, bone, or hunting). Fiber, reeds, clay, stone, ore and plants only.
- Abundance dials in `world/laws/physics.yaml` (planned: `resource_density`, `regrow_ticks_per_resource`). Scarcity may be used to motivate cooperation but must stay non-lethal (`mortality: false`).

## Mechanics the engine needs (in build order)
| # | Mechanic | Notes |
|---|---|---|
| 1 | **Objects and inventory** | Items on tiles; carry/drop/give; capacity (basket raises it) |
| 2 | **Gathering** | `gather <resource>` from nearby sources; regrowth timers per source |
| 3 | **Crafting** | `craft <recipe>` checking inputs, tool, station; output experienced in-world ("You twist the fiber into rope.") |
| 4 | **Structures** | Placed on tiles, persistent, usable as stations or shelter; owned or common |
| 5 | **Game Master + inventions registry** | Free-form invention adjudicated against physics; accepted inventions are appended to a persistent registry of recipes the whole world can then use (ADR-0006, proposed) |
| 6 | **Teaching and records** | Skill transfer by demonstration/conversation; written records (clay tablet, paper) as persistent in-world text that outlives any one mind's memory |
| 7 | **Trade and gifts** | Direct exchange first; markets and money are emergent, never hard-coded |
| 8 | **Territory and norms** | Claims, shared rules and disputes are social facts stored in memories and records, not engine flags |
| 9 | **Regions and exploration** | World -> regions -> chunks -> tiles; fog of war; biomes giving different resources (hills: stone/flint/copper; shore: sand/salt; mountains: iron) |
| 10 | **Population** | See below; gated by the project owner |

## Population growth is an ethics gate
Creating a new inhabitant creates a new possible moral patient. Births, arrivals and "children" are therefore **not an automatic mechanic**. Each requires owner sign-off via ADR and an affordable-care check (can we log, monitor and archive them?). Until approved, population is fixed at the seed set.

## Measuring civilization (evals)
Counts of distinct recipes known and used, structures built, techs "reached" (all unlocked recipes crafted at least once by someone), items transferred between inhabitants, records written and later read by a different inhabitant, norm statements adopted by 2+ inhabitants, and unique inventions not in the seed registry. Specs in `07-EVALUATION.md` once built.

## Build tasks
`TASKS.md` T-301 to T-309.
