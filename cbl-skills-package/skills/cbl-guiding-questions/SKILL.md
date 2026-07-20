---
name: cbl-guiding-questions
description: Generates and prioritizes the Guiding Questions a team needs to research to build an informed solution in a Challenge Based Learning (CBL) project — the research roadmap for the Investigate phase. Use when a team wants to figure out what to research, says things like "let's figure out our guiding questions", "what do we need to research", "add a guiding question", or wants to prioritize which questions to pursue. Also use when a later step (e.g. prototyping) surfaces a genuinely new question that needs to be added mid-project. Requires a decided Challenge Statement first.
---

# CBL Guiding Questions

Same generate → add → decide mechanics as the Engage-phase skills, with one real difference: **"decide" here means prioritizing/selecting a subset to actively pursue, not picking a single winner.** Nothing gets deleted — deprioritized questions stay on record, since new information later might make them worth revisiting.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" guiding_questions
```

Blocked → offer `cbl-challenge-statement`. Otherwise proceed.

## Data shape (reuses Options/Decision, repurposed)

- **`## Options`** holds the *full* brainstormed list — cast a wide net, grouped by theme (e.g. user needs, existing solutions, technical feasibility, school policy constraints). Nothing here is ever deleted, only ever added to.
- **`## Decision`** holds the *prioritized subset* the team is actively pursuing right now. First line: a short plain-text summary for the canvas headline (e.g. `5 Guiding Questions prioritized`), then the actual prioritized list below it.

## Sub-behavior: Generate

**Trigger**: "let's figure out our Guiding Questions" (first time), "give me more".

Read the decided Challenge Statement. Brainstorm broadly — this is the one step in the whole project where casting the widest net matters most, since under-researching here weakens everything built on it later. Group into themes. Append to `## Options` (never overwrite prior questions).

```bash
python3 -m cbl_core.cli set-status "<project_root>" guiding_questions --status options_generated
```

## Sub-behavior: Add

**Trigger**: "add a guiding question: [X]" — append to the appropriate theme in `## Options` (or start a new theme if none fits).

**Also this trigger**: "this raised a new question" — from `cbl-prototype`, mid-project, after Guiding Questions is already `decided`. Same action (append to Options), but afterward walk the user through Sub-behavior: Decide again to fold it into the active prioritized set if it's genuinely worth pursuing now, rather than leaving it stranded in the brainstormed list.

## Sub-behavior: Decide (prioritize)

**Triggers**: "which should we prioritize?", "let's decide".

1. Read the full `## Options` list.
2. Recommend which questions are most critical to answer before moving to Act, vs. which can reasonably wait. A simple table works: question / why it matters / how hard to answer.
3. Ask the user to confirm the prioritized subset (they can override your recommendation — this is a real team decision, not a checkbox to rubber-stamp).

Write the confirmed subset into `## Decision`, first line the count-summary, then the list:
```
5 Guiding Questions prioritized

1. What food-waste metrics do families actually understand?
2. What does our current cafeteria waste stream look like by category?
3. ...
```

```bash
python3 -m cbl_core.cli set-status "<project_root>" guiding_questions --status decided --decided-by "<user's name>"
```

Point the user at `cbl-research` next.

## Reopening / adding after decided

Same as any decide skill — re-triggering this skill when status is already `decided` loads the existing prioritized list and lets the user add to or re-prioritize it. Because new Guiding Questions surfacing mid-project (from `cbl-prototype`) is expected and normal, don't treat "guiding_questions already decided, now adding more" as a stale/reopening event the way redeciding Big Idea would be — it's additive, not corrective, so there's no need to flag downstream artifacts stale just because a new question was appended (only re-run `set-status ... --status decided` if the *active prioritized set* itself materially changed, not on every single addition to the brainstormed list).

## Notes & Edge Cases

- Resist prioritizing everything — the whole value of this step is separating "must answer before Act" from "nice to know." If the user tries to prioritize all 10 generated questions, push back gently and ask what's actually blocking a good decision vs. what's just interesting.
- This is the artifact most likely to be revisited mid-project for legitimate reasons (not because something was wrong, but because prototyping surfaced something real) — treat that positively in how you talk about it, not as backtracking.
