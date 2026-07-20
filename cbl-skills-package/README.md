# CBL Skills — Challenge Based Learning for Claude

A spec-kit-style set of 14 sequenced, gated Claude skills that walk a student team through
the full Challenge Based Learning (CBL) process — Engage → Investigate → Act — while actually
building a real product, not just planning one on paper.

## What's in this package

```
skills/       14 SKILL.md files — the skills themselves (this is what Claude reads/triggers on)
cbl_core/     Shared Python library the skills call into via `python3 -m cbl_core.cli ...`
              (state tracking, gating/staleness, canvas rendering, git team helpers)
```

`cbl_core` is not optional scaffolding — every skill's Bash steps shell out to it. Both folders
need to travel together.

## Requirements

- Python 3.8+ (standard library only — no pip installs needed to run the skills)
- `git` (local only; no GitHub account, token, or connector required)

## Installing

1. Copy `skills/*` into wherever your Claude setup loads skills from (a project's `.claude/skills/`
   directory, a Cowork plugin's `skills/` folder, etc. — same mechanism as any other skill).
2. Copy `cbl_core/` to the same project root the skills will run in, and make sure it's importable —
   either run Claude's Bash tool with that root as the working directory, or set
   `PYTHONPATH` to include it. Every `SKILL.md` assumes `python3 -m cbl_core.cli <command> "<project_root>" ...`
   resolves.
3. Sanity check:
   ```bash
   cd <project_root>
   python3 -m pytest cbl_core/tests/
   ```
   35 tests should pass.

## Using it

Start a new project with `cbl-init` ("let's start a new CBL project"). It scaffolds `.cbl/`,
`challenge/*` document templates, a blank `canvas/cbl-canvas.html`, and a local git repo. From
there, work through the skills in CBL's own order — `cbl-big-idea` → `cbl-essential-question` →
`cbl-challenge-statement` → `cbl-guiding-questions` → `cbl-research` → `cbl-synthesis` →
`cbl-solution-concepts` → `cbl-prototype` → `cbl-implement-evaluate` → `cbl-reflect-share` — with
`cbl-status`, `cbl-canvas`, and `cbl-merge` available at any point for read-only checks, viewing the
canvas, and pulling in a teammate's work.

Each content skill checks its own gate before doing anything and will offer to run whatever
prerequisite is missing rather than failing silently. Reopening and re-deciding an earlier step
(e.g. changing the Big Idea after later work exists) is supported — everything downstream gets
flagged stale rather than blocked, and the CBL Canvas auto-refreshes on every decision.

## Team collaboration

Local-git only, spec-kit style: each teammate works in their own `team/<name>/` folder and git
branch (created via `cbl-init`'s join mode), and `cbl-merge` reconciles contributions back into
the canonical `challenge/` docs — with plain-language conflict resolution, never raw git markers
shown to the user. No GitHub connector, API, or account required.

## Design docs

If you want the reasoning behind the architecture (why gating works the way it does, the full
staleness-propagation model, the generate → add → decide pattern, the CBL Canvas layout spec),
see `plan/01-cbl-skills-architecture-plan.md` and the rest of the `plan/` and `research/` folders
in the original project — not included in this runtime package, but worth keeping alongside it
if you plan to extend the skill set.

## Status

Built and tested through Milestone 6 (full integration test) of the project's execution plan:
35 unit tests, plus end-to-end runs covering a full Engage → Investigate → Act project, the
staleness cascade on a late reopen, canvas auto-refresh at every trigger point, and a simulated
two-person merge with a real conflict.
