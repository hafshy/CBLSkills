# CBL Skill Set — Architecture Plan

This document plans a set of sequenced, gated Claude skills that walk a student team through Challenge Based Learning (CBL) to build a real product, modeled on the spec-driven, gated-command style of GitHub's `spec-kit` (`/speckit.constitution` → `/specify` → `/plan` → `/tasks` → `/implement`), extended with git-based team collaboration, a generate → decide pattern for divergent decisions, and a visual HTML "CBL Canvas" output.

Grounded in the research in `research/01` through `research/07`. Companion documents in this same `plan/` folder: `02-skill-flow-diagrams.md` (visual diagrams of how the skills connect) and `03-prompting-scenarios.md` (worked example conversations).

---

## 1. Verdict on the Proposed Design

Your three requirements are good instincts, but as stated they'd produce a design with real friction points. Short version: **keep the spirit, change the shape.**

### What's right

- **Gated sequencing** is a genuinely good fit. CBL has a real dependency chain — you can't write a credible Challenge statement without a Big Idea, can't prioritize Guiding Questions without a Challenge, can't pick a Solution Concept without synthesized research. Spec-kit's "don't let `/plan` run before `/specify` exists" pattern maps cleanly.
- **Git-based collaboration** is the right instinct for a team producing versioned documents (challenge statements, research synthesis, prototypes) that need review and merge, not just chat output.
- **Generate → Decide as a pattern** is well-matched to CBL's divergent-then-convergent steps (Big Idea, Essential Question, Guiding Questions, Solution Concepts all genuinely benefit from "here are options + a recommendation, now choose").

### What needs to change

**1. "Apply generate/decide to every step" will over-fragment the skill set.**
Not every CBL step is a divergent decision. Guiding Question *research*, prototype *building*, and implementation/measurement are execution work — there's nothing to "generate options and decide" for a literature search or a build sprint. Forcing the pattern everywhere produces skills like `cbl-generate-research` / `cbl-decide-research`, which don't correspond to anything a team actually does. **Recommendation: apply generate/decide only to the ~5 steps that are genuinely divergent choices** (Big Idea, Essential Question, Guiding Questions prioritization, Solution Concepts, and optionally Prototype Approach). Everything else gets a single execution-style skill.

**2. Naming 20+ near-identical skills (`cbl-generate-X`, `cbl-decide-X` for every X) creates a triggering problem, not just a naming problem.**
Claude skills are invoked by matching a natural-language request against each skill's `description` — there's no slash-command dispatcher forcing an exact match the way spec-kit's CLI does. With 20+ skills whose descriptions are all variations of "generate ideas for the CBL process" / "help the team decide on X," Claude is likely to mis-trigger the wrong one, especially between adjacent phases. Spec-kit avoids this because its commands are literal, typed strings (`/speckit.plan`); Claude skills don't have that guarantee. **Recommendation: cut the total count (see §3), and give each skill a sharply distinct trigger phrase tied to its specific artifact name** (e.g., "decide on our Essential Question," not just "decide").

**3. Strict "can't continue if a step is missing" conflicts with CBL's own design.**
The research (`02-cbl-process-steps.md`) is explicit that CBL is *not* linear — prototyping in Act routinely surfaces new Guiding Questions that send the team back into Investigate. A rigid one-way gate (like spec-kit's, which assumes a mostly-linear spec → plan → tasks flow) would fight the framework it's supposed to support. **Recommendation: gate forward progress (can't skip ahead), but explicitly support and expect reopening earlier steps — with downstream artifacts marked "stale" rather than deleted, so the team knows what needs re-checking, not that they've broken something.**

**4. "Each team member has their own folder" is a reasonable low-tech convention, but it isn't how git collaboration usually works, and it doesn't by itself solve merge/review.**
A folder-per-member is fine for parallel, low-conflict work (individual research notes, independent idea drafts) but doesn't give you diffing, review, or conflict resolution on its own — that's what branches + pull requests are for. Also worth flagging plainly: **true multi-person git collaboration (different people, different machines) requires a git remote** (GitHub/GitLab/etc.). Claude's sandbox can run local git commands against your mounted folder, but it can't create accounts or push to a remote you haven't set up and authenticated. If your team is actually distributed, this plan needs a GitHub (or similar) connector; if "team" mostly means multiple people occasionally using your machine, local git is enough. **Recommendation: hybrid model — folders for raw/async individual work, git branches + a merge skill for anything that becomes a canonical team artifact.** (Detailed in §4.)

**5. Twenty-plus tiny skills is a maintenance and cognitive-load cost, for you and for Claude.**
Every skill is a file to keep in sync, test, and re-trigger correctly. The skill-creator guidance (`07-skill-authoring-notes.md`) explicitly favors fewer, well-scoped skills with internal structure over many micro-skills. **Recommendation: target roughly 14–16 skills total, organized under phase namespaces, not 20+.**

Net: the concept is sound, but I'd trim scope of the generate/decide pattern, add explicit staleness/reopening support instead of hard one-way gating, and be precise about what git collaboration can and can't do inside this environment.

> **Decisions locked in (see §8 for the full record):** team is genuinely distributed across machines → real git remote required; skill count consolidated to one skill per artifact/step rather than separate generate/decide skills (details below in §4 and the new §6); missing-prerequisite skills auto-offer to run the prerequisite; Act-phase skills stay medium-agnostic.

---

## 2. Revised Principles

1. **Gate forward, allow backward.** A skill checks that its required upstream artifacts exist before running. It never blocks *re-running* an earlier skill — it just flags downstream artifacts as stale when that happens. If a prerequisite is simply missing (not yet attempted), the skill offers to run it automatically rather than just stopping.
2. **One skill per artifact/step — generate and decide live inside the same skill, not as separate skills.** Every divergent step (Big Idea, Essential Question, Guiding Questions, Solution Concepts, Prototype Approach) is handled by a single skill that supports both "generate options" and "decide" as sub-behaviors the user triggers conversationally within that same skill. Full mechanics in §6.
3. **One canonical set of documents, git-versioned; personal folders are scratch space that feeds into it.** Individual contributions live in `team/<member>/`; anything that becomes part of the actual Challenge gets committed to the shared `challenge/` documents via a review/merge step.
4. **State lives in a file, not in Claude's memory.** A `.cbl/state.json` tracks what's been completed, by whom, when, and whether it's stale — so gating works correctly across separate conversations/sessions, separate machines, and separate team members (essential now that the team is confirmed distributed — see §7).
5. **Every "decide" action produces a recommendation + rationale, not just a menu.** This was explicit in your ask — deciding means analyzing the generated options (feasibility, alignment with the Challenge/Big Idea, effort, risk) and recommending one, while still letting the human choose or override.
6. **The canvas auto-refreshes on every state change, silently.** Any skill that writes a status update to `.cbl/state.json` — a decision confirmed, a research finding logged, a prototype iteration recorded, evaluation results captured, reflection written — also calls the shared canvas renderer afterward. The canvas is never something a team has to remember to update; it just stays current. Manually asking for it (`cbl-canvas`) still works, for viewing or requesting a print/slide variant — it just isn't the only way it gets refreshed anymore. Full mechanics in §4a.

---

## 3. Project & Repo Structure

```
project-root/
├── .cbl/
│   ├── constitution.md        # team norms, scope constraints, roles — set once at init
│   ├── state.json             # gating + staleness tracker (see §5)
│   └── team.json              # registered team members + their folder/branch
│
├── challenge/                 # canonical, git-tracked CBL documents (one per artifact)
│   ├── 01-big-idea.md
│   ├── 02-essential-question.md
│   ├── 03-challenge-statement.md
│   ├── 04-guiding-questions.md
│   ├── 05-research-findings/          # one file per guiding question, or per researcher
│   ├── 06-synthesis.md
│   ├── 07-solution-concepts.md
│   ├── 08-prototype-plan.md
│   ├── 09-prototype-log/              # iteration history, test notes
│   ├── 10-implementation-evaluation.md
│   └── 11-reflection-and-share.md
│
├── canvas/
│   └── cbl-canvas.html         # single-file visual summary of the whole Challenge, regenerated on demand (see §4a)
│
├── team/
│   └── <member-name>/         # personal scratch space: draft ideas, notes, research-in-progress
│
└── .git/
```

This mirrors spec-kit's `memory/constitution.md` + numbered feature docs pattern, adapted to CBL's own phase names instead of spec/plan/tasks.

Everything under `challenge/` and `canvas/` shown above is **created by `cbl-init` on day one**, not built up file-by-file as each phase skill first runs — see §3a.

---

## 3a. What `cbl-init` Scaffolds (new, per your feedback)

Previously the plan had `cbl-init` create empty folders and let each artifact file get written the first time its skill ran. That's a real gap: a team that's just initialized has nothing to look at, no sense of the whole shape of the project, and no visible distinction between "this step doesn't exist yet" and "this step exists but wasn't decided." **`cbl-init` should scaffold every `challenge/*` document and the canvas up front, all empty/templated, not just the folder structure.**

### Document templates

Every file in `challenge/` is created at init time with a small YAML frontmatter block plus placeholder sections, so opening any file — even before its skill has ever run — tells you exactly what belongs there and what state it's in:

```markdown
---
artifact: essential_question
status: not_started
decided_by: null
decided_at: null
stale: false
---

# Essential Question

_This document will hold the Essential Question options your team generates,
and the one you decide on. Run the Essential Question step once your Big Idea
is decided to get started._

## Options
_(none yet)_

## Decision
_(not yet decided)_
```

`status` moves through a small fixed vocabulary as a skill works on it: `not_started` → `options_generated` (once at least one option exists) → `decided` (once confirmed). This is what lets §6's "generate" and "decide" sub-behaviors know which state they're picking up from without needing separate signals from state.json.

**Decision-writing convention (added after Milestone 1 testing surfaced this as a real bug):** when a skill writes a final decision into a `## Decision` section, the first line must be a short, plain-text statement of the decided value — no markdown bold/formatting — followed by a blank line, then the rationale paragraph. The CBL Canvas (§4a) extracts just that first line for compact display (header, section titles); a Decision section that buries the actual chosen value inside a full paragraph, or wraps it in `**bold**`, renders badly on the canvas. Every `cbl-*` skill that writes a Decision section should follow this same shape.

This does two things beyond just "having a template":

1. **It makes `.cbl/state.json` and the document itself agree by construction.** The frontmatter mirrors the same fields state.json tracks (`status`, `decided_by`, `decided_at`, `stale`). state.json stays the fast lookup index for gating checks, but if anyone opens the raw file, it's self-describing — no separate system of record silently diverging from what the file says.
2. **It gives every skill one consistent write target.** `cbl-big-idea` doesn't create `challenge/01-big-idea.md` — it already exists, and the skill fills in the `Options` and `Decision` sections and updates the frontmatter. This removes an entire category of bug (a skill needing to handle both "file exists" and "file doesn't exist yet" as separate code paths).

### The empty CBL Canvas

At init, `canvas/cbl-canvas.html` is also created immediately — fully styled, all nine sections from §4a present, every one of them showing a "not yet reached" placeholder state, and the progress footer at 0%. A team can open it in a browser the moment they finish `cbl-init`, before they've decided anything, and see the shape of the whole journey they're about to go on.

**Implementation note:** `cbl-init` should not reimplement canvas rendering separately from `cbl-canvas` — both should call the same underlying rendering logic (a shared bundled script/template, per the skill-authoring guidance in `research/07-skill-authoring-notes.md` on putting deterministic/repetitive logic in `scripts/` rather than duplicating it across skills). `cbl-init` effectively just calls that shared renderer against an all-empty `challenge/` to produce the first version; `cbl-canvas` calls the exact same renderer later against whatever's actually been decided. One rendering path, two entry points.

### Registering additional (later-joining) team members

This also closes a real gap the previous draft left dangling: §7 referenced a `cbl-team-join` skill that didn't actually exist in the skill inventory in §4 — an inconsistency from an earlier consolidation pass that got missed. Fixed here: **`cbl-init` is idempotent.** The first person to run it initializes everything above. Anyone who runs it afterward against a project that already has a `.cbl/` folder is detected as a new team member joining an existing project — it skips re-scaffolding and just registers them (creates their `team/<name>/` folder and git branch) against the existing structure. One skill, two situations, no separate `cbl-team-join` skill needed. §7 below is corrected to match.

---

## 4. Skill Inventory (consolidated: 14 skills)

Per your call, this drops the separate generate/decide skills entirely. Every divergent step is **one skill** that internally supports generating, adding your own idea, and deciding — see §6 for exactly how that works conversationally. Grouped by phase, `cbl-` prefix throughout.

### Infra (cross-cutting)

| Skill | Purpose | Gate |
|---|---|---|
| `cbl-init` | Set up `.cbl/`, git repo + remote, constitution; scaffold every `challenge/*` document as an empty template plus a blank `canvas/cbl-canvas.html` (see §3a); register the first team member. Idempotent — run again by a new teammate, it just registers them against the existing project instead of re-scaffolding. | None — entry point. |
| `cbl-status` | Show current phase, completed/stale artifacts, who owns what, what's unlocked next. | None — read-only. |
| `cbl-merge` | Review a member's draft/branch and merge it into the canonical `challenge/` doc (diff-aware, flags conflicts in plain language). | Requires a draft to exist. |
| `cbl-canvas` | Generate/refresh a single-file HTML "CBL Canvas" — a visual one-pager of the whole Challenge, pulling from whatever `challenge/*` artifacts exist so far. Runs automatically as a side effect whenever any other skill updates `.cbl/state.json`; can also be triggered manually at any point (e.g., to view it, or request a print/slide variant). See §4a. | `cbl-init` done; degrades gracefully if later artifacts don't exist yet. |

### Phase 1: Engage

| Skill | Handles | Gate |
|---|---|---|
| `cbl-big-idea` | Generate Big Idea options, accept user-submitted ideas, decide/confirm one. | `cbl-init` done |
| `cbl-essential-question` | Generate Essential Questions from the decided Big Idea, accept custom ones, decide/confirm one. | Big Idea decided |
| `cbl-challenge-statement` | Turn the decided Essential Question into candidate Challenge phrasings, accept a custom phrasing, decide/confirm one. | Essential Question decided |

### Phase 2: Investigate

| Skill | Handles | Gate |
|---|---|---|
| `cbl-guiding-questions` | Generate Guiding Questions, accept user-submitted ones, decide/prioritize which to pursue. | Challenge Statement decided |
| `cbl-research` | Assign questions to team members, track findings per question in `challenge/05-research-findings/`. | Guiding Questions decided |
| `cbl-synthesis` | Synthesize findings into conclusions, flag remaining gaps. | At least one research finding recorded |

### Phase 3: Act

| Skill | Handles | Gate |
|---|---|---|
| `cbl-solution-concepts` | Generate Solution Concept options, accept user-submitted concepts, decide/confirm one. | Synthesis exists |
| `cbl-prototype` | Propose build approaches, decide/confirm a plan, then run the build-test-iterate loop; can flag "this raised new questions" and point back to Investigate. | Solution Concept decided |
| `cbl-implement-evaluate` | Ship to a real audience, record outcome metrics against the goals set in the constitution. | A tested prototype exists |
| `cbl-reflect-share` | Closing reflection + shareable case study/report, pulled from documentation across all phases. | Implementation/evaluation recorded |

**Total: 4 infra + 3 Engage + 3 Investigate + 4 Act = 14.** This is the version I'd actually build. It keeps one skill per real decision point (so trigger phrases stay unambiguous — "let's work on our Essential Question" only matches one skill) while eliminating the generate/decide duplication.

---

## 4a. The CBL Canvas

Your new requirement: a skill that produces a visual HTML artifact of the challenge data, not just markdown documents. This is worth its own section since it's a different kind of output than everything else in the plan.

### What it is

A single self-contained HTML file — think "one-page poster," in the spirit of a Business Model Canvas or Lean Canvas, but laid out around CBL's own structure instead of a generic business template. It's meant to be something a team can screenshot, print, or pull up on a projector to tell the whole story of their Challenge at a glance.

### Layout (grid sections, roughly in reading order)

1. **Header band** — Big Idea + Essential Question + team name/logo placeholder.
2. **Challenge Statement** — the hero element, largest/most prominent text on the page.
3. **Guiding Questions** — compact list/cluster, each tagged with status (answered / in progress / open).
4. **Research Synthesis** — key findings/conclusions, condensed to a few bullets, not the full report.
5. **Solution Concept** — the chosen concept, with the runner-up options shown smaller/greyed out for narrative context ("we also considered...").
6. **Prototype & Iteration** — a simple timeline/stepper showing iteration count and current state.
7. **Implementation & Evaluation** — outcome metrics vs. the goals set at the start, shown as simple stat callouts.
8. **Reflection & Impact** — a short pull-quote-style summary once `cbl-reflect-share` has run.
9. **Progress footer** — a phase-progress bar (Engage → Investigate → Act) driven directly by `.cbl/state.json`, so the canvas always visually shows where the project actually stands.

### Key design decisions

- **Single HTML file, no build step.** Inline CSS, no external dependencies beyond what's safe to pull from a CDN (matches the constraint used elsewhere for portable HTML artifacts) — this keeps it viewable by just double-clicking the file, opening in any browser, no server needed.
- **Regenerate-in-place, not append-only.** Every render rewrites `canvas/cbl-canvas.html` from the current state of `challenge/*` — it's a live reflection of the project, not a snapshot you have to remember to update by hand. The file first appears the moment `cbl-init` runs (empty/templated, per §3a) — every subsequent render (automatic or manual) uses the exact same shared renderer.
- **Auto-refreshes on every state change, not just on request.** Per the locked-in decision in §8, any skill that writes a status update to `.cbl/state.json` — a decision confirmed, a research finding logged, a prototype iteration recorded, evaluation results captured, reflection written — also silently calls the shared renderer afterward. This is a deliberately simple, uniform rule (any state.json write → refresh) rather than trying to special-case which updates are "canvas-relevant" — the render is cheap (rewriting a static file), so the simplicity is worth more than the marginal savings from being selective. A user can still explicitly ask to see it or request a variant; they just never *have* to, to keep it current.
- **Degrades gracefully.** If only the Big Idea and Essential Question are decided so far, the canvas renders just those sections filled in and the rest visibly marked "not yet reached" — useful early, not just at the end. This also makes it a nice sanity-check tool during the process ("run the canvas skill and see how the story reads so far"), not just a final deliverable.
- **Git-tracked like everything else.** Since it's regenerated from `challenge/*`, diffs on the HTML file itself aren't very meaningful — the real history lives in the markdown artifacts underneath it. Treat the canvas as a rendered view, not a second source of truth.
- **Trigger phrasing**: "show me our CBL canvas," "generate a visual summary," "make the canvas," "update the canvas" — should all reliably hit this skill given how distinct "canvas" is as a term inside this skill set.

Full visual mockups and a worked example are in `02-skill-flow-diagrams.md` and `03-prompting-scenarios.md`.

---

## 5. Gating & Staleness Mechanism

Every skill (except `cbl-init` and `cbl-status`) follows the same opening check, read from `.cbl/state.json`:

```json
{
  "big_idea": { "status": "decided", "file": "challenge/01-big-idea.md", "decided_by": "hafshy", "decided_at": "2026-07-17", "stale": false },
  "essential_question": { "status": "decided", "file": "challenge/02-essential-question.md", "stale": false },
  "challenge_statement": { "status": "not_started" },
  "guiding_questions": { "status": "not_started" },
  ...
}
```

**On skill start:**
1. Check the required upstream artifact's `status` is `decided`/`complete`. If not → stop, tell the user which skill to run first (offer to just run it now if the user wants a shortcut).
2. Check `stale` is `false` on all upstream dependencies. If any are stale → warn the user before proceeding ("your Guiding Questions were written before you changed the Challenge Statement — want to review them first?") but don't hard-block; let them proceed at their own judgment.

**On skill completion:** write this artifact's status, then walk forward through the dependency graph and set `stale: true` on anything downstream that already existed. This is what makes reopening Phase 1 after Phase 3 work is underway safe: nothing is deleted, but everything downstream is flagged for review rather than silently trusted.

This directly solves the tension in Recommendation §1.3 — forward progress is still gated, but going back is a first-class, expected action instead of something the system fights.

---

## 6. Generate → Decide, Inside One Skill: How Manual Use Actually Works

This answers your direct question — yes, users can manually ask the skill to add ideas and decide, at any point, in plain conversation. Here's the mechanism.

### Why one skill can do both

A skill isn't a single fixed action — once triggered, its instructions stay loaded for the rest of that conversation, and the user keeps talking to Claude normally. So `cbl-big-idea` isn't "run once and done" — it's more like a mode Claude stays in for that artifact, responding to whatever the user asks next about it. The skill's instructions define a small set of sub-behaviors and simple rules for which one a given message maps to:

| User says something like... | Skill does |
|---|---|
| "let's figure out our Big Idea" / "start the Big Idea step" (file still `status: not_started`, from the template §3a scaffolded at init) | **Generate**: produce 3–5 options, each with a one-line summary, why it fits, and one honest risk/limitation. Fill in the `Options` section of the already-existing `challenge/01-big-idea.md`, set `status: options_generated`. End by asking: generate more, add your own, or decide now? |
| "give me more options" / "I don't love these, try again" | **Generate again**: add new options (or replace, if the user says so), keeping prior ones unless told to drop them. |
| "add my own idea: sustainable school lunches" | **Add manually**: append the user's idea to the same options list, in the same format as generated ones (so it's treated as a first-class option, not a side note) — this is the direct answer to "can users add ideas manually," and yes. |
| "let's decide" / "go with option 2" / "what do you recommend?" | **Decide**: read the existing options (never regenerates them), produce a short comparison (option / fit / effort / risk), give one clear recommendation with reasoning, and ask the user to confirm or override. Never auto-selects — a name typed in chat isn't the same as a team's actual decision, so it always asks for explicit confirmation before writing it down as final. |
| (after confirmation) | Rewrites the artifact file to show the decided option + a one-paragraph rationale, updates `.cbl/state.json`, marks downstream artifacts stale if this changes something already built on, and silently refreshes the CBL Canvas so it reflects the new decision without the user having to ask. |

The same three sub-behaviors (generate / add manually / decide) repeat identically inside `cbl-essential-question`, `cbl-challenge-statement`, `cbl-guiding-questions`, and `cbl-solution-concepts` — so once a team has done this once, the pattern is familiar for every later step.

### Triggering a specific step later, out of order

Because each skill is scoped to one artifact, a user can jump back into an earlier step in a totally new conversation just by naming it — "I want to revisit our Essential Question" re-triggers `cbl-essential-question` on its own, loads the existing options/decision from `challenge/02-essential-question.md`, and picks up the generate/add/decide flow from wherever it left off. This is what makes the "reopen an earlier step" behavior from §5 actually usable in practice, not just a data-model idea.

### What if the user just wants to decide, with no interest in seeing generated options?

Supported directly — if a user opens with "our Big Idea is community food waste, lock that in," the skill treats that as a user-submitted option plus an immediate decide request, skips straight to the comparison/recommendation step (comparing it against nothing but still sanity-checking it against the constitution/prior artifacts), and confirms before writing it down. Generation is offered, never forced.

---

## 7. Team Collaboration Model

- **`team/<member>/`** is scratch space: draft big ideas, personal research notes, early prototype experiments. Low-friction, no review needed, git-tracked for history but not gated.
- **`challenge/*`** is canonical: only written to by a decide-skill (for G/D steps) or an execution skill's own output (for single-skills), or by `cbl-merge` pulling in something from a member's folder.
- **Git usage**:
  - `cbl-init` runs `git init` on the project folder if it isn't already a repo, and commits the initial `.cbl/` + templated `challenge/` + blank `canvas/` scaffold (see §3a).
  - Running `cbl-init` again — by a teammate on their own machine, against the shared remote — is how later members join: it detects the existing project and creates a branch per member (`team/<name>`) in addition to their folder, rather than a separate join skill. Folder for freeform drafts, branch for anything they want reviewed against `main`.
  - `cbl-merge` diffs a member's branch/folder contribution against the current canonical doc, surfaces conflicts in plain language (not raw git conflict markers — most students won't want to resolve those by hand), and asks for a decision before committing to `main`.
- **Resolved: local git only, no connector needed — same approach spec-kit itself uses.** spec-kit never talks to GitHub's API; it's plain local git commands (`git checkout -b`, commits) plus a human who's already got a remote configured outside the tool. This plan follows the same pattern instead of routing through a GitHub connector:
  - Someone (you, most likely) creates the actual remote repo once, ahead of time — Claude can't create GitHub accounts or repos on its own, connector or not.
  - Each teammate clones that remote and has their own git credentials already working *before* they run `cbl-init` in join mode — this is a one-time setup step on their end, same as it would be for any git project, and isn't something Claude does for them.
  - From there, `cbl-init` (join mode) and `cbl-merge` just run plain `git branch` / `git push` / `git pull` via the shell against that already-authenticated remote — no API calls, no connector, nothing beyond what any local git workflow needs.
  - Each teammate joins once (not per session) — `cbl-init` run a second time by a new person creates their `team/<name>` branch and folder a single time; they keep working in that same branch across all their future sessions with Claude, the same way a developer keeps working on the same feature branch across many days.
  - A GitHub connector remains a possible *future* nicety (e.g., having `cbl-merge` open an actual PR instead of merging directly) but is no longer a prerequisite for anything in this plan.

---

## 8. Decisions Locked In

| Question | Decision |
|---|---|
| Team topology | **Distributed** — teammates on different machines, each with their own clone of a remote repo someone sets up once. `cbl-init`/`cbl-merge` use plain local git commands only — no GitHub connector required, matching how spec-kit itself works (see §7). |
| Skill count | **Consolidated to 14** — one skill per artifact/step, generate+add+decide handled conversationally inside each (§4, §6), no separate generate/decide skills. |
| Gating strictness | **Auto-offer to run the missing prerequisite** rather than hard-stopping. |
| Product scope | **Medium-agnostic** — Act-phase skills don't assume software; they follow CBL's own treatment of "product development" as one of several valid outcomes (campaigns, services, physical products too). |
| Canvas refresh | **Auto-refresh on every state.json write** — not just G/D decisions, but research findings, prototype iterations, evaluation results, and reflection too. Manual `cbl-canvas` requests still work, for viewing or requesting a variant. |

### Formerly open question — now resolved

Previously this section asked whether to set up a GitHub connector before building `cbl-init`/`cbl-merge`. Resolved: no connector needed. Both skills work with plain local git commands against a remote you set up once yourself (§7) — the same no-API, local-git-only approach spec-kit uses. Nothing about this blocks starting the vertical slice in §9.

---

## 9. Suggested Next Step

The next deliverable is the actual `SKILL.md` files — starting with `cbl-init` and one full artifact skill (`cbl-big-idea`, since it's first in sequence and exercises the full generate/add/decide flow from §6) as a working vertical slice, tested end-to-end, before building out the remaining 12 skills (including `cbl-canvas`). That matches the skill-creator guidance in `research/07-skill-authoring-notes.md`: draft, test on realistic prompts, iterate, *then* scale out.
