---
title: AI Context as Code Design
type: project
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# AI Context as Code Design

## Summary

AI Context as Code is a markdown-first context system for humans and AI agents.
It starts as a publishable personal context layer.
It can later grow into an organizational context system without changing the core source format.

## Design

The system has five layers:

- authoring layer: `notes/` and `conventions/`
- safety layer: `private-staging/`, publish checks, and validation
- build layer: metadata, links, backlinks, search, and generated JSON
- serving layer: static GitHub Pages site
- agent layer: rules, commands, review loops, and future skills

## Boundary

The system is not a direct mirror of a private vault. It only contains reviewed and generalized material that is safe to publish.

## Related

- [[why-build-ai-context-as-code]]
- [[publishable-private-context-split]]
- [[context-engineering]]

