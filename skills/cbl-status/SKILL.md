---
name: cbl-status
description: Shows a read-only snapshot of a Challenge Based Learning (CBL) project — what's decided, what's stale, what's next, and who's done what. Use whenever someone asks "where are we in the process", "what's our CBL status", "what's left to do", "what's stale", "what should we work on next", or generally seems unsure what state their CBL project is in. Safe to use any time; makes no changes.
---

# CBL Status

Read-only. Never changes any file. This is the safe thing to reach for whenever a user is unsure what state their project is in — use it liberally, it has no side effects.

## Step 1: Run the status command

```bash
python3 -m cbl_core.cli status "<project_root>"
```

- **`{"ok": false, "error": "not_initialized", ...}`** — no CBL project exists here yet. Say so plainly and offer to run `cbl-init`.
- **`{"ok": true, "phases": {...}, "artifacts": {...}, "stale": [...], "team": [...]}`** — continue to Step 2.

## Step 2: Turn the JSON into a plain-language summary

Don't just dump the JSON at the user. Translate it:

- **Phase summary**: for each of `engage`, `investigate`, `act`, say `not_started` / `in_progress` / `complete` in a sentence, not a table, unless the user specifically wants a table.
- **Stale artifacts**: if `stale` is non-empty, name them and briefly explain why (which upstream artifact changed) — read the relevant entries from `artifacts` for context (each has `status`, `decided_by`, `decided_at`, `stale`).
- **What's next**: identify the first artifact (in schema order: big_idea → essential_question → challenge_statement → guiding_questions → research → synthesis → solution_concepts → prototype → implementation_evaluation → reflection_share) whose status is `not_started`, and name the skill that produces it as the next unblocked step. If multiple things could happen in parallel (e.g., several guiding questions being researched at once), say so rather than implying strict single-file linearity.
- **Team**: if the user specifically asks "who's done what," cross-reference `team` against each artifact's `decided_by` field.

## Example Response Shape

"Engage phase: done — Big Idea, Essential Question, and Challenge Statement are all decided. Investigate: in progress — Guiding Questions are decided, but Synthesis hasn't started yet. Act: not started. Nothing's currently stale. Next step: work on Research or Synthesis for Investigate."

## Notes & Edge Cases

- If `stale` is empty, don't manufacture something to say about staleness — just note nothing's stale and move on.
- With only one team member, the "who's done what" angle is just a lighter version of the full snapshot, not an error or a non-answer.
- Never suggest or perform a fix for a gate or staleness issue found here — that's the job of the skill that owns the relevant artifact (e.g., `cbl-big-idea` for Big Idea). This skill only reports.
