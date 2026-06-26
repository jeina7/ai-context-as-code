#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
REQUIRED = ["title", "type", "status", "visibility", "created", "updated"]
VALID_TYPES = {"principle", "pattern", "research", "decision", "project", "worklog", "reference"}


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def main():
    errors = []
    slugs = set()
    note_texts = []
    for path in sorted(NOTES_DIR.rglob("*.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        note_texts.append((rel, text))
        slug = path.with_suffix("").relative_to(NOTES_DIR).as_posix()
        slugs.add(slug)
        slugs.add(path.stem)
        data = parse_frontmatter(text)
        if data is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        for field in REQUIRED:
            if not data.get(field):
                errors.append(f"{rel}: missing `{field}`")
        if data.get("visibility") != "publishable":
            errors.append(f"{rel}: visibility must be publishable")
        if data.get("type") and data["type"] not in VALID_TYPES:
            errors.append(f"{rel}: invalid type `{data['type']}`")

    for rel, text in note_texts:
        for raw_target in WIKILINK_RE.findall(text):
            target = raw_target.split("|", 1)[0].strip().replace(".md", "")
            if target not in slugs:
                errors.append(f"{rel}: broken wikilink `[[{raw_target}]]`")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()
