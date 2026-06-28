---
type: reference
title: "Cloudflare Workers Static Assets Deploy Prep"
description: "Deployment fallback checklist for using Workers Builds with a required deploy command"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: CfwAsset01

---

# Cloudflare Workers Static Assets Deploy Prep

This note records the deploy values to use when the Cloudflare dashboard requires a deploy command.
That screen belongs to Workers Builds rather than the older Pages-only form.
ACAC can use it as a static assets deployment without adding Worker application code.

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

That command rebuilds `dist/` and checks that public metadata, markdown payloads, redirects, and JavaScript syntax are ready.

## What This Will Not Do

- It will not add Worker runtime code.
- It will not add Cloudflare KV, D1, R2, Queues, or AI bindings.
- It will not add MCP, hooks, Claude Code live connection, or automatic memory sync.
- It will not create custom domains or DNS records.

## Sources Checked

- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- https://developers.cloudflare.com/workers/static-assets/binding/
