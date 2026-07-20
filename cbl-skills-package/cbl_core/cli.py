"""
Command-line interface over cbl_core, for skills to invoke via Bash.

Each subcommand is one deterministic, scriptable action a CBL skill needs --
state changes, team registration, gating checks, canvas rendering. The
creative work (writing options, decisions, research findings) stays with
Claude directly editing the markdown files in challenge/; this CLI only
ever touches .cbl/state.json, .cbl/team.json, and canvas/cbl-canvas.html.
Skills should never hand-edit those three directly -- always go through
here, so staleness propagation and canvas auto-refresh actually happen.

Usage (project path is always explicit, run from anywhere):
    python3 -m cbl_core.cli init <project_root> --name <first-member-name>
    python3 -m cbl_core.cli join <project_root> --name <member-name>
    python3 -m cbl_core.cli status <project_root>
    python3 -m cbl_core.cli gate-check <project_root> <artifact-key>
    python3 -m cbl_core.cli set-status <project_root> <artifact-key> --status decided --decided-by <name>
    python3 -m cbl_core.cli render-canvas <project_root>

Every subcommand prints one JSON object to stdout and exits 0 on success,
1 on a handled failure (never initialized, gate blocked, etc.) -- never a
raw Python traceback, so a skill can always parse the output.
"""

import argparse
import json
import os
import sys

from . import schema, state, team, templates, canvas, gating


def _require_initialized(project_root):
    if not os.path.exists(os.path.join(project_root, ".cbl", "state.json")):
        print(json.dumps({
            "ok": False,
            "error": "not_initialized",
            "message": "No CBL project found here. Use 'init' to start a new one first.",
        }))
        return False
    return True


def cmd_init(args):
    project_root = args.project
    if os.path.exists(os.path.join(project_root, ".cbl", "state.json")):
        print(json.dumps({
            "ok": False,
            "error": "already_initialized",
            "message": "This project is already initialized. Use 'join' to register a new team member instead.",
        }))
        return 1
    os.makedirs(project_root, exist_ok=True)
    state.init_state(project_root)
    team.init_team(project_root, args.name)
    templates.scaffold_challenge_docs(project_root)
    canvas.render_canvas(project_root)
    print(json.dumps({"ok": True, "action": "initialized", "member": args.name}))
    return 0


def cmd_join(args):
    project_root = args.project
    if not _require_initialized(project_root):
        return 1
    already = team.is_member(project_root, args.name)
    t = team.register_member(project_root, args.name)
    entry = next(m for m in t["members"] if m["name"] == args.name)
    print(json.dumps({
        "ok": True,
        "action": "already_member" if already else "joined",
        "member": entry,
    }))
    return 0


def cmd_status(args):
    project_root = args.project
    if not _require_initialized(project_root):
        return 1
    s = state.load_state(project_root)
    t = team.load_team(project_root)
    phases = {}
    for phase_name, keys in schema.PHASES.items():
        statuses = [s[k]["status"] for k in keys]
        if all(schema.is_satisfied(v) for v in statuses):
            phases[phase_name] = "complete"
        elif any(v != schema.STATUS_NOT_STARTED for v in statuses):
            phases[phase_name] = "in_progress"
        else:
            phases[phase_name] = "not_started"
    stale = [k for k, v in s.items() if v.get("stale")]
    print(json.dumps({
        "ok": True,
        "phases": phases,
        "artifacts": s,
        "stale": stale,
        "team": t["members"],
    }, indent=2))
    return 0


def cmd_gate_check(args):
    project_root = args.project
    if not _require_initialized(project_root):
        return 1
    s = state.load_state(project_root)
    result = gating.check_gate(s, args.artifact)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def cmd_set_status(args):
    project_root = args.project
    if not _require_initialized(project_root):
        return 1
    s = state.update_artifact(
        project_root, args.artifact,
        status=args.status,
        decided_by=args.decided_by,
    )
    print(json.dumps({"ok": True, "artifact": args.artifact, "entry": s[args.artifact]}, indent=2))
    return 0


def cmd_render_canvas(args):
    project_root = args.project
    if not _require_initialized(project_root):
        return 1
    path = canvas.render_canvas(project_root)
    print(json.dumps({"ok": True, "canvas_path": path}))
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="cbl_core.cli")
    sub = p.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("project")
    p_init.add_argument("--name", required=True)
    p_init.set_defaults(func=cmd_init)

    p_join = sub.add_parser("join")
    p_join.add_argument("project")
    p_join.add_argument("--name", required=True)
    p_join.set_defaults(func=cmd_join)

    p_status = sub.add_parser("status")
    p_status.add_argument("project")
    p_status.set_defaults(func=cmd_status)

    p_gate = sub.add_parser("gate-check")
    p_gate.add_argument("project")
    p_gate.add_argument("artifact", choices=list(schema.ARTIFACTS.keys()))
    p_gate.set_defaults(func=cmd_gate_check)

    p_setstatus = sub.add_parser("set-status")
    p_setstatus.add_argument("project")
    p_setstatus.add_argument("artifact", choices=list(schema.ARTIFACTS.keys()))
    p_setstatus.add_argument("--status", required=True, choices=[
        schema.STATUS_NOT_STARTED, schema.STATUS_OPTIONS_GENERATED,
        schema.STATUS_DECIDED, schema.STATUS_IN_PROGRESS, schema.STATUS_COMPLETE,
    ])
    p_setstatus.add_argument("--decided-by", dest="decided_by", default=None)
    p_setstatus.set_defaults(func=cmd_set_status)

    p_canvas = sub.add_parser("render-canvas")
    p_canvas.add_argument("project")
    p_canvas.set_defaults(func=cmd_render_canvas)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
