---
title: Why Not Full Obsidian Migration
type: decision
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Why Not Full Obsidian Migration

## Summary

A private vault mixes reusable ideas with sensitive context.
Copying it directly into a publishable system would be unsafe.
The safer path is gradual extraction and rewriting.

## Decision

Do not migrate a private Obsidian vault wholesale. Move only reviewed, generalized, publishable material.

## Why

Raw notes often contain personal, financial, organizational, or relational context. A context layer for AI agents should not depend on accidental exposure of that material.

## Related

- [[publishable-private-context-split]]
- [[why-build-ai-context-as-code]]

