---
type: agent-entry
title: "Common Agent Rules"
description: "Shared minimal rules for agents working in the ACAC repository"
status: active
created: 2026-06-28
updated: 2026-06-30
visibility: public
id: vuO9iZrVWu

---

# Common Agent Rules

These rules apply to agents working inside this repository.
The current durable product direction is the AI-native context layer product model.
Keep new work aligned with that model unless the user explicitly changes the product direction.

## Source And Output

- Treat `trove/` as the editable public-safe product and project source layer.
- Treat `forge/` as the editable repo-local agent-facing source layer.
- Treat `data/`, `_build/`, and `dist/` as generated output unless a script explicitly says otherwise.
- Treat `forge/_assets/` as internal asset storage, not a knowledge section.
- Do not create new durable project notes unless they strengthen the new ACAC product model or a requested design spec.

## Safety

- Keep source content public-safe before setting `visibility: public`.
- Do not modify user-level runtime paths such as `~/.codex`, `~/.claude`, MCP config, or hooks from this repository.
- Do not add external runtime integration, MCP, hosted sync, or automatic memory sync unless the user explicitly asks for that implementation step.

## Writing

- Keep frontmatter values that contain natural language in double quotes.
- Keep H1 equal to the `title` frontmatter value.
- Do not create or hand-edit `id`; the build manages it through `data/id-registry.json`.
- Prefer updating the nearest canonical design note over creating parallel notes.
- If a meaningful unit of work changes durable project state, record a concise project worklog entry and Daily pointer.
