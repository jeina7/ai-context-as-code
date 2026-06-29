# AGENTS.md instructions

<!-- GENERATED FILE. Do not edit directly. -->
<!-- Source: trove/_config/Agents/agent.md + trove/_config/Agents/common.md -->
<!-- Regenerate: python3 scripts/sync_agent_docs.py -->

# Codex Agent Entry

This file is the source for the repository-local `AGENTS.md`.
It should stay small and point agents toward the trove source.
Detailed reusable rules belong in `_config/Memory/`.

## Start Here

1. Read the root `README.md`.
2. Read `trove/Projects/ai-context-as-code/index.md`.
3. Read `trove/_config/Memory/MEMORY.md`.
4. Use `scripts/sync_agent_docs.py` after changing files in `trove/_config/Agents/`.

## Implementation Scope

Build the first ACAC instance in small, verifiable steps.
The current baseline includes scaffold, validation, metadata build, and the read-only static reader.
Keep external runtime integration out of this baseline.

# Common Agent Rules

These rules apply to agents working inside this repository.
The trove source should stay readable by humans and machines.
Generated outputs should be reproducible from source and scripts.
Reusable note-writing rules live in the trove memory convention.

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

- Follow `[[trove-note-convention]]` when creating or editing `trove/**/*.md`.
- Use English for `_config/` source content.
- Use Korean-first content for `Daily/` and `Projects/`.
- Keep frontmatter values that contain natural language in double quotes.
- Keep H1 equal to the `title` frontmatter value.
- Do not create or hand-edit `id`; the build manages it through `data/id-registry.json`.
- Keep `reference`, `research`, `memory`, and `convention` notes current-state oriented.
- Preserve timing and context in `decision`, `design`, `worklog`, and `daily` notes.
- Update the nearest useful index or memory pointer when adding a reusable trove note.
