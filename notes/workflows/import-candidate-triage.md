---
title: Import Candidate Triage
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Import Candidate Triage

## Summary

Not every useful private note should become a publishable note.
Some notes contain private facts, but still point to a reusable idea.
Triage decides whether to skip, rewrite, or promote the idea.

## Triage

Classify each candidate into one of four outcomes:

- skip: the value depends on private details
- extract: rewrite the reusable idea without private details
- merge: add the insight to an existing note
- promote: create a new note because the idea is distinct

The default should be skip or extract. Direct promotion should be rare.

## Application

When scanning an Obsidian vault, AI Context as Code should not copy folders. It should produce a dry-run report, identify reusable patterns, and only write durable notes after rewriting them for the target context.

## Related

- [[publishable-import-workflow]]
- [[publishable-private-context-split]]
- [[approval-before-external-side-effects]]
