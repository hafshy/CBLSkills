"""
Read/write helper for .cbl/state.json. (Execution plan T001.)

Every skill that changes an artifact should go through update_artifact()
rather than hand-editing the JSON file directly -- that's what guarantees
staleness propagation (architecture plan S5) and the CBL Canvas auto-refresh
(architecture plan S2, principle 6) actually happen every time, instead of
depending on each skill's prose instructions to remember both steps.
"""

import json
import os
from datetime import datetime, timezone

from . import schema
from . import templates

STATE_PATH = os.path.join(".cbl", "state.json")


def _full_path(project_root, rel):
    return os.path.join(project_root, rel)


def default_state():
    return {
        key: {
            "status": schema.STATUS_NOT_STARTED,
            "decided_by": None,
            "decided_at": None,
            "stale": False,
        }
        for key in schema.ARTIFACTS
    }


def init_state(project_root):
    """Create a fresh state.json. Called once by cbl-init (first-time path).
    Raises if one already exists -- callers should check for that first if
    they want idempotent "already initialized" handling instead of an error."""
    path = _full_path(project_root, STATE_PATH)
    if os.path.exists(path):
        raise FileExistsError(f"{path} already exists -- this project is already initialized.")
    state = default_state()
    save_state(project_root, state)
    return state


def load_state(project_root):
    path = _full_path(project_root, STATE_PATH)
    if not os.path.exists(path):
        raise FileNotFoundError(f"No {STATE_PATH} found under {project_root} -- run cbl-init first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(project_root, state):
    path = _full_path(project_root, STATE_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp_path, path)  # atomic on POSIX -- avoids a half-written state.json


def update_artifact(project_root, key, *, status=None, decided_by=None,
                     refresh_canvas=True, **extra_fields):
    """
    Update one artifact's entry in state.json.

    - Propagates staleness to downstream artifacts, but only when this call
      is a genuine (re)decision: status changing to a satisfied value it
      wasn't already at, OR an explicit decided_by is passed alongside an
      already-satisfied status (a re-decision -- e.g. reopening and
      re-locking-in the Big Idea after the rest of the project exists).
      The second case matters because "decided" -> "decided" looks like a
      no-op status change on its own; decided_by is what distinguishes a
      real re-decision from an incidental re-save. Logging a research
      finding or other minor writes (no decided_by, or status not
      satisfied) shouldn't mark the whole rest of the project stale.
    - Refreshes the CBL Canvas as the last step by default. This is where
      "auto-refresh on every state.json write" is actually enforced in code,
      not left to each skill's instructions to remember.
    """
    if key not in schema.ARTIFACTS:
        raise KeyError(f"Unknown artifact '{key}'")

    state = load_state(project_root)
    entry = state[key]
    old_status = entry["status"]

    if status is not None:
        entry["status"] = status
    if decided_by is not None:
        entry["decided_by"] = decided_by
        entry["decided_at"] = datetime.now(timezone.utc).isoformat()
    entry["stale"] = False  # touching this artifact clears its own staleness
    entry.update(extra_fields)

    became_satisfied_change = (
        status is not None
        and schema.is_satisfied(status)
        and (old_status != status or decided_by is not None)
    )
    if became_satisfied_change:
        for dep_key in schema.dependents_of(key):
            # Only flag downstream artifacts that have actually started --
            # no point marking an untouched not_started artifact "stale".
            if state[dep_key]["status"] != schema.STATUS_NOT_STARTED:
                state[dep_key]["stale"] = True

    save_state(project_root, state)
    templates.sync_frontmatter(project_root, key, state[key])

    if refresh_canvas:
        # Deferred import: canvas.py imports this module at top level, so
        # importing canvas here (not at module load time) is what avoids a
        # circular import between state.py and canvas.py.
        from .canvas import render_canvas
        render_canvas(project_root)

    return state


def get_artifact(project_root, key):
    return load_state(project_root)[key]
