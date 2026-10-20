from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "proofgate" / "scripts"))
from check_pr import validate  # noqa: E402
from install_rule import install  # noqa: E402


GOOD_PR = """## Acceptance criteria

Source: Issue 42: Settings should persist

| ID | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| AC-1 | Saved URL persists after reload | verified | Browser reload showed saved URL |
| AC-2 | Clear removes saved URL | verified | Browser clear then reload showed empty input |
"""


class InstallRuleTests(unittest.TestCase):
    def test_create_then_repeat_without_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.assertEqual(install(project, "en"), "created")
            first = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Before marking work complete", first)
            self.assertEqual(install(project, "en"), "unchanged")
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8"), first)

    def test_replace_partial_marked_rule_preserving_project_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            target = project / "AGENTS.md"
            target.write_text(
                "# Project\n\nKeep secrets out of the repo.\n\n"
                "<!-- proofgate:start v1 -->\nOld partial rule\n<!-- proofgate:end -->\n"
                "\n## Tests\nRun focused checks.\n",
                encoding="utf-8",
            )
            self.assertEqual(install(project, "en"), "updated")
            result = target.read_text(encoding="utf-8")
            self.assertNotIn("Old partial rule", result)
            self.assertIn("Keep secrets out of the repo.", result)
            self.assertIn("## Tests\nRun focused checks.", result)
            self.assertEqual(result.count("<!-- proofgate:start"), 1)
            self.assertEqual(install(project, "en"), "unchanged")

    def test_thai_rule_and_existing_unmarked_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.assertEqual(install(project, "th"), "created")
            self.assertIn("เกณฑ์ปิดงาน", (project / "AGENTS.md").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text("Use proofgate for delivery.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manual review"):
                install(project, "en")

    def test_malformed_markers_do_not_modify_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            target = project / "AGENTS.md"
            content = "<!-- proofgate:start v1 -->\nMissing end\n"
            target.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Malformed"):
                install(project, "en")
            self.assertEqual(target.read_text(encoding="utf-8"), content)


class PullRequestTests(unittest.TestCase):
    def test_complete_report_passes(self) -> None:
        self.assertEqual(validate(GOOD_PR), [])

    def test_incomplete_status_and_placeholder_evidence_fail(self) -> None:
        body = GOOD_PR.replace("| verified | Browser clear then reload showed empty input |", "| incomplete | <evidence> |")
        errors = validate(body)
        self.assertTrue(any("status must be verified" in error for error in errors))
        self.assertTrue(any("provide concrete evidence" in error for error in errors))

    def test_missing_source_and_repeated_id_fail(self) -> None:
        body = GOOD_PR.replace("Source: Issue 42: Settings should persist", "Source: <source>")
        body = body.replace("| AC-2 |", "| AC-1 |")
        errors = validate(body)
        self.assertTrue(any("Source" in error for error in errors))
        self.assertTrue(any("repeated" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
