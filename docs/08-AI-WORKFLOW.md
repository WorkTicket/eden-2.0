# 08 — AI workflow (how to build this fast with many AI workers)

## Principles
1. **Contracts first.** The interfaces in `01-ARCHITECTURE.md` are the seams. Workers on opposite sides never need to talk if they respect them.
2. **Mock-first loop.** Edit -> `make test` -> `make run` -> `make eval`. Seconds, free.
3. **Small vertical slices.** Every task touches code + test + doc + TASKS.md.
4. **One owner per area.** Avoid two workers editing the same file; see ownership below.
5. **Humans decide the weird stuff.** Ethics, persistence format, action space: ADR + human sign-off.

## Parallel lanes (can run concurrently)
| Lane | Owns | Playbook |
|---|---|---|
| Engine | `engine/sim`, `engine/llm` | `agent-playbooks/build-engine.md` |
| Cognition | `cognition/` | `agent-playbooks/build-agent-cognition.md` |
| World | `world/`, `agents/` | `agent-playbooks/build-world.md` |
| Evals + QA | `evals/`, `tests/` | `agent-playbooks/review-and-test.md` |
| Docs/research | `docs/` | add to `docs/research/` |

Lanes interact only through the contracts. If a lane needs a contract change, it writes an ADR and a TASKS.md entry, then waits for approval.

## Task lifecycle
1. Pick the top unblocked task in `docs/TASKS.md` for your lane; mark `in progress` with your name/date.
2. Read the relevant docs and playbook. State your plan in 3–5 bullets.
3. Implement, test (add or update tests), run `make test` + `make run`.
4. Update docs, mark task done, add follow-ups you discovered.
5. Summarize: what changed, how verified, what's next, any open questions.

## Prompt template for dispatching an AI worker
```
You are working on Digital Eden. Read CLAUDE.md and docs/agent-playbooks/<lane>.md first.
Task: <TASK ID and text from docs/TASKS.md>
Constraints: stay within <owned paths>; mock LLM only; do not change contracts in docs/01-ARCHITECTURE.md.
Done when: make test passes, make run works, docs + TASKS.md updated.
Report: files changed, how you verified, open questions.
```

## Using Claude Code
Slash commands in `.claude/commands/`: `/new-agent`, `/run-sim`, `/adr`. Use subagents for independent lanes; give each only its playbook and task. Prefer plan mode for anything crossing lanes.

## Anti-patterns
Live-LLM tests; hidden global state; prompts with meta words; changing the action space ad hoc; giant PRs; skipping the ADR; deleting snapshots.
