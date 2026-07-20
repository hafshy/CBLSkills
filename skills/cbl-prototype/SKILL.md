---
name: cbl-prototype
description: Plans a build approach for the decided Solution Concept and runs the build-test-iterate loop for a Challenge Based Learning (CBL) project. Use when a team wants to plan how to build their solution, says "let's plan how to build this", "we built version 1, here's what happened when we tested it", "this test revealed something we didn't know", or "let's do another iteration". Medium-agnostic — works for software, physical builds, campaigns, or services. Requires a decided Solution Concept first. The one skill in this set designed to loop backward into Investigate when testing surfaces a genuine new unknown.
---

# CBL Prototype

Two phases in one skill: **plan** (once, or re-planned if the approach changes), then **build-test-iterate** (repeated, logged each time). The riskiest judgment call in this skill is distinguishing a genuine new research question from an ordinary bug or design tweak — get this wrong in either direction and it either buries the team in unnecessary research cycles or lets a real gap in understanding slide by unexamined. Take real time on this distinction; don't default to either extreme.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" prototype
```

Blocked → offer `cbl-solution-concepts`. Otherwise proceed.

## Sub-behavior: Plan (first time, or re-planning)

**Trigger**: "let's plan how to build this" (no plan exists yet, or the user wants to change approach).

Read the decided Solution Concept. Propose 2-3 build approaches appropriate to what's actually being built — genuinely different for a physical build, a software product, or a campaign, not a generic template with nouns swapped:
- **Software/app**: different tech stacks, build-vs-no-code tradeoffs, what to build first (core loop vs. full feature set)
- **Physical product**: different materials/methods, what to prototype first (cheap mockup vs. functional version)
- **Campaign/service**: different formats, pilot scale, what "testing" even means for this medium (a survey? a small trial run?)

Recommend one, confirm with the user. Write into `challenge/08-prototype-plan.md`'s `## Notes` section: the chosen approach, first line a short plain-text summary, then detail.

```bash
python3 -m cbl_core.cli set-status "<project_root>" prototype --status in_progress
```

## Sub-behavior: Log an iteration

**Trigger**: "we built version 1, here's what we found" / "let's do another iteration".

Create `challenge/09-prototype-log/iteration-<N>.md` (increment N from whatever's already there):
```markdown
# Iteration 1

**What we built:** [brief description]
**Test:** [who/how it was tested]
**Findings:** [what worked, what didn't, feedback gathered]
**Next:** [what changes next iteration, or "moving to implementation"]
```

Once at least one iteration is logged, mark the prototype as having something real to evaluate:
```bash
python3 -m cbl_core.cli set-status "<project_root>" prototype --status complete
```
(Same idempotent pattern as `cbl-research` — "complete" here means "there's a tested prototype to build on," not "iteration is finished forever." Safe to call again after each new iteration.)

## Sub-behavior: Classify a test finding — bug, or new research question?

**Trigger**: "this raised something we didn't know" / any test finding that isn't an obvious, narrow fix. This is normally part of the same conversational turn as "Log an iteration," not a separate step — a single test round often surfaces several distinct findings at once, and each one gets classified on its own even if they're all logged into the same `iteration-<N>.md` file.

This is the judgment call this skill exists to make well. Ask yourself (and, when genuinely unclear, ask the user):
- **Quick fix**: the finding is about *how* to build something the team already understood — a UI tweak, a material substitution, a scheduling adjustment. Log it in the iteration and move on.
- **New research question**: the finding reveals the team didn't actually understand something about the *problem space* — user needs, technical feasibility, context/constraints they hadn't considered. This belongs in Guiding Questions, not buried in an iteration log.

When it's a new research question: name a candidate Guiding Question, confirm with the user whether it's worth pursuing now, and if so route to `cbl-guiding-questions` to add it (that skill's "add" sub-behavior). Keep the prototype's own status as `complete` (not blocked) while this happens — Act doesn't have to stop dead while a specific new question gets investigated; log the iteration with a note that this thread is pending further research, and reference it by name in a later iteration log once it's actually resolved (e.g. "Guiding Question 5, added after iteration 1, is now answered — see finding q5-metric-language.md").

**Two different kinds of unclear — don't collapse them into one "ambiguous" bucket:**

- **Genuinely could-go-either-way** (you have enough information, it's a real judgment call): say so to the user rather than silently picking one. "This could be a quick fix or something worth researching properly — what's your read?" is a legitimate response, not a cop-out.
- **Not enough information to classify at all** (the report is too vague to tell what actually happened) — this is a different problem, and the fix isn't asking the user to classify something under-described, it's asking a targeted follow-up to get enough detail *first*. Useful prompts: "What specifically felt confusing — was it something they couldn't figure out how to do, or something they didn't understand the point of?" or "Did the family who didn't open it say why, or is that unknown?" Log the finding as unresolved with the specific follow-up needed, don't force a classification on thin information.

## Notes & Edge Cases

- Don't auto-classify every finding as trivial by default (that silently buries real gaps) or as research-worthy by default (that turns every minor UI complaint into a full research cycle) — both failure modes are real, and the point of this skill is avoiding both, not defaulting to caution in one direction.
- Prototyping legitimately looping back into Investigate is the CBL framework working as designed, not a sign something went wrong — talk about it that way with the user, not as a setback.
- The build approach proposed in the Plan sub-behavior should visibly reflect the actual medium (software, physical, campaign) — if you notice yourself writing something that could apply to any of the three unchanged, that's a sign to be more specific.
