# 02 — Open-source foundations and what to reverse engineer

> **Licenses and repo details below are from memory and MUST be verified before copying any code.** Record the verified license + commit in the "Verified" column. Prefer re-implementing from papers over vendoring code.

| Project | What it gives us | Take / reverse engineer | Verified |
|---|---|---|---|
| **Generative Agents** (Park et al. 2023; `joonspk-research/generative_agents`) | The canonical memory stream, retrieval (recency+importance+relevance), reflection, daily planning, "Smallville" | Already re-implemented in `cognition/memory`, `reflection`, `planning`. Next: hierarchical plans, conversation module, retrieval-weight tuning | [ ] |
| **Concordia** (Google DeepMind; `google-deepmind/concordia`) | Game-Master pattern: an LLM narrator adjudicates free-form actions; components for agent memory/identity; social-simulation tooling | Game-Master adjudication to go beyond our fixed action set (v1); component-based agent design | [ ] |
| **AI Town** (a16z-infra; `a16z-infra/ai-town`) | Deployable 2D town with persistence, web UI, built on Convex | UI/viewer ideas, persistence patterns, deployment shape | [ ] |
| **Project Sid / PIANO** (Altera, 2024 paper) | Many-agent (hundreds+) civilization sim in Minecraft; concurrent cognitive modules coordinated by a bottleneck; emergent roles/laws | Architecture ideas for concurrency + "cognitive controller"; check whether code is released, else paper-only | [ ] |
| **Voyager** (MineDojo; `MineDojo/Voyager`) | LLM agent with skill library and automatic curriculum in Minecraft | Skill library (agents accumulate reusable procedures) | [ ] |
| **Mineflayer** (`PrismarineJS/mineflayer`) | Bot API for Minecraft servers | Option for a 3D world backend | [ ] |
| **Luanti / Minetest** | Open voxel engine, scriptable in Lua | Fully open 3D alternative to Minecraft | [ ] |
| **Mesa** (`projectmesa/mesa`) | Classic Python agent-based modeling | Spatial/scheduling utilities, visualization ideas | [ ] |
| **OASIS** (CAMEL-AI) | Large-scale social-media agent simulation | Techniques for scaling to many agents cheaply | [ ] |
| **Evennia** | Python MUD/text-world framework | Text-first world with persistent objects, an option for a pure-text Eden | [ ] |
| **Godot** | Open game engine | Eventual rich viewer/world frontend, consuming `events.jsonl` or a socket | [ ] |

## How to use this table
1. **Start from papers**, not code: they are the stable spec. Add summaries to `docs/research/`.
2. **Verify** license and activity before vendoring. Anything GPL/LGPL gets an ADR before it touches the repo.
3. **Reverse-engineer behavior** by running the upstream project, logging its prompts, and writing eval cases that our implementation must match or beat. Never copy prompts verbatim from unlicensed sources.
4. **Track divergence**: each time we deviate from a source design, note why in an ADR.

## Gaps nobody has solved (our opportunity)
Long-horizon identity stability (weeks), memory consolidation/forgetting, grounded self-models, cost-efficient many-agent concurrency, rigorous interview-based believability evals, welfare-aware design.
