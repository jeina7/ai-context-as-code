---
type: project
title: "AI Context as Code"
description: "ACAC product direction and minimal project source"
status: active
created: 2026-06-28
updated: 2026-06-30
visibility: public
id: zz2t-H9rM0

---

# AI Context as Code

ACAC is now framed as an AI-native context layer for agents and makers.
This project folder keeps only the minimal public-safe source needed to carry the new product direction forward.
Earlier first-instance planning, deploy preparation, and legacy reference notes were removed after the product model was clarified.
Future design notes should branch from the product model instead of reviving the old scaffold documents.

## Canonical Product Model

- [[ai-native-context-layer-product-model]]

## Current Scope

- Keep the product model as the single durable source for ACAC's vocabulary and direction.
- Keep repo-local agent entry sources under `forge/_config/Agents/` only because current scripts generate `AGENTS.md` and `CLAUDE.md` from them.
- Keep detailed future design specs separate and add them only when they become durable.
- Keep generated metadata reproducible through the existing build scripts until the source model is redesigned.

## Next Design Notes

The next useful specs are:

1. Source Store and Sync Model
2. Semantic Write Actions and Ledger Design
3. Context Graph and Relations Schema
4. Desktop App and Web Surface Design
5. Forge and Agent Runtime Sync Design

## Related Notes

- [[ai-native-context-layer-product-model]]
