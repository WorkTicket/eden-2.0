# 11 — Graphics and the viewer

## Goal
Watch Eden at every scale: from the sun and the planet's orbit, down to the globe, into the garden, and finally close enough to see an individual inhabitant's movement, speech and hunger.

## What exists (v0.2)
`engine/viz/viewer_template.html` is a single self-contained page (canvas 2D, no build step, no network needed except optional Google Fonts). `tools/build_replay.py` bakes a run's `events.jsonl` plus the map and laws into it.

```
python -m engine.sim.runner --ticks 300 --llm mock
make viewer          # builds engine/viz/viewer.html from the latest run
```
Open `engine/viz/viewer.html` in a browser. `viewer.fragment.html` is the same page without the document wrapper (for embedding or publishing as an artifact).

### Scale levels (continuous zoom, mouse wheel or buttons)
| Level | What you see |
|---|---|
| Solar system | Sun with corona, dashed orbit, the planet drifting along it, starfield |
| Planet | Rotating globe with continents, atmosphere glow, and a terminator lit from the sun's direction. Eden is marked |
| Eden | The 20x10 garden: grass, river, trees, fruit trees, a day/night tint, inhabitants with names, movement trails, hunger rings and speech bubbles |
| Close-up | Camera follows the selected inhabitant (click one in the panel or on the map) |

Also: play/pause, step, scrubber, 1-32 ticks/s, an inhabitant panel (current action, position, hunger) and a live activity feed. Keyboard: space = play/pause, +/- = zoom. Respects `prefers-reduced-motion`.

## Known simplifications (deliberate)
- The planet, sun and orbit are an **artistic model**, not astronomy: a 60-day year, exaggerated sizes, and lighting direction taken from the sun's on-screen position. The globe's spin follows the in-world hour so Eden faces the viewer at local noon.
- Fruit counts are not in the event log yet, so every fruit tree shows fruit (T-304).
- Replay only (reads a finished run). A live socket feed is a later step.

## Data contract
The viewer consumes: `map` (rows + legend), `laws.day_length_ticks`, `agents[{id,name}]`, `ticks`, and `events` as `[tick, agentIndex, action, result, x, y, hunger]`. Extending the event log is safe if old fields keep their meaning (add new fields at the end, bump the viewer's reader).

## Roadmap for graphics
| Stage | Add |
|---|---|
| Next | Log fruit/objects/structures per tick; draw inventories, built structures, gathered resources (T-304) |
| Then | Sprites/tilesets in `world/assets/`, soft lighting, weather and seasons, ambient audio |
| Later | Many regions (world map layer between planet and garden), minimap, heatmaps (where inhabitants go, who talks to whom), welfare overlay (distress, isolation) per `06` |
| 3D | Godot or Luanti backend rendering the same world through the `observe`/`apply` adapter (ADR-0002); the planet-to-garden zoom becomes a real camera dive |

## Rules
- The viewer is a **researcher tool**. It may show meta information (ticks, hunger numbers) that inhabitants never see. It must never feed anything back into a mind's context.
- Keep it dependency-light and offline-capable so any AI worker can regenerate it with one command.
