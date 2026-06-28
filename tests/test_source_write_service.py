from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import source_write_service as service  # noqa: E402


class SourceWriteServiceTests(unittest.TestCase):
    def test_safe_source_path_blocks_repo_outside_trove(self) -> None:
        with self.assertRaises(service.SourceWriteError):
            service.safe_source_path("data/notes.json")

    def test_safe_source_path_blocks_assets(self) -> None:
        with self.assertRaises(service.SourceWriteError):
            service.safe_source_path("trove/_assets/example.md")

    def test_safe_source_path_blocks_repo_escape(self) -> None:
        with self.assertRaises(service.SourceWriteError):
            service.safe_source_path("../outside.md")

    def test_parse_markdown_note_checks_title_and_h1(self) -> None:
        note = service.parse_markdown_note(
            """---
type: "design"
title: "Expected Title"
description: "Short description"
status: "draft"
created: "2026-06-29"
updated: "2026-06-29"
visibility: "private"
id: "Abcdef1234"
---

# Different Title

Line one.
Line two.
Line three.
"""
        )

        self.assertIn("title and H1 differ", "\n".join(note.errors))

    def test_preview_edit_note_is_dry_run(self) -> None:
        path = ROOT / "trove" / "Projects" / "ai-context-as-code" / "index.md"
        before = path.read_text(encoding="utf-8")
        after = before + "\n"

        preview = service.preview_edit_note(
            source_path=path,
            note_id="zz2t-H9rM0",
            new_markdown=after,
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertEqual(path.read_text(encoding="utf-8"), before)
        self.assertEqual(preview.changed_files, ["trove/Projects/ai-context-as-code/index.md"])
        self.assertTrue(preview.route_impact.route_preserved)

    def test_preview_edit_note_rejects_id_change(self) -> None:
        path = ROOT / "trove" / "Projects" / "ai-context-as-code" / "index.md"
        before = path.read_text(encoding="utf-8")
        after = before.replace("id: zz2t-H9rM0", "id: Abcdef1234")

        preview = service.preview_edit_note(
            source_path=path,
            note_id="zz2t-H9rM0",
            new_markdown=after,
        )

        self.assertFalse(preview.ok)
        self.assertIn("route id would change", "\n".join(preview.errors))

    def test_run_validation_wrapper_reports_success(self) -> None:
        result = service.run_validation([[sys.executable, "-c", "print('ok')"]])

        self.assertTrue(result.ok)
        self.assertEqual(result.commands[0].returncode, 0)
        self.assertEqual(result.commands[0].stdout.strip(), "ok")


if __name__ == "__main__":
    unittest.main()
