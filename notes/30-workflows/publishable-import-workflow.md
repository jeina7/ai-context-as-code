---
title: Publishable Import Workflow
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Publishable Import Workflow

## Summary

Private notes should not move directly into a publishable context layer.
They need analysis, risk detection, rewriting, and validation.
The import process is a filter, not a copy operation.

## Workflow

```text
private source
→ dry-run import report
→ risk review
→ rewrite into durable publishable note
→ validate links and frontmatter
→ publishable safety check
→ commit
```

## Rules

- Import reports stay in `private-staging/`.
- Raw private source does not enter `notes/`.
- The rewritten note should preserve the reusable idea, not the private event.
- Safety checks reduce mistakes but do not replace judgment.

## Related

- [[publishable-private-context-split]]
- [[why-not-full-obsidian-migration]]
- [[ai-context-as-code-design]]

