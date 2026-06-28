---
type: reference
title: "Cloudflare Pages Deploy Prep"
description: "Deployment preparation checklist for publishing the ACAC first instance to Cloudflare"
status: active
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: F0lcG8SXxc

---

# Cloudflare Pages Deploy Prep

This note prepares the ACAC first instance for Cloudflare Pages Git integration deployment.
It records the build settings, local checks, analytics choice, and manual dashboard values needed before touching production.
Actual Cloudflare project creation and custom-domain changes should happen only after explicit approval.
If the dashboard requires a deploy command, use [[cloudflare-workers-static-assets-deploy-prep]] instead.

## Current Deploy Target

| Item | Value |
|---|---|
| Provider | Cloudflare Pages |
| Mode | Git integration |
| Repository | `jeina7/ai-context-as-code` |
| Domain | `acac.sh` |
| Build command | `python3 scripts/build_trove.py` |
| Build output directory | `dist` |
| Workers fallback deploy command | `npx wrangler deploy` |
| Source root | Repository root |
| Pages route fallback | `dist/_redirects` |
| Workers route fallback | `not_found_handling: single-page-application` in `wrangler.jsonc` |
| Local predeploy check | `python3 scripts/deploy_check.py` |

## Local Checks

Run this before any deploy attempt:

```bash
python3 scripts/deploy_check.py
```

That command regenerates root agent docs, rebuilds the trove metadata, checks public output safety, and verifies the reader JavaScript syntax when Node is available.

Manual route checks:

```bash
python3 scripts/serve_dist.py --host 0.0.0.0 --port 4173
```

Then open:

- `http://macmini:4173/`
- `http://macmini:4173/trove/N_TyCBWLFT`
- `http://macmini:4173/search?q=Cloudflare`

## Cloudflare Dashboard Values

Use Git integration.
Cloudflare's Git integration builds on connected repository changes and supports preview deployments for non-production branches.
Direct Upload is not the selected path for this first ACAC instance.
Cloudflare documents that a Git-integrated Pages project cannot later be switched to Direct Upload, and ACAC accepts that tradeoff.

Dashboard setup:

1. Workers & Pages.
2. Create application.
3. Pages.
4. Connect to Git.
5. Select this repository.
6. Set production branch to `main`.
7. Leave framework preset blank or use no framework.
8. Set build command to `python3 scripts/build_trove.py`.
9. Set build output directory to `dist`.
10. Add `ACAC_CF_WEB_ANALYTICS_TOKEN` only if manual beacon injection is chosen.

## Git Push Requirement

Cloudflare Pages can only build source that exists in the connected Git repository.
Before connecting Pages, commit the current baseline and push it to `origin/main`.

```bash
git status --short
python3 scripts/deploy_check.py
git add .
git commit -m "Build ACAC first instance baseline"
git push origin main
```

Do not push if `scripts/deploy_check.py` fails.

## Redirects

Cloudflare Pages reads a plain `_redirects` file from the static output directory.
ACAC previously generated this file inside `dist/`:

```text
/trove/* /index.html 200
/search /index.html 200
```

These rules let direct visits to `/trove/<id>` and `/search` return the static app shell.
Do not use these rules for the Workers static assets deployment.
Workers rejects this `_redirects` file as an infinite loop, so the active Workers path uses `not_found_handling: single-page-application` instead.

## Analytics Choice

There are two possible modes.
Use only one.

| Mode | How it works | ACAC setting |
|---|---|---|
| Cloudflare one-click Web Analytics | Cloudflare injects the beacon on the next deployment | Leave `ACAC_CF_WEB_ANALYTICS_TOKEN` unset |
| Manual token injection | `scripts/build_trove.py` injects the beacon into `dist/index.html` | Set `ACAC_CF_WEB_ANALYTICS_TOKEN` in Pages environment variables |

Cloudflare Web Analytics can measure Single Page Applications through the History API and does not support hash-based routers for that measurement.
ACAC uses real paths like `/trove/<id>`, so this matches the deploy design.

## Sources Checked

- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/configuration/build-configuration/
- https://developers.cloudflare.com/pages/configuration/redirects/
- https://developers.cloudflare.com/pages/how-to/web-analytics/
- https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/

## Not In This Step

- Creating or changing the Cloudflare Pages project.
- Changing DNS or custom domain settings for `acac.sh`.
- Enabling both one-click analytics and manual token injection.
- Adding Cloudflare Pages Functions.
- Using Direct Upload for this first instance.
