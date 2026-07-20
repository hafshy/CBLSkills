# CBL Skills — Execution Plan

A dependency-ordered, milestone-based build plan for all 14 skills plus the shared infrastructure they depend on. Modeled on spec-kit's own `tasks.md` output (task IDs, file targets, `[P]` = safe to build in parallel with other `[P]` tasks in the same milestone). Companion to every other doc in `plan/` — this is the one that turns the design into a sequence of actual work.

**Methodology**: draft → test on realistic prompts → review → iterate, per `research/07-skill-authoring-notes.md`. Recommend actually invoking the `skill-creator` skill for each milestone's build-and-test work — it already has the eval-prompt and review tooling this plan assumes.

**Checkpointing**: stop and review with the user at the end of every milestone, not just at the very end. Cheapest place to catch a wrong turn is right after the smallest working piece, not after 14 skills are built on a bad assumption.

---

## Milestone 0 — Shared Infrastructure

Nothing skill-specific yet. These are the pieces multiple skills call into, per the "one implementation, many callers" principle used throughout the design (architecture plan §3a, §4a).

| ID | Task | Depends on |
|---|---|---|
| T001 | Define the `.cbl/state.json` schema precisely (fields: `status`, `decided_by`, `decided_at`, `stale`, per-artifact) and write a small read/write helper other skills call rather than hand-rolling JSON edits. | — |
| T002 [P] | Build the document template generator: given an artifact name, produces the frontmatter + placeholder-section markdown from architecture plan §3a. | — |
| T003 [P] | Build the canvas renderer: reads `.cbl/state.json` + all `challenge/*` files, produces `canvas/cbl-canvas.html` per the 9-section layout in architecture plan §4a. Must handle the "degrades gracefully" case (`not_started` sections render as "not yet reached") from day one, not as a later patch. | — |
| T004 | Build the shared gating-check routine: given an artifact's prerequisites, returns decided/not-started/stale, and the "auto-offer to run the missing prerequisite" prompt text. | T001 |

**Definition of done**: T001–T004 exist as callable pieces (scripts or shared reference text, per the `scripts/`/`references/` pattern in `research/07-skill-authoring-notes.md`), each independently testable without a full `SKILL.md` around them yet — e.g., you can hand the renderer a fake `state.json` and get sane HTML back.

---

## Milestone 1 — Vertical Slice

The proof that the whole system works end to end, scoped exactly as agreed: `cbl-init` and `cbl-big-idea`, local-git only, no GitHub connector.

| ID | Task | Depends on |
|---|---|---|
| T005 | Write `cbl-init/SKILL.md` — first-time path only (scaffold `.cbl/`, `challenge/*` templates via T002, blank canvas via T003, local `git init` + first commit). | T001–T003 |
| T006 | Add join-mode to `cbl-init` (detect existing project, register a new teammate, create their branch + folder, no re-scaffolding). | T005 |
| T007 | Write `cbl-canvas/SKILL.md` — thin wrapper around T003's renderer, both for manual "show me the canvas" requests and as the thing other skills call silently on every state change. | T003 |
| T008 | Write `cbl-status/SKILL.md` — read-only snapshot using T001's helper. Useful now mainly to make the rest of this milestone's testing easier to verify by hand. | T001 |
| T009 | Write `cbl-big-idea/SKILL.md` — full generate/add/decide implementation, per `plan/skills/cbl-big-idea.md`. This is the reference implementation every other G/D skill copies the pattern from, so it's worth getting genuinely right here rather than fixing the pattern five times later. | T001, T004, T007 |
| T010 | Test: 4–5 realistic prompts covering first-time init, join mode, the full generate → add → decide loop, a gate hit with auto-offer accepted, and confirming the canvas silently updated without being asked. | T005–T009 |
| T011 | Review results, iterate on `cbl-init`/`cbl-big-idea` based on what T010 actually surfaced — expect the canvas renderer and the gating helper to need real adjustment here; that's the point of doing this milestone first. | T010 |

**Definition of done**: a fresh folder, given only `cbl-init` and `cbl-big-idea`, produces a scaffolded project with a decided Big Idea, an auto-refreshed canvas, and correct git history — verified by actually running it, not just reading the code.

**Checkpoint with user.**

---

## Milestone 2 — Finish Engage

Both skills copy the pattern proven in Milestone 1 directly.

| ID | Task | Depends on |
|---|---|---|
| T012 [P] | Write `cbl-essential-question/SKILL.md`, per `plan/skills/cbl-essential-question.md`. | M1 pattern |
| T013 [P] | Write `cbl-challenge-statement/SKILL.md`, per `plan/skills/cbl-challenge-statement.md`. | M1 pattern |
| T014 | Test the full Engage phase end to end: Big Idea → Essential Question → Challenge Statement, then specifically test reopening the Big Idea after Challenge Statement is decided and confirming the staleness cascade (architecture plan §5) actually fires correctly. | T012, T013 |

**Definition of done**: Phase 1 complete, staleness-on-reopen verified with a real test, not just asserted in docs.

**Checkpoint with user.**

---

## Milestone 3 — Investigate

Mix of G/D (`cbl-guiding-questions`) and pure execution skills (`cbl-research`, `cbl-synthesis`) — first real test of the non-G/D pattern.

| ID | Task | Depends on |
|---|---|---|
| T015 [P] | Write `cbl-guiding-questions/SKILL.md` — note the "decide" here is prioritization/selection, not single-pick; per `plan/skills/cbl-guiding-questions.md`. | M2 |
| T016 [P] | Write `cbl-research/SKILL.md` — assignment + findings tracking, no generate/decide. | M2 |
| T017 | Write `cbl-synthesis/SKILL.md` — depends on knowing the actual shape of files T016 produces, build after T016 is working, not just speced. | T016 |
| T018 | Test Investigate end to end: generate + prioritize Guiding Questions, log 2–3 findings (including one via a simulated second team member's folder, to shake out anything `cbl-research` assumes about single-user use), run synthesis, confirm the "ready for Act?" gap-flagging behavior actually flags an intentionally-left gap. | T015–T017 |

**Definition of done**: Phase 2 complete; the gap-flagging in `cbl-synthesis` demonstrably catches an unanswered prioritized question rather than silently proceeding.

**Checkpoint with user.**

---

## Milestone 4 — Act

The most structurally different phase — includes the one skill (`cbl-prototype`) designed to loop backward into an earlier phase.

| ID | Task | Depends on |
|---|---|---|
| T019 [P] | Write `cbl-solution-concepts/SKILL.md`, per `plan/skills/cbl-solution-concepts.md`. | M3 |
| T020 | Write `cbl-prototype/SKILL.md`, including the "flag as new Guiding Question vs. quick fix" handoff logic back to `cbl-guiding-questions` (T015). This is the riskiest single skill in the whole set to get right — the ambiguous-classification judgment call flagged in `plan/skills/cbl-prototype.md`'s edge cases deserves real test coverage, not just a happy-path check. | T019, T015 |
| T021 [P] | Write `cbl-implement-evaluate/SKILL.md` — including the pre-launch success-metrics prompt, per `plan/skills/cbl-implement-evaluate.md`. | M3 |
| T022 | Write `cbl-reflect-share/SKILL.md` — the one skill that reads across the entire project; build and test last in this milestone since it depends on everything else actually existing to pull from. | T019–T021 |
| T023 | Test Act end to end, specifically including: (a) a prototype test result that gets classified as a new Guiding Question and actually round-trips back into Investigate correctly, and (b) confirming `cbl-reflect-share`'s auto-triggered canvas refresh shows 100% completion with no manual `cbl-canvas` call needed. | T019–T022 |

**Definition of done**: a full Engage → Investigate → Act run-through works, including at least one genuine backward loop from Act into Investigate, not just the forward path.

**Checkpoint with user.**

---

## Milestone 5 — Team Collaboration

| ID | Task | Depends on |
|---|---|---|
| T024 | Write `cbl-merge/SKILL.md`, per `plan/skills/cbl-merge.md` — plain local git, no connector. | M1 (needs `cbl-init` join mode working) |
| T025 | Test with a genuinely simulated second team member: separate folder/branch, at least one clean merge and one real conflict (two people answering the same Guiding Question differently), confirm conflicts surface in plain language, never raw git markers, and confirm a merge triggers the canvas auto-refresh. | T024, T006 |

**Definition of done**: a two-"person" merge (even if both simulated from one machine for testing purposes) works cleanly through conversation, no raw git output ever shown to the user.

**Checkpoint with user.**

---

## Milestone 6 — Full Integration Test

No new skills — this is where the whole 14-skill set gets run as a system, not as isolated pieces.

| ID | Task | Depends on |
|---|---|---|
| T026 | Fresh `cbl-init` through every phase to a completed project (mirroring the Food Waste example used throughout `plan/03-prompting-scenarios.md`), verifying the final canvas, git history, and every `challenge/*` file agree with each other. | M1–M5 |
| T027 | Regression-test reopening: redecide an early artifact (Big Idea or Challenge Statement) late in the project, confirm the full staleness cascade behaves as designed across every downstream artifact, not just the immediate next one. | T026 |
| T028 | Regression-test the canvas auto-refresh rule across every trigger point named in the architecture plan (decisions, findings, iterations, evaluation results, reflection) — confirm none of them were missed in implementation. | T026 |

**Definition of done**: the system survives a full run-through plus both regression tests without manual intervention beyond normal conversation.

**Checkpoint with user — this is the "is it actually done" gate.**

---

## Milestone 7 — Polish (optional, do only if M6 passed cleanly)

| ID | Task | Depends on |
|---|---|---|
| T029 | Run description-optimization passes (skill-creator's trigger-eval workflow) on any skill where testing surfaced mistriggering risk — most likely candidates: skills with adjacent names/descriptions across phases. | M6 |
| T030 | Package the finished skill set for distribution if you want to share or reuse it elsewhere. | M6 |

---

## Sequencing Summary

```
M0 (infra) → M1 (vertical slice: init + big-idea) → M2 (Engage) → M3 (Investigate) → M4 (Act) → M5 (collaboration) → M6 (integration) → M7 (polish, optional)
```

M2–M4 could theoretically be reordered or parallelized once M1 proves the pattern, but building them in CBL's own phase order is deliberate — each phase's test in M2–M4 exercises the staleness/gating machinery a bit further than the last, so problems surface incrementally instead of all at once in M6.

## What This Plan Does Not Cover

Actual UI/visual design of the canvas HTML (colors, fonts, exact CSS) isn't specified here — that's a T003 implementation detail worth a quick separate look-and-feel pass, possibly using the `canvas-design` or `brand-guidelines` skills if you want it to look polished rather than functional-but-plain. Not blocking, but worth flagging before M1 if visual quality matters to you early.
