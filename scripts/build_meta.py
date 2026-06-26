#!/usr/bin/env python3
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
DATA_DIR = ROOT / "data"
BUILD_DIR = ROOT / "_build"
SITE_BUILD_DIR = ROOT / "site" / "_build"
REGISTRY_PATH = DATA_DIR / "id-registry.json"
ALIASES_PATH = DATA_DIR / "aliases.json"

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9가-힣]+", "-", value)
    return value.strip("-") or "note"


def load_registry():
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {}


def load_aliases():
    if ALIASES_PATH.exists():
        return json.loads(ALIASES_PATH.read_text(encoding="utf-8"))
    return {}


def save_registry(registry):
    DATA_DIR.mkdir(exist_ok=True)
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.groups()
    frontmatter = {}
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, body


def note_id_for(path, registry):
    rel = path.relative_to(ROOT).as_posix()
    if rel not in registry:
        seed = slugify(path.stem)
        registry[rel] = f"n-{seed}"
    return registry[rel]


def read_notes(registry):
    notes = []
    slug_to_note = {}
    aliases = load_aliases()
    for path in sorted(NOTES_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        rel = path.relative_to(NOTES_DIR).as_posix()
        note_id = note_id_for(path, registry)
        title = frontmatter.get("title") or path.stem.replace("-", " ").title()
        slug = path.with_suffix("").relative_to(NOTES_DIR).as_posix()
        note = {
            "id": note_id,
            "path": rel,
            "slug": slug,
            "title": title,
            "type": frontmatter.get("type", "reference"),
            "status": frontmatter.get("status", "draft"),
            "visibility": frontmatter.get("visibility", "publishable"),
            "created": frontmatter.get("created"),
            "updated": frontmatter.get("updated"),
            "body": body.strip(),
            "links": [],
            "backlinks": [],
        }
        notes.append(note)
        slug_to_note[slug] = note
        slug_to_note[path.stem] = note
        slug_to_note[slugify(title)] = note
        for alias in aliases.get(slug, []):
            slug_to_note[alias] = note
            slug_to_note[slugify(alias)] = note
    return notes, slug_to_note


def resolve_links(notes, slug_to_note):
    backlinks = {note["id"]: [] for note in notes}
    for note in notes:
        links = []
        for raw_target in WIKILINK_RE.findall(note["body"]):
            target = raw_target.split("|", 1)[0].strip()
            key = target.replace(".md", "")
            resolved = slug_to_note.get(key) or slug_to_note.get(slugify(key))
            link = {
                "raw": raw_target,
                "target": target,
                "resolved_id": resolved["id"] if resolved else None,
                "resolved_slug": resolved["slug"] if resolved else None,
                "resolved_title": resolved["title"] if resolved else None,
            }
            links.append(link)
            if resolved:
                backlinks[resolved["id"]].append({
                    "id": note["id"],
                    "slug": note["slug"],
                    "title": note["title"],
                })
        note["links"] = links
    for note in notes:
        note["backlinks"] = backlinks[note["id"]]


def build_tree(notes):
    root = {"name": "notes", "type": "directory", "children": []}
    for note in notes:
        parts = note["path"].split("/")
        current = root
        for part in parts[:-1]:
            child = next(
                (item for item in current["children"] if item["name"] == part and item["type"] == "directory"),
                None,
            )
            if not child:
                child = {"name": part, "type": "directory", "children": []}
                current["children"].append(child)
            current = child
        current["children"].append({
            "name": parts[-1],
            "type": "note",
            "slug": note["slug"],
            "title": note["title"],
        })
    return root


def build_search_index(notes):
    return [
        {
            "id": note["id"],
            "slug": note["slug"],
            "title": note["title"],
            "type": note["type"],
            "text": f"{note['title']} {note['body'][:2000]}",
        }
        for note in notes
    ]


def write_json(name, data):
    BUILD_DIR.mkdir(exist_ok=True)
    (BUILD_DIR / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def mirror_to_site():
    if SITE_BUILD_DIR.exists():
        shutil.rmtree(SITE_BUILD_DIR)
    shutil.copytree(BUILD_DIR, SITE_BUILD_DIR)


def main():
    registry = load_registry()
    notes, slug_to_note = read_notes(registry)
    resolve_links(notes, slug_to_note)
    save_registry(registry)

    broken_links = [
        {"note": note["slug"], "target": link["target"]}
        for note in notes
        for link in note["links"]
        if not link["resolved_id"]
    ]
    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note_count": len(notes),
        "broken_link_count": len(broken_links),
        "broken_links": broken_links,
    }

    write_json("notes.json", notes)
    write_json("tree.json", build_tree(notes))
    write_json("links.json", [
        {"source": note["slug"], "links": note["links"], "backlinks": note["backlinks"]}
        for note in notes
    ])
    write_json("search-index.json", build_search_index(notes))
    write_json("stats.json", stats)
    mirror_to_site()
    print(f"Built {len(notes)} notes with {len(broken_links)} broken links.")


if __name__ == "__main__":
    main()
