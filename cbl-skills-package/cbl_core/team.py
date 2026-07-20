"""
Read/write helper for .cbl/team.json -- registered team members.

Kept deliberately simple and separate from state.py: team membership isn't
part of the artifact-gating graph, it's just a roster cbl-init and cbl-merge
both need to read.
"""

import json
import os

TEAM_PATH = os.path.join(".cbl", "team.json")


def _full_path(project_root, rel):
    return os.path.join(project_root, rel)


def _member_entry(name):
    return {
        "name": name,
        "folder": f"team/{name}",
        "branch": f"team/{name}",
    }


def init_team(project_root, first_member_name):
    """Create .cbl/team.json with the first team member. Called once by
    cbl-init (first-time path)."""
    path = _full_path(project_root, TEAM_PATH)
    if os.path.exists(path):
        raise FileExistsError(f"{path} already exists -- this project is already initialized.")
    team = {"members": [_member_entry(first_member_name)]}
    save_team(project_root, team)
    return team


def load_team(project_root):
    path = _full_path(project_root, TEAM_PATH)
    if not os.path.exists(path):
        raise FileNotFoundError(f"No {TEAM_PATH} found under {project_root} -- run cbl-init first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_team(project_root, team):
    path = _full_path(project_root, TEAM_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(team, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp_path, path)


def is_member(project_root, name):
    team = load_team(project_root)
    return any(m["name"] == name for m in team["members"])


def register_member(project_root, name):
    """Idempotent: registering someone already on the team just returns the
    roster unchanged, rather than duplicating them -- this is what makes
    cbl-init safe to run again by a returning member (execution plan T006)."""
    team = load_team(project_root)
    if is_member(project_root, name):
        return team
    team["members"].append(_member_entry(name))
    save_team(project_root, team)
    return team
