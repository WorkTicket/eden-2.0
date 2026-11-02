---
description: Create a new inhabitant seed in-world and validate it
argument-hint: <name> [short character concept]
---
Create a new inhabitant for Digital Eden named and conceived as: $ARGUMENTS

1. Run `python tools/new_agent.py "<name>"`.
2. Fill the generated YAML IN-WORLD: traits, a 2–4 sentence backstory written as lived memory, goals, values. Never use words like simulation, AI, agent, model, prompt, program, game.
3. Choose a free grass `start` tile from `world/maps/eden.yaml` not used by another seed.
4. Run `make test` (includes the vocabulary leak test) and `make run`; confirm the new inhabitant acts.
5. Report the file path and a one-line summary of the character.
