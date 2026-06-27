#!/usr/bin/env python3
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
I18N_DIR = ROOT / "i18n"
DATA_DIR = ROOT / "data"
BUILD_DIR = ROOT / "_build"
SITE_BUILD_DIR = ROOT / "site" / "_build"
REGISTRY_PATH = DATA_DIR / "id-registry.json"
ALIASES_PATH = DATA_DIR / "aliases.json"
SECTION_ORDER = {
    "start": 0,
    "principles": 10,
    "concepts": 20,
    "workflows": 30,
    "projects": 40,
    "decisions": 50,
    "research": 60,
    "worklog": 90,
}

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


def prune_registry(registry, notes):
    current_paths = {f"notes/{note['path']}" for note in notes}
    stale_paths = [path for path in registry if path.startswith("notes/") and path not in current_paths]
    for path in stale_paths:
        del registry[path]


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
    sort_tree(root)
    return root


def tree_sort_key(item):
    if item["type"] == "directory":
        return (SECTION_ORDER.get(item["name"], 500), item["name"])
    return (1000, item.get("title") or item["name"])


def sort_tree(node):
    if node["type"] != "directory":
        return
    node["children"].sort(key=tree_sort_key)
    for child in node["children"]:
        sort_tree(child)


def build_search_index(notes):
    return [
        {
            "id": note["id"],
            "slug": note["slug"],
            "title": note["title"],
            "type": note["type"],
            "status": note["status"],
            "updated": note["updated"],
            "text": f"{note['title']} {note['body'][:2000]}",
        }
        for note in notes
    ]


def build_graph(notes):
    nodes = [
        {
            "id": note["slug"],
            "note_id": note["id"],
            "title": note["title"],
            "type": note["type"],
            "status": note["status"],
            "path": note["path"],
            "link_count": len([link for link in note["links"] if link["resolved_slug"]]),
            "backlink_count": len(note["backlinks"]),
        }
        for note in notes
    ]
    edges = []
    seen = set()
    for note in notes:
        for link in note["links"]:
            target = link["resolved_slug"]
            if not target:
                continue
            key = (note["slug"], target)
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                "source": note["slug"],
                "target": target,
                "label": link["target"],
            })
    return {"nodes": nodes, "edges": edges}


def build_report(notes, broken_links):
    orphan_notes = [
        {
            "slug": note["slug"],
            "title": note["title"],
            "type": note["type"],
        }
        for note in notes
        if note["slug"] != "start/overview" and not note["backlinks"]
    ]
    hub_notes = sorted(
        [
            {
                "slug": note["slug"],
                "title": note["title"],
                "type": note["type"],
                "connection_count": len(note["backlinks"]) + len([link for link in note["links"] if link["resolved_slug"]]),
            }
            for note in notes
        ],
        key=lambda item: item["connection_count"],
        reverse=True,
    )[:10]
    stale_notes = [
        {
            "slug": note["slug"],
            "title": note["title"],
            "updated": note["updated"],
        }
        for note in notes
        if not note["updated"]
    ]
    return {
        "orphan_notes": orphan_notes,
        "hub_notes": hub_notes,
        "stale_notes": stale_notes,
        "broken_links": broken_links,
    }


def note_summary(note, limit=220):
    body = re.sub(r"^# .*\n?", "", note["body"]).strip()
    body = re.sub(r"^#{2,6}\s+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[\[([^\]|]+)\|?([^\]]*)\]\]", lambda match: match.group(2) or match.group(1), body)
    body = re.sub(r"\s+", " ", body)
    return body.strip()[:limit]


def load_translation(lang, slug):
    path = I18N_DIR / lang / "notes" / f"{slug}.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    title = frontmatter.get("title")
    if not title:
        heading = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
        title = heading.group(1).strip() if heading else None
    return {
        "title": title,
        "body": body.strip(),
    }


def attach_translations(notes):
    for note in notes:
        translations = {}
        ko = load_translation("ko", note["slug"])
        if ko:
            translations["ko"] = ko
        note["lang"] = "en"
        note["translations"] = translations


def build_dashboard(notes, report):
    recent_notes = sorted(
        notes,
        key=lambda note: (note["updated"] or "", note["created"] or "", note["title"]),
        reverse=True,
    )[:8]
    review_queue = []
    connection_counts = {}
    latest_updated = max((note["updated"] or note["created"] or "") for note in notes)
    for note in notes:
        resolved_links = [link for link in note["links"] if link["resolved_slug"]]
        connection_counts[note["slug"]] = len(note["backlinks"]) + len(resolved_links)
        reasons = []
        if note["status"] != "active":
            reasons.append(f"status: {note['status']}")
        if note["slug"] != "start/overview" and not note["backlinks"]:
            reasons.append("no backlinks")
        if len(resolved_links) == 0 and note["type"] != "worklog":
            reasons.append("no outgoing links")
        if note["type"] != "worklog" and note["slug"] != "start/overview" and connection_counts[note["slug"]] <= 2:
            reasons.append(f"{connection_counts[note['slug']]} graph connections")
        if note["type"] in {"project", "decision"} and connection_counts[note["slug"]] <= 4:
            reasons.append("needs stronger context")
        if note["type"] != "worklog" and note["slug"] != "start/overview" and (note["updated"] or note["created"] or "") == latest_updated:
            reasons.append("recently changed")
        if reasons:
            review_queue.append({
                "slug": note["slug"],
                "title": note["title"],
                "type": note["type"],
                "reasons": reasons,
                "connection_count": connection_counts[note["slug"]],
            })
    review_queue = sorted(
        review_queue,
        key=lambda item: (item["connection_count"], item["type"] == "worklog", item["title"]),
    )
    stage_counts = {}
    for note in notes:
        section = note["path"].split("/", 1)[0]
        stage_counts[section] = stage_counts.get(section, 0) + 1
    return {
        "hero": {
            "title": "Context Dashboard",
            "subtitle": "A working surface for reading, linking, reviewing, and evolving AI-ready context.",
        },
        "recent_notes": [
            {
                "slug": note["slug"],
                "title": note["title"],
                "type": note["type"],
                "updated": note["updated"],
                "summary": note_summary(note, 180),
            }
            for note in recent_notes
        ],
        "hub_notes": report["hub_notes"][:6],
        "review_queue": review_queue[:10],
        "stage_counts": stage_counts,
        "context_health": {
            "notes": len(notes),
            "broken_links": len(report["broken_links"]),
            "orphans": len(report["orphan_notes"]),
            "review_items": len(review_queue),
        },
    }


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
    attach_translations(notes)
    resolve_links(notes, slug_to_note)
    prune_registry(registry, notes)
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
    report = build_report(notes, broken_links)
    write_json("graph.json", build_graph(notes))
    write_json("report.json", report)
    write_json("stats.json", stats)
    write_json("dashboard.json", build_dashboard(notes, report))
    mirror_to_site()
    print(f"Built {len(notes)} notes with {len(broken_links)} broken links.")


if __name__ == "__main__":
    main()
