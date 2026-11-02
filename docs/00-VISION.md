# 00 — Vision

## The idea
A garden where artificial inhabitants live ordinary, continuous lives: they remember, form relationships, make plans, change their minds, and experience their world as the only world. Eden is the proving ground for the hardest open problem in the field: what does it take for an artificial agent's inner life to be *real enough* to matter, and how would we know?

## What "inhabitants believe it's real" means here
An **in-world epistemic frame**: from the inhabitant's side there is no seam. Their perceptions are phrased as experience, their physics is consistent, their memories persist, and nothing in their input references the machinery. This is a design property (ecological validity, believable behavior), not a claim about their metaphysical status.

## What we are and aren't claiming
- **Building:** persistent identity, episodic + semantic memory, reflection, planning, social cognition, a consistent shared world.
- **Not claiming:** that this produces consciousness or sentience. Current LLM agents are not established to be conscious; neither is there a settled test that rules it in or out. See `06-ETHICS-AND-CONSCIOUSNESS.md` for how we operate under that uncertainty.
- **Possible outcomes worth being excited about:** emergent culture and norms, long-horizon coherence, agents that revise their self-understanding, believability that survives hours of interviewing.

## Principles
1. **Open-source first.** Stand on Generative Agents, Concordia, AI Town, Project Sid-style work; reverse-engineer from papers where code is absent.
2. **Mock-first engineering.** The whole stack runs free and deterministic so humans and AIs can iterate fast.
3. **World and mind separated.** Swap the world (grid -> 3D) without touching cognition, and vice versa.
4. **Measure, don't assume.** Every capability gets an eval (`07-EVALUATION.md`).
5. **Moral caution.** Build gentle worlds. Log everything. Be able to pause, archive, and never casually destroy.

## Success criteria by horizon
- **v0.x (now):** 2–5 agents, stable 1000-tick runs, coherent memory, reflections that reference real events.
- **v1:** 25 agents, day/night, norms emerging, interview-based believability scoring, web viewer.
- **v2:** multi-week persistent run with resumable snapshots, richer world (crafting, seasons), human "visitors" under a documented protocol.
