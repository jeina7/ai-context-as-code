---
type: memory
title: "ACAC Memory Index"
description: "Minimal pointer index for durable ACAC product context"
status: active
created: 2026-06-28
updated: 2026-06-30
visibility: public
id: qskThSYA1P

---

# ACAC Memory Index

This file is the minimal memory pointer for agents working in this repository.
The current durable source of product direction is the AI-native context layer product model.
Older first-instance conventions and scaffold notes were removed to keep future work aligned with the new product direction.

## Current Pointers

- [[ai-native-context-layer-product-model]] is the canonical product model.
- [[../Agents/common|Common Agent Rules]] defines the minimal repo-local source/output boundary.
- [[../Agents/agent|Codex Agent Entry]] and [[../Agents/claude|Claude Agent Entry]] generate root runtime entry files for this repository only.

## Promotion Rule

Do not add new Forge memory notes until a rule is stable enough to guide multiple future ACAC sessions.
Prefer adding detailed product design to `trove/Projects/ai-context-as-code/Designs/` first.
