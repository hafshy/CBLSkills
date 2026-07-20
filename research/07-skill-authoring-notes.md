# Notes on Structuring an Effective Claude Skill (from skill-creator)

Summary of how the `skill-creator` skill says a well-built Claude skill should be structured. This informs how the CBL skill itself should ultimately be authored.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description — required)
│   └── Markdown instructions (the workflow/behavior)
└── Bundled Resources (optional)
    ├── scripts/    — executable code for deterministic/repetitive tasks
    ├── references/ — docs loaded into context only as needed
    └── assets/     — files used in output (templates, icons, fonts)
```

## Progressive Disclosure (3 levels of loading)

1. **Metadata** (name + description) — always in context, ~100 words. This is the *only* thing Claude sees before deciding to trigger the skill.
2. **SKILL.md body** — loaded once the skill triggers; keep under ~500 lines.
3. **Bundled resources** — loaded on demand; effectively unlimited size, scripts can even run without being loaded into context at all.

**Implication for the CBL skill**: The three CBL phases (Engage/Investigate/Act) plus collaboration/assessment guidance could exceed a lean SKILL.md if crammed into one file. Better to put the core workflow (phase sequence, when to loop back, key prompts to ask the student) directly in SKILL.md, and push deeper reference material — e.g., the full rubric, extended role descriptions, case studies — into `references/*.md`, pointed to explicitly ("read references/roles.md if the team needs help assigning roles").

## Description Field is the Triggering Mechanism

- The `description` in frontmatter is what determines whether the skill is invoked — nothing in the body helps triggering.
- Should state both **what it does** and **when to use it**, and lean slightly "pushy" to counter Claude's tendency to under-trigger skills.
- Example framing style: not just "Guides students through Challenge Based Learning" but something like "Guides a student or team through building a real product using the Challenge Based Learning (CBL) framework — Engage, Investigate, Act. Use this whenever a student wants to build a product/app/solution as part of a class project, capstone, hackathon, or challenge, even if they don't say 'Challenge Based Learning' explicitly."

## Writing Style Guidance

- Use imperative instructions ("Ask the student to state one Essential Question" rather than passive description).
- **Explain the why**, not just rigid MUSTs — heavy ALL-CAPS/MUST-laden instructions are a "yellow flag." Since CBL itself is a pedagogical framework built on reasoning and ownership, this pairs naturally: the skill should explain *why* each CBL step matters, not just dictate steps.
- Keep the prompt lean — cut anything not pulling its weight.
- Generalize rather than overfit to one example challenge/product.
- Define output formats explicitly with templates where the deliverable is structured (e.g., a Challenge statement format, a Guiding Questions table, a completion report template).

## Domain/Variant Organization

When a skill covers multiple domains or paths, split into `references/<variant>.md` files and have SKILL.md do the routing/selection. For a CBL product-building skill, natural variants might be:
- by team experience level (novice vs. experienced, tied to the scaffolding research finding in `06-cbl-examples-case-studies.md`)
- by product type (software/app vs. physical product vs. campaign/service)
- by phase (a reference file per phase: engage.md, investigate.md, act.md, collaboration.md, assessment.md)

## Testing Philosophy (for later, once the skill is built)

- Skills with **objectively verifiable outputs** (e.g., "did it produce a Challenge statement, a Guiding Questions list, a prototype plan") benefit from test cases/assertions.
- Skills with **subjective outputs** (coaching tone, quality of facilitation) are better evaluated qualitatively via human review.
- A CBL skill is a hybrid: some outputs are checkable (did each phase produce its required artifact?) while the *quality* of facilitation is subjective — plan for a mix of both when the skill is eventually tested.

## Practical Takeaway for This Project

When it's time to build the actual skill (not now — this is still the research stage):
1. Draft SKILL.md around the three-phase CBL loop + the continuous reflect/document/share thread.
2. Bake in the collaboration roles and assessment/reflection prompts as either inline guidance or `references/` files depending on length.
3. Write a deliberately "pushy," specific description covering product-building, class projects, capstones, and hackathons so the skill reliably triggers.
4. Keep SKILL.md itself under ~500 lines; move the deeper rubric/case-study/role material into references.

## Source

- `skill-creator` SKILL.md (local skill reference, Anthropic-provided), read directly during this research session.
