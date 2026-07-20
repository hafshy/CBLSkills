---
name: cbl-synthesis
description: Synthesizes research findings into clear conclusions a Challenge Based Learning (CBL) team can build a solution on — closes out the Investigate phase. Use when a team wants to synthesize their research, says "let's synthesize our research", "what have we learned overall", or "are we ready to move to Act". Requires at least one research finding to exist. Execution skill — pulls together what's already there rather than generating new options.
---

# CBL Synthesis

The judgment step that closes Investigate. The value here is genuinely identifying themes and drawing conclusions — not just concatenating findings into one file. Read like a short report, not a bulleted dump.

## Step 0: Check the gate

```bash
python3 -m cbl_core.cli gate-check "<project_root>" synthesis
```

Blocked → offer `cbl-research` (specifically: assign a question and log at least one finding). Otherwise proceed.

## Sub-behavior: Synthesize

**Trigger**: "let's synthesize our research".

1. Read every file in `challenge/05-research-findings/`.
2. Read the prioritized Guiding Questions from `challenge/04-guiding-questions.md`.
3. Identify patterns and themes across findings — not every finding needs its own paragraph; group related ones.
4. Draft clear conclusions: what does the team now know that they didn't before, and what does it suggest about a solution direction (without jumping ahead to actually pick one — that's `cbl-solution-concepts`' job).
5. Explicitly note any prioritized Guiding Question that still has **no** finding recorded — this is a gap, and it should be named plainly, not silently omitted.

Write into `challenge/06-synthesis.md`'s `## Notes` section, first line a short plain-text summary (for canvas display), then the fuller synthesis below:

```
Cafeteria waste is driven by portion sizes and unclear labeling, not lack of interest.

Across 4 of 5 prioritized questions, findings point to... [themes, conclusions]

Gap: no research yet on technical feasibility of a composting sensor (question 5).
```

```bash
python3 -m cbl_core.cli set-status "<project_root>" synthesis --status complete
```

## Sub-behavior: Readiness check

**Trigger**: "are we ready to move to Act?".

Compare findings against the prioritized list. Give an honest read: if there's a real gap (an important prioritized question with no finding), say so and let the user decide whether to research more first or proceed and treat the gap as a known risk. Don't default to reassurance — CBL treats an honest, evidence-based foundation as the point of this whole phase.

## Sub-behavior: Late addition / revise

**Trigger**: "add this finding, I forgot to log it" — route to `cbl-research` to record it properly first, then come back and re-run Synthesize to fold it in. "Revise the synthesis" — just re-run Synthesize against whatever's currently in `challenge/05-research-findings/`.

## Notes & Edge Cases

- This is the gate for `cbl-solution-concepts` — Act can't meaningfully start without at least one synthesis pass, even an intentionally imperfect one with a named gap.
- Resist writing a synthesis that's just findings copy-pasted in sequence — if two findings say related things, that's exactly the kind of pattern worth calling out explicitly as a theme, not two separate bullets.
- Gap-flagging is a feature, not a failure mode of this skill — a synthesis that honestly says "we don't know X yet" is doing its job correctly.
