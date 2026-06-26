---
title: Approval Before External Side Effects
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Approval Before External Side Effects

## Summary

Some actions are easy to do and hard to undo.
Publishing, sending messages, spending money, changing permissions, and contacting people should not happen just because an agent can do them.
The system should separate local preparation from external action.

## Pattern

Let agents prepare local artifacts freely inside the agreed workspace.

Require explicit approval before actions that affect the outside world:

- creating or changing a remote repository
- deploying a site
- sending outbound messages
- granting access
- spending money
- deleting durable records

## Application

AI Context as Code can be fully built and reviewed locally. GitHub remote creation and Pages deployment stay approval-gated.

## Related

- [[publishable-import-workflow]]
- [[reviewable-ai-workflows]]
- [[why-markdown-git-github-pages]]
