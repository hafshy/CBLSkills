"""
Document template generator. (Execution plan T002; architecture plan S3a.)

Every challenge/*.md file is created at init time with a small frontmatter
block plus placeholder sections, so state.json and the document itself
agree by construction, and every artifact skill has one consistent write
target instead of separate "file exists" / "file doesn't exist yet" paths.
"""

import os
import re

from . import schema

DECIDE_BODY = """
## Options
_(none yet)_

## Decision
_(not yet decided)_
"""

EXECUTION_BODY = """
## Notes
_(nothing recorded yet)_
"""

INTRO_TEXT = {
    schema.KIND_DECIDE: "This document will hold the options your team generates for your {title}, and the one you decide on.",
    schema.KIND_PRIORITIZE: "This document will hold the {title} your team generates, and which ones you prioritize to pursue.",
    schema.KIND_EXECUTION: "This document will be filled in as your team works on {title}.",
}


def _fmt_value(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _frontmatter_block(artifact_key, status="not_started", decided_by=None, decided_at=None, stale=False):
    lines = [
        "---",
        f"artifact: {artifact_key}",
        f"status: {_fmt_value(status)}",
        f"decided_by: {_fmt_value(decided_by)}",
        f"decided_at: {_fmt_value(decided_at)}",
        f"stale: {_fmt_value(stale)}",
        "---",
    ]
    return "\n".join(lines)


def parse_frontmatter(markdown_text):
    """
    Parse the small, fixed frontmatter block this module writes.

    Deliberately not a general YAML parser: the format is fully controlled
    by this module (five flat fields, no nesting), so a tiny hand-rolled
    parser is safer than pulling in a YAML dependency for something this
    constrained.
    """
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", markdown_text, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter block found at the top of this document.")
    fm_text, body = match.group(1), match.group(2)
    data = {}
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value == "null":
            value = None
        elif value == "true":
            value = True
        elif value == "false":
            value = False
        data[key] = value
    return data, body


def generate_template(artifact_key):
    meta = schema.ARTIFACTS[artifact_key]
    frontmatter = _frontmatter_block(artifact_key)
    intro = INTRO_TEXT[meta["kind"]].format(title=meta["title"])
    body = EXECUTION_BODY if meta["kind"] == schema.KIND_EXECUTION else DECIDE_BODY
    return f"{frontmatter}\n\n# {meta['title']}\n\n_{intro}_\n{body}"


def sync_frontmatter(project_root, artifact_key, entry):
    """
    Rewrite just the frontmatter block of an artifact's markdown file to
    match its current state.json entry, leaving the body (Options/Decision
    or Notes, whatever a skill already wrote there) completely untouched.

    Called automatically by state.update_artifact() -- this is what keeps
    the file's own frontmatter and state.json from silently disagreeing
    with each other, the same failure mode that made canvas auto-refresh
    worth baking into state.py rather than trusting skill prose to do it.

    No-op for directory-type artifacts (e.g. "research"), which have no
    single frontmatter file of their own.
    """
    meta = schema.ARTIFACTS[artifact_key]
    rel_path = meta["file"]
    if not rel_path.endswith(".md"):
        return
    full_path = os.path.join(project_root, rel_path)
    if not os.path.exists(full_path):
        return

    with open(full_path, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        _, body = parse_frontmatter(text)
    except ValueError:
        return  # file doesn't have a frontmatter block yet -- leave it alone

    new_frontmatter = _frontmatter_block(
        artifact_key,
        status=entry.get("status", "not_started"),
        decided_by=entry.get("decided_by"),
        decided_at=entry.get("decided_at"),
        stale=entry.get("stale", False),
    )
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_frontmatter + body)


def scaffold_challenge_docs(project_root):
    """
    Write every challenge/*.md template plus the sub-directories that hold
    multi-file artifacts (research findings, prototype log). Called once by
    cbl-init; never overwrites a file that already exists, so it's safe to
    call again without clobbering real content.
    """
    written = []

    for key, meta in schema.ARTIFACTS.items():
        rel_path = meta["file"]
        if not rel_path.endswith(".md"):
            # e.g. "research" -> challenge/05-research-findings/ is a directory
            os.makedirs(os.path.join(project_root, rel_path), exist_ok=True)
            continue
        full_path = os.path.join(project_root, rel_path)
        if os.path.exists(full_path):
            continue
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(generate_template(key))
        written.append(rel_path)

    # Prototype has both a plan file (covered by the loop above, since its
    # "file" entry is a .md path) and a log directory, which isn't modeled
    # in the schema as a separate artifact -- create it explicitly here.
    proto_log_dir = os.path.join(project_root, "challenge", "09-prototype-log")
    os.makedirs(proto_log_dir, exist_ok=True)

    return written
