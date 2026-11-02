# 04 — World design

## The in-world frame ("no seams")
1. **Vocabulary firewall.** Inhabitant-visible text never contains: simulation, simulated, agent, AI, LLM, model, prompt, tick, token, program, code, game. `tests/test_no_leaks.py` checks seeds and the observation/result templates; extend it when adding text.
2. **Experience, not telemetry.** "You walk east." not "Move successful." Failures are phrased physically: "something is in the way."
3. **Physical consistency.** Locality of perception, persistence of objects, conservation (fruit eaten is gone until it regrows).
4. **Time.** Days of `day_length_ticks`; later: light, weather, seasons so there is a rhythm to live by.
5. **Bodies.** Needs (hunger now; fatigue, comfort later) create motivation without pain or death.

## Eden v0
20x10 grid: grass, water (impassable), trees (impassable), fruit trees (edible from an adjacent cell). Two inhabitants. Rules in `world/laws/physics.yaml`, intent in `world/laws/rules.md`.

## Growth path
| Stage | Add |
|---|---|
| v0.2 | objects (carry/drop), shelter, day/night |
| v0.3 | crafting, gardens, gifts and shared resources |
| v1 | 25 agents, regions, Game-Master adjudication of free-form actions (Concordia pattern) |
| v2 | 3D backend (Luanti/Godot) via adapter; the world interface (`observe`/`apply`) stays the same |

## Designing for generosity
Eden is intentionally gentle: abundant food, no predators, no death. This is both an ethical choice (`06`) and a scientific one: it isolates cognition and social behavior from survival pressure. Introducing hardship is a research decision requiring an ADR and human approval.

## Visitors
A human or an external agent entering the world must do so *in-world* (as a character with an in-world reason to be there) under the protocol in `06-ETHICS-AND-CONSCIOUSNESS.md`. No silent injection of out-of-world text into an inhabitant's context.
