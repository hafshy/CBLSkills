---
name: cbl-init
description: Sets up a new Challenge Based Learning (CBL) project from scratch, or joins an existing CBL project as a new team member. This is always the first CBL skill to use — trigger it whenever a student, teacher, or team wants to start a class project using Challenge Based Learning, begin a CBL challenge, build a product using CBL, or says things like "help us set up a CBL project", "let's start a new challenge based learning project", "I need to join my team's CBL project", or references beginning any CBL-based work for the first time in a folder. Do not use this for continuing work on an already-set-up project — this only handles first-time setup and joining; use cbl-status, cbl-big-idea, or another cbl- skill for ongoing work.
---

# CBL Init

Sets up a Challenge Based Learning project (first-time), or registers a new team member on an already-set-up project (join mode). Both paths go through the same skill because the check for "does a project already exist here" is what decides which one applies — the user doesn't need to know which mode they need.

All state changes for this skill go through the bundled CLI, never by hand-editing files:

```
python3 -m cbl_core.cli init <project_root> --name <name>
python3 -m cbl_core.cli join <project_root> --name <name>
```

Run these from a location where `cbl_core` is importable (the project root this skill set ships alongside). `<project_root>` is the folder the student's actual CBL project lives in — usually their current working directory, but ask if it's ambiguous.

## Step 1: Determine the project root and ask setup questions

Before running anything, ask (briefly, not as a rigid form): what should we call this project/challenge, roughly how long is the timeline, and is there already a shared git remote (GitHub, GitLab, etc.) or does the team need to set one up. Don't block on the git remote question — a team can start locally and add a remote later.

## Step 2: Run the init command

```bash
python3 -m cbl_core.cli init "<project_root>" --name "<user's name>"
```

Read the JSON result.

- **`{"ok": true, "action": "initialized", ...}`** — first-time setup succeeded. This has already created `.cbl/state.json`, `.cbl/team.json`, every `challenge/*.md` template (empty, frontmatter + placeholders), and a blank `canvas/cbl-canvas.html` (all sections "Not yet reached", progress bar at 0%). Continue to Step 3.
- **`{"ok": false, "error": "already_initialized", ...}`** — a project already exists here. This is join mode — skip to Step 4.

## Step 3: First-time setup only — constitution, git, and confirmation

1. Write `.cbl/constitution.md` directly (plain prose, not through the CLI — this is freeform content, not schema-tracked state). Include: project/challenge name, timeline, and any scope constraints or team norms mentioned. Keep it short; this file can be edited again later by anyone, any time.
2. Initialize git and commit the scaffold, local only, no remote required yet:
   ```bash
   cd "<project_root>"
   git init
   git add .
   git commit -m "cbl-init: scaffold project"
   ```
   If the user gave a remote URL, also run `git remote add origin <url>` — but don't block setup if they didn't; just note that team collaboration features (`cbl-merge`) won't work fully until one exists.
3. Confirm to the user: project is set up, empty templates exist for every step ahead, blank canvas is ready to view at `canvas/cbl-canvas.html`. Point them at `cbl-big-idea` as the natural next step.

## Step 4: Join mode only

Run:

```bash
python3 -m cbl_core.cli join "<project_root>" --name "<user's name>"
```

- **`{"ok": true, "action": "joined", "member": {...}}`** — this is a genuinely new member. Create their branch and folder in git:
  ```bash
  cd "<project_root>"
  git checkout -b "team/<name>"
  mkdir -p "team/<name>"
  git add "team/<name>"
  git commit -m "cbl-init: register team member <name>" --allow-empty
  ```
  This assumes the user has already cloned the shared remote and has working git credentials — that's a one-time setup step on their end, not something this skill does for them. If `git checkout -b` fails because there's no repo here yet, that means they're not actually working from a clone of the team's remote — tell them plainly and ask for the remote URL or a local path to clone from first.
- **`{"ok": true, "action": "already_member", ...}`** — they're already registered (e.g., running this again by mistake, or an idempotent retry). Just report their current status via `cbl-status`, don't re-run anything.

Confirm to the user either way: they're set up on `team/<name>` branch and folder, ready to work alongside the rest of the team.

## Notes & Edge Cases

- **Idempotency is the core property here.** `cbl_core.cli init` and `cbl_core.cli join` both fail cleanly (structured JSON, exit code 1) rather than throwing errors when called in the wrong mode — always check the `ok` field and `error` field before deciding what to tell the user.
- Never hand-edit `.cbl/state.json`, `.cbl/team.json`, or `canvas/cbl-canvas.html` directly — always go through the CLI, which is what guarantees the canvas stays in sync and staleness propagation works correctly for every other skill downstream.
- The constitution (`constitution.md`) is the one file in `.cbl/` this skill writes directly rather than through the CLI, since it's freeform prose with no schema — and it isn't a one-time artifact; anyone can ask to revise it later, and this skill remains the one that owns it.
