---
title: Why Build Process Becomes Context
type: decision
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# Why Build Process Becomes Context

## Summary

The process of building acac.sh should become part of the system itself.
Implementation choices, validation failures, naming decisions, and import rules are reusable context.
If they stay only in chat or private logs, future agents will rediscover the same context repeatedly.

## Decision

Promote useful build history into notes, decisions, conventions, and scripts.

## Why

This project is about context that improves through use. The first proof is whether the project can capture and improve its own context while it is being built.

## Related

- [[self-evolving-context-loop]]
- [[operating-routine]]
- [[2026-06-27-initial-build]]
