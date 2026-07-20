# `cbl-reflect-share`

## Purpose

Closes out the project: a genuine reflection on the whole journey, plus a shareable case study/report — the "Reflect, Document, Share" thread that CBL treats as running underneath the entire process, brought to a formal close here.

## When It Triggers

- "We're basically done — help us wrap this up."
- "Let's write our closing reflection."
- "Can you put together something we can present to the class?"
- "Make us a case study of what we did."

## Prerequisites (Gate)

Requires Implementation & Evaluation to have at least recorded results (`challenge/10-implementation-evaluation.md` not empty). Auto-offers to route to `cbl-implement-evaluate` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's write our closing reflection" | **Reflect**: prompts the team through what was learned, what challenges came up, how they were (or weren't) overcome, and what they'd do differently — pulled together from documentation across all phases, not written from scratch. Fills `challenge/11-reflection-and-share.md`. |
| "make us a case study" / "something to present" | **Produce shareable artifact**: assembles a presentation-ready report or case study narrative — Big Idea through outcomes — suitable for a class presentation, printout, or write-up. |
| "update the canvas too" | **Redundant, but harmless**: writing the reflection already auto-refreshes the canvas as part of the standard state.json-write behavior, so by the time this skill finishes, the canvas already shows all sections filled and the progress footer at 100% — a manual request just re-confirms that. |

## Reads / Writes

- **Reads**: every `challenge/*` artifact — this is the one skill that genuinely pulls from the entire project, not just its immediate upstream neighbor.
- **Writes**: `challenge/11-reflection-and-share.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "We're basically done — can you put together something we can present to the class?"
>
> **Claude:** runs the reflection prompts (what worked, what didn't, what changed the team's thinking along the way), then assembles a case study covering Food Waste as the Big Idea through the implemented signage redesign and its measured impact. Also offers to refresh the CBL Canvas so it's presentation-ready.
>
> **Claude:** "Done — you've got a written case study and an updated one-page canvas. Good for either a slide or a printout for presentation day."

## Notes & Edge Cases

- Reflection quality matters more than polish here — the CBL research is explicit that documentation and reflection are core learning mechanisms, not an afterthought (`research/05-cbl-assessment-reflection.md`); this skill should genuinely prompt for honest reflection, not just auto-summarize the project's documentation into a report.
- This is a natural place to loop in `cbl-canvas` as a matched pair, but it shouldn't assume the user wants that automatically — offer it, don't force it.
- Marks the formal "close" of the tracked CBL process in `.cbl/state.json`, but per the architecture plan's non-linearity principle, nothing about this skill prevents a team from later reopening any earlier step if they genuinely want to keep iterating past a class deadline.
