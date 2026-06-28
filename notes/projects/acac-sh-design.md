---
title: acac.sh Design
type: project
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# acac.sh Design

## Summary

`acac.sh` is a markdown-first context system for humans and AI agents.
It starts as a product repo with its own development context as the first working corpus.
It can later grow into an organizational context system without changing the core source format.

## Design

The system has five layers:

- authoring layer: `notes/` and `conventions/`
- safety layer: `private-staging/`, publish checks, and validation
- build layer: metadata, links, backlinks, search, and generated JSON
- serving layer: static GitHub Pages site published at `acac.sh`
- agent configuration layer: familiar agent surfaces such as rules, commands, skills, memory pointers, and future `AGENTS.md` or `CLAUDE.md` entries

## Boundary

The repository should not look like a private vault that happened to have a UI.
It should look like a product whose first dataset is its own reviewed context and whose public surface is `acac.sh`.

That means product code, product decisions, and example context can live together, but they need distinct roles:

- product code proves the system can be used
- product decisions explain why the system exists
- context corpus shows how the system captures useful knowledge over time
- agent configuration shows what agents can read directly without inventing a custom runtime

The corpus is not a full mirror of a private vault. It only contains reviewed and generalized material that can stand without private source context.

## Related

- [[why-build-acac-sh]]
- [[agent-runtime-references]]
- [[implementation-roadmap-review]]
- [[publishable-private-context-split]]
- [[context-engineering]]
