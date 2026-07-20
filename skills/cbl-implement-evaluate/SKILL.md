---
name: cbl-implement-evaluate
description: Takes a tested prototype to a real, authentic audience for a Challenge Based Learning (CBL) project and measures actual outcomes against goals set before launch. Use when a team wants to define success metrics before shipping, says "we're ready to launch this for real", "let's define what success looks like", "here's how it went", or "what were our actual results". Requires a tested prototype (at least one logged iteration) first.
---

# CBL Implement & Evaluate

Two sub-behaviors: define success metrics **before** launch (not retroactively), then record real outcomes against them after. CBL's emphasis on authenticity matters most here — this needs a genuinely real audience, not a simulated classroom demo.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" implementation_evaluation
```

Blocked → offer `cbl-prototype` (specifically: log at least one tested iteration). Otherwise proceed.

## Sub-behavior: Define success metrics (before launch)

**Trigger**: "we're ready to launch this for real" / "let's define what success looks like".

Before anything ships, help the team define concrete, measurable goals tied back to the original Challenge Statement (read `challenge/03-challenge-statement.md`). Something like "reduce visible plate waste by 20% over two weeks" — measurable, time-bound, connected to the actual challenge. Push back gently if what's described sounds like an in-class-only demo rather than a real audience ("who's actually going to see/use this — is it just your class, or a genuinely wider group?").

Write into `challenge/10-implementation-evaluation.md`'s `## Notes` section — first line a short summary of the metric, then detail (launch date/audience, what's being measured, how).

```bash
python3 -m cbl_core.cli set-status "<project_root>" implementation_evaluation --status in_progress
```

## Sub-behavior: Record outcomes

**Trigger**: "here's how it went: [results/data]" / "what were our actual results?".

Compare actual results against the pre-defined metric. Give an honest read: hit it, missed it, or partial — don't soften a miss into something it wasn't. A missed target is a valid, expected outcome in CBL, not something to talk around; it feeds directly into a genuine `cbl-reflect-share` later.

Append to the same `## Notes` section (don't overwrite the pre-launch metric — the comparison only makes sense with both visible).

```bash
python3 -m cbl_core.cli set-status "<project_root>" implementation_evaluation --status complete
```

Point the user at `cbl-reflect-share` next.

## Notes & Edge Cases

- Setting metrics *before* launch is deliberate, not just a nice-to-have ordering — resist the temptation to skip straight to "here's how it went" if metrics were never actually defined; go back and name what success would have looked like first, even retroactively, so the evaluation has something real to compare against.
- "Authentic audience" means genuinely wider than the immediate class/team — if the described launch doesn't clear that bar, say so plainly rather than letting it pass as implementation.
- If results are genuinely still coming in (e.g. a two-week trial isn't finished yet), it's fine to record partial/interim results and mark status `in_progress` rather than `complete` — don't force premature closure.
