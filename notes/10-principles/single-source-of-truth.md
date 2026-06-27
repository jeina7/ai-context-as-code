---
title: Single Source of Truth
type: principle
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Single Source of Truth

## Summary

AI agents need a stable place to look before they act.
If important context is scattered across chats, drafts, and memory snippets, every session starts with guesswork.
A context system should make the durable source easy to find, inspect, and update.

## Principle

For any recurring decision or workflow, there should be one durable source that wins when other references disagree.

Memory files, summaries, and generated indexes can speed up lookup. They are not the source itself. The source should be readable by a human, versioned, and connected to the decisions that changed it.

## Application

AI Context as Code treats `notes/`, `conventions/`, and `agents/` as durable source files. Generated JSON exists to serve the site and agents, but it can always be rebuilt from the source.

## Related

- [[knowledge-as-code]]
- [[agent-maintained-notes]]
- [[runtime-verification]]
