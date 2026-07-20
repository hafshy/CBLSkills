# `cbl-challenge-statement`

## Purpose

Converts the decided Essential Question into a Challenge Statement — an actionable call to action that closes out the Engage phase and becomes the anchor everything downstream (Guiding Questions, Solution Concepts) is checked against.

## When It Triggers

- "Let's write our Challenge Statement."
- "Turn our essential question into a challenge."
- "I think our Challenge Statement is too broad, can we revisit it?"
- "Our challenge is [X], lock it in."

## Prerequisites (Gate)

Requires the Essential Question to be `decided`. Auto-offers to run `cbl-essential-question` first if missing.

## What Users Can Do

A lighter version of the generate/add/decide pattern — candidate phrasings tend to be closer variations of each other than, say, Big Idea options, so this skill folds generation and decision into a tighter loop:

| User says something like... | Skill does |
|---|---|
| "let's write our Challenge Statement" | **Generate**: produces 2–3 candidate phrasings from the decided Essential Question, each actionable, specific, and open enough to allow multiple solution paths (per the "Design/Create/Develop a ___ that ___ for ___" pattern from `research/02-cbl-process-steps.md`). Fills `challenge/03-challenge-statement.md`. |
| "try a different phrasing" | **Generate again**: appends alternative phrasings. |
| "I'd phrase it as: [X]" | **Add manually**: appended as a candidate. |
| "which one's best?" / "let's decide" | **Decide**: recommends one phrasing with reasoning (does it call for real action? is it too broad or too narrow?), confirms before finalizing. |
| "our Challenge Statement is too broad, can we revisit it?" (already decided) | **Reopen**: loads the existing statement, offers narrower/alternate phrasings; on redecision, marks Guiding Questions, Synthesis, Solution Concepts, and Prototype Plan `stale`. |
| (on any confirmed decision) | Also silently refreshes `canvas/cbl-canvas.html` as the last step. |

## Reads / Writes

- **Reads**: `challenge/02-essential-question.md` (decided EQ), `challenge/03-challenge-statement.md` (existing state), `.cbl/constitution.md`.
- **Writes**: `challenge/03-challenge-statement.md`, `.cbl/state.json`.

## Example Interaction

> **User (mid-project):** "Actually, I think our Challenge Statement is too broad. Can we revisit it?"
>
> **Claude:** loads the current statement, offers 2 narrower alternatives, explains the tradeoff (narrower = more focused research and prototyping, less room to pivot later).
>
> **User:** picks one, confirms.
>
> **Claude:** "Updated. Heads up: your Guiding Questions, Synthesis, Solution Concept, and Prototype Plan were all written against the old Challenge Statement, so they're flagged for review — nothing's broken, just worth a look."

## Notes & Edge Cases

- This is the artifact with the widest blast radius on reopening — nearly the entire rest of the project depends on it, so the staleness-cascade behavior (architecture plan §5) matters most here. Should always explicitly name what's about to be marked stale before finalizing a change, not just do it silently.
- The output closes Phase 1 — this skill should end its "decided" confirmation by pointing the user at `cbl-guiding-questions` as the natural next step, the same way `cbl-big-idea` points at `cbl-essential-question`.
