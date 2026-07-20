# `cbl-synthesis`

## Purpose

Closes out the Investigate phase: pulls together everything recorded in `cbl-research` into clear conclusions the team can actually build a solution on. Execution/synthesis skill, not generate/decide.

## When It Triggers

- "Let's synthesize our research."
- "What have we learned overall?"
- "Are we ready to move to Act?"

## Prerequisites (Gate)

Requires at least one research finding to exist in `challenge/05-research-findings/`. Doesn't require *every* Guiding Question to be answered — the skill itself will flag gaps rather than silently ignoring them or blocking entirely.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's synthesize our research" | **Synthesize**: reads all recorded findings, identifies patterns/themes across them, drafts clear conclusions. Fills `challenge/06-synthesis.md`. |
| "are we ready to move to Act?" | **Readiness check**: compares findings against the prioritized Guiding Questions list, explicitly flags which questions still have no findings, and gives an honest read on whether the gap is safe to proceed with or worth going back to research first. |
| "add this finding, I forgot to log it" | **Late addition**: routes to `cbl-research` to record the finding properly, then re-synthesizes to fold it in. |
| "revise the synthesis" | **Redo**: re-runs synthesis against the current findings (useful after late additions or new research). |
| (on any written/revised synthesis) | Also silently refreshes `canvas/cbl-canvas.html` — this is the skill whose output actually fills the canvas's Research Synthesis section for the first time. |

## Reads / Writes

- **Reads**: everything in `challenge/05-research-findings/`, `challenge/04-guiding-questions.md` (to check coverage).
- **Writes**: `challenge/06-synthesis.md`, `.cbl/state.json`.

## Example Interaction

> **User:** "Are we ready to move to Act?"
>
> **Claude:** "Mostly — you've got solid findings on 4 of your 5 prioritized questions. The one gap is technical feasibility of the composting sensor, which nobody's researched yet. You could proceed and treat that as a prototyping risk, or spend a bit more time on it first — your call."

## Notes & Edge Cases

- This is a genuine judgment step, not just concatenation — the value is in identifying *themes and conclusions*, not just listing what was found. Should read more like a short report than a bulleted dump of raw findings.
- Explicitly flagging gaps (rather than silently proceeding) matters — this is where a team could otherwise walk into Act without a real foundation, which the CBL research (`research/05-cbl-assessment-reflection.md`) treats as a real quality risk.
- This is the gate for `cbl-solution-concepts` — Act can't meaningfully start without at least one synthesis pass, even an imperfect one.
