---
type: agent-entry
title: "Common Agent Rules"
description: "Shared rules for agents working in the ACAC first instance"
status: active
created: 2026-06-28
updated: 2026-06-29
visibility: public
id: vuO9iZrVWu

---

# Common Agent Rules

These rules apply to agents working inside this repository.
The trove and forge source should stay readable by humans and machines.
Generated outputs should be reproducible from source and scripts.
Reusable note-writing and worklog rules live in the trove memory conventions.

## Source And Output

- Treat `trove/` as the editable user-facing context source layer.
- Treat `forge/` as the editable agent-facing and system source layer.
- Treat `data/`, `_build/`, and `dist/` as generated output unless a script explicitly says otherwise.
- Do not create `trove/Home.md`; the root `README.md` and generated home data own the first screen.
- Do not expose `_assets/` in navigation or search as a knowledge section.

## Safety

- Keep seed content public-safe.
- Do not copy private Obsidian notes into this repo without a separate review.
- Do not modify user-level runtime paths such as `~/.codex`, `~/.claude`, MCP config, or hooks from this repository.
- Do not implement live Claude Code connection, MCP, hooks, or automatic memory sync in the first scaffold.

## Writing

- Follow `[[trove-note-convention]]` when creating or editing `trove/**/*.md` or `forge/**/*.md`.
- Follow `[[worklog-note-convention]]` when recording meaningful ACAC work in project worklog notes or Daily pointers.
- Use English for `forge/_config/` source content.
- Use Korean-first content for `trove/Daily/` and `trove/Projects/`.
- Keep frontmatter values that contain natural language in double quotes.
- Keep H1 equal to the `title` frontmatter value.
- Do not create or hand-edit `id`; the build manages it through `data/id-registry.json`.
- Keep `reference`, `research`, `memory`, and `convention` notes current-state oriented.
- Preserve timing and context in `decision`, `design`, `worklog`, and `daily` notes.
- Update the nearest useful index or memory pointer when adding a reusable trove note.
