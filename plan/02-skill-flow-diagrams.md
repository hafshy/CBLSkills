# CBL Skill Flow — Diagrams

Companion to `01-cbl-skills-architecture-plan.md`. These are Mermaid diagrams — they render inline on GitHub, GitLab, most markdown viewers, and Mermaid Live Editor. If your viewer doesn't render Mermaid, paste the code blocks into https://mermaid.live.

---

## 1. Overall Phase Flow (CBL framework, as skills)

Shows the three CBL phases, the artifact each skill produces, and where the process is allowed to loop backward (dashed lines) versus only ever move forward (solid lines).

```mermaid
flowchart TD
    INIT[cbl-init] --> BI[cbl-big-idea]

    subgraph ENGAGE["PHASE 1 · ENGAGE"]
        BI[cbl-big-idea] --> EQ[cbl-essential-question]
        EQ --> CS[cbl-challenge-statement]
    end

    subgraph INVESTIGATE["PHASE 2 · INVESTIGATE"]
        CS --> GQ[cbl-guiding-questions]
        GQ --> RES[cbl-research]
        RES --> SYN[cbl-synthesis]
    end

    subgraph ACT["PHASE 3 · ACT"]
        SYN --> SC[cbl-solution-concepts]
        SC --> PROTO[cbl-prototype]
        PROTO --> IMPL[cbl-implement-evaluate]
        IMPL --> REFLECT[cbl-reflect-share]
    end

    PROTO -. "new questions surface\n(loop back, not blocked)" .-> GQ
    CS -. "reopen if scope was wrong" .-> BI

    CANVAS[cbl-canvas]
    BI -. "auto-refresh\non decide" .-> CANVAS
    EQ -. "auto-refresh\non decide" .-> CANVAS
    CS -. "auto-refresh\non decide" .-> CANVAS
    GQ -. "auto-refresh\non each finding" .-> CANVAS
    SYN -. "auto-refresh\non decide" .-> CANVAS
    SC -. "auto-refresh\non decide" .-> CANVAS
    PROTO -. "auto-refresh\non each iteration" .-> CANVAS
    IMPL -. "auto-refresh\non results recorded" .-> CANVAS
    REFLECT -. "auto-refresh\non completion" .-> CANVAS

    style CANVAS fill:#f5e6ff,stroke:#8a4fd1
    style ENGAGE fill:#eaf4ff,stroke:#4a90d9
    style INVESTIGATE fill:#eafff0,stroke:#3fa876
    style ACT fill:#fff4e6,stroke:#d98a3f
```

**Reading this**: solid arrows are the normal forward path each skill gates on. The two backward-loop dashed arrows (Act → Investigate, Challenge Statement → Big Idea) are expected and supported, not errors — see §5 of the architecture plan for how staleness flags this without blocking anyone. The dashed arrows into `cbl-canvas` are a different kind of "anytime" — every one of them fires automatically the moment its source skill writes a state change, with no user request needed (architecture plan §2, principle 6).

---

## 2. Skill Dependency / Gating Graph

A more literal view of what each skill checks for before it will proceed, and what "auto-offer to run the missing prerequisite" looks like as a decision tree.

```mermaid
flowchart LR
    START([User asks for a skill]) --> CHECK{Required upstream\nartifact decided?}
    CHECK -- "No, not started" --> OFFER["Explain what's missing,\noffer to run the\nprerequisite skill now"]
    OFFER -- "User says yes" --> RUNPREREQ[Run prerequisite skill]
    RUNPREREQ --> CHECK
    OFFER -- "User says no" --> STOP([Stop, wait for user])

    CHECK -- "Yes, decided" --> STALE{Any upstream\ndependency stale?}
    STALE -- "Yes" --> WARN["Warn, but don't block:\n'X changed after Y was written —\nwant to review Y first?'"]
    WARN -- "Proceed anyway" --> RUN[Run this skill]
    WARN -- "Go fix upstream first" --> REDO[Re-trigger the stale skill]

    STALE -- "No" --> RUN
    RUN --> WRITE[Write artifact + update state.json]
    WRITE --> PROPAGATE["Mark any existing\ndownstream artifacts stale"]
```

---

## 3. Generate → Add → Decide Sub-Flow (inside one skill)

This is the internal conversational logic described in §6 of the architecture plan — how a single skill like `cbl-big-idea` handles generating, accepting user ideas, and deciding, all as one continuous conversation.

```mermaid
stateDiagram-v2
    [*] --> NoOptions: skill first triggered,\nartifact file empty

    NoOptions --> OptionsListed: "let's figure out X"\n→ generate 3-5 options

    OptionsListed --> OptionsListed: "give me more options"\n→ generate again (append)
    OptionsListed --> OptionsListed: "add my own idea: ___"\n→ append user's option

    OptionsListed --> Comparing: "let's decide" /\n"what do you recommend?"
    NoOptions --> Comparing: "our answer is ___,\nlock it in" (skip straight to decide)

    Comparing --> AwaitingConfirm: show comparison table\n+ one recommendation

    AwaitingConfirm --> OptionsListed: user rejects,\nwants different options
    AwaitingConfirm --> Decided: user confirms\n(or explicitly overrides)

    Decided --> [*]: write final artifact,\nupdate state.json,\nmark downstream stale,\nsilently refresh CBL Canvas
```

---

## 4. Team Collaboration & Git Flow

How a distributed team's work moves from an individual's scratch folder into the canonical `challenge/` documents.

```mermaid
sequenceDiagram
    participant M as Teammate (own machine)
    participant F as team/&lt;name&gt;/ (scratch)
    participant B as git branch (team/&lt;name&gt;)
    participant C as challenge/ (canonical, main)
    participant Merge as cbl-merge

    M->>F: Draft ideas, notes,\nresearch-in-progress
    Note over F: Low-friction, no review needed,\ngit-tracked for history only

    M->>B: Push anything meant\nfor team review
    M->>Merge: "help me merge my\nGuiding Questions research"

    Merge->>B: Read teammate's branch
    Merge->>C: Diff against canonical doc
    Merge-->>M: Show conflicts in plain language\n(not raw git markers)
    M->>Merge: Resolve / confirm
    Merge->>C: Commit merged result to main
    Merge->>C: Update .cbl/state.json
```

---

## 5. CBL Canvas Data Flow — From Init to Full Story

How the canvas first appears (empty, at init) and then gets re-rendered as real content gets decided. Both `cbl-init` and `cbl-canvas` call the same underlying renderer — one rendering path, two entry points (see architecture plan §3a).

```mermaid
flowchart TD
    subgraph DAY0["Day 0 — cbl-init"]
        EMPTYCHAL["challenge/*.md\ncreated as templates\n(frontmatter: status=not_started)"] --> RENDERER
        RENDERER["Shared canvas renderer\n(one implementation,\ncalled by both skills)"] --> EMPTYHTML["canvas/cbl-canvas.html\nall 9 sections = 'not yet reached'\nprogress footer = 0%"]
    end

    subgraph LATER["Any time later — auto-triggered on any state.json write, or manual request"]
        STATE[".cbl/state.json"] --> CANVASGEN[cbl-canvas]
        BI2["challenge/01-big-idea.md"] --> CANVASGEN
        EQ2["challenge/02-essential-question.md"] --> CANVASGEN
        CS2["challenge/03-challenge-statement.md"] --> CANVASGEN
        GQ2["challenge/04-guiding-questions.md"] --> CANVASGEN
        SYN2["challenge/06-synthesis.md"] --> CANVASGEN
        SC2["challenge/07-solution-concepts.md"] --> CANVASGEN
        PROTO2["challenge/08-prototype-plan.md +\n09-prototype-log/"] --> CANVASGEN
        IMPL2["challenge/10-implementation-evaluation.md"] --> CANVASGEN
        REFL2["challenge/11-reflection-and-share.md"] --> CANVASGEN
        CANVASGEN --> RENDERER2["Shared canvas renderer\n(same one as init)"]
        RENDERER2 --> HTML["canvas/cbl-canvas.html\nrewritten in place,\nnot appended"]
        HTML --> RENDER1["Sections with a decision:\nfully rendered"]
        HTML --> RENDER2["Sections still not_started:\nshown as 'not yet reached'"]
        HTML --> PROGRESS["Footer progress bar:\ndriven directly by state.json"]
    end

    EMPTYHTML -. "same file, re-rendered\nas the project progresses" .-> CANVASGEN
```

---

## Notes on Using These Diagrams

- Diagram 1 is the one to show a new team member on day one — it's the whole system at a glance.
- Diagram 2 is what the skill-builder (me, later) will translate directly into each `SKILL.md`'s opening gating check.
- Diagram 3 is the one worth re-reading if a generate/decide interaction feels confusing in practice — it's the exact state machine each of the five divergent-decision skills implements.
- Diagrams 4 and 5 are scoped to features that depend on open items in the architecture plan (§7's GitHub connector question, and the canvas skill being newly added) — expect these two to get more detail once those are settled.
- Diagram 5's "any time later" subgraph is doing double duty: it fires automatically every time any other skill writes to `.cbl/state.json` (architecture plan §2, principle 6), and it's also what runs if a user manually asks to see the canvas. Same rendering path either way.
