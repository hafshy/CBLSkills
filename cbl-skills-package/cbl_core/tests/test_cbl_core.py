"""
Tests for Milestone 0 (execution plan T001-T004).

Run from the CBLSkills/ directory:
    python3 -m unittest cbl_core.tests.test_cbl_core -v
"""

import os
import shutil
import tempfile
import unittest

from cbl_core import schema, state, team, templates, canvas, gating


class CblCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _init_project(self):
        state.init_state(self.tmp)
        team.init_team(self.tmp, "hafshy")
        templates.scaffold_challenge_docs(self.tmp)
        canvas.render_canvas(self.tmp)

    def _write_decided_artifact(self, key, decision_text):
        """Simulate what an artifact skill does to its own file before
        calling state.update_artifact: write real content into the
        Options/Decision (or Notes) section."""
        meta = schema.ARTIFACTS[key]
        heading = "## Notes" if meta["kind"] == schema.KIND_EXECUTION else "## Decision"
        full_path = os.path.join(self.tmp, meta["file"])
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(
                f"---\nartifact: {key}\nstatus: decided\ndecided_by: hafshy\n"
                f"decided_at: 2026-07-17\nstale: false\n---\n\n"
                f"# {meta['title']}\n\n{heading}\n{decision_text}\n"
            )

    # -- state.py --------------------------------------------------------

    def test_init_state_creates_all_artifacts_not_started(self):
        s = state.init_state(self.tmp)
        self.assertEqual(set(s.keys()), set(schema.ARTIFACTS.keys()))
        for entry in s.values():
            self.assertEqual(entry["status"], schema.STATUS_NOT_STARTED)
            self.assertFalse(entry["stale"])
            self.assertIsNone(entry["decided_by"])

    def test_init_state_twice_raises(self):
        state.init_state(self.tmp)
        with self.assertRaises(FileExistsError):
            state.init_state(self.tmp)

    def test_load_state_before_init_raises(self):
        with self.assertRaises(FileNotFoundError):
            state.load_state(self.tmp)

    def test_update_artifact_sets_decided_by_and_timestamp(self):
        state.init_state(self.tmp)
        s = state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy",
                                   refresh_canvas=False)
        self.assertEqual(s["big_idea"]["status"], "decided")
        self.assertEqual(s["big_idea"]["decided_by"], "hafshy")
        self.assertIsNotNone(s["big_idea"]["decided_at"])

    def test_staleness_propagates_only_on_real_redecision(self):
        self._init_project()
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        state.update_artifact(self.tmp, "essential_question", status=schema.STATUS_DECIDED, decided_by="hafshy")
        s = state.load_state(self.tmp)
        self.assertFalse(s["essential_question"]["stale"])

        # Simulate genuinely reopening + redeciding the Big Idea.
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_NOT_STARTED)
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")

        s = state.load_state(self.tmp)
        self.assertTrue(s["essential_question"]["stale"], "downstream artifact should be flagged stale")

    def test_staleness_does_not_touch_untouched_downstream(self):
        self._init_project()
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        # essential_question was never started -- redeciding big_idea shouldn't
        # mark something that was never touched as "stale".
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_NOT_STARTED)
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        s = state.load_state(self.tmp)
        self.assertFalse(s["essential_question"]["stale"])

    # -- team.py -----------------------------------------------------------

    def test_team_registration_is_idempotent(self):
        team.init_team(self.tmp, "hafshy")
        t1 = team.register_member(self.tmp, "hafshy")
        self.assertEqual(len(t1["members"]), 1, "re-registering an existing member should not duplicate them")
        t2 = team.register_member(self.tmp, "teammate-b")
        self.assertEqual(len(t2["members"]), 2)
        self.assertTrue(team.is_member(self.tmp, "teammate-b"))
        self.assertFalse(team.is_member(self.tmp, "teammate-c"))

    def test_team_member_folder_and_branch_names(self):
        team.init_team(self.tmp, "hafshy")
        t = team.register_member(self.tmp, "teammate-b")
        entry = [m for m in t["members"] if m["name"] == "teammate-b"][0]
        self.assertEqual(entry["folder"], "team/teammate-b")
        self.assertEqual(entry["branch"], "team/teammate-b")

    # -- templates.py --------------------------------------------------------

    def test_template_frontmatter_round_trips(self):
        text = templates.generate_template("big_idea")
        data, body = templates.parse_frontmatter(text)
        self.assertEqual(data["artifact"], "big_idea")
        self.assertEqual(data["status"], "not_started")
        self.assertIsNone(data["decided_by"])
        self.assertFalse(data["stale"])
        self.assertIn("_(none yet)_", body)
        self.assertIn("_(not yet decided)_", body)

    def test_execution_artifact_template_uses_notes_section(self):
        text = templates.generate_template("research")
        _, body = templates.parse_frontmatter(text)
        self.assertIn("## Notes", body)
        self.assertNotIn("## Decision", body)

    def test_scaffold_creates_every_markdown_artifact_and_subdirs(self):
        state.init_state(self.tmp)
        templates.scaffold_challenge_docs(self.tmp)
        for key, meta in schema.ARTIFACTS.items():
            if meta["file"].endswith(".md"):
                self.assertTrue(
                    os.path.exists(os.path.join(self.tmp, meta["file"])),
                    f"missing template for {key}",
                )
        self.assertTrue(os.path.isdir(os.path.join(self.tmp, "challenge", "05-research-findings")))
        self.assertTrue(os.path.isdir(os.path.join(self.tmp, "challenge", "09-prototype-log")))

    def test_scaffold_never_overwrites_existing_content(self):
        state.init_state(self.tmp)
        templates.scaffold_challenge_docs(self.tmp)
        self._write_decided_artifact("big_idea", "Food Waste")
        # Calling scaffold again (e.g. a teammate joining) must not clobber it.
        templates.scaffold_challenge_docs(self.tmp)
        with open(os.path.join(self.tmp, "challenge", "01-big-idea.md")) as f:
            self.assertIn("Food Waste", f.read())

    # -- canvas.py --------------------------------------------------------

    def test_canvas_renders_blank_project(self):
        self._init_project()
        path = os.path.join(self.tmp, canvas.CANVAS_REL_PATH)
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            html_text = f.read()
        self.assertIn("not yet reached", html_text)
        self.assertIn("Not yet reached", html_text)
        self.assertIn("Engage: not started", html_text)
        self.assertIn("Investigate: not started", html_text)
        self.assertIn("Act: not started", html_text)

    def test_canvas_refreshes_via_update_artifact(self):
        self._init_project()
        path = os.path.join(self.tmp, canvas.CANVAS_REL_PATH)
        with open(path) as f:
            before = f.read()

        self._write_decided_artifact("big_idea", "Food Waste -- specific and locally actionable.")
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")

        with open(path) as f:
            after = f.read()
        self.assertNotEqual(before, after)
        self.assertIn("Food Waste", after)
        self.assertIn("Engage: in progress", after)

    def test_canvas_marks_phase_complete_only_when_all_its_artifacts_decided(self):
        self._init_project()
        self._write_decided_artifact("big_idea", "Food Waste")
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        self._write_decided_artifact("essential_question", "Why does our cafeteria waste so much food?")
        state.update_artifact(self.tmp, "essential_question", status=schema.STATUS_DECIDED, decided_by="hafshy")

        path = os.path.join(self.tmp, canvas.CANVAS_REL_PATH)
        with open(path) as f:
            html_text = f.read()
        self.assertIn("Engage: in progress", html_text, "should not say complete with challenge_statement still undecided")

        self._write_decided_artifact("challenge_statement", "Design a way to cut cafeteria food waste in half.")
        state.update_artifact(self.tmp, "challenge_statement", status=schema.STATUS_DECIDED, decided_by="hafshy")
        with open(path) as f:
            html_text = f.read()
        self.assertIn("Engage: complete", html_text)

    # -- gating.py --------------------------------------------------------

    def test_gating_blocks_when_prereq_missing(self):
        self._init_project()
        s = state.load_state(self.tmp)
        result = gating.check_gate(s, "essential_question")
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "blocked")
        self.assertEqual(result["prereq"], "big_idea")
        self.assertIn("Big Idea", result["message"])

    def test_gating_passes_with_no_warnings_when_prereq_fresh(self):
        self._init_project()
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        s = state.load_state(self.tmp)
        result = gating.check_gate(s, "essential_question")
        self.assertTrue(result["ok"])
        self.assertNotIn("warnings", result)

    def test_gating_warns_on_stale_prereq_but_does_not_block(self):
        self._init_project()
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")
        state.update_artifact(self.tmp, "essential_question", status=schema.STATUS_DECIDED, decided_by="hafshy")
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_NOT_STARTED)
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="hafshy")

        s = state.load_state(self.tmp)
        result = gating.check_gate(s, "essential_question")
        self.assertTrue(result["ok"], "a stale artifact should warn, never block")
        self.assertIn("warnings", result)
        self.assertEqual(result["warnings"][0]["key"], "essential_question")
        self.assertIn("Big Idea", result["warnings"][0]["message"])

    def test_gating_root_artifact_has_no_prereq(self):
        self._init_project()
        s = state.load_state(self.tmp)
        result = gating.check_gate(s, "big_idea")
        self.assertTrue(result["ok"])
        self.assertNotIn("warnings", result)

    # -- Regression tests for bugs found by the Milestone 1 subagent test ---
    # (real multi-paragraph, markdown-formatted decisions -- not the
    # single-line fixtures used above, which didn't exercise these paths.)

    def test_canvas_header_shows_only_first_line_not_full_rationale(self):
        self._init_project()
        self._write_decided_artifact(
            "big_idea",
            "Sustainability\n\nThe team is choosing Sustainability as its Big Idea because it connects "
            "to their interest in reducing cafeteria food waste. Decided by Alex.",
        )
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="alex")

        with open(os.path.join(self.tmp, canvas.CANVAS_REL_PATH)) as f:
            html_text = f.read()

        self.assertIn("<h1>Sustainability</h1>", html_text,
                       "header should show only the short first line")
        self.assertNotIn("Decided by Alex", html_text,
                          "the full rationale paragraph should not leak into the h1")

    def test_canvas_strips_markdown_bold_from_headline(self):
        self._init_project()
        self._write_decided_artifact("big_idea", "**Sustainability**\n\nRationale here.")
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="alex")

        with open(os.path.join(self.tmp, canvas.CANVAS_REL_PATH)) as f:
            html_text = f.read()

        self.assertIn("<h1>Sustainability</h1>", html_text)
        self.assertNotIn("**", html_text, "raw markdown bold markers should never reach the HTML")

    def test_section_excerpt_is_capped_and_markdown_stripped(self):
        self._init_project()
        long_text = "This synthesis has a **key finding** that is " + ("quite long. " * 60)
        self._write_decided_artifact("synthesis", long_text)
        state.update_artifact(self.tmp, "synthesis", status=schema.STATUS_COMPLETE)

        with open(os.path.join(self.tmp, canvas.CANVAS_REL_PATH)) as f:
            html_text = f.read()

        self.assertNotIn("**", html_text)
        self.assertIn("...", html_text, "very long section content should be truncated with an ellipsis")

    def test_frontmatter_stays_in_sync_with_state_after_update(self):
        self._init_project()
        self._write_decided_artifact("big_idea", "Sustainability\n\nRationale.")
        state.update_artifact(self.tmp, "big_idea", status=schema.STATUS_DECIDED, decided_by="alex")

        with open(os.path.join(self.tmp, "challenge", "01-big-idea.md")) as f:
            text = f.read()
        data, body = templates.parse_frontmatter(text)

        self.assertEqual(data["status"], "decided",
                          "frontmatter must reflect the real status, not stay stuck at not_started")
        self.assertEqual(data["decided_by"], "alex")
        self.assertIn("Sustainability", body, "syncing frontmatter must not touch the body content")
        self.assertIn("Rationale.", body)

    def test_frontmatter_sync_is_noop_for_directory_artifacts(self):
        # "research" is a directory, not a single .md file -- sync_frontmatter
        # must not error when called for it.
        self._init_project()
        state.update_artifact(self.tmp, "research", status=schema.STATUS_IN_PROGRESS)
        # No assertion beyond "did not raise" -- this is a crash-guard test.


if __name__ == "__main__":
    unittest.main()
