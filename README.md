# CBL Skills

A spec-kit-style set of 14 sequenced, gated [Claude](https://claude.com) skills that walk a
student team through the full **Challenge Based Learning (CBL)** process — **Engage → Investigate
→ Act** — while actually building a real product, not just planning one on paper.

Modeled on the spec-driven, gated-command style of GitHub's [spec-kit](https://github.com/github/spec-kit)
(`/specify` → `/plan` → `/tasks` → `/implement`), extended with local-git team collaboration, a
generate → add → decide pattern for divergent decisions, and a visual HTML **CBL Canvas** that
auto-refreshes as the project progresses.

## What is Challenge Based Learning?

CBL is a framework where a team works through three phases:

- **Engage** — narrow a broad **Big Idea** down to a personal **Essential Question**, then an
  actionable **Challenge Statement**.
- **Investigate** — turn the Challenge into a set of prioritized **Guiding Questions**, research
  them, and **synthesize** findings into conclusions.
- **Act** — decide a **Solution Concept**, **prototype** it through a real build-test-iterate
  loop, **implement** it for a genuinely authentic audience, and **reflect** on the outcome.

Unlike a rigid waterfall, CBL expects backward loops — a prototype test routinely surfaces a new
Guiding Question that sends the team back into Investigate. This skill set is built to support
that explicitly (see [Staleness, not blocking](#staleness-not-blocking) below).

## What's in this repo

```
skills/       14 SKILL.md files — the skills themselves, one per CBL artifact
cbl_core/     Shared Python library every skill calls into via `python3 -m cbl_core.cli ...`
              (state tracking, gating/staleness, canvas rendering, git team helpers)
plan/         Architecture plan, flow diagrams, prompting scenarios, execution plan,
              and a dedicated spec file per skill
research/     Background research on CBL grounding the design (framework, process,
              collaboration, product-building, assessment, skill-authoring notes)
```

`cbl_core` is not optional scaffolding — every skill's Bash steps shell out to it, so the two
folders always travel together.

## Requirements

- Python 3.8+ (standard library only — no pip installs needed to run the skills)
- `git` (local only; no GitHub account, token, or connector required for the CBL skills themselves)

## Installing

1. Copy `skills/*` into wherever your Claude setup loads skills from (a project's
   `.claude/skills/` directory, a Cowork plugin's `skills/` folder, etc.).
2. Copy `cbl_core/` into the same project root the skills will run in, and make sure it's
   importable — run from that root, or put it on `PYTHONPATH`.
3. Sanity check:
   ```bash
   python3 -m pytest cbl_core/tests/
   ```
   35 tests should pass.

## Using it

Start a new project with `cbl-init` ("let's start a new CBL project"). It scaffolds `.cbl/`,
document templates under `challenge/`, a blank `canvas/cbl-canvas.html`, and a local git repo.
From there, work through the skills in CBL's own order:

```
cbl-init
  → cbl-big-idea → cbl-essential-question → cbl-challenge-statement      (Engage)
  → cbl-guiding-questions → cbl-research → cbl-synthesis                 (Investigate)
  → cbl-solution-concepts → cbl-prototype → cbl-implement-evaluate → cbl-reflect-share  (Act)
```

`cbl-status`, `cbl-canvas`, and `cbl-merge` are available at any point — a read-only project
snapshot, the visual canvas, and pulling in a teammate's work.

### Gating and staleness

Each content skill checks its own gate before doing anything, and offers to run whatever
prerequisite is missing rather than failing silently. Reopening and re-deciding an earlier
artifact (e.g. changing the Big Idea after later work exists) is fully supported — CBL is not
linear, so this isn't an edge case. Everything downstream gets flagged `stale` rather than
blocked or deleted, so the team knows what to re-check without losing prior work.

### The CBL Canvas

A single-page HTML visual summary — header through Reflection — that **auto-refreshes on every
decision**, no manual regeneration needed. `cbl-canvas` exists mainly for explicitly viewing it
(e.g. to put on a screen for a presentation), not for generating it.

### Team collaboration

Local-git only, spec-kit style: each teammate works in their own `team/<name>/` folder and git
branch, created via `cbl-init`'s join mode. `cbl-merge` reconciles contributions back into the
canonical `challenge/` docs — with plain-language conflict resolution, never raw git conflict
markers shown to the user.

## Design docs

- [`plan/01-cbl-skills-architecture-plan.md`](plan/01-cbl-skills-architecture-plan.md) — full
  design: principles, gating/staleness mechanism, generate → add → decide pattern, CBL Canvas
  layout spec, team collaboration model.
- [`plan/02-skill-flow-diagrams.md`](plan/02-skill-flow-diagrams.md) — Mermaid diagrams of phase
  flow, gating decisions, the generate/add/decide state machine, team merge sequence, and canvas
  data flow.
- [`plan/03-prompting-scenarios.md`](plan/03-prompting-scenarios.md) — nine worked example
  conversations.
- [`plan/04-execution-plan.md`](plan/04-execution-plan.md) — the milestone-by-milestone build
  plan this repo was actually built against.
- [`plan/skills/`](plan/skills/) — one spec file per skill: purpose, triggers, gate, what users
  can do, reads/writes, worked example, edge cases.

## Status

Built and tested through the full execution plan (Milestones 0–7): 35 unit tests, plus
end-to-end integration runs covering a full Engage → Investigate → Act project, the staleness
cascade on a late reopen, canvas auto-refresh at every trigger point, and a simulated two-person
merge with a real conflict. Every bug found during testing (canvas markdown leakage, frontmatter
desync, an ambiguous classification gap in `cbl-prototype`) was fixed structurally in `cbl_core`
rather than patched over in skill prose.

## License

Add a license of your choice before publishing (MIT is a reasonable default for a skill set like
this).
