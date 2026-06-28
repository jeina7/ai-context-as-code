---
title: Operating Routine
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-28
---

# Operating Routine

## Summary

acac.sh needs a small repeatable routine to stay healthy.
Every meaningful change should move through write, link, validate, build, and review.
This keeps the context layer usable by both humans and agents.

## Routine

For every new note or change:

1. Search existing notes.
2. Write or update the smallest useful note.
3. Add related wikilinks.
4. Run `python3 scripts/review_context.py`.
5. Fix safety, validation, and broken link findings.
6. Commit only after checks pass.

## Weekly Review

Once per week:

- look for duplicate concepts
- improve weak summaries
- check stale decisions
- promote useful worklog entries
- update conventions when mistakes repeat

## Related

- [[self-evolving-context-loop]]
- [[agent-maintained-notes]]
- [[publishable-import-workflow]]

