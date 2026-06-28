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

The current product now has a working static context workspace, Korean reading mode, graph views, browser draft editing, modal search, and recognizable agent config surfaces.

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

## Still Worth Building

- Content structure migration from the current topic folders into a clearer product, method, corpus, research, and operations split.
- Search ranking backed by a generated index instead of only browser-side scoring.
- Browser editing that can produce structured local patches per note section.
- Graph insights that explain why a connection matters, not just that it exists.
- More systematic mobile QA with real viewport measurements.
- Better import review reports for Obsidian candidates.

## Deferred Because It Changes Product Boundaries

- GitHub API commits from the browser.
- Authentication and permission management.
- Organization-level workspaces.
- Full private Obsidian migration.
- Automatic publishing of private-source material.

## Related

- [[ai-context-as-code-design]]
- [[interface-design-direction]]
- [[agent-runtime-references]]
- [[content-structure-plan]]
