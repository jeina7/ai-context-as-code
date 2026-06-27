---
title: AI Context as Code Design
type: project
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# AI Context as Code Design

## Summary

AI Context as Code is a markdown-first context system for humans and AI agents.
It starts as a product repo with its own development context as the first working corpus.
It can later grow into an organizational context system without changing the core source format.

## Design

The system has five layers:

- authoring layer: `notes/` and `conventions/`
- safety layer: `private-staging/`, publish checks, and validation
- build layer: metadata, links, backlinks, search, and generated JSON
- serving layer: static GitHub Pages site
- agent runtime layer: symlinked rules, commands, review loops, and future skills or memory references

## Boundary

The repository should not look like a private vault that happened to have a UI.
It should look like a product whose first dataset is its own reviewed context.

That means product code, product decisions, and example context can live together, but they need distinct roles:

- product code proves the system can be used
- product decisions explain why the system exists
- context corpus shows how the system captures useful knowledge over time
- agent runtime shows what agents can read directly while operating

The corpus is not a full mirror of a private vault. It only contains reviewed and generalized material that can stand without private source context.

## Related

- [[why-build-ai-context-as-code]]
- [[agent-runtime-references]]
- [[publishable-private-context-split]]
- [[context-engineering]]
