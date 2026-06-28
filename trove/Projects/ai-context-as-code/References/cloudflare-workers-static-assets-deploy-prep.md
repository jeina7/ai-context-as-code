---
type: reference
title: "Cloudflare Workers Static Assets Deploy Prep"
description: "Deployment checklist for the active ACAC Workers static assets deployment"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: CfwAsset01

---

# Cloudflare Workers Static Assets Deploy Prep

This note records the active deploy values for the ACAC Workers static assets deployment.
The first `acac.sh` deployment uses Workers Builds, `wrangler.jsonc`, and generated `dist/` assets.
ACAC uses this as a static assets deployment without adding Worker application code.

## Dashboard Values

Use these values when the Cloudflare form requires a deploy command:

| Item | Value |
|---|---|
| Repository | `jeina7/ai-context-as-code` |
| Production branch | `main` |
| Path | `/` |
| Build command | `python3 scripts/build_trove.py` |
| Deploy command | `npx wrangler deploy` |
| Compatibility date | `2026-06-28` |
| Non-production branch builds | Enabled |
| Non-production deploy command | `npx wrangler versions upload` |

The deploy command depends on the committed `wrangler.jsonc` file.
That file points Workers static assets at `./dist` and enables single-page app fallback handling.
The path value `/` means the repository root.
The compatibility date intentionally uses `2026-06-28` because Cloudflare may validate deploy requests in a timezone where `2026-06-29` is still in the future.
Do not include `dist/_redirects` for Workers static assets.
Workers validates that file differently from Pages, and the Pages rewrite rules can fail as an infinite loop.

## Web Analytics

Prefer Cloudflare dashboard automatic setup for the proxied `acac.sh` hostname.
Keep `ACAC_CF_WEB_ANALYTICS_TOKEN` unset unless ACAC explicitly switches to manual beacon injection.
`data/build.json` reports repo-level injection status:

| Field | Meaning |
|---|---|
| `analytics.enabled: false` | The build did not inject the manual Cloudflare beacon script. |
| `analytics.manualBeacon: false` | `ACAC_CF_WEB_ANALYTICS_TOKEN` was empty during build. |
| `analytics.mode: cloudflare-dashboard-or-disabled` | Analytics must be confirmed in Cloudflare dashboard or by checking served HTML after automatic setup. |

Dashboard path for automatic setup on the active proxied hostname:

1. Web Analytics.
2. Add a site.
3. Select the proxied `acac.sh` hostname.
4. Select Done.
5. Open Manage site and keep automatic setup enabled.

Confirmation criteria:

- `ACAC_CF_WEB_ANALYTICS_TOKEN` remains unset in the Workers build settings.
- A fresh deployment still has no repo-injected `static.cloudflareinsights.com/beacon.min.js` script in `dist/index.html`.
- The served `https://acac.sh/` HTML shows the Cloudflare-injected beacon after automatic setup is active.
- Web Analytics starts showing page views for `/`, `/trove/<id>`, and `/search`.

## Custom Domain

After the first successful deployment, attach `acac.sh` as a Workers custom domain.
Use the dashboard path:

1. Workers & Pages.
2. Select the `ai-context-as-code` Worker.
3. Settings.
4. Domains & Routes.
5. Add.
6. Custom domain.
7. Enter `acac.sh`.

Do not create a separate CNAME for `acac.sh` before adding the custom domain.
Cloudflare custom domains create the needed DNS records and certificates for a hostname in an active Cloudflare zone.

## Local Checks

Run this before pushing changes that Cloudflare will deploy:

```bash
python3 scripts/deploy_check.py
```

That command rebuilds `dist/` and checks that public metadata, markdown payloads, Workers fallback expectations, and JavaScript syntax are ready.

## What This Will Not Do

- It will not add Worker runtime code.
- It will not add Cloudflare KV, D1, R2, Queues, or AI bindings.
- It will not add MCP, hooks, Claude Code live connection, or automatic memory sync.
- It will not create custom domains or DNS records.

## Sources Checked

- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- https://developers.cloudflare.com/workers/static-assets/binding/
- https://developers.cloudflare.com/workers/static-assets/routing/single-page-application/
- https://developers.cloudflare.com/web-analytics/get-started/
- https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/
