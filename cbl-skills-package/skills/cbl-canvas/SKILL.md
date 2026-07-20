---
name: cbl-canvas
description: Shows or manually refreshes the CBL Canvas — a single-page HTML visual summary of a Challenge Based Learning project, from Big Idea through Reflection. Use when someone asks to "show me our CBL canvas", "update the canvas", "generate a visual summary of our project", or wants something to put on a screen or printout for a presentation. Note that the canvas already auto-refreshes on its own every time another CBL skill finalizes a decision — most of the time this skill is just for viewing an already-current file, not generating something new.
---

# CBL Canvas

Renders `canvas/cbl-canvas.html` — a single self-contained HTML file, no server needed, viewable by opening it directly in a browser.

**Important context before using this skill**: every other CBL skill that changes `.cbl/state.json` (via `cbl_core.cli set-status`) automatically re-renders the canvas as its last step. That means by the time a user asks to see it, it's almost always already current. This skill exists for two real cases: (1) the user wants to *view* it (nothing to regenerate, just point them at the file and describe what's in it), or (2) they want a manual re-render for some reason (e.g., checking after a doc was hand-edited outside the normal skill flow).

## Step 1: Refresh (usually redundant, but cheap and harmless)

```bash
python3 -m cbl_core.cli render-canvas "<project_root>"
```

- **`{"ok": false, "error": "not_initialized", ...}`** — no project exists yet. Offer to run `cbl-init`.
- **`{"ok": true, "canvas_path": "..."}`** — continue to Step 2.

## Step 2: Describe what's in it

Don't just say "done" — briefly tell the user what the canvas currently shows, pulled from `cbl_core.cli status` if useful context is needed (which phases are complete/in-progress/not-started). Point them at the file path so they know where to open it.

If the project is very early (only Big Idea decided, say), say so plainly rather than implying there's more content than there is — the canvas is designed to degrade gracefully and be honest about incomplete sections ("Not yet reached"), and the response describing it should match that honesty.

## Notes & Edge Cases

- This skill never writes to `challenge/*` or `.cbl/state.json` — it only reads them and rewrites `canvas/cbl-canvas.html`. If a user wants to change what's *in* the canvas, that means changing a decision, which is a different skill's job (e.g., `cbl-big-idea` to redecide the Big Idea).
- Because the canvas is rewritten wholesale on every render, don't treat it as having meaningful edit history — the real history lives in the markdown files under `challenge/` and in git.
- If a user wants a print-friendly or slide-sized variant and one doesn't exist yet, that's a reasonable ad hoc request to fulfill by generating an alternate layout — but keep the underlying content identical to what `canvas/cbl-canvas.html` shows, don't invent new content for it.
