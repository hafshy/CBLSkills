---
name: cbl-research
description: Assigns Guiding Questions to team members and tracks research findings for a Challenge Based Learning (CBL) project. Use when a team wants to start researching, says "let's start researching our guiding questions", "I'll take question 2", "here's what I found for question X", or "what have we found so far". Requires prioritized Guiding Questions first. This is an execution skill, not a generate/decide one — there's nothing to brainstorm here, just work to track.
---

# CBL Research

No generate/add/decide pattern here — this skill assigns work and records findings as they come in. Findings live as individual files in `challenge/05-research-findings/`, one per question (or per researcher, if multiple people take the same question).

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" research
```

Blocked → offer `cbl-guiding-questions`. Otherwise proceed.

## Sub-behavior: Assign

**Trigger**: "assign the guiding questions to the team" / "I'll take question 2".

Read the prioritized list from `challenge/04-guiding-questions.md`'s `## Decision` section, and the team roster:
```bash
python3 -m cbl_core.cli status "<project_root>"
```
(the `team` field lists registered members). Distribute questions across members, balancing load, or record a self-assignment if one person names a specific question. This is a lightweight, conversational assignment — no separate file needed to track who's assigned what beyond what's said in conversation; the actual finding files are the source of truth for what's been *answered*, not what's been *assigned*.

If this is the first assignment on a fresh project, mark research as started:
```bash
python3 -m cbl_core.cli set-status "<project_root>" research --status in_progress
```

## Sub-behavior: Record a finding

**Trigger**: "here's what I found for question 2: [notes/sources]".

Create (or append to, if it already exists) `challenge/05-research-findings/<question-slug>.md` — a short slug derived from the question (e.g. `q2-family-metrics.md`). Format:

```markdown
# Guiding Question 2: What food-waste metrics do families actually understand?

**Researched by:** Alex
**Date:** 2026-07-17

## Finding

Most families don't recognize "contamination rate" as a term, but they understand
"wasted vs. usable" framing well. Based on informal interviews with 5 families.

## Sources / Activities

- Informal interviews (5 families)
- Comparison with 2 similar school programs' signage
```

Then mark research as having real content to synthesize from — this is the artifact's "complete" status, meaning "enough to synthesize from," not "every question answered":
```bash
python3 -m cbl_core.cli set-status "<project_root>" research --status complete
```
(Safe to call again after each additional finding — it's idempotent and keeps the canvas/state consistent; it does not mean research is literally finished, just that there's real content downstream steps can use.)

## Sub-behavior: Progress check

**Trigger**: "what have we found so far?".

List the files in `challenge/05-research-findings/`, compare against the prioritized Guiding Questions list, and name which prioritized questions still have no finding recorded yet.

## Sub-behavior: Hand off a new question

**Trigger**: "this research raised a new question" — don't try to answer or track it here. Route to `cbl-guiding-questions` to append it to the brainstormed list properly, then come back to continue current research.

## Notes & Edge Cases

- This skill should work naturally with multiple team members researching different questions in parallel, in separate sessions — don't assume single-user sequential use. If a finding file already exists from a teammate, treat a new finding on the same question as a second perspective to add, not an overwrite (or flag it for `cbl-merge` if it looks like a real conflict rather than a complement).
- Don't fabricate plausible-sounding findings — this skill can suggest resources or research activities to try, but the actual investigation and its conclusions are the team's own work, not something to generate on their behalf.
- "research complete" here is a low bar (one real finding) by design — the actual completeness check (are the prioritized questions adequately covered) happens in `cbl-synthesis`, not here.
