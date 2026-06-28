---
title: Implementation Roadmap Review
type: project
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# Implementation Roadmap Review

## Summary

The current product now has a working static context workspace, Korean reading mode, graph views, browser draft editing, modal search, generated search metadata, and recognizable agent config surfaces.

The biggest finished gap was the agent configuration shape.
`AGENTS.md`, `CLAUDE.md`, `skills/`, and `memory/` now exist as real repository surfaces, while `agent-runtime/` remains only a compatibility index.

## Completed In This Pass

- Added root `AGENTS.md`.
- Added root `CLAUDE.md`.
- Added `skills/` with reusable agent procedure candidates.
- Added `memory/` with compact pointers into durable context.
- Improved navbar search into a compact trigger.
- Improved search modal with grouped commands, note snippets, keyboard navigation, empty state, and ranking.
- Added `Interface Design Direction`.
- Reframed agent runtime documentation as agent configuration documentation.
- Connected the command/search modal to generated search metadata.
- Improved browser patch export with section-level review blocks.
- Added graph insight copy that explains the strongest relationship.
- Improved Obsidian import reports with risk level, destination, rewrite checklist, and rewrite prompt.
- Added a viewport QA script for desktop and mobile screenshots.

## Still Worth Building

- Content structure migration from the current topic folders into a clearer product, method, corpus, research, and operations split.
- Safe alias and redirect support before moving existing note slugs.
- Semantic search or embedding-backed search once the static index is no longer enough.
- A richer review queue that groups notes by missing links, stale wording, and translation drift.
- Import reports that can compare several Obsidian candidates and suggest one rewritten note outline.

## Deferred Because It Changes Product Boundaries

- GitHub API commits from the browser.
- Authentication and permission management.
- Organization-level workspaces.
- Full private Obsidian migration.
- Automatic publishing of private-source material.

## Related

- [[acac-sh-design]]
- [[interface-design-direction]]
- [[agent-runtime-references]]
- [[content-structure-plan]]
