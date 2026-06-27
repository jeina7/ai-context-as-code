---
title: Why Markdown Git and GitHub Pages
type: decision
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Why Markdown Git and GitHub Pages

## Summary

The first version should be inspectable, forkable, and cheap to operate.
Markdown, Git, and GitHub Pages keep the system simple enough to trust.
More complex editing and agent execution layers can come later.

## Decision

Use markdown files as source, Git for history, Python scripts for metadata, and GitHub Pages for static hosting.

## Why

This stack keeps the core knowledge portable. It also makes the first safety boundary simple: if a note is in `notes/`, it is intended to be publishable.

## Related

- [[knowledge-as-code]]
- [[ai-context-as-code-design]]

