# Interface Polish Skill

Use this when an agent changes the static site UI.

## Inputs

- `site/index.html`
- `site/styles.css`
- `site/app.js`
- The current design direction note

## Steps

1. Check whether the change affects desktop, mobile, or both.
2. Keep navbar, content, dashboard, and modal insets aligned.
3. Prefer compact controls over large decorative surfaces.
4. Verify search, navigation, language switching, and graph controls still work.
5. Capture desktop and mobile screenshots when layout changed.
6. Use `scripts/qa_viewports.py` when local Chrome or Chromium is available.

## Verification

- `node --check site/app.js`
- `python3 scripts/review_context.py`
- `python3 scripts/qa_viewports.py`
- `git diff --check`
- Desktop and mobile screenshot review
