# CBL Skills — Detailed Reference

One dedicated file per skill: what it does, exactly when it fires, what's required before it'll run, every sub-action a user can trigger inside it, what files it reads and writes, a worked example, and edge cases to watch for.

Companion to `../01-cbl-skills-architecture-plan.md` (the system-level design), `../02-skill-flow-diagrams.md` (visual flow), and `../03-prompting-scenarios.md` (end-to-end conversations). Where those docs describe the system, these describe each individual piece of it — this is the closest thing to a spec for what gets built into each `SKILL.md`.

## Infra (cross-cutting)

| Skill | One-line summary |
|---|---|
| [cbl-init](cbl-init.md) | Set up a new project (or join an existing one): folders, git, constitution, blank document templates, blank canvas. |
| [cbl-status](cbl-status.md) | Read-only snapshot of where the project stands — what's decided, what's stale, what's next. |
| [cbl-merge](cbl-merge.md) | Review a teammate's contribution and merge it into the canonical `challenge/` documents. |
| [cbl-canvas](cbl-canvas.md) | Render/refresh the single-page HTML CBL Canvas from whatever's been decided so far. |

## Phase 1 — Engage

| Skill | One-line summary |
|---|---|
| [cbl-big-idea](cbl-big-idea.md) | Generate, add, and decide on the project's Big Idea. |
| [cbl-essential-question](cbl-essential-question.md) | Generate, add, and decide on the Essential Question that turns the Big Idea personal. |
| [cbl-challenge-statement](cbl-challenge-statement.md) | Turn the decided Essential Question into an actionable Challenge Statement. |

## Phase 2 — Investigate

| Skill | One-line summary |
|---|---|
| [cbl-guiding-questions](cbl-guiding-questions.md) | Generate, add, and prioritize the Guiding Questions the team will research. |
| [cbl-research](cbl-research.md) | Assign Guiding Questions to researchers and track findings. |
| [cbl-synthesis](cbl-synthesis.md) | Synthesize research findings into conclusions the team can build a solution on. |

## Phase 3 — Act

| Skill | One-line summary |
|---|---|
| [cbl-solution-concepts](cbl-solution-concepts.md) | Generate, add, and decide on a Solution Concept to build. |
| [cbl-prototype](cbl-prototype.md) | Plan a build approach and run the build-test-iterate loop. |
| [cbl-implement-evaluate](cbl-implement-evaluate.md) | Ship the solution to a real audience and measure outcomes. |
| [cbl-reflect-share](cbl-reflect-share.md) | Produce the closing reflection and shareable case study. |

## How to Read These Docs

Each file follows the same shape:

- **Purpose** — what it's for, in one or two sentences.
- **When it triggers** — example phrases a user would actually type.
- **Prerequisites (gate)** — what has to be decided first, and what happens if it isn't (per the auto-offer rule in the architecture plan §2.1).
- **What users can do** — every sub-action available once the skill is active, phrased as "user says X → skill does Y."
- **Reads / writes** — exact files touched, tying back to the project structure in the architecture plan §3.
- **Example interaction** — a short, realistic exchange.
- **Notes & edge cases** — anything non-obvious: what happens on conflicting input, what "done" looks like, how it interacts with other skills.
