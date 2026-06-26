---
title: Reviewable AI Workflows
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Reviewable AI Workflows

## Summary

AI output becomes more useful when it leaves evidence behind.
A reviewable workflow shows the sources used, the checks run, and the decision that followed.
This makes AI work easier to trust, correct, and reuse.

## Pattern

Design AI workflows so that each meaningful change has:

- input context
- generated output
- validation result
- human decision when needed
- durable record

The record does not need to be long. It needs enough detail for the next reader to understand what changed and why.

## Application

For this project, a reviewable AI workflow means an agent should update notes through explicit files, run `scripts/review_context.py`, and leave a worklog when the change is meaningful.

## Related

- [[ai-native-expertise]]
- [[self-evolving-context-loop]]
- [[decision-records-as-context]]
