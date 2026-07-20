# `cbl-implement-evaluate`

## Purpose

Takes a tested prototype out to a real, authentic audience — not just a classroom demo — and measures actual outcomes against the goals the team set at the start. The moment CBL's emphasis on "real" pays off.

## When It Triggers

- "We're ready to launch this for real."
- "Let's define what success looks like before we ship."
- "Here's how it went after our launch."
- "What were our actual results?"

## Prerequisites (Gate)

Requires a tested prototype to exist (at least one entry in `challenge/09-prototype-log/`). Auto-offers to route to `cbl-prototype` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's define what success looks like" (before launch) | **Set success metrics**: helps the team define concrete, measurable goals tied back to the original Challenge Statement — before shipping, not after, per the CBL research emphasis on measuring outcomes against defined goals (`research/04-cbl-product-building.md`). Records this in `challenge/10-implementation-evaluation.md`. |
| "we're ready to launch this for real" | **Implementation checklist**: confirms this is going to an authentic audience (not just the class), records launch details. |
| "here's how it went: [results/data]" | **Record outcomes**: logs actual results, compares against the pre-defined success metrics, and gives an honest read on whether the team hit them. |
| "what were our actual results?" | **Outcome summary**: reads back what's recorded so far, with the metrics-vs-actuals comparison. |
| (on any recorded metrics or results) | Also silently refreshes `canvas/cbl-canvas.html` — the Implementation & Evaluation stat callouts update as soon as real numbers are recorded, not just once the whole phase wraps. |

## Reads / Writes

- **Reads**: `challenge/03-challenge-statement.md` (original goal, for metric alignment), `challenge/08-prototype-plan.md` / `09-prototype-log/` (what's being implemented).
- **Writes**: `challenge/10-implementation-evaluation.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "We're ready to launch the signage redesign for real."
>
> **Claude:** "Before you do — what does success look like? Something like 'reduce visible plate waste by X% over two weeks' would be measurable and ties back to your Challenge Statement."
>
> **User:** defines the metric, launches, comes back two weeks later with results.
>
> **Claude:** compares actual vs. target, gives an honest read (hit it, missed it, or partial), records it.

## Notes & Edge Cases

- The CBL research is explicit that this needs a *real* audience, not a simulated one (`research/04-cbl-product-building.md`) — this skill should push back gently if a user describes something that sounds like an in-class-only demo rather than genuine implementation.
- Defining success metrics *before* launch (not retroactively) is a deliberate design choice here, matching the assessment guidance in `research/05-cbl-assessment-reflection.md` that rubrics/criteria work best set early, not just at grading time.
- "Missed the target" is a valid, expected outcome, not something the skill should soften — honest evaluation feeds directly into `cbl-reflect-share`, and CBL treats the process (including setbacks) as gradable, not just success.
