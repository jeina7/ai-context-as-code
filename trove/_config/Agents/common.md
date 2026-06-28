---
type: agent-entry
title: "Common Agent Rules"
description: "Shared rules for agents working in the ACAC first instance"
status: active
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: vuO9iZrVWu

---

# Common Agent Rules

These rules apply to agents working inside this repository.
The trove source should stay readable by humans and machines.
Generated outputs should be reproducible from source and scripts.

## Source And Output

- Treat `trove/` as the editable source layer.
- Treat `data/`, `_build/`, and `dist/` as generated output unless a script explicitly says otherwise.
- Do not create `trove/Home.md`; the root `README.md` and generated home data own the first screen.
- Do not expose `_assets/` in navigation or search as a knowledge section.

## Safety

- Keep seed content public-safe.
- Do not copy private Obsidian notes into this repo without a separate review.
- Do not modify user-level runtime paths such as `~/.codex`, `~/.claude`, MCP config, or hooks from this repository.
- Do not implement live Claude Code connection, MCP, hooks, or automatic memory sync in the first scaffold.

## Writing

- Use English for `_config/` source content.
- Use Korean-first content for `Daily/` and `Projects/`.
- Keep frontmatter values that contain natural language in double quotes.
- Keep H1 equal to the `title` frontmatter value.
