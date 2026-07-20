"""
Shared gating-check routine. (Execution plan T004; architecture plan S5.)

Every artifact skill's opening move should be to call check_gate() for its
own artifact key and act on the result, rather than each skill
re-implementing its own upstream check and auto-offer wording by hand.
"""

from . import schema


def check_gate(state, artifact_key):
    """
    Returns one of:
      {"ok": True}
      {"ok": True, "warnings": [{"key": stale_key, "message": "..."}]}
      {"ok": False, "reason": "blocked", "prereq": key, "message": "..."}
    """
    meta = schema.ARTIFACTS[artifact_key]
    prereq = meta["depends_on"]

    if prereq is not None:
        prereq_status = state[prereq]["status"]
        if not schema.is_satisfied(prereq_status):
            prereq_title = schema.ARTIFACTS[prereq]["title"]
            return {
                "ok": False,
                "reason": "blocked",
                "prereq": prereq,
                "message": (
                    f"You haven't locked in your {prereq_title} yet -- "
                    f"{meta['title']} is built from that. Want me to run through "
                    f"that step now?"
                ),
            }

    # Gate itself passes; being stale is a soft warning, never a block.
    # Staleness lives on THIS artifact (set by state.update_artifact when an
    # upstream artifact it depends on was redecided) -- not on the
    # prerequisite itself, which was just freshly (re)decided and is why
    # this artifact became stale in the first place.
    warnings = []
    if state[artifact_key].get("stale"):
        prereq_title = schema.ARTIFACTS[prereq]["title"] if prereq else "an earlier step"
        warnings.append({
            "key": artifact_key,
            "message": (
                f"Your {prereq_title} changed after {meta['title']} was written -- "
                f"want to review it first?"
            ),
        })

    result = {"ok": True}
    if warnings:
        result["warnings"] = warnings
    return result
