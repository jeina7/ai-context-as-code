---
type: convention
title: "Trove Note Convention"
description: "Executable writing rules for ACAC source notes"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: Tx8SwdTFoS

---

# Trove Note Convention

This convention keeps `trove/` and `forge/` readable as source, not as generated site output.
It adapts the strongest legacy knowledge-base rules to the ACAC first instance without private infrastructure assumptions.
Use it when creating or editing `trove/**/*.md` or `forge/**/*.md`, then verify with the local trove scripts.

## Scope

- `trove/` is the editable user-facing context source layer.
- `forge/` is the editable agent-facing and system source layer.
- `data/`, `_build/`, and `dist/` are generated outputs unless a script explicitly says otherwise.
- This convention covers markdown notes only; code, static assets, and generated JSON follow their own toolchain.
- `forge/_config/` source content is written in English.
- `trove/Daily/` and `trove/Projects/` content stays Korean-first unless a note has a clear reason to be English.

## Frontmatter

Every markdown note starts with YAML frontmatter.

Required fields:

```yaml
---
type: convention
title: "Example Title"
description: "One-line description for search and summaries"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
---
```

- Keep natural-language values such as `title` and `description` in double quotes.
- Use `status: draft`, `active`, or `archived`.
- Use `visibility: public`, `private`, or `internal`; public builds expose only public notes.
- Do not create or edit `id` manually. The build assigns and preserves it through `data/id-registry.json`.
- If a built note already has `id`, keep it unless the build script updates it.

## Body Shape

- H1 must exactly match the `title` frontmatter value.
- H1 is followed immediately by a 3-5 line summary.
- Start with the durable context: what the note is, why it exists, and what decision or knowledge it preserves.
- Put low-level identifiers, file paths, settings, and command details after the reader has the overall picture.
- Keep one note focused on one topic that a reader or agent can reuse without opening a Daily note first.

## Type Behavior

- `reference`, `research`, `memory`, and `convention` describe the current best understanding. When facts change, rewrite the section naturally instead of appending a change log.
- `decision`, `design`, `worklog`, and `daily` preserve time, constraints, and reasoning from the moment they record.
- `project` and `index` notes are entry points. Keep them short, navigable, and linked to the most useful child notes.
- `agent-entry`, `skill`, and `command` notes are executable operating content for agents. Keep instructions concrete and scoped to this repository.

## Links And Indexes

- Wikilinks use the target file stem, not the H1 text: `[[trove-note-convention]]`.
- Use aliases when the file stem is long: `[[2026-06-29-cloudflare-workers-static-assets-fallback|Workers static assets decision]]`.
- When adding or moving a note, update the nearest useful index or hub note.
- Project `index.md` files should help a new reader enter decisions, designs, references, research, and worklogs in a meaningful order.
- Do not expose `_assets/` as a knowledge section in navigation, search, or index notes.

## Public Safety

- Do not copy private Obsidian originals into this repository without separate review.
- Do not include company-private URLs, credentials, tokens, internal dashboards, or private collaboration threads.
- If a legacy source mentions private infrastructure, rewrite the reusable idea in public-safe terms or leave it out.
- Prefer explaining the ACAC rule over preserving a legacy tool-specific workflow.

## Edit Checklist

Before finishing a source note edit:

- Required frontmatter fields are present.
- Natural-language frontmatter values use double quotes.
- `title` and H1 match exactly.
- H1 has a 3-5 line summary directly below it.
- Wikilinks resolve by file stem or intentional relative path.
- The nearest index or memory pointer is updated when the edit creates a new reusable entry point.
- `python3 scripts/validate_trove.py` passes.

## What This Will Not Do

- It does not import the full private Obsidian vault.
- It does not define live Claude Code, MCP, hook, or automatic memory sync behavior.
- It does not require legacy knowledge-base footers, internal Pages links, or private dashboard references.
- It does not replace the validator; it explains what the source should look like before the validator and build run.
