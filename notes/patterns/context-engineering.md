---
title: Context Engineering
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Context Engineering

## Summary

Context engineering designs the information environment an AI system uses to make decisions.
It is broader than prompt writing.
It includes source selection, structure, validation, retrieval, update rules, and provenance.

## Pattern

An AI system needs context that is:

- relevant to the task
- sufficient for judgment
- isolated from unrelated noise
- economical enough to fit runtime limits
- traceable to a source
- updatable when reality changes

## Application

AI Context as Code treats markdown notes and conventions as context infrastructure. The goal is to make useful context durable enough for agents to reuse without repeatedly rediscovering it.

## Related

- [[ai-native-expertise]]
- [[codified-context]]
- [[agentic-context-engineering]]

