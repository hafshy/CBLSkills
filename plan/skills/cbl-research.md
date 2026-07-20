# `cbl-research`

## Purpose

The execution engine of the Investigate phase: assigns prioritized Guiding Questions to team members and tracks the findings as they come in. Not a generate/decide skill — there's nothing to "decide" here, just work to track.

## When It Triggers

- "Let's start researching our guiding questions."
- "I'll take question 2, here's what I found."
- "Assign the guiding questions to the team."
- "What have we found so far?"

## Prerequisites (Gate)

Requires Guiding Questions to be `decided` (i.e., prioritized). Auto-offers to run `cbl-guiding-questions` first if missing.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "assign the guiding questions to the team" | **Assign**: distributes prioritized questions across registered team members (from `.cbl/team.json`), balancing load, and records assignments. |
| "I'll take question 2" | **Self-assign**: records this user as the owner of a specific question. |
| "here's what I found for question 2: [notes/sources]" | **Record finding**: writes/updates `challenge/05-research-findings/<question>.md` with the finding, source, and contributor; marks that question `answered`. |
| "what have we found so far?" | **Progress view**: summarizes findings recorded to date, flags which prioritized questions still have no findings. |
| "this research raised a new question" | **Hand off**: routes back to `cbl-guiding-questions` to append the new question rather than absorbing it here. |
| (on any recorded finding) | Also silently refreshes `canvas/cbl-canvas.html` — even though individual findings aren't shown on the canvas directly (only the eventual Synthesis is), the render still runs so the canvas stays in lockstep with `.cbl/state.json` at all times, per the uniform refresh rule. |

## Reads / Writes

- **Reads**: `challenge/04-guiding-questions.md` (prioritized list), `.cbl/team.json`.
- **Writes**: `challenge/05-research-findings/<question-slug>.md` (one file per question or per researcher), `.cbl/state.json` (per-question status, contributor).

## Example Interaction

> **User:** "I'll take question 2 — what do families actually understand about food waste metrics?"
>
> **Claude:** "Got it, that's yours. Let me know what you find, or if you want a hand identifying good sources/activities to start with."
>
> *(later)* **User:** "Found it — most families don't recognize 'contamination rate' as a term, but they do understand 'wasted vs. usable.'"
>
> **Claude:** records the finding to `challenge/05-research-findings/q2-family-metrics.md`, marks question 2 `answered`.

## Notes & Edge Cases

- This skill can offer research *support* (suggesting resources/activities per the CBL "Guiding Resources/Activities" concept from `research/02-cbl-process-steps.md`) without doing the research itself — the actual investigation is the team's work, not something to auto-generate plausible-sounding findings for.
- With a distributed team, this is one of the more naturally parallel skills — multiple teammates can be actively researching different questions in their own sessions simultaneously; the skill shouldn't assume single-user sequential use.
- Feeds `cbl-synthesis`, which needs at least one recorded finding to have anything to work with — this skill's gate for downstream progress is "at least one finding," not "every question answered."
