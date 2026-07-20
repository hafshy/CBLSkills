---
name: cbl-merge
description: Reviews a teammate's draft contribution or branch and merges it into the canonical Challenge Based Learning (CBL) project documents, with a human-readable review step instead of raw git conflict markers. Use when someone says "help me merge my research into the team's docs", "can you review what [teammate] drafted", "I finished my part, how do I get it committed", or "what's waiting to be merged". Plain local git only — no GitHub connector or API required.
---

# CBL Merge

Two kinds of contributions this skill handles, and they need different git operations:

1. **Draft content in a teammate's `team/<name>/` folder** — freeform notes/ideas, not yet in the canonical structure. No git conflict risk (it's untracked scratch content); the job here is figuring out *where it belongs* in `challenge/` and getting it there in the right format.
2. **Committed changes on a teammate's `team/<name>` branch** — they've actually edited a `challenge/*` file directly on their branch. This is a real git merge, with real conflict potential.

## Sub-behavior: What's waiting to be merged?

**Trigger**: "what's waiting to be merged?"

```bash
cd "<project_root>"
git status --porcelain team/  # untracked/modified draft content across all member folders
git log main..team/<name> --oneline  # commits on a member's branch not yet in main, per member
```

Summarize in plain language: whose folders have unmerged drafts, whose branches have unmerged commits.

## Sub-behavior: Merge draft folder content

**Trigger**: "merge my research on guiding question 2" / "help me get my draft into the team's docs" (content lives in `team/<name>/`, not yet committed to `challenge/`).

1. Read the draft file(s) in `team/<name>/`.
2. Figure out where it belongs — a set of Big Idea ideas maps to `challenge/01-big-idea.md`'s `## Options`; research notes on a specific Guiding Question map to a new file in `challenge/05-research-findings/`; etc. If it's ambiguous, ask rather than guess.
3. Show the user a plain-language summary of what you're about to add (not a raw diff).
4. On confirmation, write it into the canonical location **using that artifact's own established format** (e.g. research findings follow `cbl-research`'s finding-file format; Big Idea options follow `cbl-big-idea`'s Options format) — don't invent a different shape just because it arrived via merge instead of directly.
5. Commit:
   ```bash
   git add "challenge/<path>"
   git commit -m "cbl-merge: <name>'s <what> into <artifact>"
   ```
6. If the merge changes an artifact's status meaningfully (e.g. this is the first research finding logged), update state the same way the owning skill would:
   ```bash
   python3 -m cbl_core.cli set-status "<project_root>" <artifact> --status <appropriate-status>
   ```
   This also triggers the canvas auto-refresh, same as any other skill's write.

## Sub-behavior: Merge a teammate's branch

**Trigger**: same phrasings, but the contribution is committed on `team/<name>` rather than sitting as an untracked draft.

1. See what's different:
   ```bash
   git diff main team/<name> -- challenge/
   ```
2. **No conflict** (the branch only touches files main hasn't touched, or only adds new files): this is the common case for research findings from different people on different questions. Summarize what's new, confirm, then:
   ```bash
   git checkout main
   git merge team/<name> --no-ff -m "cbl-merge: merge <name>'s contribution"
   ```
3. **Real conflict** (both branches changed the same file in incompatible ways — e.g. two people both wrote a finding for the same Guiding Question with different content): do **not** run a raw `git merge` and show the user conflict markers. Instead:
   - Read both versions yourself (`git show main:<path>` and `git show team/<name>:<path>`).
   - Describe the actual difference in plain language: "your teammate's version says X, the canonical version says Y — want to keep yours, theirs, or combine both?"
   - Once the user decides, write the resolved content yourself and commit it directly — never surface `<<<<<<<`/`=======`/`>>>>>>>` markers to the user.
   ```bash
   git add "challenge/<path>"
   git commit -m "cbl-merge: resolve conflict on <path>, combining <name> and canonical"
   ```
4. Same as the draft-folder case: if this changes an artifact's status, call `set-status` afterward so state.json and the canvas stay current.

## Notes & Edge Cases

- **Never auto-merge without showing the user what's changing first**, even when it looks like an obviously clean addition — confirmation before writing to canonical docs is the same rule every decide-skill in this set follows, and it applies here too.
- Distinguish "no conflict, straightforward addition" from "genuine conflict, needs a human call" up front — most merges (a new research finding, a new option someone drafted) are the former and don't need heavy ceremony; treat them lightly. Save the careful conflict-resolution walkthrough for when there's an actual incompatibility.
- If `git diff main team/<name>` or similar commands fail because the branch doesn't exist locally, that likely means this teammate hasn't actually pushed/fetched through a shared remote yet — say so plainly rather than treating it as "nothing to merge." This is the collaboration model's real dependency on a working git remote (architecture plan S7) surfacing in practice.
- This skill only ever writes to `challenge/*` and (via the CLI) to `.cbl/state.json` — never asks the user to resolve git internals themselves.
