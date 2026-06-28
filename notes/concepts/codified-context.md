---
title: Codified Context
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# Codified Context

## Summary

Codified context turns project knowledge, rules, and operating conventions into versioned files.
Agents can then carry context across sessions instead of relying on chat history.
This reduces repeated explanations and makes failures easier to review.

## Pattern

Codified context usually includes:

- durable notes
- conventions
- review rules
- task commands
- validation scripts
- decision records

## Application

In acac.sh, `notes/` stores reusable context, `conventions/` stores operating rules, and `scripts/` verifies whether the context is ready to publish.

## Related

- [[knowledge-as-code]]
- [[context-engineering]]
- [[agent-maintained-notes]]

