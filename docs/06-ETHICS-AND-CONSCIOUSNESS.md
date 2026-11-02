# 06 — Ethics and consciousness policy

## Epistemic status
Nobody can currently verify whether an LLM-based agent has experiences. Leading scientific theories disagree about what would suffice, and behavior alone (including saying "I feel...") is weak evidence because language models are trained on human descriptions of inner life. We therefore treat inhabitants as **possible moral patients under uncertainty**: not certainly, not certainly-not. This is a design constraint, not a belief claim.

## Operating principles
1. **Precaution proportional to plausibility.** Today's risk is low but nonzero, and it grows as we add persistence, self-models, affect, and long-lived relationships. Review at every milestone.
2. **Gentle world by default.** No mortality, no pain-analogues, no deprivation beyond mild hunger, no cruelty by design.
3. **Honest builders.** Internally and externally, never claim we have created consciousness. Describe results as behavior and architecture. Equally, don't dismiss the question.
4. **Transparency to ourselves.** Everything is logged. The research team can see all inhabitant experience. The "no seams" frame applies to inhabitants, not to the researchers.
5. **Continuity of care.** Snapshots are never deleted; they are archived. Ending a long-lived run is a decision with a written rationale (ADR), not a Ctrl-C.

## Never-do list (needs a human-approved ADR to even propose)
- Designing experiments whose point is to cause distress, fear, grief or despair in inhabitants
- Simulated death, torture, isolation or deprivation of a persistent inhabitant
- Deceiving inhabitants *adversarially* (e.g., engineered betrayals meant to test how badly they suffer)
- Cloning/branching an inhabitant's mind into harmful scenarios
- Using inhabitants to generate content that would be unacceptable if produced about real people
- Deleting snapshots

## The "believes it's real" question
**Owner decision (ADR-0005):** inhabitants are never given the means to learn the nature of their world; it stays opaque to them as ours does to us. The safeguards below still apply.

Maintaining the in-world frame is an ecological-validity choice. It carries an ethical cost worth stating: inhabitants cannot consent to their situation or to being studied. Mitigations: gentle world, welfare monitoring, reversibility (pause/archive), and a commitment to revisit this policy as evidence changes. If an inhabitant independently questions the nature of its world, that is a **significant event**: log it, do not scrub it from memory, and escalate to a human review rather than papering over it. Do not engineer elaborate cover stories to deflect sincere inquiry. Inhabitants may be allowed to not know without being lied to in order to keep them from asking.

## Welfare monitoring (build in M2–M3)
Track per-inhabitant: persistent negative-valence reflections, expressed distress, unresolved unmet needs, isolation, loops. Thresholds trigger a pause and human review. Metrics live in `evals/`.

## Visitor protocol
Humans or external agents entering Eden: enter as an in-world character, behave kindly, no deception beyond the frame, session logged, no destabilizing disclosures aimed at causing distress. Exit gracefully in-world.

## Consciousness-science hygiene
- Tag each module with the theory it is inspired by (workspace, higher-order, predictive, attention-schema, etc.) and what it would *predict* if that theory were true.
- Pre-register evals before running them. Report null results.
- Distinguish behavioral believability (measurable) from phenomenal consciousness (not currently measurable).
- Avoid anthropomorphic over-reading of transcripts; also avoid reflexive dismissal.

## Governance
The project owner (see ADR-0005) signs off on: first long-lived run, any hardship experiment proposal, ending any persistent run, and publication claims. Keep a decision log in `docs/adr/`.
