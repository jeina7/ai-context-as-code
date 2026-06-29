---
type: index
title: "Forge Source"
description: "Minimal repo-local agent-facing source for ACAC"
status: active
created: 2026-06-28
updated: 2026-06-30
visibility: public
id: FL87bCPt08

---

# Forge Source

Forge is the account-level agent and system source in the ACAC product model.
This repository currently keeps only the minimal Forge source needed for repo-local agent entry generation.
The full future Forge model is described in the ACAC product model note.

## Current Contents

- `Agents/`: source markdown for generated repo-local `AGENTS.md` and `CLAUDE.md`.
- `Memory/`: minimal pointer index for durable ACAC product context.

## Boundary

This repository may generate repo-local `AGENTS.md` and `CLAUDE.md`.
It does not write to user-level Claude Code, Codex, MCP, hook, or runtime config.

## Related Notes

- [[ai-native-context-layer-product-model]]
