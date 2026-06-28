# AI Context as Code

AI Context as Code, or ACAC, is starting as one real cloud-based context instance.
This repository is the first instance for moving jeina's local Obsidian operating system into a durable markdown source that can be validated, built, searched, and published.
The first goal is not to create a general open-source framework yet.

## Current Scope

This repo begins with a small public-safe scaffold.
`trove/` is the source of durable context, and the future public reader will show generated data from that source.
Claude Code live connection, MCP, hooks, and automatic memory sync are intentionally outside this first scaffold.

## Repository Shape

```text
trove/
  Daily/
  Projects/
  _config/
    Agents/
    Memory/
    Skills/
    Commands/
  _assets/
  _archived/
site/
scripts/
data/
dist/
```

## Important Boundaries

- `trove/` is the source layer people and agents edit.
- `data/` will contain generated metadata for the site.
- `dist/` will contain Cloudflare Pages output and should not be edited by hand.
- `_config/` stores agent-facing markdown content, not user-level runtime configuration.
- `_assets/` is internal storage and is not a knowledge section.

## First Implementation Path

1. Keep the initial `trove/` structure small and public-safe.
2. Seed the ACAC project, daily context, and agent-facing config documents.
3. Generate root `AGENTS.md` and `CLAUDE.md` from `trove/_config/Agents/`.
4. Validate trove notes, build metadata, and assemble the read-only static reader.
5. Migrate the first reviewed public-safe notes, then connect Cloudflare.

## Deploy Prep

Run the local predeploy check before creating or updating a Cloudflare deployment:

```bash
python3 scripts/deploy_check.py
```

The expected build command is `python3 scripts/build_trove.py`, and the output directory is `dist`.
The preferred deployment mode is Cloudflare Pages Git integration from `origin/main`.
If the Cloudflare dashboard requires a Workers Builds deploy command, use the committed `wrangler.jsonc` static assets config and set the deploy command to `npx wrangler deploy`.
