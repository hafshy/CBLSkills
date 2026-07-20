# `cbl-prototype`

## Purpose

Turns the decided Solution Concept into an actual built thing, through a lightweight plan-then-iterate loop. The one skill explicitly designed to loop backward into Investigate when building surfaces new unknowns.

## When It Triggers

- "Let's plan how to build this."
- "We built version 1, here's what happened when we tested it."
- "This test revealed something we didn't know."
- "Let's do another iteration."

## Prerequisites (Gate)

Requires the Solution Concept to be `decided`. Auto-offers to run `cbl-solution-concepts` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's plan how to build this" (no plan exists yet) | **Propose approaches**: suggests 2–3 build approaches for the decided concept (e.g., different tech stacks, different physical build methods, different campaign formats — genuinely medium-agnostic), with a recommendation, then records the chosen plan in `challenge/08-prototype-plan.md` once confirmed. |
| "we built version 1, here's what we found" | **Log iteration**: records the build + test results as a new entry in `challenge/09-prototype-log/`, including what worked, what didn't, and any feedback gathered. |
| "this raised a new question we hadn't considered" | **Flag & route**: recognizes this as a new unknown rather than a simple bug, and offers to send it to `cbl-guiding-questions` as a new research question — keeps prototyping work marked "in progress, pending new research" rather than silently absorbing the gap. |
| "let's do another iteration" | **Next cycle**: starts a new logged iteration, referencing what changed since the last one. |
| (on any plan confirmation or logged iteration) | Also silently refreshes `canvas/cbl-canvas.html` — the Prototype & Iteration section's timeline/stepper stays current after every build-test cycle, not just at the end. |

## Reads / Writes

- **Reads**: `challenge/07-solution-concepts.md` (decided concept), `challenge/08-prototype-plan.md`, `challenge/09-prototype-log/` (iteration history).
- **Writes**: `challenge/08-prototype-plan.md`, `challenge/09-prototype-log/<iteration-N>.md`, `.cbl/state.json`; may also trigger a write to `challenge/04-guiding-questions.md` (via handoff, not directly) when new questions surface.

## Example Interaction

> **User:** "We built the first version of our composting tracker app and tested it with three families — turns out nobody understood the 'contamination rate' metric we used."
>
> **Claude:** "That sounds like a new Guiding Question worth investigating — something like 'what food-waste metrics do families actually understand?' Want me to add that and loop back into research, or is this a quick fix you can just make in the next iteration?"
>
> **User:** "Let's add it as a real guiding question."
>
> **Claude:** hands off to `cbl-guiding-questions` with the new question appended; logs this iteration's finding either way.

## Notes & Edge Cases

- This is the one skill in the whole set expected to routinely trigger backward movement into an earlier phase — that's not a failure mode, it's the CBL framework working as designed (`research/02-cbl-process-steps.md`).
- Should resist the temptation to auto-classify every test finding as either "trivial fix" or "new research question" — when it's ambiguous, ask, rather than guessing wrong in either direction (silently absorbing something that actually needed research, or over-escalating a minor UI complaint into a full research cycle).
- Because it's genuinely medium-agnostic, the "build approaches" it proposes should visibly reflect whatever the Solution Concept actually is — a physical build, a campaign, and a piece of software should produce meaningfully different-looking plans, not a generic template with the nouns swapped.
