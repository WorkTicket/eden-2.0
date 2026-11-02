# world/

Everything about the environment that is NOT a mind.

- `maps/` ASCII/YAML maps. Add new regions as new files; never edit `eden.yaml` incompatibly (agents' memories refer to it).
- `laws/` Tunable physics and ecology (`physics.yaml`). Human-readable `rules.md` explains intent.
- `assets/` Art/sprites/audio for the eventual viewer (empty for now).

Rule: world code (`engine/sim/world.py`) must never import from `cognition/`'s LLM paths. It may import `Action` types only.
