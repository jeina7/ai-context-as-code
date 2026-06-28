#!/usr/bin/env python3
"""Local-only source write service helpers for ACAC note changes.

This module is intentionally not imported by the public reader. It provides
dry-run previews, path safety checks, markdown note inspection, and validation
runner wrappers that a future local editor or local API can call.
"""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import validate_trove


ROOT = Path(__file__).resolve().parents[1]
TROVE_DIR = ROOT / "trove"

KNOWN_TROVE_ROOTS = {"Daily", "Projects", "_config", "_archived", "_assets"}
FORBIDDEN_TROVE_PARTS = {"_assets"}
DEFAULT_VALIDATION_COMMANDS = [
    [sys.executable, "scripts/validate_trove.py"],
    [sys.executable, "scripts/build_trove.py"],
    [sys.executable, "scripts/check_public_payload.py"],
]


class SourceWriteError(ValueError):
    """Raised when a requested source write would violate ACAC boundaries."""


@dataclass
class MarkdownNote:
    source_path: str
    frontmatter: dict[str, str]
    raw_frontmatter: str
    body: str
    h1: str | None
    title: str
    note_id: str
    visibility: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class FileChange:
    path: str
    before: str
    after: str
    change_type: str = "modify"


@dataclass
class RouteImpact:
    before_route: str | None
    after_route: str | None
    route_preserved: bool
    public_surface_changed: bool


@dataclass
class DiffPreview:
    ok: bool
    operation: str
    mode: str
    changed_files: list[str]
    blocked_files: list[str]
    before_summary: dict[str, Any]
    after_summary: dict[str, Any]
    route_impact: RouteImpact
    validation_commands: list[list[str]]
    diff: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass
class ValidationResult:
    ok: bool
    commands: list[CommandResult]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_candidate_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()

    parts = path.parts
    if parts and parts[0] in KNOWN_TROVE_ROOTS:
        return (TROVE_DIR / path).resolve()
    return (ROOT / path).resolve()


def safe_source_path(path_value: str | Path, *, must_exist: bool = False) -> Path:
    path = resolve_candidate_path(path_value)

    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise SourceWriteError(f"path is outside repo: {path_value}") from exc

    try:
        rel_to_trove = path.relative_to(TROVE_DIR)
    except ValueError as exc:
        raise SourceWriteError(f"source writes must stay under trove/: {path_value}") from exc

    if any(part in FORBIDDEN_TROVE_PARTS for part in rel_to_trove.parts):
        raise SourceWriteError(f"source writes are forbidden under trove/_assets/: {path_value}")

    if path.suffix != ".md":
        raise SourceWriteError(f"source write target must be a markdown file: {path_value}")

    if must_exist and not path.is_file():
        raise SourceWriteError(f"source markdown file does not exist: {path_value}")

    return path


def parse_markdown_note(text: str, source_path: str = "") -> MarkdownNote:
    errors: list[str] = []
    warnings: list[str] = []

    if not text.startswith("---\n"):
        return MarkdownNote(source_path, {}, "", text, None, "", "", "", ["frontmatter is missing"], [])

    end = text.find("\n---\n", 4)
    if end == -1:
        return MarkdownNote(
            source_path,
            {},
            "",
            text,
            None,
            "",
            "",
            "",
            ["frontmatter closing marker is missing"],
            [],
        )

    raw_frontmatter = text[4:end]
    frontmatter = validate_trove.parse_frontmatter(raw_frontmatter)
    body = text[end + len("\n---\n") :].lstrip("\n")
    h1_match = validate_trove.re.search(r"^#\s+(.+)$", body, flags=validate_trove.re.MULTILINE)
    h1 = h1_match.group(1).strip() if h1_match else None
    title = frontmatter.get("title", "")
    note_id = frontmatter.get("id", "")
    visibility = frontmatter.get("visibility", "")

    if not h1:
        errors.append("H1 is missing")
    elif title and h1 != title:
        errors.append(f"title and H1 differ: {title!r} != {h1!r}")

    if visibility and visibility not in validate_trove.ALLOWED_VISIBILITY:
        errors.append(f"unsupported visibility: {visibility}")
    if frontmatter.get("type", "") and frontmatter["type"] not in validate_trove.ALLOWED_TYPES:
        errors.append(f"unsupported type: {frontmatter['type']}")
    if frontmatter.get("status", "") and frontmatter["status"] not in validate_trove.ALLOWED_STATUS:
        errors.append(f"unsupported status: {frontmatter['status']}")
    if note_id and not validate_trove.ID_PATTERN.match(note_id):
        errors.append("id must be 10 URL-safe characters")

    return MarkdownNote(
        source_path=source_path,
        frontmatter=frontmatter,
        raw_frontmatter=raw_frontmatter,
        body=body,
        h1=h1,
        title=title,
        note_id=note_id,
        visibility=visibility,
        errors=errors,
        warnings=warnings,
    )


def note_summary(note: MarkdownNote) -> dict[str, Any]:
    route = f"/trove/{note.note_id}" if note.note_id else None
    return {
        "id": note.note_id or None,
        "route": route,
        "title": note.title or None,
        "h1": note.h1,
        "type": note.frontmatter.get("type") or None,
        "status": note.frontmatter.get("status") or None,
        "visibility": note.visibility or None,
        "sourcePath": note.source_path,
        "errors": note.errors,
        "warnings": note.warnings,
    }


def route_impact(before_note: MarkdownNote, after_note: MarkdownNote) -> RouteImpact:
    before_route = f"/trove/{before_note.note_id}" if before_note.note_id else None
    after_route = f"/trove/{after_note.note_id}" if after_note.note_id else None
    public_surface_changed = (
        before_note.visibility == "public"
        or after_note.visibility == "public"
        or before_route != after_route
    )
    return RouteImpact(
        before_route=before_route,
        after_route=after_route,
        route_preserved=before_route == after_route,
        public_surface_changed=public_surface_changed,
    )


def unified_diff_for_change(change: FileChange) -> str:
    before_lines = change.before.splitlines(keepends=True)
    after_lines = change.after.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=f"a/{change.path}",
            tofile=f"b/{change.path}",
            lineterm="",
        )
    )


def build_preview_diff(
    operation: str,
    changes: list[FileChange],
    *,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
) -> DiffPreview:
    errors = list(errors or [])
    warnings = list(warnings or [])
    changed_files = [change.path for change in changes if change.before != change.after]
    diff = "\n".join(unified_diff_for_change(change) for change in changes if change.before != change.after)

    before_note = parse_markdown_note(changes[0].before, changes[0].path) if changes else empty_note()
    after_note = parse_markdown_note(changes[0].after, changes[0].path) if changes else empty_note()
    errors.extend(before_note.errors)
    errors.extend(after_note.errors)
    warnings.extend(before_note.warnings)
    warnings.extend(after_note.warnings)

    return DiffPreview(
        ok=not errors,
        operation=operation,
        mode="dry-run",
        changed_files=changed_files,
        blocked_files=[],
        before_summary=note_summary(before_note),
        after_summary=note_summary(after_note),
        route_impact=route_impact(before_note, after_note),
        validation_commands=DEFAULT_VALIDATION_COMMANDS,
        diff=diff,
        errors=errors,
        warnings=warnings,
    )


def empty_note() -> MarkdownNote:
    return MarkdownNote("", {}, "", "", None, "", "", "")


def preview_edit_note(
    *,
    source_path: str | Path,
    new_markdown: str,
    note_id: str | None = None,
) -> DiffPreview:
    path = safe_source_path(source_path, must_exist=True)
    rel_path = repo_relative(path)
    before = path.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, rel_path)
    after_note = parse_markdown_note(new_markdown, rel_path)

    errors: list[str] = []
    if note_id and before_note.note_id and before_note.note_id != note_id:
        errors.append(f"note id mismatch: expected {note_id}, found {before_note.note_id}")
    if note_id and after_note.note_id and after_note.note_id != note_id:
        errors.append(f"new markdown changes note id: expected {note_id}, found {after_note.note_id}")
    if before_note.note_id and after_note.note_id and before_note.note_id != after_note.note_id:
        errors.append(f"route id would change: {before_note.note_id} -> {after_note.note_id}")

    return build_preview_diff(
        "edit_note",
        [FileChange(rel_path, before, new_markdown)],
        errors=errors,
    )


def run_validation(commands: list[list[str]] | None = None) -> ValidationResult:
    command_list = commands or DEFAULT_VALIDATION_COMMANDS
    results: list[CommandResult] = []
    for command in command_list:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        results.append(
            CommandResult(
                command=command,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        )
        if completed.returncode != 0:
            break
    return ValidationResult(ok=all(result.returncode == 0 for result in results), commands=results)


def unsupported_lifecycle_preview(operation: str) -> DiffPreview:
    return DiffPreview(
        ok=False,
        operation=operation,
        mode="dry-run",
        changed_files=[],
        blocked_files=[],
        before_summary={},
        after_summary={},
        route_impact=RouteImpact(None, None, True, False),
        validation_commands=DEFAULT_VALIDATION_COMMANDS,
        diff="",
        errors=[f"{operation} is not implemented in the skeleton yet"],
    )


def create_note(*_: Any, **__: Any) -> DiffPreview:
    return unsupported_lifecycle_preview("create_note")


def rename_note(*_: Any, **__: Any) -> DiffPreview:
    return unsupported_lifecycle_preview("rename_note")


def move_note(*_: Any, **__: Any) -> DiffPreview:
    return unsupported_lifecycle_preview("move_note")


def archive_note(*_: Any, **__: Any) -> DiffPreview:
    return unsupported_lifecycle_preview("archive_note")


def hard_delete_note(*_: Any, **__: Any) -> DiffPreview:
    return unsupported_lifecycle_preview("hard_delete_note")


createNote = create_note
renameNote = rename_note
moveNote = move_note
archiveNote = archive_note
hardDeleteNote = hard_delete_note
runValidation = run_validation
buildPreviewDiff = build_preview_diff


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser("preview-edit", help="Preview an edit without writing files")
    preview_parser.add_argument("--source-path", required=True)
    preview_parser.add_argument("--new-markdown-file", required=True)
    preview_parser.add_argument("--note-id")

    validate_parser = subparsers.add_parser("run-validation", help="Run ACAC validation/build commands")
    validate_parser.add_argument("--skip-build", action="store_true")

    args = parser.parse_args(argv)

    try:
        if args.command == "preview-edit":
            new_markdown = Path(args.new_markdown_file).read_text(encoding="utf-8")
            preview = preview_edit_note(
                source_path=args.source_path,
                new_markdown=new_markdown,
                note_id=args.note_id,
            )
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "run-validation":
            commands = DEFAULT_VALIDATION_COMMANDS[:1] if args.skip_build else DEFAULT_VALIDATION_COMMANDS
            result = run_validation(commands)
            print_json(result.to_dict())
            return 0 if result.ok else 1
    except SourceWriteError as exc:
        print_json({"ok": False, "errors": [str(exc)]})
        return 1

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
