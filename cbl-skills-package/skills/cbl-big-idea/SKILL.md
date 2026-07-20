---
name: cbl-big-idea
description: Generates, adds, and decides on the Big Idea for a Challenge Based Learning (CBL) project — the broad, personally and communally meaningful theme (e.g. Community, Sustainability, Health) everything else in the project builds on. Use when a team wants to figure out their Big Idea, brainstorm themes for a CBL challenge, says things like "let's figure out our big idea", "what should our theme be", "add my own big idea option", or wants to decide on/lock in a Big Idea. This is the first content skill after cbl-init — trigger it early in a new CBL project, before Essential Question or Challenge Statement work.
---

# CBL Big Idea

The reference implementation for every "decide" skill in this set (`cbl-essential-question`, `cbl-challenge-statement`, `cbl-guiding-questions`, `cbl-solution-concepts` all follow this exact shape). Get this one right; the others copy it.

This skill isn't "run once and done" — once triggered, keep responding to whatever the user asks next about their Big Idea in the same conversation. There are three sub-behaviors: **generate**, **add**, and **decide**. Which one applies is determined by what the user actually says, not by a fixed sequence.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" big_idea
```

Big Idea has no prerequisite (it's the first artifact), so this should always return `{"ok": true}` as long as the project is initialized. If it returns `not_initialized`, offer to run `cbl-init` first.

## Reading current state

Before deciding which sub-behavior applies, read `challenge/01-big-idea.md` directly (it's a plain markdown file with frontmatter) to see whether options already exist and whether one's already decided. Also worth checking `status` via:

```bash
python3 -m cbl_core.cli status "<project_root>"
```

look at `artifacts.big_idea.status` — one of `not_started`, `options_generated`, or `decided`.

## Sub-behavior: Generate

**Triggers**: "let's figure out our Big Idea", "start the Big Idea step", "give me more options", "I don't love these, try again" (status is `not_started` or `options_generated`, and the user wants ideas, not a decision).

Produce 3-5 distinct options. For each: a one-line summary, why it fits the team/context (ask about their interests, community, or class subject if you don't already know), and one honest risk or limitation — don't oversell every option as perfect. A Big Idea should be broad (Community, Sustainability, Health, Creativity, Digital Wellbeing, etc.), not already narrowed down to something Challenge-Statement-specific.

Write these into `challenge/01-big-idea.md`'s `## Options` section (edit the file directly — replace `_(none yet)_` the first time, or append below existing options on a later call, never delete prior options unless the user explicitly asks to drop one).

Then update status:

```bash
python3 -m cbl_core.cli set-status "<project_root>" big_idea --status options_generated
```

End by asking: more options, add your own, or ready to decide?

## Sub-behavior: Add

**Trigger**: "add my own idea: [X]" or similar.

Append the user's idea to the same `## Options` section, in the same format as generated ones (one-line summary if they didn't give one, ask what draws them to it, no risk note needed unless you genuinely see one worth naming) — treat it as a first-class option, not a footnote. This is what makes it a true "add," not just accepting their answer as the final decision. Update status to `options_generated` if it wasn't already (via the same `set-status` command above), since options now exist.

## Sub-behavior: Decide

**Triggers**: "let's decide", "what do you recommend?", "go with option 2", or a direct statement like "our Big Idea is [X], lock that in" (this last one is valid even with zero prior options — treat it as an add + immediate decide request).

1. Read the current options from `challenge/01-big-idea.md` (or, for the direct-statement case, treat the stated idea as the sole option).
2. Produce a short comparison: for each option, personal relevance, community relevance, and feasibility. A simple table is usually enough.
3. Give **one** clear recommendation with reasoning — never just a menu with no opinion.
4. Ask the user to confirm or override. **Never auto-select** — always wait for explicit confirmation before writing anything as final, even if the user's intent seems obvious.

On confirmation:

1. Edit `challenge/01-big-idea.md`'s `## Decision` section directly — replace `_(not yet decided)_` with the chosen option. **Write it as a short, plain-text name on its own first line (no markdown bold/formatting), then a blank line, then a one-paragraph rationale.** For example:
   ```
   Sustainability

   The team chose Sustainability because it connects directly to their interest in reducing
   cafeteria food waste, while staying broad enough to explore multiple angles. Decided by Alex.
   ```
   This convention matters beyond readability — the CBL Canvas pulls just that first line for its compact header display, so a Decision section that buries the actual chosen name inside a full paragraph (or wraps it in `**bold**` markdown) will render awkwardly on the canvas. Keep the first line short and plain.
2. Update state (this also silently refreshes the CBL Canvas — no separate step needed):
   ```bash
   python3 -m cbl_core.cli set-status "<project_root>" big_idea --status decided --decided-by "<user's name>"
   ```
3. Confirm to the user and point them at `cbl-essential-question` as the natural next step.

## Reopening an already-decided Big Idea

**Trigger**: "I want to revisit our Big Idea" (status is already `decided`).

Load the existing decision, offer to generate alternatives or refine. On a new decision, the `set-status ... --status decided` call above already handles staleness propagation automatically (any downstream artifact that's already started gets flagged stale) — nothing extra to do here beyond the normal decide flow. Just be explicit with the user about what's about to be marked for review downstream, since the blast radius from redeciding the Big Idea can be large.

## Notes & Edge Cases

- Never call `set-status` with a status that doesn't match what actually happened — e.g. don't mark `decided` before the user has actually confirmed, even if their message sounds confident. A typed name isn't the same as a team's actual decision.
- Big Ideas are intentionally broad. If a user's proposed option already sounds like a Challenge Statement (specific, action-oriented), gently note that and ask if they want to broaden it, rather than silently accepting or silently narrowing it yourself.
- If `gate-check` or `status` return `not_initialized`, don't try to work around it — offer to run `cbl-init` and stop until that's done.
