---
type: agent-entry
title: "Codex Agent Entry"
description: "Repo-local Codex entry generated into AGENTS.md"
status: active
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: 9m41s1bWfU

---

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
