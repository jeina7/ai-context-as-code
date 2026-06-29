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
import secrets
import string
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import validate_trove


ROOT = Path(__file__).resolve().parents[1]
TROVE_DIR = ROOT / "trove"
FORGE_DIR = ROOT / "forge"
SOURCE_ROOTS = ((TROVE_DIR, ""), (FORGE_DIR, "forge"))

FORBIDDEN_SOURCE_PARTS = {"_assets"}
ALLOWED_TROVE_ROOTS = {"Daily", "Projects"}
ALLOWED_FORGE_ROOTS = {"_config", "_archived"}
ID_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase + "_-"
HARD_DELETE_CONFIRMATION = "HARD_DELETE_UNCOMMITTED_LOCAL_NOTE"
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


@dataclass
class ApplyResult:
    ok: bool
    operation: str
    mode: str
    preview: DiffPreview
    validation: ValidationResult | None
    applied_files: list[str]
    rolled_back_files: list[str]
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_relative_path(path: Path) -> str | None:
    resolved = path.resolve()
    for source_root, prefix in SOURCE_ROOTS:
        try:
            rel_path = resolved.relative_to(source_root.resolve()).as_posix()
        except ValueError:
            continue
        return f"{prefix}/{rel_path}" if prefix else rel_path
    return None


def source_root_and_parts(path: Path) -> tuple[str, tuple[str, ...]]:
    resolved = path.resolve()
    try:
        rel_to_trove = resolved.relative_to(TROVE_DIR.resolve())
        return "trove", rel_to_trove.parts
    except ValueError:
        pass

    try:
        rel_to_forge = resolved.relative_to(FORGE_DIR.resolve())
        return "forge", rel_to_forge.parts
    except ValueError as exc:
        raise SourceWriteError(f"source writes must stay under trove/ or forge/: {path}") from exc


def resolve_candidate_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()

    parts = path.parts
    if parts and parts[0] in {"trove", "forge"}:
        return (ROOT / path).resolve()
    if parts and parts[0] in {"Daily", "Projects"}:
        return (TROVE_DIR / path).resolve()
    if parts and parts[0] in {"_config", "_archived", "_assets"}:
        return (FORGE_DIR / path).resolve()
    return (ROOT / path).resolve()


def safe_source_path(path_value: str | Path, *, must_exist: bool = False) -> Path:
    path = resolve_candidate_path(path_value)

    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise SourceWriteError(f"path is outside repo: {path_value}") from exc

    _source_root, source_parts = source_root_and_parts(path)

    if any(part in FORBIDDEN_SOURCE_PARTS for part in source_parts):
        raise SourceWriteError(f"source writes are forbidden under _assets/: {path_value}")

    if path.suffix != ".md":
        raise SourceWriteError(f"source write target must be a markdown file: {path_value}")

    if must_exist and not path.is_file():
        raise SourceWriteError(f"source markdown file does not exist: {path_value}")

    return path


def require_lifecycle_path(path: Path) -> None:
    source_root, source_parts = source_root_and_parts(path)
    if source_root == "trove":
        allowed = ALLOWED_TROVE_ROOTS
    else:
        allowed = ALLOWED_FORGE_ROOTS
    if not source_parts or source_parts[0] not in allowed:
        allowed_display = "trove/Daily, trove/Projects, forge/_config, forge/_archived"
        raise SourceWriteError(f"source lifecycle writes must target one of: {allowed_display}")


def require_existing_parent(path: Path) -> None:
    if not path.parent.is_dir():
        raise SourceWriteError(f"target parent folder does not exist: {repo_relative(path.parent)}")


def require_available_target(path: Path) -> None:
    if path.exists():
        raise SourceWriteError(f"target path already exists: {repo_relative(path)}")


def load_id_registry() -> dict[str, Any]:
    registry_path = ROOT / "data" / "id-registry.json"
    if not registry_path.is_file():
        return {"version": 1, "ids": {}, "paths": {}}
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SourceWriteError("data/id-registry.json is not valid JSON") from exc
    registry.setdefault("ids", {})
    registry.setdefault("paths", {})
    return registry


def registry_source_path(path: Path) -> str:
    rel_path = source_relative_path(path)
    if rel_path is None:
        raise SourceWriteError(f"path is outside source roots: {repo_relative(path)}")
    return rel_path


def require_unregistered_target(path: Path) -> None:
    registry = load_id_registry()
    rel_path = registry_source_path(path)
    if rel_path in registry.get("paths", {}):
        raise SourceWriteError(f"target path is already registered: {rel_path}")


def require_available_note_id(note_id: str | None) -> None:
    if note_id and note_id in collect_used_ids():
        raise SourceWriteError(f"note id is already registered: {note_id}")


def normalize_markdown_filename(file_name: str) -> str:
    if "/" in file_name or "\\" in file_name:
        raise SourceWriteError("file name rename cannot contain path separators")
    path = Path(file_name)
    return path.name if path.suffix == ".md" else f"{path.name}.md"


def markdown_path_for_target(path_value: str | Path) -> Path:
    path = resolve_candidate_path(path_value)
    if path.suffix != ".md":
        path = path.with_suffix(".md")
    path = safe_source_path(path, must_exist=False)
    require_lifecycle_path(path)
    require_existing_parent(path)
    return path


def existing_note_path(path_value: str | Path) -> Path:
    path = safe_source_path(path_value, must_exist=True)
    require_lifecycle_path(path)
    return path


def collect_used_ids() -> set[str]:
    used: set[str] = set()
    for path in validate_trove.iter_markdown_files():
        note, _ = validate_trove.parse_markdown(path)
        if note and note.frontmatter.get("id"):
            used.add(note.frontmatter["id"])

    registry_path = ROOT / "data" / "id-registry.json"
    if registry_path.is_file():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            registry = {}
        used.update(registry.get("ids", {}).keys())
    return used


def generate_note_id(used: set[str] | None = None) -> str:
    used = set(used or collect_used_ids())
    while True:
        note_id = "".join(secrets.choice(ID_ALPHABET) for _ in range(10))
        if note_id not in used:
            return note_id


def quote_frontmatter_value(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def frontmatter_line(key: str, value: str) -> str:
    if key == "id":
        return f"{key}: {value}"
    return f"{key}: {quote_frontmatter_value(value)}"


def replace_frontmatter_value(text: str, key: str, value: str) -> str:
    if not text.startswith("---\n"):
        raise SourceWriteError("frontmatter is missing")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise SourceWriteError("frontmatter closing marker is missing")

    raw_frontmatter = text[4:end]
    replacement = frontmatter_line(key, value)
    pattern = validate_trove.re.compile(rf"^{validate_trove.re.escape(key)}:\s*.*$", flags=validate_trove.re.MULTILINE)
    if pattern.search(raw_frontmatter):
        raw_frontmatter = pattern.sub(replacement, raw_frontmatter, count=1)
    else:
        raw_frontmatter = raw_frontmatter.rstrip() + f"\n{replacement}"
    return f"---\n{raw_frontmatter}{text[end:]}"


def replace_first_h1(text: str, title: str) -> str:
    replacement = f"# {title}"
    if validate_trove.re.search(r"^#\s+.+$", text, flags=validate_trove.re.MULTILINE):
        return validate_trove.re.sub(
            r"^#\s+.+$",
            replacement,
            text,
            count=1,
            flags=validate_trove.re.MULTILINE,
        )
    return text.rstrip() + f"\n\n{replacement}\n"


def compose_note_markdown(
    *,
    title: str,
    description: str,
    note_type: str,
    status: str = "draft",
    visibility: str = "private",
    note_id: str | None = None,
    created: str | None = None,
    updated: str | None = None,
    summary_lines: list[str] | None = None,
) -> str:
    if note_type not in validate_trove.ALLOWED_TYPES:
        raise SourceWriteError(f"unsupported type: {note_type}")
    if status not in validate_trove.ALLOWED_STATUS:
        raise SourceWriteError(f"unsupported status: {status}")
    if visibility not in validate_trove.ALLOWED_VISIBILITY:
        raise SourceWriteError(f"unsupported visibility: {visibility}")
    if not title.strip():
        raise SourceWriteError("title is required")

    note_id = note_id or generate_note_id()
    if not validate_trove.ID_PATTERN.match(note_id):
        raise SourceWriteError("id must be 10 URL-safe characters")

    today = date.today().isoformat()
    summary = summary_lines or [
        "Write the first durable summary line here.",
        "Write the second durable summary line here.",
        "Write the third durable summary line here.",
    ]
    if not (3 <= len(summary) <= 5):
        raise SourceWriteError("summary must contain 3-5 lines")

    fields = [
        ("type", note_type),
        ("title", title),
        ("description", description),
        ("status", status),
        ("created", created or today),
        ("updated", updated or today),
        ("visibility", visibility),
        ("id", note_id),
    ]
    frontmatter = "\n".join(frontmatter_line(key, value) for key, value in fields)
    body = "\n".join(line.strip() for line in summary)
    return f"---\n{frontmatter}\n---\n\n# {title}\n\n{body}\n"


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
    public_surface_changed = before_note.visibility == "public" or after_note.visibility == "public"
    return RouteImpact(
        before_route=before_route,
        after_route=after_route,
        route_preserved=before_route == after_route,
        public_surface_changed=public_surface_changed,
    )


def unified_diff_for_change(change: FileChange) -> str:
    before_lines = change.before.splitlines(keepends=True)
    after_lines = change.after.splitlines(keepends=True)
    fromfile = f"a/{change.path}"
    tofile = f"b/{change.path}"
    if change.change_type == "create":
        fromfile = "/dev/null"
    elif change.change_type == "delete":
        tofile = "/dev/null"
    return "".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=fromfile,
            tofile=tofile,
            lineterm="\n",
        )
    )


def build_preview_diff(
    operation: str,
    changes: list[FileChange],
    *,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
    before_note: MarkdownNote | None = None,
    after_note: MarkdownNote | None = None,
) -> DiffPreview:
    errors = list(errors or [])
    warnings = list(warnings or [])
    changed_files = [change.path for change in changes if change.before != change.after]
    diff = "\n".join(unified_diff_for_change(change) for change in changes if change.before != change.after)

    first_change = changes[0] if changes else None
    if before_note is None:
        if first_change and first_change.before:
            before_note = parse_markdown_note(first_change.before, first_change.path)
        else:
            before_note = empty_note()
    if after_note is None:
        if first_change and first_change.after:
            after_note = parse_markdown_note(first_change.after, first_change.path)
        else:
            after_note = empty_note()
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


def rollback_created_file(path: Path, expected_text: str) -> tuple[bool, str | None]:
    if not path.exists():
        return True, None
    if path.read_text(encoding="utf-8") != expected_text:
        return False, f"rollback skipped because file changed after write: {repo_relative(path)}"
    path.unlink()
    return True, None


def rollback_modified_file(path: Path, before_text: str, expected_text: str) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"rollback failed because file is missing: {repo_relative(path)}"
    if path.read_text(encoding="utf-8") != expected_text:
        return False, f"rollback skipped because file changed after write: {repo_relative(path)}"
    path.write_text(before_text, encoding="utf-8")
    return True, None


def rollback_renamed_file(source: Path, target: Path, expected_text: str) -> tuple[bool, str | None]:
    if source.exists():
        return False, f"rollback failed because source path already exists: {repo_relative(source)}"
    if not target.exists():
        return False, f"rollback failed because target path is missing: {repo_relative(target)}"
    if target.read_text(encoding="utf-8") != expected_text:
        return False, f"rollback skipped because file changed after rename: {repo_relative(target)}"
    target.rename(source)
    return True, None


def create_note(
    *,
    source_path: str | Path,
    title: str,
    description: str,
    note_type: str,
    status: str = "draft",
    visibility: str = "private",
    note_id: str | None = None,
    created: str | None = None,
    updated: str | None = None,
    summary_lines: list[str] | None = None,
) -> DiffPreview:
    path = markdown_path_for_target(source_path)
    require_available_target(path)
    require_unregistered_target(path)
    require_available_note_id(note_id)
    rel_path = repo_relative(path)
    markdown = compose_note_markdown(
        title=title,
        description=description,
        note_type=note_type,
        status=status,
        visibility=visibility,
        note_id=note_id,
        created=created,
        updated=updated,
        summary_lines=summary_lines,
    )
    after_note = parse_markdown_note(markdown, rel_path)
    return build_preview_diff(
        "create_note",
        [FileChange(rel_path, "", markdown, "create")],
        before_note=empty_note(),
        after_note=after_note,
    )


def apply_create_note(
    *,
    source_path: str | Path,
    title: str,
    description: str,
    note_type: str,
    status: str = "draft",
    visibility: str = "private",
    note_id: str | None = None,
    created: str | None = None,
    updated: str | None = None,
    summary_lines: list[str] | None = None,
    validation_commands: list[list[str]] | None = None,
) -> ApplyResult:
    preview = create_note(
        source_path=source_path,
        title=title,
        description=description,
        note_type=note_type,
        status=status,
        visibility=visibility,
        note_id=note_id,
        created=created,
        updated=updated,
        summary_lines=summary_lines,
    )
    if not preview.ok:
        return ApplyResult(
            ok=False,
            operation="apply_create_note",
            mode="apply",
            preview=preview,
            validation=None,
            applied_files=[],
            rolled_back_files=[],
            errors=list(preview.errors),
            warnings=list(preview.warnings),
        )

    if len(preview.changed_files) != 1:
        raise SourceWriteError("create apply expected exactly one changed file")

    note_id_to_write = preview.after_summary.get("id")
    if not note_id_to_write:
        raise SourceWriteError("create preview did not produce a note id")

    target = safe_source_path(preview.changed_files[0], must_exist=False)
    require_lifecycle_path(target)
    require_existing_parent(target)
    require_available_target(target)

    # The diff is for humans. Rebuild the markdown from the preview summary to
    # keep the actual write independent from unified diff parsing.
    markdown = compose_note_markdown(
        title=title,
        description=description,
        note_type=note_type,
        status=status,
        visibility=visibility,
        note_id=note_id_to_write,
        created=created,
        updated=updated,
        summary_lines=summary_lines,
    )
    after_note = parse_markdown_note(markdown, repo_relative(target))
    if after_note.errors:
        raise SourceWriteError(f"create markdown is invalid: {'; '.join(after_note.errors)}")

    target.write_text(markdown, encoding="utf-8")
    validation = run_validation(validation_commands)

    if validation.ok:
        return ApplyResult(
            ok=True,
            operation="apply_create_note",
            mode="apply",
            preview=preview,
            validation=validation,
            applied_files=[repo_relative(target)],
            rolled_back_files=[],
            warnings=list(preview.warnings),
        )

    rollback_ok, rollback_error = rollback_created_file(target, markdown)
    errors = ["validation failed; create apply was not completed"]
    if rollback_error:
        errors.append(rollback_error)
    return ApplyResult(
        ok=False,
        operation="apply_create_note",
        mode="apply",
        preview=preview,
        validation=validation,
        applied_files=[] if rollback_ok else [repo_relative(target)],
        rolled_back_files=[repo_relative(target)] if rollback_ok else [],
        errors=errors,
        warnings=list(preview.warnings),
    )


def apply_rename_title(
    *,
    source_path: str | Path,
    new_title: str,
    note_id: str | None = None,
    validation_commands: list[list[str]] | None = None,
) -> ApplyResult:
    preview = rename_note(
        source_path=source_path,
        new_title=new_title,
        note_id=note_id,
    )
    if not preview.ok:
        return ApplyResult(
            ok=False,
            operation="apply_rename_title",
            mode="apply",
            preview=preview,
            validation=None,
            applied_files=[],
            rolled_back_files=[],
            errors=list(preview.errors),
            warnings=list(preview.warnings),
        )

    if not preview.changed_files:
        return ApplyResult(
            ok=True,
            operation="apply_rename_title",
            mode="apply",
            preview=preview,
            validation=None,
            applied_files=[],
            rolled_back_files=[],
            warnings=[*preview.warnings, "no title changes to apply"],
        )

    if len(preview.changed_files) != 1:
        raise SourceWriteError("rename title apply expected exactly one changed file")

    path = existing_note_path(source_path)
    rel_path = repo_relative(path)
    if rel_path != preview.changed_files[0]:
        raise SourceWriteError("rename title preview target does not match source path")

    before = path.read_text(encoding="utf-8")
    after = replace_frontmatter_value(before, "title", new_title)
    after = replace_first_h1(after, new_title)
    after_note = parse_markdown_note(after, rel_path)
    if after_note.errors:
        raise SourceWriteError(f"rename title markdown is invalid: {'; '.join(after_note.errors)}")

    before_note = parse_markdown_note(before, rel_path)
    if before_note.note_id and after_note.note_id and before_note.note_id != after_note.note_id:
        raise SourceWriteError(f"route id would change: {before_note.note_id} -> {after_note.note_id}")

    path.write_text(after, encoding="utf-8")
    validation = run_validation(validation_commands)

    if validation.ok:
        return ApplyResult(
            ok=True,
            operation="apply_rename_title",
            mode="apply",
            preview=preview,
            validation=validation,
            applied_files=[rel_path],
            rolled_back_files=[],
            warnings=list(preview.warnings),
        )

    rollback_ok, rollback_error = rollback_modified_file(path, before, after)
    errors = ["validation failed; rename title apply was not completed"]
    if rollback_error:
        errors.append(rollback_error)
    return ApplyResult(
        ok=False,
        operation="apply_rename_title",
        mode="apply",
        preview=preview,
        validation=validation,
        applied_files=[] if rollback_ok else [rel_path],
        rolled_back_files=[rel_path] if rollback_ok else [],
        errors=errors,
        warnings=list(preview.warnings),
    )


def apply_rename_path(
    *,
    source_path: str | Path,
    note_id: str | None = None,
    new_file_name: str | None = None,
    target_path: str | Path | None = None,
    validation_commands: list[list[str]] | None = None,
) -> ApplyResult:
    preview = rename_note(
        source_path=source_path,
        note_id=note_id,
        new_file_name=new_file_name,
        target_path=target_path,
    )
    if not preview.ok:
        return ApplyResult(
            ok=False,
            operation="apply_rename_path",
            mode="apply",
            preview=preview,
            validation=None,
            applied_files=[],
            rolled_back_files=[],
            errors=list(preview.errors),
            warnings=list(preview.warnings),
        )

    if len(preview.changed_files) != 2:
        raise SourceWriteError("rename path apply expected exactly two changed file entries")

    source = existing_note_path(source_path)
    source_rel = repo_relative(source)
    target_rel = preview.after_summary.get("sourcePath")
    if not target_rel:
        raise SourceWriteError("rename path preview did not produce a target path")
    if source_rel != preview.before_summary.get("sourcePath") or source_rel != preview.changed_files[0]:
        raise SourceWriteError("rename path preview source does not match source path")

    target = safe_source_path(target_rel, must_exist=False)
    require_lifecycle_path(target)
    require_existing_parent(target)
    require_available_target(target)
    if source.parent != target.parent:
        raise SourceWriteError("rename path apply cannot move folders; use move apply instead")

    before = source.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, source_rel)
    after_note = parse_markdown_note(before, target_rel)
    if before_note.errors:
        raise SourceWriteError(f"source markdown is invalid: {'; '.join(before_note.errors)}")
    if after_note.errors:
        raise SourceWriteError(f"target markdown is invalid: {'; '.join(after_note.errors)}")
    if before_note.note_id and after_note.note_id and before_note.note_id != after_note.note_id:
        raise SourceWriteError(f"route id would change: {before_note.note_id} -> {after_note.note_id}")

    source.rename(target)
    validation = run_validation(validation_commands)

    if validation.ok:
        return ApplyResult(
            ok=True,
            operation="apply_rename_path",
            mode="apply",
            preview=preview,
            validation=validation,
            applied_files=list(preview.changed_files),
            rolled_back_files=[],
            warnings=list(preview.warnings),
        )

    rollback_ok, rollback_error = rollback_renamed_file(source, target, before)
    errors = ["validation failed; rename path apply was not completed"]
    if rollback_error:
        errors.append(rollback_error)
    return ApplyResult(
        ok=False,
        operation="apply_rename_path",
        mode="apply",
        preview=preview,
        validation=validation,
        applied_files=[] if rollback_ok else list(preview.changed_files),
        rolled_back_files=list(preview.changed_files) if rollback_ok else [],
        errors=errors,
        warnings=list(preview.warnings),
    )


def apply_move_note(
    *,
    source_path: str | Path,
    target_path: str | Path | None = None,
    target_folder: str | Path | None = None,
    note_id: str | None = None,
    validation_commands: list[list[str]] | None = None,
) -> ApplyResult:
    preview = move_note(
        source_path=source_path,
        target_path=target_path,
        target_folder=target_folder,
        note_id=note_id,
    )
    if not preview.ok:
        return ApplyResult(
            ok=False,
            operation="apply_move_note",
            mode="apply",
            preview=preview,
            validation=None,
            applied_files=[],
            rolled_back_files=[],
            errors=list(preview.errors),
            warnings=list(preview.warnings),
        )

    if len(preview.changed_files) != 2:
        raise SourceWriteError("move apply expected exactly two changed file entries")

    source = existing_note_path(source_path)
    source_rel = repo_relative(source)
    target_rel = preview.after_summary.get("sourcePath")
    if not target_rel:
        raise SourceWriteError("move preview did not produce a target path")
    if source_rel != preview.before_summary.get("sourcePath") or source_rel != preview.changed_files[0]:
        raise SourceWriteError("move preview source does not match source path")

    target = safe_source_path(target_rel, must_exist=False)
    require_lifecycle_path(target)
    require_existing_parent(target)
    require_available_target(target)
    if source.parent == target.parent:
        raise SourceWriteError("move apply must change folders; use rename path apply instead")

    before = source.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, source_rel)
    after_note = parse_markdown_note(before, target_rel)
    if before_note.errors:
        raise SourceWriteError(f"source markdown is invalid: {'; '.join(before_note.errors)}")
    if after_note.errors:
        raise SourceWriteError(f"target markdown is invalid: {'; '.join(after_note.errors)}")
    if before_note.note_id and after_note.note_id and before_note.note_id != after_note.note_id:
        raise SourceWriteError(f"route id would change: {before_note.note_id} -> {after_note.note_id}")

    source.rename(target)
    validation = run_validation(validation_commands)

    if validation.ok:
        return ApplyResult(
            ok=True,
            operation="apply_move_note",
            mode="apply",
            preview=preview,
            validation=validation,
            applied_files=list(preview.changed_files),
            rolled_back_files=[],
            warnings=list(preview.warnings),
        )

    rollback_ok, rollback_error = rollback_renamed_file(source, target, before)
    errors = ["validation failed; move apply was not completed"]
    if rollback_error:
        errors.append(rollback_error)
    return ApplyResult(
        ok=False,
        operation="apply_move_note",
        mode="apply",
        preview=preview,
        validation=validation,
        applied_files=[] if rollback_ok else list(preview.changed_files),
        rolled_back_files=list(preview.changed_files) if rollback_ok else [],
        errors=errors,
        warnings=list(preview.warnings),
    )


def rename_note(
    *,
    source_path: str | Path,
    note_id: str | None = None,
    new_title: str | None = None,
    new_file_name: str | None = None,
    target_path: str | Path | None = None,
) -> DiffPreview:
    if bool(new_title) == bool(new_file_name or target_path):
        raise SourceWriteError("provide exactly one rename target: new_title or new_file_name/target_path")

    path = existing_note_path(source_path)
    rel_path = repo_relative(path)
    before = path.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, rel_path)
    errors = note_id_errors(before_note, note_id)

    if new_title:
        after = replace_frontmatter_value(before, "title", new_title)
        after = replace_first_h1(after, new_title)
        after_note = parse_markdown_note(after, rel_path)
        return build_preview_diff(
            "rename_title",
            [FileChange(rel_path, before, after)],
            errors=errors,
            before_note=before_note,
            after_note=after_note,
        )

    target = markdown_path_for_target(target_path) if target_path else path.with_name(normalize_markdown_filename(new_file_name or ""))
    target = safe_source_path(target, must_exist=False)
    require_lifecycle_path(target)
    require_existing_parent(target)
    require_available_target(target)
    target_rel_path = repo_relative(target)
    after_note = parse_markdown_note(before, target_rel_path)
    return build_preview_diff(
        "rename_path",
        [
            FileChange(rel_path, before, "", "delete"),
            FileChange(target_rel_path, "", before, "create"),
        ],
        errors=errors,
        before_note=before_note,
        after_note=after_note,
    )


def move_note(
    *,
    source_path: str | Path,
    target_path: str | Path | None = None,
    target_folder: str | Path | None = None,
    note_id: str | None = None,
) -> DiffPreview:
    if bool(target_path) == bool(target_folder):
        raise SourceWriteError("provide exactly one move target: target_path or target_folder")

    path = existing_note_path(source_path)
    rel_path = repo_relative(path)
    before = path.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, rel_path)
    errors = note_id_errors(before_note, note_id)

    if target_folder:
        folder = resolve_candidate_path(target_folder)
        try:
            folder.relative_to(ROOT)
        except ValueError as exc:
            raise SourceWriteError(f"target folder must stay under trove/ or forge/: {target_folder}") from exc
        source_root, source_parts = source_root_and_parts(folder)
        allowed = ALLOWED_TROVE_ROOTS if source_root == "trove" else ALLOWED_FORGE_ROOTS
        if not source_parts or source_parts[0] not in allowed:
            raise SourceWriteError("target folder is not an allowed lifecycle folder")
        if any(part in FORBIDDEN_SOURCE_PARTS for part in source_parts):
            raise SourceWriteError("target folder cannot be under _assets/")
        if not folder.is_dir():
            raise SourceWriteError(f"target folder does not exist: {repo_relative(folder)}")
        target = folder / path.name
    else:
        target = markdown_path_for_target(target_path or "")

    target = safe_source_path(target, must_exist=False)
    require_lifecycle_path(target)
    require_existing_parent(target)
    require_available_target(target)
    target_rel_path = repo_relative(target)
    after_note = parse_markdown_note(before, target_rel_path)
    return build_preview_diff(
        "move_note",
        [
            FileChange(rel_path, before, "", "delete"),
            FileChange(target_rel_path, "", before, "create"),
        ],
        errors=errors,
        before_note=before_note,
        after_note=after_note,
    )


def archive_note(
    *,
    source_path: str | Path,
    note_id: str | None = None,
    archive_root: str | Path = "_archived",
) -> DiffPreview:
    path = existing_note_path(source_path)
    rel_path = repo_relative(path)
    source_root, source_parts = source_root_and_parts(path)
    if source_root == "forge" and source_parts and source_parts[0] == "_archived":
        raise SourceWriteError("note is already under _archived/")

    before = path.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, rel_path)
    errors = note_id_errors(before_note, note_id)

    archive_base = resolve_candidate_path(archive_root)
    try:
        archive_rel = archive_base.relative_to(FORGE_DIR)
    except ValueError as exc:
        raise SourceWriteError("archive root must stay under forge/") from exc
    if not archive_rel.parts or archive_rel.parts[0] != "_archived":
        raise SourceWriteError("archive root must be under forge/_archived/")
    if not archive_base.is_dir():
        raise SourceWriteError(f"archive root does not exist: {repo_relative(archive_base)}")

    target = archive_base.joinpath(*source_parts)
    target = safe_source_path(target, must_exist=False)
    require_lifecycle_path(target)
    require_available_target(target)
    target_rel_path = repo_relative(target)
    after = replace_frontmatter_value(before, "status", "archived")
    after_note = parse_markdown_note(after, target_rel_path)
    return build_preview_diff(
        "archive_note",
        [
            FileChange(rel_path, before, "", "delete"),
            FileChange(target_rel_path, "", after, "create"),
        ],
        errors=errors,
        before_note=before_note,
        after_note=after_note,
        warnings=["archive preview moves the note under forge/_archived/ and keeps its id"],
    )


def hard_delete_note(
    *,
    source_path: str | Path,
    confirmation_token: str | None = None,
    note_id: str | None = None,
) -> DiffPreview:
    path = existing_note_path(source_path)
    rel_path = repo_relative(path)
    before = path.read_text(encoding="utf-8")
    before_note = parse_markdown_note(before, rel_path)
    errors = note_id_errors(before_note, note_id)
    if confirmation_token != HARD_DELETE_CONFIRMATION:
        errors.append(f"hard delete requires confirmation token: {HARD_DELETE_CONFIRMATION}")

    return build_preview_diff(
        "hard_delete_note",
        [FileChange(rel_path, before, "", "delete")],
        errors=errors,
        before_note=before_note,
        after_note=empty_note(),
        warnings=["hard delete preview does not remove git history or deployed cache"],
    )


def note_id_errors(note: MarkdownNote, expected_note_id: str | None) -> list[str]:
    if expected_note_id and note.note_id and note.note_id != expected_note_id:
        return [f"note id mismatch: expected {expected_note_id}, found {note.note_id}"]
    return []


createNote = create_note
applyCreateNote = apply_create_note
applyRenameTitle = apply_rename_title
applyRenamePath = apply_rename_path
renameNote = rename_note
applyMoveNote = apply_move_note
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

    create_parser = subparsers.add_parser("preview-create", help="Preview creating a note")
    create_parser.add_argument("--source-path", required=True)
    create_parser.add_argument("--title", required=True)
    create_parser.add_argument("--description", required=True)
    create_parser.add_argument("--type", required=True, dest="note_type")
    create_parser.add_argument("--status", default="draft")
    create_parser.add_argument("--visibility", default="private")
    create_parser.add_argument("--note-id")
    create_parser.add_argument("--summary-line", action="append", dest="summary_lines")

    apply_create_parser = subparsers.add_parser("apply-create", help="Create a note and run validation")
    apply_create_parser.add_argument("--source-path", required=True)
    apply_create_parser.add_argument("--title", required=True)
    apply_create_parser.add_argument("--description", required=True)
    apply_create_parser.add_argument("--type", required=True, dest="note_type")
    apply_create_parser.add_argument("--status", default="draft")
    apply_create_parser.add_argument("--visibility", default="private")
    apply_create_parser.add_argument("--note-id")
    apply_create_parser.add_argument("--summary-line", action="append", dest="summary_lines")
    apply_create_parser.add_argument("--skip-build", action="store_true")

    rename_title_parser = subparsers.add_parser("preview-rename-title", help="Preview title rename")
    rename_title_parser.add_argument("--source-path", required=True)
    rename_title_parser.add_argument("--new-title", required=True)
    rename_title_parser.add_argument("--note-id")

    apply_rename_title_parser = subparsers.add_parser("apply-rename-title", help="Rename a note title and run validation")
    apply_rename_title_parser.add_argument("--source-path", required=True)
    apply_rename_title_parser.add_argument("--new-title", required=True)
    apply_rename_title_parser.add_argument("--note-id")
    apply_rename_title_parser.add_argument("--skip-build", action="store_true")

    rename_path_parser = subparsers.add_parser("preview-rename-path", help="Preview file path rename")
    rename_path_parser.add_argument("--source-path", required=True)
    rename_path_parser.add_argument("--new-file-name")
    rename_path_parser.add_argument("--target-path")
    rename_path_parser.add_argument("--note-id")

    apply_rename_path_parser = subparsers.add_parser("apply-rename-path", help="Rename a note file path and run validation")
    apply_rename_path_parser.add_argument("--source-path", required=True)
    apply_rename_path_parser.add_argument("--new-file-name")
    apply_rename_path_parser.add_argument("--target-path")
    apply_rename_path_parser.add_argument("--note-id")
    apply_rename_path_parser.add_argument("--skip-build", action="store_true")

    move_parser = subparsers.add_parser("preview-move", help="Preview moving a note")
    move_parser.add_argument("--source-path", required=True)
    move_parser.add_argument("--target-path")
    move_parser.add_argument("--target-folder")
    move_parser.add_argument("--note-id")

    apply_move_parser = subparsers.add_parser("apply-move", help="Move a note file and run validation")
    apply_move_parser.add_argument("--source-path", required=True)
    apply_move_parser.add_argument("--target-path")
    apply_move_parser.add_argument("--target-folder")
    apply_move_parser.add_argument("--note-id")
    apply_move_parser.add_argument("--skip-build", action="store_true")

    archive_parser = subparsers.add_parser("preview-archive", help="Preview archiving a note")
    archive_parser.add_argument("--source-path", required=True)
    archive_parser.add_argument("--note-id")

    hard_delete_parser = subparsers.add_parser("preview-hard-delete", help="Preview hard delete guard")
    hard_delete_parser.add_argument("--source-path", required=True)
    hard_delete_parser.add_argument("--confirmation-token")
    hard_delete_parser.add_argument("--note-id")

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

        if args.command == "preview-create":
            preview = create_note(
                source_path=args.source_path,
                title=args.title,
                description=args.description,
                note_type=args.note_type,
                status=args.status,
                visibility=args.visibility,
                note_id=args.note_id,
                summary_lines=args.summary_lines,
            )
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "apply-create":
            commands = DEFAULT_VALIDATION_COMMANDS[:1] if args.skip_build else DEFAULT_VALIDATION_COMMANDS
            result = apply_create_note(
                source_path=args.source_path,
                title=args.title,
                description=args.description,
                note_type=args.note_type,
                status=args.status,
                visibility=args.visibility,
                note_id=args.note_id,
                summary_lines=args.summary_lines,
                validation_commands=commands,
            )
            print_json(result.to_dict())
            return 0 if result.ok else 1

        if args.command == "preview-rename-title":
            preview = rename_note(
                source_path=args.source_path,
                new_title=args.new_title,
                note_id=args.note_id,
            )
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "apply-rename-title":
            commands = DEFAULT_VALIDATION_COMMANDS[:1] if args.skip_build else DEFAULT_VALIDATION_COMMANDS
            result = apply_rename_title(
                source_path=args.source_path,
                new_title=args.new_title,
                note_id=args.note_id,
                validation_commands=commands,
            )
            print_json(result.to_dict())
            return 0 if result.ok else 1

        if args.command == "preview-rename-path":
            preview = rename_note(
                source_path=args.source_path,
                new_file_name=args.new_file_name,
                target_path=args.target_path,
                note_id=args.note_id,
            )
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "apply-rename-path":
            commands = DEFAULT_VALIDATION_COMMANDS[:1] if args.skip_build else DEFAULT_VALIDATION_COMMANDS
            result = apply_rename_path(
                source_path=args.source_path,
                new_file_name=args.new_file_name,
                target_path=args.target_path,
                note_id=args.note_id,
                validation_commands=commands,
            )
            print_json(result.to_dict())
            return 0 if result.ok else 1

        if args.command == "preview-move":
            preview = move_note(
                source_path=args.source_path,
                target_path=args.target_path,
                target_folder=args.target_folder,
                note_id=args.note_id,
            )
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "apply-move":
            commands = DEFAULT_VALIDATION_COMMANDS[:1] if args.skip_build else DEFAULT_VALIDATION_COMMANDS
            result = apply_move_note(
                source_path=args.source_path,
                target_path=args.target_path,
                target_folder=args.target_folder,
                note_id=args.note_id,
                validation_commands=commands,
            )
            print_json(result.to_dict())
            return 0 if result.ok else 1

        if args.command == "preview-archive":
            preview = archive_note(source_path=args.source_path, note_id=args.note_id)
            print_json(preview.to_dict())
            return 0 if preview.ok else 1

        if args.command == "preview-hard-delete":
            preview = hard_delete_note(
                source_path=args.source_path,
                confirmation_token=args.confirmation_token,
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
