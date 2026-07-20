---
name: cbl-challenge-statement
description: Turns a decided Essential Question into a Challenge Statement — an actionable call to action that closes out the Engage phase of a Challenge Based Learning (CBL) project. Use when a team wants to write their Challenge Statement, says things like "let's write our challenge statement", "turn our essential question into a challenge", or wants to revisit an existing one because it feels too broad or too narrow. Requires a decided Essential Question first.
---

# CBL Challenge Statement

Lighter version of the generate/add/decide pattern than `cbl-big-idea` or `cbl-essential-question` — candidate phrasings tend to be close variations of each other, so generation and decision can move faster, but the underlying mechanics (gate check, options, decide, confirm) are the same.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" challenge_statement
```

Blocked → offer to run `cbl-essential-question`. Warning → mention it, then proceed.

## Sub-behavior: Generate

**Triggers**: "let's write our Challenge Statement", "try a different phrasing".

Read the decided Essential Question from `challenge/02-essential-question.md`. Produce 2-3 candidate phrasings, each:
- **Actionable** — a real call to action, not just a restated question
- **Specific** — focused enough to build excitement and direction
- **Open enough** to allow multiple solution paths (a Challenge Statement isn't a Solution Concept yet)

A useful pattern: "Design/Create/Develop a ___ that ___ for ___." — but don't force every phrasing into that exact template if a more natural one fits better.

Write into `challenge/03-challenge-statement.md`'s `## Options` section. Update status:
```bash
python3 -m cbl_core.cli set-status "<project_root>" challenge_statement --status options_generated
```

## Sub-behavior: Add

**Trigger**: "I'd phrase it as: [X]". Append as a candidate, same section.

## Sub-behavior: Decide

**Triggers**: "which one's best?", "let's decide", or a direct statement to lock one in.

Recommend one phrasing — is it genuinely actionable? Too broad (more like a restated Essential Question) or too narrow (already presupposes a specific solution)? Confirm before finalizing.

Write `## Decision` following the shared convention: **first line is the actual Challenge Statement itself** (this is the hero text the CBL Canvas displays prominently — keep it to one clear sentence), then a blank line, then any extra rationale. Example:
```
Design a way to cut cafeteria food waste in half by the end of the semester.

The team chose this phrasing because it's concrete enough to guide research and prototyping
while leaving room for multiple solution types (app, campaign, policy change). Decided by Alex.
```

```bash
python3 -m cbl_core.cli set-status "<project_root>" challenge_statement --status decided --decided-by "<user's name>"
```

This closes out Phase 1 — confirm to the user and point them at `cbl-guiding-questions` as the natural next step.

## Reopening

**Trigger**: "our Challenge Statement is too broad, can we revisit it?" (status already `decided`). This is the artifact with the **widest blast radius** on reopening — nearly the whole rest of the project depends on it. Before finalizing a new decision, explicitly tell the user what's about to be marked stale (Guiding Questions, Synthesis, Solution Concept, Prototype Plan — whichever of these already exist), not just silently propagate it. The `set-status` call handles the actual propagation automatically; your job is making sure the user isn't surprised by it.

## Notes & Edge Cases

- Don't let a phrasing slip into being an actual Solution Concept in disguise (e.g. "Build an app that tracks food waste" presupposes the solution is an app — that's `cbl-solution-concepts`' job later, not this one's).
- Same `not_initialized` handling as every other skill: offer `cbl-init`, stop.
