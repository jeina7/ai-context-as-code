---
title: Agent Maintained Notes
type: pattern
status: active
visibility: publishable
created: 2026-06-26
updated: 2026-06-26
---

# Agent Maintained Notes

## Summary

AI agents can help maintain a knowledge system, but they need rules and review.
The useful loop is not automatic writing alone.
The useful loop is search, propose, verify, and then improve the shared memory.

## Pattern

An agent-maintained note system should:

- search existing notes before writing
- prefer improving existing notes over creating duplicates
- run validation before publishing
- keep sensitive context out of publishable notes
- update conventions when feedback repeats

## Related

- [[knowledge-as-code]]
- [[publishable-private-context-split]]

