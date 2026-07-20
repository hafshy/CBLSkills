# `cbl-big-idea`

## Purpose

Handles the first real decision of the project: picking a Big Idea — a broad, personally and communally meaningful theme (Community, Sustainability, Health, etc.) that everything else builds on. First artifact skill in the sequence.

## When It Triggers

- "Let's figure out our Big Idea."
- "What should our theme be?"
- "I want to add my own idea: [X]."
- "Our Big Idea is [X], lock that in."
- "I want to revisit our Big Idea." (reopening, mid- or late-project)

## Prerequisites (Gate)

Requires `cbl-init` to have run. This is the lightest gate in the whole skill set — nothing upstream except project setup itself.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's figure out our Big Idea" (file still `status: not_started`) | **Generate**: produces 3–5 options, each with a one-line summary, why it fits the team/context, and one honest risk or limitation. Fills in the `Options` section of `challenge/01-big-idea.md`, sets `status: options_generated`. Ends by asking: generate more, add your own, or decide now? |
| "give me more options" / "try again, I don't love these" | **Generate again**: appends new options, keeps existing ones unless told to drop them. |
| "add my own idea: [X]" | **Add manually**: appends the user's idea to the options list in the same format as generated ones — treated as a first-class option, not a footnote. |
| "let's decide" / "what do you recommend?" / "go with option 2" | **Decide**: compares existing options (personal relevance, community relevance, feasibility), gives one clear recommendation with reasoning, asks for explicit confirmation. |
| "our Big Idea is [X], lock that in" (no options exist yet) | **Direct decide**: treats this as a user-submitted option plus an immediate decide request — sanity-checks it against the constitution, confirms before writing. |
| "I want to revisit our Big Idea" (already decided) | **Reopen**: loads the existing decision, offers to generate alternatives or refine, and on a new decision, marks Essential Question / Challenge Statement / everything downstream as `stale` if they already exist. |
| (on any confirmed decision) | Also silently refreshes `canvas/cbl-canvas.html` as the last step — no separate request needed. |

## Reads / Writes

- **Reads**: `challenge/01-big-idea.md` (existing options/decision, if any), `.cbl/constitution.md` (scope/context for generation and sanity-checking).
- **Writes**: `challenge/01-big-idea.md`, `.cbl/state.json` (status, `decided_by`, `decided_at`, and staleness propagation to downstream artifacts on redecision).

## Example Interaction

> **User:** "Let's figure out our Big Idea."
>
> **Claude:** presents 5 options (Community, Sustainability, Digital Wellbeing, Accessibility, and a user-added "Food Waste") with fit/risk notes, asks what's next.
>
> **User:** "What do you recommend?"
>
> **Claude:** recommends Food Waste — "specific, locally actionable, ties to Sustainability without being abstract" — asks for confirmation.
>
> **User:** "Let's go with that."
>
> **Claude:** "Locked in: 'Food Waste.' Ready to move to your Essential Question?"

## Notes & Edge Cases

- This is the reference implementation for the generate/add/decide pattern (architecture plan §6) — `cbl-essential-question`, `cbl-guiding-questions`, and `cbl-solution-concepts` all follow this exact shape, so getting this one right matters disproportionately.
- Never auto-selects on a vague signal ("I like the second one" without an explicit go-ahead) — always confirms before writing `status: decided`.
- Big Ideas are intentionally broad; the skill shouldn't push toward something that's already specific enough to be a Challenge Statement — that narrowing happens two steps later, deliberately.
