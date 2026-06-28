---
title: Why Build acac.sh
type: decision
status: active
visibility: publishable
created: 2026-06-26
updated: 2026-06-28
---

# Why Build acac.sh

## Summary

Private notes are useful but hard to share safely.
Publishable writing is shareable but often loses the structure needed for reuse.
This project keeps publishable knowledge in a system that agents can search, validate, and improve.

## Decision

Build `acac.sh` instead of publishing a private Obsidian vault.

## Why

Private vaults mix durable ideas with sensitive context. Publishing them directly creates unnecessary risk.

`acac.sh` makes the boundary explicit. Only knowledge that has been reviewed, generalized, and marked publishable enters `notes/`.

## Related

- [[publishable-private-context-split]]
- [[agent-maintained-notes]]
