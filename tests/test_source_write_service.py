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

    def test_create_note_preview_builds_private_draft_without_writing(self) -> None:
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-preview-note.md"
        self.assertFalse(target.exists())

        preview = service.create_note(
            source_path=target,
            title="Local Preview Note",
            description="Preview note used by source write service tests",
            note_type="research",
            note_id="Preview001",
            summary_lines=[
                "First preview summary line.",
                "Second preview summary line.",
                "Third preview summary line.",
            ],
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertFalse(target.exists())
        self.assertEqual(preview.changed_files, ["trove/Projects/ai-context-as-code/Research/local-preview-note.md"])
        self.assertEqual(preview.after_summary["route"], "/trove/Preview001")
        self.assertFalse(preview.route_impact.public_surface_changed)
        self.assertIn('visibility: "private"', preview.diff)

    def test_rename_title_preview_updates_frontmatter_and_h1(self) -> None:
        preview = service.rename_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
            new_title="AI Context as Code Preview",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["title"], "AI Context as Code Preview")
        self.assertEqual(preview.after_summary["h1"], "AI Context as Code Preview")
        self.assertIn('title: "AI Context as Code Preview"', preview.diff)
        self.assertIn("# AI Context as Code Preview", preview.diff)

    def test_rename_path_preview_keeps_route_id(self) -> None:
        preview = service.rename_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
            new_file_name="index-preview-rename.md",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertEqual(
            preview.changed_files,
            [
                "trove/Projects/ai-context-as-code/index.md",
                "trove/Projects/ai-context-as-code/index-preview-rename.md",
            ],
        )
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["route"], "/trove/zz2t-H9rM0")

    def test_move_note_preview_blocks_assets_and_allows_project_folder(self) -> None:
        with self.assertRaises(service.SourceWriteError):
            service.move_note(
                source_path="trove/Projects/ai-context-as-code/index.md",
                target_path="trove/_assets/index.md",
            )

        preview = service.move_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
            target_path="trove/Projects/ai-context-as-code/Research/index-preview-move.md",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["sourcePath"], "trove/Projects/ai-context-as-code/Research/index-preview-move.md")

    def test_archive_note_preview_moves_to_archived_and_sets_status(self) -> None:
        preview = service.archive_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["status"], "archived")
        self.assertEqual(preview.after_summary["sourcePath"], "trove/_archived/Projects/ai-context-as-code/index.md")
        self.assertIn('status: "archived"', preview.diff)

    def test_hard_delete_note_requires_confirmation_token(self) -> None:
        blocked = service.hard_delete_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
        )

        self.assertFalse(blocked.ok)
        self.assertIn(service.HARD_DELETE_CONFIRMATION, "\n".join(blocked.errors))

        allowed = service.hard_delete_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
            confirmation_token=service.HARD_DELETE_CONFIRMATION,
        )

        self.assertTrue(allowed.ok, allowed.errors)
        self.assertFalse(allowed.route_impact.route_preserved)
        self.assertIn("does not remove git history", "\n".join(allowed.warnings))

    def test_run_validation_wrapper_reports_success(self) -> None:
        result = service.run_validation([[sys.executable, "-c", "print('ok')"]])

        self.assertTrue(result.ok)
        self.assertEqual(result.commands[0].returncode, 0)
        self.assertEqual(result.commands[0].stdout.strip(), "ok")


if __name__ == "__main__":
    unittest.main()
