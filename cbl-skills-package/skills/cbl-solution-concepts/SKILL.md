---
name: cbl-solution-concepts
description: Generates, adds, and decides on a Solution Concept for a Challenge Based Learning (CBL) project — the concrete thing the team will actually build, grounded in their research synthesis. Use when a team wants to brainstorm solutions, says "what could we actually build", "let's brainstorm solution concepts", "add my own solution idea", or wants to decide on one. Medium-agnostic — a Solution Concept can be a product, app, campaign, service, or community project, not software specifically. Requires a completed Research Synthesis first.
---

# CBL Solution Concepts

Same generate → add → decide mechanics as `cbl-big-idea` — the last of the five artifacts in this set that follows that exact pattern. One important difference from the Engage-phase skills: options here must be **medium-agnostic**. Don't default to assuming the solution is software just because that's a common outcome — a campaign, a physical redesign, a policy proposal, and an app are all equally valid Solution Concepts. Let the synthesis findings and the team's own interests point to the medium, don't presume it.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" solution_concepts
```

Blocked → offer `cbl-synthesis`. Otherwise proceed.

## Sub-behavior: Generate

**Trigger**: "what could we actually build?" / "let's brainstorm solution concepts".

Read the synthesis from `challenge/06-synthesis.md` — every option must be grounded in what was actually found there, not generic ideas unconnected to the research. Produce 3-5 options across different mediums where it makes sense (don't force variety for its own sake if the findings really do point toward one type of solution). For each: summary, why it fits the synthesis findings, one honest risk.

Also weigh feasibility against the team's actual constraints — read `.cbl/constitution.md` for timeline and team size, and let that inform (but not solely determine) what you generate.

Append to `## Options` in `challenge/07-solution-concepts.md`:
```bash
python3 -m cbl_core.cli set-status "<project_root>" solution_concepts --status options_generated
```

## Sub-behavior: Add

**Trigger**: "add my own idea: [X]" — append as a first-class option, same section.

## Sub-behavior: Decide

**Triggers**: "what do you recommend?", "let's decide", or a direct statement to lock one in.

1. Compare options: fit with synthesis findings, feasibility given the actual timeline/team size, risk.
2. Recommend one — weight feasibility honestly against the real timeline, not just novelty or ambition. If the most exciting option is genuinely too risky for the time remaining, say so plainly, while still naming it as worth considering if circumstances allow.
3. Confirm before finalizing.

Write `## Decision`: first line the concept name (short, plain text), then rationale, following the shared convention from `cbl-big-idea`.

```bash
python3 -m cbl_core.cli set-status "<project_root>" solution_concepts --status decided --decided-by "<user's name>"
```

Point the user at `cbl-prototype` next.

## Notes & Edge Cases

- The runner-up options (generated but not chosen) matter beyond this step — the CBL Canvas shows them for narrative context ("we also considered..."), so don't delete them from `## Options` even after a decision is made.
- This is the artifact most likely to get pulled toward "just build the coolest idea" — the decide step's job is to keep feasibility honest, not to dampen ambition unnecessarily. Both matter; don't collapse into only optimizing for one.
