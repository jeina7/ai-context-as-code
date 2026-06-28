---
type: decision
title: "Cloudflare Pages Git Integration"
description: "Decision to deploy the ACAC first instance through Cloudflare Pages Git integration"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: X_Vwcz2ZL1

---

# Cloudflare Pages Git Integration

ACAC will use Cloudflare Pages Git integration for the first public deployment path.
This keeps deployment tied to repository history and supports preview deployments for non-production branches.
Direct Upload is not the selected path for this first instance.

## Decision

Use Cloudflare Pages Git integration.

## Reason

- ACAC source lives in this repository, and the build can be reproduced with `python3 scripts/build_trove.py`.
- Git integration deploys from repository changes, so the public site can track committed source.
- Preview deployments can be used before the production branch is promoted.
- The deploy output is deterministic and already generated from `trove/` into `dist/`.

## Accepted Tradeoff

Cloudflare documents that a project created with Git integration cannot later be switched to Direct Upload.
That tradeoff is acceptable for this first instance because ACAC should use Git history as its source of operational truth.

## Deployment Values

| Item | Value |
|---|---|
| Provider | Cloudflare Pages |
| Mode | Git integration |
| Repository | `jeina7/ai-context-as-code` |
| Production branch | `main` |
| Build command | `python3 scripts/build_trove.py` |
| Build output directory | `dist` |
| Domain | `acac.sh` |

## Follow-up

- Run `python3 scripts/deploy_check.py` before connecting or updating the Pages project.
- Keep `ACAC_CF_WEB_ANALYTICS_TOKEN` unset if Cloudflare one-click Web Analytics is enabled.
- Add the custom domain only after the first preview or production deployment is verified.
