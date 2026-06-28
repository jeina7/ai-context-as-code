#!/usr/bin/env python3
"""Build ACAC trove metadata and static site output."""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import string
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import validate_trove


ROOT = Path(__file__).resolve().parents[1]
TROVE_DIR = ROOT / "trove"
DATA_DIR = ROOT / "data"
BUILD_DIR = ROOT / "_build"
PAYLOAD_DIR = BUILD_DIR / "trove"
SITE_DIR = ROOT / "site"
DIST_DIR = ROOT / "dist"
REGISTRY_PATH = DATA_DIR / "id-registry.json"

ID_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase + "_-"
ANALYTICS_ENV = "ACAC_CF_WEB_ANALYTICS_TOKEN"
ANALYTICS_PLACEHOLDER = "<!-- ACAC_ANALYTICS -->"


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def generate_id(used: set[str]) -> str:
    while True:
        note_id = "".join(secrets.choice(ID_ALPHABET) for _ in range(10))
        if note_id not in used:
            used.add(note_id)
            return note_id


def write_frontmatter_id(note: validate_trove.Note, note_id: str) -> None:
    text = note.path.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{note.rel_path}: frontmatter closing marker is missing")

    frontmatter = text[4:end]
    body = text[end:]
    id_line = f"id: {note_id}"

    if re.search(r"^id:\s*.+$", frontmatter, flags=re.MULTILINE):
        frontmatter = re.sub(r"^id:\s*.+$", id_line, frontmatter, flags=re.MULTILINE)
    else:
        frontmatter = frontmatter.rstrip() + f"\n{id_line}\n"

    note.path.write_text(f"---\n{frontmatter}{body}", encoding="utf-8")
    note.frontmatter["id"] = note_id


def load_registry() -> dict[str, Any]:
    registry = read_json(REGISTRY_PATH, {"version": 1, "ids": {}, "paths": {}})
    registry.setdefault("version", 1)
    registry.setdefault("ids", {})
    registry.setdefault("paths", {})
    return registry


def choose_note_ids(notes: list[validate_trove.Note], registry: dict[str, Any]) -> None:
    ids = registry["ids"]
    paths = registry["paths"]
    current_paths = {note.rel_path for note in notes}
    used_ids = set(ids.keys())

    for note in notes:
        rel_path = note.rel_path
        source_id = note.frontmatter.get("id", "")
        registry_id = paths.get(rel_path, "")

        if registry_id and registry_id in ids:
            note_id = registry_id
        elif source_id:
            note_id = source_id
            used_ids.add(note_id)
        else:
            note_id = generate_id(used_ids)

        if note_id in ids:
            previous_path = ids[note_id].get("currentPath")
            if previous_path and previous_path != rel_path:
                if previous_path in current_paths:
                    raise RuntimeError(
                        f"{rel_path}: id {note_id} is already assigned to {previous_path}"
                    )
                previous_paths = ids[note_id].setdefault("previousPaths", [])
                if previous_path not in previous_paths:
                    previous_paths.append(previous_path)

        if source_id != note_id:
            write_frontmatter_id(note, note_id)

        ids[note_id] = {
            "currentPath": rel_path,
            "title": note.frontmatter.get("title", ""),
            "type": note.frontmatter.get("type", ""),
            "visibility": note.frontmatter.get("visibility", ""),
            "created": note.frontmatter.get("created", ""),
            "updated": note.frontmatter.get("updated", ""),
            "route": f"/trove/{note_id}",
            "previousPaths": ids.get(note_id, {}).get("previousPaths", []),
        }
        paths[rel_path] = note_id

    live_ids = {note.frontmatter["id"] for note in notes}
    for path, note_id in list(paths.items()):
        if note_id not in live_ids and path in current_paths:
            del paths[path]


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[#>*\-\s]+", "", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", text).strip()


def note_summary(note: validate_trove.Note) -> str:
    return "\n".join(note.summary_lines)


def public_notes(notes: list[validate_trove.Note]) -> list[validate_trove.Note]:
    return [note for note in notes if note.frontmatter.get("visibility") == "public"]


def note_item(note: validate_trove.Note) -> dict[str, Any]:
    note_id = note.frontmatter["id"]
    layer = layer_for_path(note.rel_path)
    return {
        "id": note_id,
        "route": f"/trove/{note_id}",
        "path": note.rel_path,
        "layer": layer["key"],
        "layerLabel": layer["label"],
        "title": note.frontmatter.get("title", ""),
        "description": note.frontmatter.get("description", ""),
        "type": note.frontmatter.get("type", ""),
        "status": note.frontmatter.get("status", ""),
        "visibility": note.frontmatter.get("visibility", ""),
        "summary": note_summary(note),
        "updated": note.frontmatter.get("updated", ""),
    }


def layer_for_path(path: str) -> dict[str, str]:
    if path.startswith("Daily/"):
        return {"key": "daily", "label": "Daily context"}
    if path.startswith("Projects/"):
        return {"key": "projects", "label": "Project context"}
    if path.startswith("_config/"):
        return {"key": "operating", "label": "Operating layer"}
    if path.startswith("_archived/"):
        return {"key": "archive", "label": "Archive"}
    return {"key": "trove", "label": "Trove"}


def display_folder_name(rel_path: str, raw_name: str) -> str:
    names = {
        "_config": "Operating layer",
        "_archived": "Archive",
        "_config/Agents": "Agent entries",
        "_config/Commands": "Commands",
        "_config/Memory": "Memory",
        "_config/Skills": "Skills",
    }
    if rel_path in names:
        return names[rel_path]
    if raw_name.startswith("_"):
        return raw_name.lstrip("_").replace("-", " ").replace("_", " ").title()
    return raw_name


def resolve_link_target(
    note: validate_trove.Note,
    raw_target: str,
    lookup: dict[str, str],
) -> str | None:
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return None

    normalized = target.removesuffix(".md")
    if normalized in lookup:
        return lookup[normalized]

    if "/" in target:
        candidate = (note.path.parent / target).resolve()
        candidate_md = candidate if candidate.suffix == ".md" else candidate.with_suffix(".md")
        try:
            rel_path = candidate_md.relative_to(TROVE_DIR.resolve()).as_posix()
        except ValueError:
            return None
        return lookup.get(rel_path) or lookup.get(rel_path.removesuffix(".md"))

    return None


def build_link_lookup(notes: list[validate_trove.Note]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for note in notes:
        note_id = note.frontmatter["id"]
        rel_no_ext = note.rel_path.removesuffix(".md")
        lookup[note.path.stem] = note_id
        lookup[rel_no_ext] = note_id
        lookup[note.rel_path] = note_id
        lookup[note.frontmatter.get("title", "")] = note_id
    return {key: value for key, value in lookup.items() if key}


def build_backlinks(notes: list[validate_trove.Note]) -> dict[str, Any]:
    lookup = build_link_lookup(notes)
    by_id = {note.frontmatter["id"]: note_item(note) for note in notes}
    result: dict[str, Any] = {
        note.frontmatter["id"]: {"backlinks": [], "outgoing": []} for note in notes
    }

    for note in notes:
        source_id = note.frontmatter["id"]
        for raw in validate_trove.WIKILINK_PATTERN.findall(validate_trove.without_fenced_code(note.body)):
            target_id = resolve_link_target(note, raw, lookup)
            outgoing = {"raw": raw, "targetId": target_id, "broken": target_id is None}
            if target_id and target_id in by_id:
                outgoing["targetTitle"] = by_id[target_id]["title"]
                result[target_id]["backlinks"].append(
                    {
                        "sourceId": source_id,
                        "sourceTitle": note.frontmatter.get("title", ""),
                        "sourcePath": note.rel_path,
                        "sourceRoute": f"/trove/{source_id}",
                    }
                )
            result[source_id]["outgoing"].append(outgoing)

    return result


def build_tree_node(path: Path, note_by_path: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rel = path.relative_to(TROVE_DIR).as_posix()
    node: dict[str, Any] = {
        "name": path.name,
        "displayName": display_folder_name(rel, path.name),
        "path": rel,
        "kind": "folder",
        "layer": layer_for_path(f"{rel}/")["key"],
        "layerLabel": layer_for_path(f"{rel}/")["label"],
        "children": [],
    }

    index_rel = f"{rel}/index.md" if rel != "." else "index.md"
    if index_rel in note_by_path:
        node["indexNoteId"] = note_by_path[index_rel]["id"]
        node["route"] = note_by_path[index_rel]["route"]
        node["title"] = note_by_path[index_rel]["title"]

    children: list[dict[str, Any]] = []
    for child in sorted(path.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
        if child.name.startswith("."):
            continue
        if child.is_dir():
            if child.name == "_assets":
                continue
            children.append(build_tree_node(child, note_by_path))
        elif child.suffix == ".md" and child.name != "index.md":
            child_rel = child.relative_to(TROVE_DIR).as_posix()
            item = note_by_path.get(child_rel)
            if item:
                children.append(
                    {
                        "name": child.name,
                        "path": child_rel,
                        "kind": "note",
                        "noteId": item["id"],
                        "route": item["route"],
                        "title": item["title"],
                        "type": item["type"],
                        "status": item["status"],
                    }
                )

    node["children"] = children
    return node


def build_tree(notes: list[validate_trove.Note]) -> dict[str, Any]:
    note_by_path = {note.rel_path: note_item(note) for note in notes}
    groups = {"main": ["Daily", "Projects"], "system": ["_config", "_archived"], "hidden": ["_assets"]}
    tree: dict[str, Any] = {**groups, "nodes": {"main": [], "system": []}}

    for group in ("main", "system"):
        for name in groups[group]:
            path = TROVE_DIR / name
            if path.exists():
                tree["nodes"][group].append(build_tree_node(path, note_by_path))

    return tree


def project_key_for_path(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "Projects":
        return parts[1]
    return None


def build_graph(notes: list[validate_trove.Note], backlinks: dict[str, Any]) -> dict[str, Any]:
    items = [note_item(note) for note in notes]
    by_id = {item["id"]: item for item in items}
    by_path = {item["path"]: item for item in items}

    nodes = [
        {
            "id": item["id"],
            "title": item["title"],
            "type": item["type"],
            "status": item["status"],
            "visibility": item["visibility"],
            "path": item["path"],
            "route": item["route"],
            "layer": item["layer"],
            "layerLabel": item["layerLabel"],
            "project": project_key_for_path(item["path"]),
        }
        for item in items
    ]

    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str, str]] = set()

    def add_edge(kind: str, source_id: str, target_id: str, **extra: Any) -> None:
        if source_id == target_id or source_id not in by_id or target_id not in by_id:
            return
        edge_key = (kind, source_id, target_id, str(extra.get("raw", "")))
        if edge_key in seen_edges:
            return
        seen_edges.add(edge_key)
        edges.append(
            {
                "kind": kind,
                "sourceId": source_id,
                "targetId": target_id,
                "sourcePath": by_id[source_id]["path"],
                "targetPath": by_id[target_id]["path"],
                **extra,
            }
        )

    for source_id, links in backlinks.items():
        for outgoing in links.get("outgoing", []):
            target_id = outgoing.get("targetId")
            if target_id:
                add_edge("wikilink", source_id, target_id, raw=outgoing.get("raw", ""))
                add_edge("backlink", target_id, source_id, derivedFrom="wikilink")

    project_indexes = {
        project_key_for_path(item["path"]): item["id"]
        for item in items
        if item["path"].startswith("Projects/") and item["path"].endswith("/index.md")
    }
    for item in items:
        project = project_key_for_path(item["path"])
        index_id = project_indexes.get(project)
        if project and index_id and item["id"] != index_id:
            add_edge("project", index_id, item["id"], project=project)

    for item in items:
        parent = str(Path(item["path"]).parent).replace(".", "")
        while parent:
            index = by_path.get(f"{parent}/index.md")
            if index and index["id"] != item["id"]:
                add_edge("folder", index["id"], item["id"], folderPath=parent)
                break
            next_parent = str(Path(parent).parent).replace(".", "")
            if next_parent == parent:
                break
            parent = next_parent

    layer_counts: dict[str, dict[str, Any]] = {}
    folder_counts: dict[str, int] = {}
    project_counts: dict[str, int] = {}
    for item in items:
        layer = item["layer"]
        layer_counts.setdefault(
            layer,
            {"key": layer, "label": item["layerLabel"], "count": 0},
        )["count"] += 1
        folder = item["path"].split("/")[0]
        folder_counts[folder] = folder_counts.get(folder, 0) + 1
        project = project_key_for_path(item["path"])
        if project:
            project_counts[project] = project_counts.get(project, 0) + 1

    return {
        "version": 1,
        "nodes": nodes,
        "edges": edges,
        "clusters": {
            "layers": sorted(layer_counts.values(), key=lambda item: item["key"]),
            "folders": [
                {"path": path, "count": count}
                for path, count in sorted(folder_counts.items())
            ],
            "projects": [
                {"key": key, "count": count}
                for key, count in sorted(project_counts.items())
            ],
        },
        "contract": {
            "summary": "Read-only static graph data for bounded ACAC relation previews.",
            "nodeId": "Matches note id and /trove/<id> route.",
            "edgeKinds": ["wikilink", "backlink", "folder", "project"],
            "nonGoals": ["full interactive graph", "runtime sync", "live editor"],
        },
    }


def build_search_index(notes: list[validate_trove.Note]) -> list[dict[str, Any]]:
    index = []
    for note in notes:
        body_text = strip_markdown(note.body)
        index.append(
            {
                **note_item(note),
                "filename": note.path.name,
                "snippet": body_text[:360],
                "body": body_text,
            }
        )
    return index


def latest_item(items: list[dict[str, Any]], predicate) -> dict[str, Any] | None:
    candidates = [item for item in items if predicate(item)]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda item: (item.get("updated", ""), item.get("path", "")),
        reverse=True,
    )[0]


def compact_items(items: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        if not item:
            continue
        item_id = item.get("id", "")
        if not item_id or item_id in seen:
            continue
        seen.add(item_id)
        result.append(item)
    return result


def build_home(notes: list[validate_trove.Note]) -> dict[str, Any]:
    note_items = [note_item(note) for note in notes]
    by_path = {item["path"]: item for item in note_items}
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    latest_daily = latest_item(note_items, lambda item: item["path"].startswith("Daily/"))
    latest_design = latest_item(
        note_items,
        lambda item: item["path"].startswith("Projects/ai-context-as-code/Designs/")
        and item["type"] in {"design", "context-design"},
    )
    latest_decision = latest_item(
        note_items,
        lambda item: item["path"].startswith("Projects/ai-context-as-code/Decisions/")
        and item["type"] == "decision",
    )
    latest_worklog = latest_item(
        note_items,
        lambda item: item["path"].startswith("Projects/ai-context-as-code/Worklog/")
        and item["type"] == "worklog",
    )

    start_here = compact_items(
        [
            by_path.get("Projects/ai-context-as-code/index.md"),
            latest_daily,
            latest_design,
            by_path.get("_config/index.md"),
            by_path.get("_config/Memory/MEMORY.md"),
        ]
    )

    return {
        "title": "AI Context as Code",
        "description": "First cloud-based ACAC context instance built from trove markdown source.",
        "readme": readme,
        "startHere": start_here,
        "currentProject": by_path.get("Projects/ai-context-as-code/index.md"),
        "today": latest_daily,
        "recentDaily": latest_daily,
        "latestDesign": latest_design,
        "latestDecision": latest_decision,
        "latestWorklog": latest_worklog,
        "troveLayers": [
            by_path[path]
            for path in ["_config/index.md", "_config/Memory/MEMORY.md"]
            if path in by_path
        ],
    }


def write_payload(notes: list[validate_trove.Note]) -> None:
    if PAYLOAD_DIR.exists():
        shutil.rmtree(PAYLOAD_DIR)
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)

    for note in notes:
        note_id = note.frontmatter["id"]
        (PAYLOAD_DIR / f"{note_id}.md").write_text(note.body, encoding="utf-8")


def copy_site_to_dist(analytics_token: str | None) -> None:
    if not (SITE_DIR / "index.html").exists():
        raise RuntimeError("site/index.html is missing")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    for path in SITE_DIR.rglob("*"):
        if path.is_dir() or path.name == ".gitkeep":
            continue
        rel = path.relative_to(SITE_DIR)
        target = DIST_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.name == "index.html":
            html = path.read_text(encoding="utf-8")
            html = html.replace(ANALYTICS_PLACEHOLDER, analytics_script(analytics_token))
            target.write_text(html, encoding="utf-8")
        else:
            shutil.copy2(path, target)

    shutil.copytree(DATA_DIR, DIST_DIR / "data", ignore=shutil.ignore_patterns(".gitkeep"), dirs_exist_ok=True)
    shutil.copytree(PAYLOAD_DIR, DIST_DIR / "content" / "trove", dirs_exist_ok=True)


def analytics_script(token: str | None) -> str:
    if not token:
        return ""
    payload = json.dumps({"token": token})
    return (
        '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
        f"data-cf-beacon='{payload}'></script>"
    )


def main() -> int:
    report = validate_trove.validate()
    validate_trove.print_report(report)
    if report.errors:
        return 1

    registry = load_registry()
    try:
        choose_note_ids(report.notes, registry)
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return 1

    notes = public_notes(report.notes)
    note_items = [note_item(note) for note in notes]
    analytics_token = os.environ.get(ANALYTICS_ENV)
    built_at = datetime.now(timezone.utc).isoformat()
    backlinks = build_backlinks(notes)

    write_json(REGISTRY_PATH, registry)
    write_json(DATA_DIR / "notes.json", note_items)
    write_json(DATA_DIR / "tree.json", build_tree(notes))
    write_json(DATA_DIR / "search-index.json", build_search_index(notes))
    write_json(DATA_DIR / "backlinks.json", backlinks)
    write_json(DATA_DIR / "graph.json", build_graph(notes, backlinks))
    write_json(DATA_DIR / "home.json", build_home(notes))
    write_json(
        DATA_DIR / "build.json",
        {
            "builtAt": built_at,
            "publicNotes": len(notes),
            "warnings": len(report.warnings),
            "analytics": {
                "enabled": bool(analytics_token),
                "manualBeacon": bool(analytics_token),
                "mode": "manual-beacon" if analytics_token else "cloudflare-dashboard-or-disabled",
                "provider": "cloudflare-web-analytics",
                "source": ANALYTICS_ENV if analytics_token else "cloudflare-dashboard",
            },
        },
    )
    write_payload(notes)
    copy_site_to_dist(analytics_token)

    print(f"Built {len(notes)} public note(s) into dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
