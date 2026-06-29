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
            service.safe_source_path("forge/_assets/example.md")

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

    def test_create_note_preview_rejects_duplicate_note_id(self) -> None:
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "duplicate-id-note.md"
        self.assertFalse(target.exists())

        with self.assertRaises(service.SourceWriteError):
            service.create_note(
                source_path=target,
                title="Duplicate ID Note",
                description="Duplicate ID note used by source write service tests",
                note_type="research",
                note_id="zz2t-H9rM0",
                summary_lines=[
                    "First duplicate summary line.",
                    "Second duplicate summary line.",
                    "Third duplicate summary line.",
                ],
            )

    def test_apply_create_note_writes_file_after_successful_validation(self) -> None:
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-apply-note.md"
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        result = service.apply_create_note(
            source_path=target,
            title="Local Apply Note",
            description="Apply note used by source write service tests",
            note_type="research",
            note_id="ApplyOk001",
            summary_lines=[
                "First apply summary line.",
                "Second apply summary line.",
                "Third apply summary line.",
            ],
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertTrue(result.ok, result.errors)
        self.assertTrue(target.exists())
        self.assertEqual(result.applied_files, ["trove/Projects/ai-context-as-code/Research/local-apply-note.md"])
        self.assertEqual(result.rolled_back_files, [])
        self.assertIn("# Local Apply Note", target.read_text(encoding="utf-8"))

    def test_apply_create_note_rolls_back_when_validation_fails(self) -> None:
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-apply-fail-note.md"
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        result = service.apply_create_note(
            source_path=target,
            title="Local Apply Failure Note",
            description="Apply failure note used by source write service tests",
            note_type="research",
            note_id="ApplyFail1",
            summary_lines=[
                "First failed apply summary line.",
                "Second failed apply summary line.",
                "Third failed apply summary line.",
            ],
            validation_commands=[[sys.executable, "-c", "import sys; sys.exit(7)"]],
        )

        self.assertFalse(result.ok)
        self.assertFalse(target.exists())
        self.assertEqual(result.applied_files, [])
        self.assertEqual(result.rolled_back_files, ["trove/Projects/ai-context-as-code/Research/local-apply-fail-note.md"])
        self.assertIn("validation failed", "\n".join(result.errors))

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

    def test_apply_rename_title_updates_file_after_successful_validation(self) -> None:
        path = ROOT / "trove" / "Projects" / "ai-context-as-code" / "index.md"
        before = path.read_text(encoding="utf-8")
        self.addCleanup(lambda: path.write_text(before, encoding="utf-8"))

        result = service.apply_rename_title(
            source_path=path,
            note_id="zz2t-H9rM0",
            new_title="AI Context as Code Apply Preview",
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        after = path.read_text(encoding="utf-8")
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.applied_files, ["trove/Projects/ai-context-as-code/index.md"])
        self.assertEqual(result.rolled_back_files, [])
        self.assertIn('title: "AI Context as Code Apply Preview"', after)
        self.assertIn("# AI Context as Code Apply Preview", after)
        self.assertIn("id: zz2t-H9rM0", after)

    def test_apply_rename_title_rolls_back_when_validation_fails(self) -> None:
        path = ROOT / "trove" / "Projects" / "ai-context-as-code" / "index.md"
        before = path.read_text(encoding="utf-8")
        self.addCleanup(lambda: path.write_text(before, encoding="utf-8"))

        result = service.apply_rename_title(
            source_path=path,
            note_id="zz2t-H9rM0",
            new_title="AI Context as Code Failed Apply",
            validation_commands=[[sys.executable, "-c", "import sys; sys.exit(7)"]],
        )

        self.assertFalse(result.ok)
        self.assertEqual(path.read_text(encoding="utf-8"), before)
        self.assertEqual(result.applied_files, [])
        self.assertEqual(result.rolled_back_files, ["trove/Projects/ai-context-as-code/index.md"])
        self.assertIn("validation failed", "\n".join(result.errors))

    def test_apply_rename_title_rejects_wrong_note_id_without_writing(self) -> None:
        path = ROOT / "trove" / "Projects" / "ai-context-as-code" / "index.md"
        before = path.read_text(encoding="utf-8")

        result = service.apply_rename_title(
            source_path=path,
            note_id="WrongNote1",
            new_title="AI Context as Code Wrong ID",
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertFalse(result.ok)
        self.assertEqual(path.read_text(encoding="utf-8"), before)
        self.assertEqual(result.applied_files, [])
        self.assertIn("note id mismatch", "\n".join(result.errors))

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

    def test_apply_rename_path_renames_file_after_successful_validation(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-source.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-target.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Rename Path",
            description="Rename path note used by source write service tests",
            note_type="research",
            note_id="RenPath001",
            summary_lines=[
                "First rename path summary line.",
                "Second rename path summary line.",
                "Third rename path summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_rename_path(
            source_path=source,
            note_id="RenPath001",
            new_file_name=target.name,
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertTrue(result.ok, result.errors)
        self.assertFalse(source.exists())
        self.assertTrue(target.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), markdown)
        self.assertEqual(
            result.applied_files,
            [
                "trove/Projects/ai-context-as-code/Research/local-rename-path-source.md",
                "trove/Projects/ai-context-as-code/Research/local-rename-path-target.md",
            ],
        )
        self.assertTrue(result.preview.route_impact.route_preserved)

    def test_apply_rename_path_rolls_back_when_validation_fails(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-fail-source.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-fail-target.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Rename Path Failure",
            description="Rename path failure note used by source write service tests",
            note_type="research",
            note_id="RenPathBad",
            summary_lines=[
                "First failed rename path summary line.",
                "Second failed rename path summary line.",
                "Third failed rename path summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_rename_path(
            source_path=source,
            note_id="RenPathBad",
            new_file_name=target.name,
            validation_commands=[[sys.executable, "-c", "import sys; sys.exit(7)"]],
        )

        self.assertFalse(result.ok)
        self.assertTrue(source.exists())
        self.assertFalse(target.exists())
        self.assertEqual(source.read_text(encoding="utf-8"), markdown)
        self.assertEqual(result.applied_files, [])
        self.assertEqual(
            result.rolled_back_files,
            [
                "trove/Projects/ai-context-as-code/Research/local-rename-path-fail-source.md",
                "trove/Projects/ai-context-as-code/Research/local-rename-path-fail-target.md",
            ],
        )
        self.assertIn("validation failed", "\n".join(result.errors))

    def test_apply_rename_path_rejects_wrong_note_id_without_writing(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-wrong-id.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-wrong-id-target.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Rename Path Wrong ID",
            description="Rename path wrong id note used by source write service tests",
            note_type="research",
            note_id="RenPathMis",
            summary_lines=[
                "First wrong id rename path summary line.",
                "Second wrong id rename path summary line.",
                "Third wrong id rename path summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_rename_path(
            source_path=source,
            note_id="WrongNote1",
            new_file_name=target.name,
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertFalse(result.ok)
        self.assertTrue(source.exists())
        self.assertFalse(target.exists())
        self.assertEqual(source.read_text(encoding="utf-8"), markdown)
        self.assertIn("note id mismatch", "\n".join(result.errors))

    def test_apply_rename_path_does_not_move_between_folders(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-rename-path-no-move.md"
        target = ROOT / "trove" / "Daily" / "2026-06" / "local-rename-path-no-move.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Rename Path No Move",
            description="Rename path no move note used by source write service tests",
            note_type="research",
            note_id="RenNoMove1",
            summary_lines=[
                "First no move rename path summary line.",
                "Second no move rename path summary line.",
                "Third no move rename path summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        with self.assertRaises(service.SourceWriteError):
            service.apply_rename_path(
                source_path=source,
                note_id="RenNoMove1",
                target_path=target,
                validation_commands=[[sys.executable, "-c", "print('ok')"]],
            )

        self.assertTrue(source.exists())
        self.assertFalse(target.exists())

    def test_move_note_preview_blocks_assets_and_allows_project_folder(self) -> None:
        with self.assertRaises(service.SourceWriteError):
            service.move_note(
                source_path="trove/Projects/ai-context-as-code/index.md",
                target_path="forge/_assets/index.md",
            )

        preview = service.move_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
            target_path="trove/Projects/ai-context-as-code/Research/index-preview-move.md",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["sourcePath"], "trove/Projects/ai-context-as-code/Research/index-preview-move.md")

    def test_apply_move_note_moves_file_after_successful_validation(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-source.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "References" / "local-move-source.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Move Note",
            description="Move note used by source write service tests",
            note_type="research",
            note_id="MoveOk0001",
            summary_lines=[
                "First move summary line.",
                "Second move summary line.",
                "Third move summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_move_note(
            source_path=source,
            note_id="MoveOk0001",
            target_folder=target.parent,
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertTrue(result.ok, result.errors)
        self.assertFalse(source.exists())
        self.assertTrue(target.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), markdown)
        self.assertEqual(
            result.applied_files,
            [
                "trove/Projects/ai-context-as-code/Research/local-move-source.md",
                "trove/Projects/ai-context-as-code/References/local-move-source.md",
            ],
        )
        self.assertTrue(result.preview.route_impact.route_preserved)

    def test_apply_move_note_rolls_back_when_validation_fails(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-fail.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "References" / "local-move-fail.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Move Failure",
            description="Move failure note used by source write service tests",
            note_type="research",
            note_id="MoveFail01",
            summary_lines=[
                "First failed move summary line.",
                "Second failed move summary line.",
                "Third failed move summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_move_note(
            source_path=source,
            note_id="MoveFail01",
            target_folder=target.parent,
            validation_commands=[[sys.executable, "-c", "import sys; sys.exit(7)"]],
        )

        self.assertFalse(result.ok)
        self.assertTrue(source.exists())
        self.assertFalse(target.exists())
        self.assertEqual(source.read_text(encoding="utf-8"), markdown)
        self.assertEqual(result.applied_files, [])
        self.assertEqual(
            result.rolled_back_files,
            [
                "trove/Projects/ai-context-as-code/Research/local-move-fail.md",
                "trove/Projects/ai-context-as-code/References/local-move-fail.md",
            ],
        )
        self.assertIn("validation failed", "\n".join(result.errors))

    def test_apply_move_note_rejects_wrong_note_id_without_writing(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-wrong-id.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "References" / "local-move-wrong-id.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Move Wrong ID",
            description="Move wrong id note used by source write service tests",
            note_type="research",
            note_id="MoveBadID1",
            summary_lines=[
                "First wrong id move summary line.",
                "Second wrong id move summary line.",
                "Third wrong id move summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        result = service.apply_move_note(
            source_path=source,
            note_id="WrongNote1",
            target_folder=target.parent,
            validation_commands=[[sys.executable, "-c", "print('ok')"]],
        )

        self.assertFalse(result.ok)
        self.assertTrue(source.exists())
        self.assertFalse(target.exists())
        self.assertIn("note id mismatch", "\n".join(result.errors))

    def test_apply_move_note_requires_folder_change(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-same-folder.md"
        target = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-same-folder-target.md"
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))
        self.addCleanup(lambda: target.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Move Same Folder",
            description="Move same folder note used by source write service tests",
            note_type="research",
            note_id="MoveSame01",
            summary_lines=[
                "First same folder move summary line.",
                "Second same folder move summary line.",
                "Third same folder move summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        with self.assertRaises(service.SourceWriteError):
            service.apply_move_note(
                source_path=source,
                note_id="MoveSame01",
                target_path=target,
                validation_commands=[[sys.executable, "-c", "print('ok')"]],
            )

        self.assertTrue(source.exists())
        self.assertFalse(target.exists())

    def test_apply_move_note_blocks_assets(self) -> None:
        source = ROOT / "trove" / "Projects" / "ai-context-as-code" / "Research" / "local-move-assets.md"
        source.unlink(missing_ok=True)
        self.addCleanup(lambda: source.unlink(missing_ok=True))

        markdown = service.compose_note_markdown(
            title="Local Move Assets",
            description="Move assets note used by source write service tests",
            note_type="research",
            note_id="MoveAsset1",
            summary_lines=[
                "First assets move summary line.",
                "Second assets move summary line.",
                "Third assets move summary line.",
            ],
        )
        source.write_text(markdown, encoding="utf-8")

        with self.assertRaises(service.SourceWriteError):
            service.apply_move_note(
                source_path=source,
                note_id="MoveAsset1",
                target_path="forge/_assets/local-move-assets.md",
                validation_commands=[[sys.executable, "-c", "print('ok')"]],
            )

        self.assertTrue(source.exists())

    def test_archive_note_preview_moves_to_archived_and_sets_status(self) -> None:
        preview = service.archive_note(
            source_path="trove/Projects/ai-context-as-code/index.md",
            note_id="zz2t-H9rM0",
        )

        self.assertTrue(preview.ok, preview.errors)
        self.assertTrue(preview.route_impact.route_preserved)
        self.assertEqual(preview.after_summary["status"], "archived")
        self.assertEqual(preview.after_summary["sourcePath"], "forge/_archived/Projects/ai-context-as-code/index.md")
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
