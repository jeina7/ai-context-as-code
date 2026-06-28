---
type: decision
title: "Cloudflare Workers Static Assets Fallback"
description: "Decision to support the Workers Builds deploy-command flow when Cloudflare Pages is not the active dashboard path"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: CfwBuildA1

---

# Cloudflare Workers Static Assets Fallback

ACAC still prefers a Git-connected Cloudflare deployment from `origin/main`.
The Cloudflare dashboard can route repository import through Workers Builds, where a deploy command is required.
ACAC supports that path with a minimal static assets Wrangler configuration.

## Decision

Support Cloudflare Workers Builds as the deploy-command fallback for the first public deployment.
Keep the output source unchanged: `python3 scripts/build_trove.py` builds `dist/`, and Wrangler deploys those static assets.
Do not add Worker application logic in this step.

## Reason

- The current Cloudflare UI may require a deploy command when importing a Git repository.
- Workers static assets can serve the same generated `dist/` output.
- A committed `wrangler.jsonc` makes the deployment reproducible from repository source.
- This keeps the first deployment unblocked without introducing MCP, hooks, Claude Code live connection, or automatic memory sync.

## Deployment Values

| Item | Value |
|---|---|
| Provider | Cloudflare Workers |
| Mode | Workers Builds Git integration |
| Repository | `jeina7/ai-context-as-code` |
| Production branch | `main` |
| Build command | `python3 scripts/build_trove.py` |
| Deploy command | `npx wrangler deploy` |
| Static assets directory | `./dist` in `wrangler.jsonc` |
| Compatibility date | `2026-06-28` |
| Path | `/` |
| Non-production branch builds | Enabled |
| Non-production branch deploy command | `npx wrangler versions upload` |

## Accepted Tradeoff

This fallback no longer uses Cloudflare Pages route handling as the primary deploy surface.
The repo does not generate `_redirects` for this Workers deployment because Workers static assets use the explicit `not_found_handling` setting in `wrangler.jsonc`.
The first deployment remains static-only and public-safe.
Non-production branches can create preview versions, but `main` remains the production branch.
The compatibility date stays one calendar day behind the KST project date to avoid timezone-based deploy failures.

## Follow-up

- Run `python3 scripts/deploy_check.py` before pushing deploy config changes.
- Verify direct routes such as `/trove/<id>` after the Cloudflare deployment completes.
- Revisit whether the durable deploy target should stay Workers static assets or move back to Pages after the first live URL is verified.
