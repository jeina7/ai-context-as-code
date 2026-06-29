---
type: index
title: "Configuration Contents"
description: "Agent-facing markdown content managed inside the ACAC forge"
status: active
created: 2026-06-28
updated: 2026-06-29
visibility: public
id: FL87bCPt08

---

# Configuration Contents

This folder stores agent-facing markdown content for the ACAC first instance.
It is content inside the forge, not a direct sync target for user-level runtime folders.
The first seed keeps only the smallest reusable rules needed by future agents and build scripts.
Durable writing conventions live under `Memory/Conventions/`.

## Sections

- `Agents/`: source documents for generated root agent entry files.
- `Memory/`: long-term context pointers and durable operating principles.
- `Memory/Conventions/`: reusable rules for writing and maintaining trove source notes.
- `Skills/`: repeatable agent workflows, added only when a workflow becomes stable.
- `Commands/`: repeatable command procedures, added only when they are useful across sessions.

## Boundary

This repository may generate repo-local `AGENTS.md` and `CLAUDE.md`.
It does not automatically write to `~/.codex`, `~/.claude`, MCP config, hooks, or external runtime memory.
