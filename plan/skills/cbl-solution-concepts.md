# `cbl-solution-concepts`

## Purpose

The last of the five generate/add/decide skills (architecture plan §6): turns the Investigate-phase synthesis into concrete Solution Concept options and helps the team pick one to actually build. Medium-agnostic — a Solution Concept can be a product, a campaign, a service, or a community project, per CBL's own treatment of Act-phase outcomes.

## When It Triggers

- "Let's brainstorm solution concepts."
- "What could we actually build?"
- "Add my own idea: [X]."
- "Which concept should we go with?"

## Prerequisites (Gate)

Requires Synthesis to exist (`challenge/06-synthesis.md`). Auto-offers to run `cbl-synthesis` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's brainstorm solution concepts" | **Generate**: produces 3–5 concept options grounded directly in the synthesis findings — explicitly not software-only; can be a product, campaign, service, or community project. Each option: summary, why it fits the findings, one honest risk. Fills `challenge/07-solution-concepts.md`. |
| "give me more options" | **Generate again**: appends. |
| "add my own idea: [X]" | **Add manually**: appended as a first-class option. |
| "what do you recommend?" / "let's decide" | **Decide**: compares options (fit with synthesis findings, feasibility given team/timeline from the constitution, risk), recommends one, asks for confirmation. |
| "our concept is [X], lock it in" | **Direct decide**: skips straight to comparison/recommendation against the synthesis, confirms before writing. |
| (on any confirmed decision) | Also silently refreshes `canvas/cbl-canvas.html` — this is what first populates the canvas's Solution Concept section, including showing runner-up options greyed out for context. |

## Reads / Writes

- **Reads**: `challenge/06-synthesis.md`, `.cbl/constitution.md` (timeline/team size, for feasibility judgment), `challenge/07-solution-concepts.md` (existing state).
- **Writes**: `challenge/07-solution-concepts.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "What could we actually build, based on what we found?"
>
> **Claude:** presents 4 options grounded in the synthesis: a composting tracker app, a cafeteria signage redesign, a "adopt a lunch tray" awareness campaign, and a portion-size pilot program — each with fit/risk notes.
>
> **User:** "What's your recommendation given we only have 4 weeks left?"
>
> **Claude:** recommends the signage redesign as lower-risk given the timeline, while noting the composting tracker was the most ambitious/interesting option if they had more time.

## Notes & Edge Cases

- This is the skill most likely to get pulled toward "just build the coolest idea" — the decide step should weight feasibility against the constitution's actual timeline/team size honestly, not just novelty.
- Runner-up options (generated but not chosen) matter beyond this step — the CBL Canvas (§4a of the architecture plan) explicitly shows them, greyed out, for narrative context ("we also considered...").
- Once decided, this is the gate for `cbl-prototype` — nothing in Act's build phase should start before a concept is actually locked in.
