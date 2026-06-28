# Context Review Skill

Use this when an agent needs to check whether the repository is coherent after note, UI, or convention changes.

## Inputs

- Changed files
- Current `notes/` and `i18n/ko/notes/`
- Generated metadata under `site/_build/`

## Steps

1. Read the changed notes or UI files.
2. Check whether new concepts already exist under `notes/`.
3. Run `python3 scripts/review_context.py`.
4. Inspect review queue changes in `site/_build/dashboard.json`.
5. If user-facing UI changed, verify at least one desktop and one mobile viewport.
6. Record meaningful changes in the project worklog.

## Verification

- `python3 scripts/review_context.py`
- `node --check site/app.js` when JavaScript changed
- `git diff --check`
