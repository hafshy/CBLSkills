# `cbl-essential-question`

## Purpose

Turns the decided Big Idea into a personal, specific Essential Question — the bridge between an abstract theme and an actionable Challenge.

## When It Triggers

- "Let's work on our Essential Question."
- "What's our essential question?"
- "Add my own essential question: [X]."
- "Our essential question is [X], confirm that."
- "I want to revisit our Essential Question."

## Prerequisites (Gate)

Requires the Big Idea to be `decided`. If not, offers to auto-run `cbl-big-idea` first rather than just stopping.

## What Users Can Do

Same three-part shape as `cbl-big-idea` (generate / add / decide), scoped to this artifact:

| User says something like... | Skill does |
|---|---|
| "let's work on our Essential Question" | **Generate**: produces 3–5 candidate questions rooted in the decided Big Idea, each testing personal relevance ("why does this matter to me?") and community relevance ("where does this intersect with my world?"). Fills `challenge/02-essential-question.md`. |
| "give me more options" | **Generate again**: appends, doesn't overwrite. |
| "add my own: [X]" | **Add manually**: appended as a first-class option. |
| "what do you recommend?" / "let's decide" | **Decide**: compares candidates on specificity and personal connection, recommends one, asks for confirmation. |
| "our Essential Question is [X], confirm that" | **Direct decide**: sanity-checks against the decided Big Idea (does this question actually connect to it?), confirms before writing. |
| "revisit our Essential Question" (already decided) | **Reopen**: loads existing decision, offers alternatives; on redecision, marks Challenge Statement and everything downstream `stale`. |
| (on any confirmed decision) | Also silently refreshes `canvas/cbl-canvas.html` as the last step. |

## Reads / Writes

- **Reads**: `challenge/01-big-idea.md` (decided Big Idea), `challenge/02-essential-question.md` (existing state), `.cbl/constitution.md`.
- **Writes**: `challenge/02-essential-question.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "Our Essential Question is 'why does our cafeteria throw away so much food every day?' — that's what we're going with."
>
> **Claude:** "That connects clearly to your Big Idea (Food Waste) and it's personally specific — good essential question. Confirm this as your decision?"
>
> **User:** "Confirmed."
>
> **Claude:** written to `challenge/02-essential-question.md`, state updated.

## Notes & Edge Cases

- The main quality check this skill should apply — more than the others — is *personal relevance*. A technically-correct question that doesn't actually connect to the team's own experience is a weaker Essential Question even if it's well-formed, per the CBL research (`research/02-cbl-process-steps.md`).
- Should gently push back (not block) if a proposed question is really a Big Idea restated too broadly, or a Challenge Statement already too narrow/action-oriented — this step sits deliberately in between.
