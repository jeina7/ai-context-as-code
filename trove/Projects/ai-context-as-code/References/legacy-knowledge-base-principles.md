---
type: reference
title: "Legacy Knowledge Base Principles"
description: "Public-safe principles carried from an earlier knowledge base into ACAC"
status: active
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: 9PsNP3egH4

---

# Legacy Knowledge Base Principles

This note records the public-safe principles ACAC keeps from an earlier markdown knowledge base.
It is a sanitized reference, not a raw migration of the previous system.
Internal company names, private URLs, token flows, and editing workflows are intentionally excluded.

## Principles Kept

- File paths should explain document identity enough for humans to browse the source.
- Source markdown and generated output should stay separate.
- Folder `index.md` files should act as readable entry points.
- Every durable note should have frontmatter, an H1, a short summary, and wikilinks when useful.
- Stable public links should use generated IDs instead of raw source paths.
- A static reader is enough for the first ACAC instance.
- Build scripts should stop deployment when source validation fails.

## Principles Changed

- ACAC uses `trove/` instead of a generic `notes/` root.
- ACAC routes public notes through `/trove/<id>`, not hash routes.
- ACAC starts read-only and does not include browser editing in the first implementation.
- ACAC uses `_config/` for agent-facing special contents.
- ACAC treats `_assets/` as hidden internal storage.

## Migration Boundary

The previous knowledge base was designed for a different team and runtime.
Only general source, build, route, validation, and reader principles are carried forward here.
Anything tied to private infrastructure, credentials, or internal collaboration channels stays outside the public trove.
