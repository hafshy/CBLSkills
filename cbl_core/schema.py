"""
Shared schema definitions for the CBL skill set.

Single source of truth for: the list of artifacts, their dependency chain,
what "kind" of skill produces each one (decide / prioritize / execution),
the markdown file each lives at, and which canvas section it feeds. Every
other module in cbl_core reads this instead of hard-coding artifact names.
"""

from collections import OrderedDict

# Status vocabulary.
# Decide/prioritize artifacts: not_started -> options_generated -> decided
# Execution artifacts:         not_started -> in_progress -> complete
STATUS_NOT_STARTED = "not_started"
STATUS_OPTIONS_GENERATED = "options_generated"
STATUS_DECIDED = "decided"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETE = "complete"

# Statuses that count as "satisfied" for gating purposes -- a downstream
# artifact can proceed once its prerequisite reaches one of these.
SATISFIED_STATUSES = {STATUS_DECIDED, STATUS_COMPLETE}

KIND_DECIDE = "decide"          # cbl-big-idea, cbl-essential-question, cbl-challenge-statement, cbl-solution-concepts
KIND_PRIORITIZE = "prioritize"  # cbl-guiding-questions
KIND_EXECUTION = "execution"    # cbl-research, cbl-synthesis, cbl-prototype, cbl-implement-evaluate, cbl-reflect-share

# Ordered: this order IS the dependency chain (via depends_on) unless a
# skill's own logic branches out of it (e.g. cbl-prototype handing new
# questions back to cbl-guiding-questions is handled in skill logic, not
# as a second edge here).
ARTIFACTS = OrderedDict([
    ("big_idea", {
        "title": "Big Idea",
        "file": "challenge/01-big-idea.md",
        "phase": "engage",
        "kind": KIND_DECIDE,
        "depends_on": None,
        "canvas_section": "header",
    }),
    ("essential_question", {
        "title": "Essential Question",
        "file": "challenge/02-essential-question.md",
        "phase": "engage",
        "kind": KIND_DECIDE,
        "depends_on": "big_idea",
        "canvas_section": "header",
    }),
    ("challenge_statement", {
        "title": "Challenge Statement",
        "file": "challenge/03-challenge-statement.md",
        "phase": "engage",
        "kind": KIND_DECIDE,
        "depends_on": "essential_question",
        "canvas_section": "challenge_statement",
    }),
    ("guiding_questions", {
        "title": "Guiding Questions",
        "file": "challenge/04-guiding-questions.md",
        "phase": "investigate",
        "kind": KIND_PRIORITIZE,
        "depends_on": "challenge_statement",
        "canvas_section": "guiding_questions",
    }),
    ("research", {
        "title": "Research Findings",
        "file": "challenge/05-research-findings",  # directory, not a single file
        "phase": "investigate",
        "kind": KIND_EXECUTION,
        "depends_on": "guiding_questions",
        "canvas_section": None,  # findings feed synthesis; not shown directly
    }),
    ("synthesis", {
        "title": "Research Synthesis",
        "file": "challenge/06-synthesis.md",
        "phase": "investigate",
        "kind": KIND_EXECUTION,
        "depends_on": "research",
        "canvas_section": "synthesis",
    }),
    ("solution_concepts", {
        "title": "Solution Concept",
        "file": "challenge/07-solution-concepts.md",
        "phase": "act",
        "kind": KIND_DECIDE,
        "depends_on": "synthesis",
        "canvas_section": "solution_concept",
    }),
    ("prototype", {
        "title": "Prototype & Iteration",
        "file": "challenge/08-prototype-plan.md",  # plus challenge/09-prototype-log/
        "phase": "act",
        "kind": KIND_EXECUTION,
        "depends_on": "solution_concepts",
        "canvas_section": "prototype",
    }),
    ("implementation_evaluation", {
        "title": "Implementation & Evaluation",
        "file": "challenge/10-implementation-evaluation.md",
        "phase": "act",
        "kind": KIND_EXECUTION,
        "depends_on": "prototype",
        "canvas_section": "evaluation",
    }),
    ("reflection_share", {
        "title": "Reflection & Share",
        "file": "challenge/11-reflection-and-share.md",
        "phase": "act",
        "kind": KIND_EXECUTION,
        "depends_on": "implementation_evaluation",
        "canvas_section": "reflection",
    }),
])

PHASES = OrderedDict([
    ("engage", ["big_idea", "essential_question", "challenge_statement"]),
    ("investigate", ["guiding_questions", "research", "synthesis"]),
    ("act", ["solution_concepts", "prototype", "implementation_evaluation", "reflection_share"]),
])


def dependents_of(artifact_key):
    """Direct + transitive downstream artifacts of a given artifact, in
    schema order. Used by state.update_artifact() to propagate staleness."""
    result = []
    for key, meta in ARTIFACTS.items():
        if meta["depends_on"] == artifact_key:
            result.append(key)
            result.extend(dependents_of(key))
    return result


def is_satisfied(status):
    return status in SATISFIED_STATUSES
