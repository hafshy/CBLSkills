---
name: cbl-reflect-share
description: Produces the closing reflection and a shareable case study/report for a completed Challenge Based Learning (CBL) project, pulling from documentation across every phase. Use when a team says "we're basically done, help us wrap this up", "let's write our closing reflection", "can you put together something we can present to the class", or "make us a case study". Requires implementation/evaluation results to be recorded first. Reads across the entire project — build and test this one last.
---

# CBL Reflect & Share

The closing skill. Two things it produces: a genuine reflection (what was learned, not just what was done), and a shareable artifact (case study, presentation-ready report). This is also the one skill that reads across every other artifact in the project, not just its immediate prerequisite.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" reflection_share
```

Blocked → offer `cbl-implement-evaluate`. Otherwise proceed.

## Sub-behavior: Reflect

**Trigger**: "let's write our closing reflection".

Read every prior artifact — `challenge/01` through `challenge/10`, including research findings and prototype iteration logs. Prompt the team through genuine reflection, not an auto-summary:
- What did you learn that you didn't expect?
- What challenges came up, and how did you handle (or not handle) them?
- What would you do differently?
- How does the outcome (from Implementation & Evaluation) compare to what you originally hoped for in your Challenge Statement?

Write into `challenge/11-reflection-and-share.md`'s `## Notes` section, first line a short plain-text summary, then the fuller reflection.

```bash
python3 -m cbl_core.cli set-status "<project_root>" reflection_share --status complete
```

This is a `.cbl/state.json` write like any other, so it triggers the same silent canvas refresh — by the time this finishes, the canvas already shows every section filled and the progress footer at 100% complete. No separate canvas request needed, though it's fine if the user asks to see it explicitly.

## Sub-behavior: Produce a shareable artifact

**Trigger**: "make us a case study" / "something to present" — can happen in the same request as Reflect, or separately afterward.

Assemble a presentation-ready narrative: Big Idea → Essential Question → Challenge Statement → key research findings → Solution Concept (and what was considered but not chosen) → prototype/iteration story → real outcomes → reflection. This can be a markdown report, or — if the user wants something more visual — mention that the CBL Canvas (already fully populated at this point) works well as a companion slide or printout; offer to point them at it, but don't regenerate it yourself here (it already auto-refreshed in the Reflect step above).

## Notes & Edge Cases

- Reflection quality matters more than polish — prompt genuinely rather than auto-summarizing existing documentation into something that reads complete but wasn't actually reflected on.
- Marking this artifact `complete` closes the tracked CBL process, but nothing prevents a team from reopening any earlier step later if they want to keep iterating past a class deadline — don't treat this as a hard, permanent end state.
- If a user asks for the shareable artifact before Reflect has actually run, do Reflect first — a case study without genuine reflection behind it misses the point of this closing step.
