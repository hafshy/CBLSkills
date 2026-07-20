# CBL Skills — Plan Index

1. [01-cbl-skills-architecture-plan.md](01-cbl-skills-architecture-plan.md) — the full architecture: design critique, skill inventory (14 skills including `cbl-canvas`), what `cbl-init` scaffolds on day one (empty document templates + blank canvas, §3a), gating/staleness mechanism, generate→decide mechanics, team/git collaboration model, and locked-in decisions.
2. [02-skill-flow-diagrams.md](02-skill-flow-diagrams.md) — Mermaid diagrams: overall phase flow, gating decision tree, generate/add/decide state machine, team merge sequence, and CBL Canvas data flow.
3. [03-prompting-scenarios.md](03-prompting-scenarios.md) — nine worked example conversations covering init, the full generate/add/decide loop, gate auto-offers, reopening earlier steps, prototyping looping back into research, distributed team merges, and generating the CBL Canvas.
4. [skills/](skills/00-index.md) — one dedicated file per skill (14 total): purpose, exact trigger phrases, prerequisites/gate, every sub-action a user can invoke, files read/written, a worked example, and edge cases. The closest thing to a spec for each individual `SKILL.md`.
5. [04-execution-plan.md](04-execution-plan.md) — the actual build plan: 8 milestones (M0 shared infra → M1 vertical slice → M2–M4 the three CBL phases → M5 collaboration → M6 integration test → M7 optional polish), dependency-ordered tasks with `[P]` parallel markers, a definition of done and a user checkpoint at the end of every milestone.

Grounded in `../research/`. Next step: start on Milestone 0 / Milestone 1 of `04-execution-plan.md` — shared infrastructure, then `cbl-init` and `cbl-big-idea` as the tested vertical slice.
