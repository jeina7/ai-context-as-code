#!/usr/bin/env python3
"""Validate ACAC trove markdown source files."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TROVE_DIR = ROOT / "trove"
FORGE_DIR = ROOT / "forge"
REGISTRY_PATH = ROOT / "data" / "id-registry.json"
SOURCE_ROOTS = ((TROVE_DIR, ""), (FORGE_DIR, "forge"))

REQUIRED_FIELDS = {
    "type",
    "title",
    "description",
    "status",
    "created",
    "updated",
    "visibility",
}

ALLOWED_TYPES = {
    "agent-entry",
    "command",
    "context-design",
    "convention",
    "daily",
    "decision",
    "design",
    "index",
    "memory",
    "principle",
    "project",
    "reference",
    "research",
    "skill",
    "worklog",
}

ALLOWED_STATUS = {"draft", "active", "archived"}
ALLOWED_VISIBILITY = {"public", "private", "internal"}
ID_PATTERN = re.compile(r"^[0-9A-Za-z_-]{10}$")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)


@dataclass
class Note:
    path: Path
    rel_path: str
    frontmatter: dict[str, str]
    body: str
    h1: str | None
    summary_lines: list[str]


@dataclass
class ValidationReport:
    notes: list[Note]
    errors: list[tuple[str, str]]
    warnings: list[tuple[str, str]]


def source_relative_path(path: Path) -> str | None:
    resolved = path.resolve()
    for source_root, prefix in SOURCE_ROOTS:
        try:
            rel_path = resolved.relative_to(source_root.resolve()).as_posix()
        except ValueError:
            continue
        return f"{prefix}/{rel_path}" if prefix else rel_path
    return None


def rel_trove_path(path: Path) -> str:
    rel_path = source_relative_path(path)
    if rel_path is None:
        raise ValueError(f"{path} is outside source roots")
    return rel_path


def iter_markdown_files() -> list[Path]:
    paths: list[Path] = []
    for source_root, _prefix in SOURCE_ROOTS:
        if source_root.exists():
            paths.extend(source_root.rglob("*.md"))
    return sorted(paths)


def parse_frontmatter(raw: str) -> dict[str, str]:
    frontmatter: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        frontmatter[key.strip()] = value
    return frontmatter


def parse_markdown(path: Path) -> tuple[Note | None, list[str]]:
    rel_path = rel_trove_path(path)
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.startswith("---\n"):
        return None, ["frontmatter is missing"]

    end = text.find("\n---\n", 4)
    if end == -1:
        return None, ["frontmatter closing marker is missing"]

    frontmatter = parse_frontmatter(text[4:end])
    body = text[end + len("\n---\n") :].lstrip("\n")
    h1_match = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    h1 = h1_match.group(1).strip() if h1_match else None
    summary_lines: list[str] = []

    if h1_match:
        after_h1 = body[h1_match.end() :].splitlines()
        for line in after_h1:
            stripped = line.strip()
            if not stripped:
                if summary_lines:
                    break
                continue
            if stripped.startswith("#"):
                break
            summary_lines.append(stripped)

    return Note(path, rel_path, frontmatter, body, h1, summary_lines), errors


def build_note_lookup(notes: list[Note]) -> set[str]:
    lookup: set[str] = set()
    for note in notes:
        rel_no_ext = note.rel_path.removesuffix(".md")
        lookup.add(note.path.stem)
        lookup.add(rel_no_ext)
        lookup.add(note.frontmatter.get("title", ""))
    return {item for item in lookup if item}


def without_fenced_code(text: str) -> str:
    return FENCED_CODE_PATTERN.sub("", text)


def resolve_wikilink_target(note: Note, target: str, lookup: set[str]) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return True

    normalized = target.removesuffix(".md")
    if normalized in lookup:
        return True

    if "/" in target:
        base = note.path.parent
        candidate = (base / target).resolve()
        try:
            rel_path = rel_trove_path(candidate)
        except ValueError:
            return False
        candidate_md = candidate if candidate.suffix == ".md" else candidate.with_suffix(".md")
        rel_md = source_relative_path(candidate_md)
        return rel_path in lookup or (rel_md in lookup if rel_md else False) or candidate_md.exists() or candidate.exists()

    return False


def validate() -> ValidationReport:
    errors: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []
    notes: list[Note] = []
    seen_ids: dict[str, str] = {}

    for path in iter_markdown_files():
        rel_path = rel_trove_path(path)
        if "_assets" in Path(rel_path).parts:
            errors.append((rel_path, "markdown files are not allowed under _assets/"))

        note, parse_errors = parse_markdown(path)
        for message in parse_errors:
            errors.append((rel_path, message))
        if note is None:
            continue

        notes.append(note)
        missing = sorted(REQUIRED_FIELDS - note.frontmatter.keys())
        if missing:
            errors.append((rel_path, f"missing frontmatter fields: {', '.join(missing)}"))

        note_type = note.frontmatter.get("type", "")
        if note_type and note_type not in ALLOWED_TYPES:
            errors.append((rel_path, f"unsupported type: {note_type}"))

        status = note.frontmatter.get("status", "")
        if status and status not in ALLOWED_STATUS:
            errors.append((rel_path, f"unsupported status: {status}"))

        visibility = note.frontmatter.get("visibility", "")
        if visibility and visibility not in ALLOWED_VISIBILITY:
            errors.append((rel_path, f"unsupported visibility: {visibility}"))

        title = note.frontmatter.get("title", "")
        if not note.h1:
            errors.append((rel_path, "H1 is missing"))
        elif title and note.h1 != title:
            errors.append((rel_path, f"title and H1 differ: {title!r} != {note.h1!r}"))

        if not (3 <= len(note.summary_lines) <= 5):
            errors.append((rel_path, "H1 must be followed by a 3-5 line summary"))

        description = note.frontmatter.get("description", "")
        if not description:
            warnings.append((rel_path, "description is empty"))
        elif len(description) > 160:
            warnings.append((rel_path, "description is longer than 160 characters"))

        note_id = note.frontmatter.get("id", "")
        if note_id:
            if not ID_PATTERN.match(note_id):
                errors.append((rel_path, "id must be 10 URL-safe characters"))
            if note_id in seen_ids:
                errors.append((rel_path, f"duplicate id also used by {seen_ids[note_id]}"))
            seen_ids[note_id] = rel_path

    lookup = build_note_lookup(notes)
    for note in notes:
        for match in WIKILINK_PATTERN.findall(without_fenced_code(note.body)):
            if not resolve_wikilink_target(note, match, lookup):
                warnings.append((note.rel_path, f"possible broken wikilink: [[{match}]]"))

    return ValidationReport(notes, errors, warnings)


def print_report(report: ValidationReport) -> None:
    for path, message in report.errors:
        print(f"ERROR {path}: {message}")
    for path, message in report.warnings:
        print(f"WARNING {path}: {message}")

    if report.errors:
        print(f"Validation failed: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    else:
        print(f"Validation passed: {len(report.notes)} note(s), {len(report.warnings)} warning(s)")


def main() -> int:
    report = validate()
    print_report(report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
