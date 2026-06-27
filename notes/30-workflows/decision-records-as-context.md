---
title: Decision Records as Context
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Decision Records as Context

## Summary

Decisions are not just history.
They are context that prevents future agents from reopening the same question without evidence.
A useful decision record explains the choice, rejected alternatives, and the reason the choice made sense at the time.

## Pattern

Write a decision note when a choice changes the shape of the system.

The note should answer:

- What changed?
- Why this option?
- What did we intentionally not do?
- What should a future agent check before changing it?

## Application

This repo uses `notes/50-decisions/` for durable project choices such as naming, local-first implementation, GitHub Pages, and why the build process itself becomes context.

## Related

- [[why-context-as-code]]
- [[why-build-process-becomes-context]]
- [[reviewable-ai-workflows]]
