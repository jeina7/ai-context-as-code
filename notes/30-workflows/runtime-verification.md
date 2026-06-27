---
title: Runtime Verification
type: pattern
status: active
visibility: publishable
created: 2026-06-27
updated: 2026-06-27
---

# Runtime Verification

## Summary

A workflow is not proven by a script existing.
It is proven when the script runs in the environment where it matters and the result is checked.
AI-maintained systems need verification that is close to real use.

## Pattern

After changing an automated or generated system, verify three layers:

- source checks pass
- generated artifacts are rebuilt
- the user-facing path can load the result

For a static knowledge system, this means validating notes, rebuilding metadata, and opening the site enough to confirm that navigation and status are not broken.

## Application

`scripts/review_context.py` is the local runtime verification entrypoint for this repo. It runs safety checks, note validation, and metadata build in one command.

## Related

- [[reviewable-ai-workflows]]
- [[single-source-of-truth]]
- [[operating-routine]]
