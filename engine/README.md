# engine/

- `sim/` runner loop and world rules (`world.py` is pure rules, no LLM)
- `llm/` the only model interface (`client.py`: `MockLLM`, `AnthropicLLM`)
- `viz/` future replay viewer; reads `data/runs/<id>/events.jsonl`

Recipes: `docs/agent-playbooks/build-engine.md`.
