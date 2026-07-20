# `cbl-canvas`

## Purpose

Renders/refreshes the single-file HTML "CBL Canvas" — a one-page visual summary of the whole Challenge, from Big Idea through Reflection. First created blank by `cbl-init`; from then on it's kept current automatically — every other skill silently calls this same rendering logic whenever it writes a state change, so there's rarely a moment where a user needs to explicitly ask for a refresh. Manual triggering still exists, mainly for viewing or requesting a layout variant. See architecture plan §4a and §2 (principle 6) for the full spec.

## When It Triggers

- "Show me our CBL canvas."
- "Generate a visual summary of our project."
- "Update the canvas."
- "Can you make something we can put on a screen for presentation day?"

## Prerequisites (Gate)

Requires `cbl-init` to have run (the canvas file has to exist to be re-rendered). Degrades gracefully otherwise — it never requires any *specific* phase to be complete; it just renders whatever's there and marks the rest "not yet reached."

## What Users Can Do

| Trigger | Skill does |
|---|---|
| (automatic) any skill finalizes a decision, logs a finding, records an iteration, etc. — a write to `.cbl/state.json` | **Silent auto-refresh**: no user-facing interaction at all. The writing skill calls this skill's shared renderer as its last step; the canvas is updated in the background and nothing is said about it unless the user asks. |
| "show me our canvas" / "update the canvas" | **Manual re-render** (usually redundant, since it's already current, but harmless): reads `.cbl/state.json` and every `challenge/*` artifact, rewrites `canvas/cbl-canvas.html` in place. Sections with a decision render fully; sections still `not_started` stay marked "not yet reached." |
| "what does our canvas look like so far?" (early in the project) | Same behavior — this is not a special case, just a normal view where most sections happen to still be empty. |
| "print-friendly version" / "smaller version for a slide" | **Layout variant** (if requested): same content, adjusted for the target medium — still a single HTML file. |

## Reads / Writes

- **Reads**: `.cbl/state.json`, all `challenge/*` files (`01-big-idea.md` through `11-reflection-and-share.md`, plus `05-research-findings/` and `09-prototype-log/`).
- **Writes**: `canvas/cbl-canvas.html` (overwritten in place, not appended).

## Example Interaction

> **User (partway through Investigate):** "Can you show me a visual summary of where we're at?"
>
> **Claude:** "Here's your CBL Canvas — it's been kept current automatically the whole way through, so it already shows everything up through your Guiding Questions. Synthesis and Act are still marked 'not yet reached.' Nothing to update, just take a look."

## Notes & Edge Cases

- **Never a second source of truth.** The canvas is a rendered view of `challenge/*` — if there's ever a discrepancy, the markdown documents are authoritative, not the HTML. This skill should never accept edits written directly into the canvas.
- Shares its rendering logic with every other skill's auto-refresh call, and with `cbl-init`'s initial blank-canvas creation (architecture plan §3a) — one implementation, many callers, so layout/behavior can't drift between "the empty version," an auto-refreshed version, and a manually requested one.
- Because it's regenerated wholesale each run, git diffs on the HTML file itself aren't meaningful history — the real history lives in the markdown artifacts underneath.
- Should stay honest about incomplete sections rather than making "not yet reached" placeholders look like real content — the whole point is the canvas is trustworthy at a glance, even half-finished.
- **Performance note**: since a full-project render fires on every single state change (including granular ones like an individual research finding), the renderer should stay fast and cheap — it's rewriting a static file, not doing anything expensive, and it should stay that way as the design gets built out.
