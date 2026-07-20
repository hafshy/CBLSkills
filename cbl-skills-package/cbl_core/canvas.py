"""
CBL Canvas renderer. (Execution plan T003; architecture plan S4a.)

Single shared implementation. cbl-init calls this once, against an
all-not_started project, to produce the first blank version. Every
subsequent state.update_artifact() call re-invokes it automatically.
Manual "show me the canvas" requests call it too. Same code path, always --
there is no second implementation anywhere that could drift from this one.
"""

import html
import os
import re

from . import schema
from . import state as state_mod
from . import templates as templates_mod

CANVAS_REL_PATH = os.path.join("canvas", "cbl-canvas.html")

_CSS = """
body { font-family: -apple-system, Helvetica, Arial, sans-serif; margin: 0; background: #f4f2ef; color: #22201c; }
.canvas { max-width: 960px; margin: 24px auto; background: #fff; border-radius: 12px;
          box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }
.header { background: linear-gradient(135deg, #4a90d9, #3fa876); color: #fff; padding: 28px 32px; }
.header h1 { margin: 0 0 4px; font-size: 26px; }
.header .sub { opacity: 0.9; font-size: 15px; }
.section { padding: 24px 32px; border-bottom: 1px solid #eee; }
.section h2 { margin: 0 0 10px; font-size: 15px; text-transform: uppercase;
              letter-spacing: 0.06em; color: #6b6459; }
.section .content { font-size: 16px; line-height: 1.5; white-space: pre-wrap; }
.placeholder { color: #b2ab9e; font-style: italic; }
.hero { font-size: 22px; font-weight: 600; }
.footer { padding: 20px 32px; background: #f9f8f6; }
.progress-bar { display: flex; gap: 4px; margin-top: 8px; }
.progress-seg { flex: 1; height: 8px; border-radius: 4px; background: #e4e0d8; }
.progress-seg.done { background: #3fa876; }
.progress-seg.active { background: #d98a3f; }
.phase-labels { display: flex; justify-content: space-between; font-size: 12px;
                color: #6b6459; margin-top: 6px; }
"""


def _read_artifact_text(project_root, key):
    meta = schema.ARTIFACTS[key]
    rel = meta["file"]
    if not rel.endswith(".md"):
        return None
    full = os.path.join(project_root, rel)
    if not os.path.exists(full):
        return None
    with open(full, "r", encoding="utf-8") as f:
        return f.read()


def _decision_text(project_root, key):
    """Pull the raw '## Decision' (decide/prioritize artifacts) or '## Notes'
    (execution artifacts) body out of an artifact file. Returns the raw text
    as written (may be multiple paragraphs, may contain markdown) -- callers
    that need a canvas-safe excerpt should go through _headline() or
    _excerpt(), not use this directly for display."""
    text = _read_artifact_text(project_root, key)
    if text is None:
        return None
    try:
        _, body = templates_mod.parse_frontmatter(text)
    except ValueError:
        return None
    for heading in ("## Decision", "## Notes"):
        if heading in body:
            section = body.split(heading, 1)[1]
            section = section.split("##", 1)[0].strip()
            if section and section not in ("_(not yet decided)_", "_(nothing recorded yet)_"):
                return section
    return None


def _strip_markdown(text):
    """Light markdown-to-plain-text cleanup. The canvas shows rendered
    summaries, not raw markdown source -- a decision written as
    "**Sustainability**\\n\\nWe chose this because..." should not show
    literal asterisks in the HTML output."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # **bold**
    text = re.sub(r"__(.+?)__", r"\1", text)  # __bold__
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", text)  # *italic*
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)  # # headings
    return text.strip()


def _headline(text):
    """First non-empty line, markdown stripped -- for compact display
    (canvas header, section titles) where the full rationale paragraph
    would overflow. Relies on the convention (documented in each decide
    skill's SKILL.md) that a Decision section leads with a short plain-text
    name/statement on its own line before the rationale."""
    if not text:
        return None
    text = _strip_markdown(text)
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return None


def _excerpt(text, max_len=400):
    """First paragraph, markdown stripped, capped at max_len -- for
    section bodies where a bit more context than a single headline is
    useful (per architecture plan S4a: 'condensed to a few bullets, not
    the full report'), without risking a full multi-paragraph essay
    ending up verbatim in a supposedly-compact canvas section."""
    if not text:
        return None
    text = _strip_markdown(text)
    paragraph = text.split("\n\n", 1)[0].strip()
    if len(paragraph) > max_len:
        paragraph = paragraph[:max_len].rstrip() + "..."
    return paragraph


def _section_html(title, key, project_root):
    raw = _decision_text(project_root, key)
    excerpt = _excerpt(raw) if raw else None
    if excerpt:
        body_html = f'<div class="content">{html.escape(excerpt)}</div>'
    else:
        body_html = '<div class="content placeholder">Not yet reached.</div>'
    return f'<div class="section"><h2>{html.escape(title)}</h2>{body_html}</div>'


def _phase_status(state, phase_keys):
    statuses = [state[k]["status"] for k in phase_keys]
    if all(schema.is_satisfied(s) for s in statuses):
        return "done"
    if any(s != schema.STATUS_NOT_STARTED for s in statuses):
        return "active"
    return "pending"


def _footer_html(state):
    segs, labels = [], []
    for phase_name, keys in schema.PHASES.items():
        status = _phase_status(state, keys)
        css_class = "done" if status == "done" else ("active" if status == "active" else "")
        segs.append(f'<div class="progress-seg {css_class}"></div>')
        readable = {"done": "complete", "active": "in progress", "pending": "not started"}[status]
        labels.append(f"<span>{html.escape(phase_name.title())}: {readable}</span>")
    return (
        '<div class="footer"><div class="progress-bar">' + "".join(segs) + "</div>"
        '<div class="phase-labels">' + "".join(labels) + "</div></div>"
    )


def render_canvas(project_root):
    """
    Rewrite canvas/cbl-canvas.html in place from the current state.json +
    challenge/* files. Degrades gracefully: any artifact without a real
    decision yet renders as "Not yet reached" rather than being omitted or
    erroring, so this is safe to call at any point in the project,
    including immediately after cbl-init with nothing decided at all.
    """
    state = state_mod.load_state(project_root)

    big_idea_headline = _headline(_decision_text(project_root, "big_idea")) or "not yet reached"
    eq_headline = _headline(_decision_text(project_root, "essential_question")) or "not yet reached"
    header_html = (
        f'<div class="header"><h1>{html.escape(big_idea_headline)}</h1>'
        f'<div class="sub">{html.escape(eq_headline)}</div></div>'
    )

    challenge_excerpt = _excerpt(_decision_text(project_root, "challenge_statement"), max_len=200)
    if challenge_excerpt:
        challenge_body = f'<div class="content hero">{html.escape(challenge_excerpt)}</div>'
    else:
        challenge_body = '<div class="content hero placeholder">Not yet reached.</div>'
    challenge_html = f'<div class="section"><h2>Challenge Statement</h2>{challenge_body}</div>'

    sections_html = "".join([
        _section_html("Guiding Questions", "guiding_questions", project_root),
        _section_html("Research Synthesis", "synthesis", project_root),
        _section_html("Solution Concept", "solution_concepts", project_root),
        _section_html("Prototype & Iteration", "prototype", project_root),
        _section_html("Implementation & Evaluation", "implementation_evaluation", project_root),
        _section_html("Reflection & Impact", "reflection_share", project_root),
    ])

    footer_html = _footer_html(state)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CBL Canvas</title>
<style>{_CSS}</style>
</head>
<body>
<div class="canvas">
{header_html}
{challenge_html}
{sections_html}
{footer_html}
</div>
</body>
</html>
"""

    out_path = os.path.join(project_root, CANVAS_REL_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return out_path
