---
title: Agentic Context Engineering
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Agentic Context Engineering

## Summary

Agentic context engineering treats context as something that improves through use.
Agents do not only consume context.
They help propose updates to notes, rules, and validation based on execution feedback.

## Pattern

A self-improving context loop has four steps:

1. Use existing context to answer or act.
2. Notice missing, stale, duplicated, or unsafe context.
3. Propose a targeted update.
4. Validate and commit the improved context.

## Application

AI Context as Code should make agent updates explicit and reviewable. The system should improve notes and conventions without silently copying private source material.

## Related

- [[agent-maintained-notes]]
- [[context-engineering]]
- [[publishable-private-context-split]]

