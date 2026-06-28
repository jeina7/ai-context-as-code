---
title: Knowledge as Code
type: pattern
status: active
visibility: publishable
created: 2026-06-26
updated: 2026-06-28
---

# Knowledge as Code

## Summary

Knowledge as code treats durable notes like a software project.
Notes live in version control, follow conventions, and pass validation before publishing.
This makes the knowledge easier for humans and agents to reuse.

## Pattern

Use plain files as the source of truth, then generate indexes and views from them.

```text
markdown notes
→ metadata build
→ validation
→ static site
→ agent review
```

## Related

- [[agent-maintained-notes]]
- [[why-build-acac-sh]]
