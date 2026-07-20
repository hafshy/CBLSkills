# `cbl-guiding-questions`

## Purpose

Generates and prioritizes the Guiding Questions the team needs to answer to build an informed solution — the research roadmap for the whole Investigate phase. Unlike the Engage-phase skills, "deciding" here means selecting/prioritizing a set, not picking exactly one.

## When It Triggers

- "Let's figure out our Guiding Questions."
- "What do we need to research?"
- "Add a guiding question: [X]."
- "Which questions should we prioritize?"

## Prerequisites (Gate)

Requires the Challenge Statement to be `decided`. Auto-offers to run `cbl-challenge-statement` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's figure out our Guiding Questions" | **Generate**: casts a wide net — produces a full list of questions the team would need answered to build a credible solution, grouped by theme (e.g., user needs, technical constraints, existing solutions, context/market). Fills `challenge/04-guiding-questions.md`. |
| "give me more" | **Generate again**: appends more questions/themes. |
| "add a guiding question: [X]" | **Add manually**: appended to the appropriate theme (or a new one). |
| "which should we prioritize?" / "let's decide" | **Decide (prioritize, not single-select)**: analyzes the full list for what's most critical to answer first vs. nice-to-have, recommends a prioritized subset to actively pursue, asks for confirmation — but doesn't delete the rest, since new questions can surface later (e.g., from `cbl-prototype`). |
| "this raised a new question: [X]" (from a later phase, e.g. prototyping) | **Append mid-project**: adds a new question flagged as arising from later work, without disturbing already-answered ones. |
| (on any confirmed prioritization or addition) | Also silently refreshes `canvas/cbl-canvas.html` as the last step. |

## Reads / Writes

- **Reads**: `challenge/03-challenge-statement.md`, `challenge/04-guiding-questions.md` (existing state).
- **Writes**: `challenge/04-guiding-questions.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "Let's figure out our Guiding Questions."
>
> **Claude:** generates ~10 questions across 4 themes (user needs, existing solutions, technical feasibility, school policy constraints), asks whether to prioritize now or add more first.
>
> **User:** "Prioritize."
>
> **Claude:** recommends the 5 most critical to answer before Act, explains why the other 5 can wait, asks for confirmation.

## Notes & Edge Cases

- The "decide" step here is fundamentally different from the Engage-phase skills — it's a *selection/ranking* action, not a single pick. The comparison table should reflect that (question / why it matters / how hard to answer), not force a single winner.
- This is the artifact most likely to be reopened mid-project, not because the Challenge changed but because `cbl-prototype` legitimately surfaces new unknowns — the skill should treat additions from that path as completely normal, not as reopening/staleness in the usual sense (nothing here becomes wrong, it just grows).
- Feeds directly into `cbl-research`, which needs the prioritized subset, not the full brainstormed list, to know what to actually assign.
