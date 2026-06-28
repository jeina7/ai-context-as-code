---
title: Context Harness Boundary
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# Context Harness Boundary

## Summary

A context layer and an agent harness are related but not identical.
The context layer stores durable knowledge and rules.
The harness wraps an agent with tools, permissions, observations, verification, and execution state.

## Boundary

acac.sh starts as a context layer.

It becomes a harness only when it also manages:

- tool access
- task state
- execution traces
- verification reports
- permission boundaries
- intervention records
- commit or pull request workflows

## Implication

Do not add harness features before the context source is trustworthy. A weak context layer makes the execution layer harder to debug.

## Related

- [[context-engineering]]
- [[agentic-context-engineering]]
- [[acac-sh-design]]

