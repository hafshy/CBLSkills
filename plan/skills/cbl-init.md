# `cbl-init`

## Purpose

Sets up a CBL project from scratch, or — run again by a new teammate — joins an existing one. This is always the first skill anyone touches, and the only one with no prerequisites.

## When It Triggers

- "I'm starting a class project with my team, can you help us set up CBL?"
- "We want to use Challenge Based Learning to build something — where do we start?"
- "My teammate already set this up, I need to join the project."
- "Set up a new CBL challenge for [team name]."

## Prerequisites (Gate)

None. This is the entry point. It's the only skill in the set that never has anything to check for before running.

## What Users Can Do

| User says something like... | Skill does |
|---|---|
| "let's set up a new CBL project" (no `.cbl/` folder exists yet in this location) | **First-time init**: asks a few setup questions (team/challenge name, rough timeline, whether a git remote already exists or needs creating), writes `.cbl/constitution.md`, creates `.cbl/state.json` and `.cbl/team.json`, scaffolds every `challenge/*.md` file as an empty template (frontmatter + placeholder sections), renders a blank `canvas/cbl-canvas.html`, initializes git and commits the scaffold, registers the user as the first team member. |
| "help me join my team's project" (`.cbl/` already exists, this user isn't in `team.json` yet) | **Join mode**: assumes this user has already cloned the shared remote and has their own git credentials working (a one-time setup step outside this skill, same as joining any git project). Detects the existing project, does *not* re-scaffold anything, creates `team/<name>/` for this user and a `team/<name>` git branch — once, not per session — registers them in `.cbl/team.json`. From then on they keep working in that same branch across all future sessions. |
| "what does our constitution say?" / "can we change our timeline?" | **Constitution edit**: reads/updates `.cbl/constitution.md` — team norms, scope constraints, roles, timeline. Available any time, not just at setup. |
| "we don't have a GitHub repo yet" | **Remote setup guidance**: Claude can't create hosting accounts or repos on its own, connector or not — walks the user through creating the remote themselves and configuring `git remote add origin`. Everything after that (branches, commits, push/pull) is plain local git via the shell, no connector required — same approach spec-kit uses. |

## Reads / Writes

- **Reads**: nothing (first-time run); `.cbl/team.json` (join mode, to check if this user is already registered).
- **Writes**: `.cbl/constitution.md`, `.cbl/state.json`, `.cbl/team.json`, all 11 `challenge/*.md` templates, `canvas/cbl-canvas.html` (blank), `.git/` (init + first commit), `team/<name>/` (per member).

## Example Interaction

> **User:** "I'm starting a class project with my team — we want to use Challenge Based Learning to build something. Can you help us set up?"
>
> **Claude:** "Happy to. A few quick things: what should we call this project? Roughly how long do you have? And do you already have a shared GitHub repo, or should we set one up?"
>
> *(after answers)*
>
> **Claude:** "You're set up — I've laid out empty templates for every step ahead of you and a blank CBL Canvas so you can see the shape of the whole project before you've decided anything. Next step is figuring out your Big Idea — want to jump into that now, or invite your teammates first?"

## Notes & Edge Cases

- **Idempotency is the core design property here.** The skill must correctly distinguish "no project exists" from "project exists, this person isn't in it" from "project exists, this person is already in it" (in the last case, it should just report status, not re-register or duplicate anything).
- If a git remote hasn't been configured yet (no URL given), the skill should still complete local setup and clearly flag that team collaboration features (`cbl-merge`) won't work correctly until a remote exists — not silently proceed as if everything's fine. No connector is needed once a remote does exist — plain git commands handle the rest.
- The constitution isn't a one-time artifact — teams may reasonably want to revisit scope or timeline mid-project; this skill stays the owner of that file throughout, not just at t=0.
- The blank canvas created here uses the exact same renderer that `cbl-canvas` calls later — this skill's first-time render and every subsequent auto-refresh (triggered by other skills writing to `.cbl/state.json`) are the same code path, not two implementations.
