# CBL Skills — Prompting Scenarios

Worked examples of how a team would actually talk to these skills, start to finish, in plain language. Companion to `01-cbl-skills-architecture-plan.md` (§6 especially) and `02-skill-flow-diagrams.md`.

These are illustrative — the real skills, once built, should be tested against prompts like these (see `research/07-skill-authoring-notes.md` on realistic test prompts).

---

## Scenario 1: Starting a brand-new project

**User:** "I'm starting a class project with my team — we want to use Challenge Based Learning to build something. Can you help us set up?"

→ Triggers `cbl-init`. Sets up `.cbl/`, initializes git, asks a few setup questions (team name, rough timeline, whether there's a git remote already or one needs setting up), writes `constitution.md`, registers the user as the first team member. It also scaffolds every `challenge/*.md` document as an empty template (frontmatter + placeholder sections, per architecture plan §3a) and renders a blank `canvas/cbl-canvas.html` — all nine sections present, marked "not yet reached," progress footer at 0%.

**Claude:** "You're set up — I've also laid out empty templates for every step ahead of you (`challenge/`) and a blank CBL Canvas (`canvas/cbl-canvas.html`) so you can see the shape of the whole project before you've decided anything. Next step is figuring out your Big Idea — want to jump into that now, or invite your teammates first?"

---

## Scenario 2: The full generate → add → decide loop (Big Idea)

**User:** "Let's figure out our Big Idea."

→ Triggers `cbl-big-idea`. No options exist yet, so it generates.

**Claude:** presents 4 options (e.g., Community, Sustainability, Digital Wellbeing, Accessibility), each with a one-line summary, why it could work, and one honest risk. Ends with: "Want more options, want to add your own, or ready to decide?"

**User:** "Add my own: food waste in our school cafeteria."

→ Skill appends this as a fifth option, same format, flags it as user-submitted.

**User:** "Give me a couple more too."

→ Skill generates 2 more, appends without dropping the earlier ones.

**User:** "Okay, what do you recommend?"

→ Triggers the decide sub-flow. Skill produces a short comparison table (option / personal relevance / community relevance / feasibility) and recommends one — say, the food waste idea — with reasoning ("it's specific, locally actionable, and ties to Sustainability without being as abstract").

**User:** "Yeah let's go with that."

→ Skill confirms, writes the decided Big Idea to `challenge/01-big-idea.md` with a one-paragraph rationale, updates `.cbl/state.json`, and silently refreshes `canvas/cbl-canvas.html` — the Big Idea section now shows "Food Waste" instead of "not yet reached," with no separate request needed.

**Claude:** "Locked in: 'Food Waste.' Ready to move to your Essential Question?"

---

## Scenario 3: Skipping straight to a decision

**User:** "Our Essential Question is 'why does our cafeteria throw away so much food every day?' — that's what we're going with."

→ Triggers `cbl-essential-question`. No generated options exist, but the skill recognizes this as a direct decide request (per the state diagram in `02-skill-flow-diagrams.md`, §3). It sanity-checks the question against the decided Big Idea, gives a short take ("this connects clearly to Food Waste and it's personally specific — good essential question"), and asks for confirmation rather than silently accepting it.

**User:** "Confirmed."

→ Written to `challenge/02-essential-question.md`, state updated.

---

## Scenario 4: Hitting a gate, and the auto-offer

**User:** "Let's start prioritizing our Guiding Questions."

→ Triggers `cbl-guiding-questions`. Checks state: the Challenge Statement hasn't been decided yet.

**Claude:** "You haven't locked in a Challenge Statement yet — Guiding Questions are built from that. Want me to run through that step now? It'll only take a couple minutes since your Essential Question is already decided."

**User:** "Yeah go ahead."

→ Runs `cbl-challenge-statement` inline (auto-offer, per the locked-in gating decision), then returns to Guiding Questions once that's decided.

---

## Scenario 5: Reopening an earlier step mid-project

**User (two weeks later, deep into prototyping):** "Actually, I think our Challenge Statement is too broad. Can we revisit it?"

→ Re-triggers `cbl-challenge-statement` directly (matched purely by naming the artifact). Loads the existing decision from `challenge/03-challenge-statement.md`, shows what's there, and offers to generate alternatives or refine it.

**User:** picks a narrower phrasing, confirms.

→ Skill rewrites the Challenge Statement, and per the staleness rule (architecture plan §5), walks forward and flags Guiding Questions, Synthesis, Solution Concepts, and the Prototype Plan as stale — without touching or deleting any of them.

**Claude:** "Updated. Heads up: your Guiding Questions, Synthesis, Solution Concept, and Prototype Plan were all written against the old Challenge Statement, so they're flagged for review — nothing's broken, just worth a look when you get to them again."

---

## Scenario 6: Prototyping loops back into research

**User:** "We built the first version of our composting tracker app and tested it with three families — turns out nobody understood the 'contamination rate' metric we used."

→ Inside `cbl-prototype`'s build-test-iterate loop. The skill records this as a test finding, and recognizes it as a new unknown, not just a bug — flags it as a candidate new Guiding Question rather than silently absorbing it.

**Claude:** "That sounds like a new Guiding Question worth investigating — something like 'what food-waste metrics do families actually understand?' Want me to add that to your Guiding Questions and loop back into research, or is this a quick fix you can just make in the next iteration?"

**User:** "Let's add it as a real guiding question, this seems important."

→ Triggers `cbl-guiding-questions` again with the new question appended (not overwriting prior ones), keeping the Act-phase prototype work marked as "in progress, pending new research" rather than blocked.

---

## Scenario 7: Distributed team merge

**Teammate B (different machine, own Claude session):** "I did the research on our second guiding question, can you help me get it merged into the team's docs?"

→ Triggers `cbl-merge`. Reads Teammate B's branch/folder contribution, diffs it against the current canonical `challenge/05-research-findings/` doc.

**Claude:** "This adds a new file, no conflicts. Here's a summary of what you found: [...]. Want me to merge this into the shared branch?"

**Teammate B:** "Yes."

→ Commits to the shared repo, updates `.cbl/state.json` to reflect the new finding, notes Teammate B as the contributor.

---

## Scenario 8: Checking the CBL Canvas mid-project

**User (partway through Investigate, before Act has started):** "Can you show me a visual summary of where we're at?"

→ Triggers `cbl-canvas`. Because every decision and research finding along the way has already been silently refreshing `canvas/cbl-canvas.html` in the background (architecture plan §2, principle 6), there's nothing new to render here — this request is purely to *view* the file, not to generate or update it. Reads the file, confirms it's current against `.cbl/state.json`.

**Claude:** "Here's your CBL Canvas (`canvas/cbl-canvas.html`) — it's been kept current automatically the whole way through, so it already shows everything up through your Guiding Questions and the two research findings you've logged so far. Synthesis and Act are still marked 'not yet reached.' Nothing to update, just open it in a browser whenever you want to look."

---

## Scenario 9: Final canvas + wrap-up

**User (after implementation and reflection are done):** "We're basically done — can you put together something we can present to the class?"

→ `cbl-reflect-share` runs, produces the closing reflection and shareable report from documentation across all phases. Writing that reflection is itself a `.cbl/state.json` update, so it automatically triggers the same silent canvas refresh every other decision does — by the time `cbl-reflect-share` finishes, the canvas already shows every section filled in and the footer at "Act: complete," with no separate `cbl-canvas` call needed.

**Claude:** "Done — you've got a written case study (`challenge/11-reflection-and-share.md`) and a one-page visual canvas (`canvas/cbl-canvas.html`, already up to date) that tells the whole story from Food Waste as your Big Idea through to your implemented composting tracker. Good for either a slide or a printout for presentation day."

---

## What These Scenarios Are Meant to Show

- Every artifact-producing skill (`cbl-big-idea` through `cbl-solution-concepts`) supports the same three moves — generate, add manually, decide — in any order the user brings them up.
- Gating never dead-ends a user; it either offers to auto-run the missing step or clearly names what to go do.
- Reopening an earlier step is treated as completely normal, with staleness as a soft nudge, not an error state.
- The canvas is designed to be useful early and often, not just as a final deliverable — Scenario 8 is deliberately mid-project, not end-of-project. It also exists from minute one (created blank at `cbl-init`, Scenario 1) and stays current on its own from then on: every other skill's decisions silently refresh it, so by the time anyone asks to see it (Scenario 8) or wraps up (Scenario 9), there's nothing left to generate — only to look at.
- Team collaboration surfaces as its own request pattern ("help me merge my ___") rather than something bolted onto every other skill.
