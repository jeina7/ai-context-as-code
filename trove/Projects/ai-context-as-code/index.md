---
type: project
title: "AI Context as Code"
description: "ACAC first instance project inside the trove source"
status: active
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: zz2t-H9rM0

---

# AI Context as Code

ACAC starts here as a real first instance rather than a generic framework.
This project folder holds the public-safe source notes for building the cloud-based context system.
The first implementation keeps the structure small, validates markdown source, builds metadata, and serves a read-only static reader.

## Current Scope

- Build the first `trove/` source structure.
- Keep `Daily/`, `Projects/`, and `_config/` clearly separated.
- Treat `_config/Agents/`, `_config/Memory/`, `_config/Skills/`, and `_config/Commands/` as markdown content.
- Generate `data/*.json`, `_build/trove/`, and `dist/` from source.
- Defer Claude Code live connection, MCP, hooks, and automatic memory sync.

## Folder Map

- `Decisions/`: decisions and reasons.
- `Designs/`: architecture and implementation design notes.
- `Worklog/`: detailed project worklog entries.
- `References/`: reusable project references.
- `Research/`: research outputs that are not yet durable rules.

## Migrated Designs

- [[first-instance-frame]]
- [[first-instance-architecture]]
- [[first-implementation-plan]]
- [[first-instance-ui-ux-design]]

## References

- [[legacy-knowledge-base-principles]]
- [[cloudflare-pages-deploy-prep]]

## Decisions

- [[2026-06-29-cloudflare-pages-git-integration]]

## Next Work

- Commit and push the first instance baseline to `origin/main`.
- Connect Cloudflare Pages through Git integration after the pushed baseline is verified.
- Add the first reviewed non-ACAC public-safe note after the deploy route is stable.
