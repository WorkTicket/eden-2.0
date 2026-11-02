# 01 — Architecture

```
            ┌────────────────────────── engine/sim/runner.py ───────────────────────────┐
            │  for tick in range(N):                                                    │
            │     world.tick_begin()                                                    │
            │     for agent in shuffled(agents):                                        │
            │        action = agent.step(world, tick)   ◄── cognition/                  │
            │        result = world.apply(agent.id, action)                             │
            │        agent.record_outcome(tick, result)                                 │
            │        log(event)                                                         │
            └───────────────────────────────────────────────────────────────────────────┘
   world (engine/sim/world.py)                      cognition (cognition/)
   - grid, fruit, hunger, speech buffer             - Persona       who I am (in-world text)
   - observe(aid) -> list[str]  ───────────────►    - MemoryStream  everything I've experienced
   - apply(aid, Action) -> str  ◄───────────────    - perceive      dedupe new observations
   - laws from world/laws/*.yaml                    - reflect       synthesize beliefs
                                                    - planner       daily plan + next action
                                                    - Agent         wiring
                                   engine/llm/client.py : the ONLY model door (Mock | Anthropic)
```

## Contracts (stable interfaces; change only via ADR)
| Boundary | Contract |
|---|---|
| World -> mind | `observe(aid) -> list[str]`: in-world sentences, no meta vocabulary |
| Mind -> world | `Action(kind, arg)`; kinds: `move{north,south,east,west}`, `say`, `eat`, `wait` |
| Mind -> model | `LLM.complete(system, prompt, max_tokens, task)`, `LLM.embed(text)` |
| Persistence | `events.jsonl` (one JSON per agent-tick), `snapshots/<id>.json` (full memory + plan) |

## Tick model
Synchronous, turn-based, agents shuffled per tick with the run's seeded RNG. Speech spoken at tick *t* is heard at *t+1* by anyone within perception radius. Simple, deterministic, debuggable. Async/real-time is a v2 question (ADR needed).

## Scaling notes
- LLM calls dominate cost: per agent-tick ~1 `act` call, plus periodic `plan`/`reflect`. Budget in `07-EVALUATION.md`.
- Planned optimizations: act only when something changes, cache by situation hash, cheap model for `act`, strong model for `reflect`, batch agents per call, replace hash embeddings with a real embedder (ADR-0004).
- World stays O(agents * radius^2) per tick; fine up to hundreds.

## Extension points
- New action: add to `planner.parse_action`, `world.apply`, prompt text, docs, tests (playbook: `build-world.md`).
- New cognition module: new folder under `cognition/`, hook in `Agent.step`, eval for it (playbook: `build-agent-cognition.md`).
- New world: new map + laws file, runner flag. Viewer: `engine/viz/` consumes `events.jsonl` (replay, not live coupling).
