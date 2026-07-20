"""
Tests for cbl_core.cli -- the command layer skills actually invoke via Bash.

Run from CBLSkills/: python3 -m unittest cbl_core.tests.test_cli -v
"""

import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest

from cbl_core import cli


class CblCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(argv)
        return code, json.loads(buf.getvalue())

    def test_init_creates_project_and_prints_ok(self):
        code, out = self._run(["init", self.tmp, "--name", "hafshy"])
        self.assertEqual(code, 0)
        self.assertTrue(out["ok"])
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "canvas", "cbl-canvas.html")))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "challenge", "01-big-idea.md")))

    def test_init_twice_fails_cleanly_not_a_traceback(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        code, out = self._run(["init", self.tmp, "--name", "hafshy"])
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "already_initialized")

    def test_join_before_init_fails_cleanly(self):
        code, out = self._run(["join", self.tmp, "--name", "teammate-b"])
        self.assertEqual(code, 1)
        self.assertEqual(out["error"], "not_initialized")

    def test_status_before_init_fails_cleanly(self):
        code, out = self._run(["status", self.tmp])
        self.assertEqual(code, 1)
        self.assertEqual(out["error"], "not_initialized")

    def test_gate_check_before_init_fails_cleanly(self):
        code, out = self._run(["gate-check", self.tmp, "big_idea"])
        self.assertEqual(code, 1)
        self.assertEqual(out["error"], "not_initialized")

    def test_join_registers_new_member_and_is_idempotent(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        code, out = self._run(["join", self.tmp, "--name", "teammate-b"])
        self.assertEqual(code, 0)
        self.assertEqual(out["action"], "joined")
        self.assertEqual(out["member"]["folder"], "team/teammate-b")

        code, out = self._run(["join", self.tmp, "--name", "teammate-b"])
        self.assertEqual(code, 0)
        self.assertEqual(out["action"], "already_member")

    def test_status_reports_not_started_phases_on_fresh_project(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        code, out = self._run(["status", self.tmp])
        self.assertEqual(code, 0)
        self.assertEqual(out["phases"]["engage"], "not_started")
        self.assertEqual(out["phases"]["investigate"], "not_started")
        self.assertEqual(out["phases"]["act"], "not_started")
        self.assertEqual(out["stale"], [])
        self.assertEqual(len(out["team"]), 1)

    def test_gate_check_blocks_before_prereq_decided(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        code, out = self._run(["gate-check", self.tmp, "essential_question"])
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertEqual(out["prereq"], "big_idea")

    def test_set_status_decides_artifact_and_refreshes_canvas(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        canvas_path = os.path.join(self.tmp, "canvas", "cbl-canvas.html")
        with open(canvas_path) as f:
            before = f.read()

        code, out = self._run(["set-status", self.tmp, "big_idea", "--status", "decided", "--decided-by", "hafshy"])
        self.assertEqual(code, 0)
        self.assertEqual(out["entry"]["status"], "decided")
        self.assertEqual(out["entry"]["decided_by"], "hafshy")

        with open(canvas_path) as f:
            after = f.read()
        self.assertNotEqual(before, after, "canvas should auto-refresh on set-status")

    def test_gate_check_passes_after_prereq_decided(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        self._run(["set-status", self.tmp, "big_idea", "--status", "decided", "--decided-by", "hafshy"])
        code, out = self._run(["gate-check", self.tmp, "essential_question"])
        self.assertEqual(code, 0)
        self.assertTrue(out["ok"])

    def test_render_canvas_manual_command_works_standalone(self):
        self._run(["init", self.tmp, "--name", "hafshy"])
        code, out = self._run(["render-canvas", self.tmp])
        self.assertEqual(code, 0)
        self.assertTrue(out["ok"])
        self.assertTrue(os.path.exists(out["canvas_path"]))


if __name__ == "__main__":
    unittest.main()
