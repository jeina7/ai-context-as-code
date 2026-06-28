#!/usr/bin/env python3
"""Check that generated public output is ready for Cloudflare deployment."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"
CONTENT_DIR = DIST_DIR / "content" / "trove"


def read_json(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    notes = read_json(DATA_DIR / "notes.json")
    dist_notes = read_json(DIST_DIR / "data" / "notes.json")
    tree = read_json(DATA_DIR / "tree.json")
    search_index = read_json(DATA_DIR / "search-index.json")
    build = read_json(DATA_DIR / "build.json")
    registry = read_json(DATA_DIR / "id-registry.json")

    if notes != dist_notes:
        fail(errors, "dist/data/notes.json differs from data/notes.json")

    public_ids = {note["id"] for note in notes}
    if len(public_ids) != len(notes):
        fail(errors, "data/notes.json contains duplicate note IDs")

    for note in notes:
        if note.get("visibility") != "public":
            fail(errors, f"non-public note in public metadata: {note.get('path')}")
        if note.get("route") != f"/trove/{note.get('id')}":
            fail(errors, f"route mismatch for {note.get('path')}")
        if "_assets/" in note.get("path", ""):
            fail(errors, f"_assets note leaked into public metadata: {note.get('path')}")

    for item in search_index:
        if item.get("id") not in public_ids:
            fail(errors, f"search item is not public: {item.get('path')}")
        if "_assets/" in item.get("path", ""):
            fail(errors, f"_assets item leaked into search: {item.get('path')}")

    hidden = set(tree.get("hidden", []))
    if "_assets" not in hidden:
        fail(errors, "tree.json does not mark _assets as hidden")
    tree_text = json.dumps(tree, ensure_ascii=False)
    if '"path": "_assets' in tree_text or '"path": "_assets/' in tree_text:
        fail(errors, "_assets appears in rendered tree nodes")

    if not CONTENT_DIR.is_dir():
        fail(errors, "dist/content/trove is missing")
    else:
        payload_ids = {path.stem for path in CONTENT_DIR.glob("*.md")}
        missing_payloads = sorted(public_ids - payload_ids)
        extra_payloads = sorted(payload_ids - public_ids)
        if missing_payloads:
            fail(errors, f"missing markdown payloads: {', '.join(missing_payloads)}")
        if extra_payloads:
            fail(errors, f"unexpected markdown payloads: {', '.join(extra_payloads)}")

    redirects_path = DIST_DIR / "_redirects"
    if redirects_path.exists():
        fail(errors, "dist/_redirects must not be generated for Workers static assets")

    registry_ids = set(registry.get("ids", {}).keys())
    if not public_ids.issubset(registry_ids):
        fail(errors, "some public notes are missing from data/id-registry.json")

    if build.get("publicNotes") != len(notes):
        fail(errors, "data/build.json publicNotes does not match data/notes.json")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"Public payload check failed: {len(errors)} error(s)")
        return 1

    print(f"Public payload check passed: {len(notes)} public note(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
