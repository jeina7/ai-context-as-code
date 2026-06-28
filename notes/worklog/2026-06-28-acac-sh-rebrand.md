---
title: acac.sh Rebrand and Domain Setup
type: worklog
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# acac.sh Rebrand and Domain Setup

## Summary

The product moved from the descriptive name `AI Context as Code` to the public product name `acac.sh`.
The site chrome, README, active product notes, decision notes, runtime pointers, and QA checks now use `acac.sh`.
GitHub Pages is configured for the `acac.sh` custom domain, but live DNS still depends on registering the domain and adding records.

## Completed

- Set the GitHub Pages custom domain to `acac.sh`.
- Added `site/CNAME`.
- Changed the visible site brand, browser title, and dashboard product label to `acac.sh`.
- Renamed the core design and decision notes to `acac-sh-design`, `why-build-acac-sh`, and `why-acac-sh`.
- Updated English source notes and Korean reading copies to use `acac.sh` as the product name.
- Kept old slugs in `data/aliases.json` so old source references can still resolve during builds.

## Verification

- `python3 scripts/check_publish_safety.py`
- `python3 scripts/validate_notes.py`
- `python3 scripts/build_meta.py`
- `python3 scripts/review_context.py`
- `node --check site/app.js`
- `python3 scripts/qa_viewports.py`

## Remaining External Step

Register `acac.sh`, then point DNS to GitHub Pages.

## Related

- [[why-acac-sh]]
- [[acac-sh-design]]
- [[why-markdown-git-github-pages]]
