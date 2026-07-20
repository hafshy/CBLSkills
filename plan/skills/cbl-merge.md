# `cbl-merge`

## Purpose

Takes a teammate's contribution — living in their `team/<name>/` folder or branch — and gets it into the canonical `challenge/` documents, with a human-readable review step in between, not raw git conflict markers.

## When It Triggers

- "Help me merge my research into the team's docs."
- "Can you review what [teammate] drafted and get it into our shared files?"
- "I finished my part, how do I get it committed?"

## Prerequisites (Gate)

Requires a draft or branch to actually exist in someone's `team/<name>/` folder. If there's nothing to merge, the skill says so plainly rather than pretending to do work.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "merge my research on guiding question 2" | **Diff & review**: reads the contribution from the teammate's branch/folder, diffs it against the current canonical file in `challenge/`, and shows a plain-language summary of what's new/changed — not a raw diff dump. |
| (after review) "yes, merge it" | **Commit**: writes the merged result into the canonical `challenge/` file, commits to the shared branch, updates `.cbl/state.json` (including `decided_by`/contributor attribution where relevant). |
| "there's a conflict, what do I do?" | **Conflict resolution, in plain language**: describes what's different between the two versions in terms of content ("your teammate's version answers the question differently — here's both, which do you want to keep, or should I combine them?"), never surfaces raw `<<<<<<<` markers to the user. |
| "what's waiting to be merged?" | **Pending list**: scans all `team/<name>/` folders/branches for contributions not yet reflected in `challenge/`. |

## Reads / Writes

- **Reads**: the relevant `team/<name>/` folder or git branch, the corresponding canonical `challenge/*` file, `.cbl/team.json`.
- **Writes**: the canonical `challenge/*` file (on confirm), `.cbl/state.json` (contributor + timestamp), commits to the shared git branch/remote.

## Example Interaction

> **Teammate B:** "I did the research on our second guiding question, can you help me get it merged into the team's docs?"
>
> **Claude:** "This adds a new file to `challenge/05-research-findings/` — no conflicts with what's already there. Here's a summary of what you found: [...]. Want me to merge this in?"
>
> **Teammate B:** "Yes."
>
> **Claude:** "Merged and committed. I've noted you as the contributor for this finding."

## Notes & Edge Cases

- Resolved (architecture plan §7): this skill runs on plain local git commands (`git diff`, `git merge`, `git push`) via the shell against a remote the team already set up and authenticated — no GitHub connector required, matching how spec-kit itself operates. A connector remains a possible future nicety (e.g., opening an actual PR instead of merging directly), but nothing here depends on one.
- Should distinguish "no conflict, straightforward addition" from "genuine conflict, needs a human call" — most merges (new research findings, new options added to a list) are the former and shouldn't be treated with the same ceremony as the latter.
- Never auto-merges without the explicit confirmation step, even when a conflict looks trivial — matches the broader "never auto-select, always confirm" principle used throughout the generate/decide skills.
- A successful merge into `challenge/*` is itself a `.cbl/state.json` update, so it triggers the same silent canvas auto-refresh as any other skill — a teammate's merged research shows up in the canvas without anyone needing to ask.
