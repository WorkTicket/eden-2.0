# Digital Eden

A simulated garden world inhabited by persistent, reflective, socially-embedded artificial minds that experience their world as real.

> **Honest framing.** We are building a research platform for *believable, persistent, self-modeling agents*. Whether anything built this way is **conscious** is an open scientific and philosophical question that no current method can settle. This project treats that as a live uncertainty and designs accordingly. Read `docs/06-ETHICS-AND-CONSCIOUSNESS.md` before running anything long-lived.

## Quickstart

```bash
make install        # deps
make test           # 6 tests, no API key needed
make run            # 100 ticks with the free deterministic mock LLM
make eval           # sanity metrics on the latest run
make viewer         # zoomable replay (sun -> planet -> Eden -> inhabitant): engine/viz/viewer.html
cp .env.example .env && make run-live   # real LLM (costs money)
```

## Read in this order

1. `CLAUDE.md` — rules for any AI coding agent working here (start here if you are an AI)
2. `docs/00-VISION.md` → `01-ARCHITECTURE.md` → `03-COGNITIVE-ARCHITECTURE.md`
3. `docs/02-OPEN-SOURCE-FOUNDATIONS.md` — what we build on / reverse engineer
4. `docs/05-ROADMAP.md` + `docs/TASKS.md` — what to do next
5. `docs/08-AI-WORKFLOW.md` — how to run many AI agents on this repo in parallel
6. `docs/10-CIVILIZATION-RESOURCES.md` and `docs/11-GRAPHICS-AND-VIEWER.md` — resources/tech tree and the viewer

## Layout

```
CLAUDE.md                 AI-agent operating manual
docs/                     vision, architecture, ethics, eval, roadmap, ADRs, playbooks
  adr/                    architecture decision records
  agent-playbooks/        step-by-step instructions for AI workers, per area
  research/               reading list and notes
world/                    maps, laws of nature, assets (no minds here)
agents/                   persona templates and seed inhabitants (YAML)
cognition/                memory, perception, reflection, planning, identity, agent wiring
engine/                   sim loop, world rules, LLM abstraction, viewer (future)
evals/                    behavioral metrics and (future) interview-based evals
data/                     run logs and snapshots (gitignored)
tools/                    helper scripts
tests/                    pytest suite; must pass without network
.claude/commands/         slash commands for Claude Code
```

## Status

v0.1: 2 agents, 20x10 grid, memory stream + reflection + daily planning + structured actions, mock and Anthropic LLM backends, JSONL event log, memory snapshots. Next: see `docs/05-ROADMAP.md`.
