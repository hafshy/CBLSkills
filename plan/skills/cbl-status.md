# `cbl-status`

## Purpose

A read-only snapshot of the whole project: what's decided, what's still open, what's stale, and who's done what. The thing to run when you're not sure what to do next.

## When It Triggers

- "Where are we in the process?"
- "What's left to do?"
- "Show me the status of our CBL project."
- "What's stale / needs review?"
- "Who's done what so far?"

## Prerequisites (Gate)

Requires `cbl-init` to have run (there has to be a `.cbl/state.json` to read). If it hasn't, this skill itself triggers the standard auto-offer: "There's no CBL project here yet — want me to set one up?"

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "what's our status?" | **Full snapshot**: reads `.cbl/state.json`, renders a phase-by-phase summary — which artifacts are `not_started` / `options_generated` / `decided`, which are `stale`, and what the single next unblocked action is. |
| "what's stale?" | **Staleness-only view**: filters the snapshot down to just artifacts flagged `stale: true`, with a one-line reason for each (which upstream change caused it). |
| "who's done what?" | **Team view**: cross-references `.cbl/team.json` with `decided_by` fields across artifacts to show contribution by person. |
| "what's blocking us?" | **Gate view**: identifies the single next artifact that's `not_started` and explains what needs to happen to unblock it. |

## Reads / Writes

- **Reads**: `.cbl/state.json`, `.cbl/team.json`, `.cbl/constitution.md` (for timeline/deadline context).
- **Writes**: nothing. This is the one skill in the set (besides being paired with `cbl-init`) that's guaranteed side-effect-free.

## Example Interaction

> **User:** "Where are we in the process?"
>
> **Claude:** "Engage phase: done — Big Idea (Food Waste), Essential Question, and Challenge Statement are all decided. Investigate: in progress — Guiding Questions are decided, 2 of 5 have research findings recorded, Synthesis hasn't started. Act: not started. Nothing's currently stale. Next unblocked step: finish research on the remaining 3 Guiding Questions, or run Synthesis early if you think you have enough."

## Notes & Edge Cases

- Should never modify any file — this is the safe, no-risk skill to reach for when a user is unsure what state things are in, so it needs to be reliably side-effect-free to be trustworthy as that fallback.
- When multiple artifacts are simultaneously unblocked (e.g., research on several Guiding Questions can happen in parallel), the "what's blocking us" view should say so rather than implying strict single-file linearity.
- Should surface team-attribution data gracefully even for solo users — if there's only one team member, the "who's done what" view is just a lighter-weight version of the full snapshot, not an error.
- Doesn't trigger a canvas refresh itself (it writes nothing), but its snapshot should always agree with what the canvas currently shows, since both read from the same `.cbl/state.json` — if they ever disagree, that's a bug worth catching.
