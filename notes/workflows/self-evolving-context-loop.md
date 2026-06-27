---
title: Self-Evolving Context Loop
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Self-Evolving Context Loop

## Summary

A useful context system improves through use.
When an agent or human finds a missing rule, stale note, or repeated correction, the system should update its durable context.
The loop should improve both notes and the rules that create notes.

## Loop

```text
use context
→ find gap
→ propose update
→ validate update
→ commit improved note, rule, or script
```

## Rule

Repeated feedback should not stay as chat history. It should become a convention, validation rule, or durable note.

## Related

- [[agentic-context-engineering]]
- [[agent-maintained-notes]]
- [[context-engineering]]

