---
name: cbl-essential-question
description: Generates, adds, and decides on the Essential Question for a Challenge Based Learning (CBL) project — the personal, specific question that bridges the broad Big Idea to an actionable Challenge. Use when a team wants to figure out their Essential Question, says things like "let's work on our essential question", "what's our essential question", "add my own essential question", or wants to decide on/confirm one. Requires a decided Big Idea first — if there isn't one yet, offer to run cbl-big-idea.
---

# CBL Essential Question

Same shape as `cbl-big-idea` (read that skill first if you haven't — this one follows it exactly): three sub-behaviors, **generate**, **add**, **decide**, triggered conversationally, not by a fixed sequence.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" essential_question
```

- **`{"ok": false, "reason": "blocked", "prereq": "big_idea", ...}`** — Big Idea isn't decided yet. Use the `message` field as your explanation, and offer to run `cbl-big-idea` now.
- **`{"ok": true}`** — proceed.
- **`{"ok": true, "warnings": [...]}`** — proceed, but mention the warning (Big Idea was redecided after this artifact already had content) before diving in.

## Sub-behavior: Generate

**Triggers**: "let's work on our Essential Question", "give me more options" (status `not_started` or `options_generated`).

Read the decided Big Idea from `challenge/01-big-idea.md` first — every generated question must genuinely connect to it. Produce 3-5 candidate questions, each testing:
- **Personal relevance**: why does this matter to the team specifically?
- **Community relevance**: where does this intersect with their school/community?

Write into `challenge/02-essential-question.md`'s `## Options` section (append, don't overwrite prior options). Update status:

```bash
python3 -m cbl_core.cli set-status "<project_root>" essential_question --status options_generated
```

## Sub-behavior: Add

**Trigger**: "add my own: [X]".

Append as a first-class option in the same section, same format. If the user's question doesn't obviously connect back to the decided Big Idea, ask how they see the connection rather than silently accepting or silently rejecting it.

## Sub-behavior: Decide

**Triggers**: "what do you recommend?", "let's decide", "our Essential Question is [X], confirm that" (valid even with no prior options — treat as add + immediate decide).

1. Compare options on specificity and personal connection — a technically well-formed question that doesn't actually connect to the team's own experience is weaker even if grammatically fine.
2. Give one clear recommendation with reasoning.
3. Ask for explicit confirmation. Never auto-select.

On confirmation, write `## Decision` following the same convention as every decide skill in this set: **first line is the question itself, short and plain (no markdown formatting), then a blank line, then rationale.** Example:
```
Why does our cafeteria throw away so much food every day?

This connects directly to the team's decided Big Idea (Sustainability) and is personally
specific rather than abstract — the team sees this happen daily. Decided by Alex.
```

Then:
```bash
python3 -m cbl_core.cli set-status "<project_root>" essential_question --status decided --decided-by "<user's name>"
```

Confirm to the user, point them at `cbl-challenge-statement` next.

## Reopening

**Trigger**: "revisit our Essential Question" (status already `decided`). Load the existing decision, offer alternatives. The `set-status` call above already handles staleness propagation to Challenge Statement and anything built on it — no extra step needed, just be clear with the user about what's getting flagged for review downstream.

## Notes & Edge Cases

- The quality bar here is *personal relevance* more than technical correctness — push gently on questions that just restate the Big Idea more narrowly without adding personal/community connection.
- If a proposed Essential Question already reads like a Challenge Statement (an action-oriented call to build/design something), note that gently — this step sits deliberately between the broad Big Idea and the actionable Challenge, not past it yet.
- Same rule as `cbl-big-idea`: if the gate check returns `not_initialized`, offer `cbl-init` and stop.
