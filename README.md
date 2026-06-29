# AI Context as Code

AI Context as Code, or ACAC, is a live first instance of context-as-code: a public-safe markdown source that can be validated, built into static metadata, searched, linked, and served as a read-only website.

Live reader: [https://acac.sh](https://acac.sh/)

This repository is intentionally concrete.
It is not a general open-source framework yet.
It is the working reference implementation for moving jeina's local Obsidian operating system into a durable cloud-readable source.

## Current Status

- `acac.sh` is deployed with Cloudflare Workers static assets.
- `trove/` is the editable source layer for public-safe context notes.
- `scripts/build_trove.py` builds JSON metadata, markdown payloads, and static site output from `trove/`.
- The static reader supports the home view, trove navigation, note pages, search, wikilinks, backlinks, and bounded relation previews.
- `scripts/source_write_service.py` provides local-only helpers for future source edits with preview, validation, and rollback behavior.
- Claude Code live connection, MCP, hooks, and automatic memory sync stay outside this first baseline.

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
tests/
data/
_build/
dist/
```

## Source And Output

- `trove/` is the source layer people and agents edit.
- `site/` is the static reader shell.
- `scripts/` contains validation, build, deploy-check, local serving, and source-write helper scripts.
- `tests/` covers local helper behavior that should stay independent from the public reader.
- `data/id-registry.json` is committed so stable `/trove/<id>` routes can survive file moves.
- Other `data/*.json`, `_build/`, and `dist/` are generated output and should not be edited by hand.
- `trove/_assets/` is internal storage and is intentionally hidden from navigation and search.

## Trove Note Rules

Every markdown source note in `trove/` should have:

- required frontmatter fields such as `type`, `title`, `description`, `status`, `created`, `updated`, and `visibility`;
- an H1 that exactly matches the `title` frontmatter value;
- a 3-5 line summary immediately after the H1;
- a stable 10-character `id`, assigned by the build when missing;
- `visibility: public` only when the note is safe for the public site.

Wikilinks are resolved during validation and build.
Possible broken wikilinks are warnings today, not hard failures.

## Local Commands

Validate the trove source:

```bash
python3 scripts/validate_trove.py
```

Build generated metadata, payloads, and `dist/`:

```bash
python3 scripts/build_trove.py
```

Run the full local predeploy check:

```bash
python3 scripts/deploy_check.py
```

Serve the built `dist/` output locally with the same app-shell fallback used by Workers static assets:

```bash
python3 scripts/serve_dist.py --port 4173
```

Regenerate root agent entry files after editing `trove/_config/Agents/`:

```bash
python3 scripts/sync_agent_docs.py
```

## Deployment

The active deployment path is Cloudflare Workers static assets.

- Build command: `python3 scripts/build_trove.py`
- Output directory: `dist`
- Wrangler config: `wrangler.jsonc`
- Deploy command: `npx wrangler deploy`
- Custom domain: [https://acac.sh](https://acac.sh/)

Workers static assets use `not_found_handling: single-page-application`, so `/trove/<id>` and `/search` routes fall back to the app shell.
`dist/_redirects` is intentionally not generated.

For Cloudflare Web Analytics, prefer Cloudflare dashboard automatic setup for the proxied `acac.sh` hostname.
Keep `ACAC_CF_WEB_ANALYTICS_TOKEN` unset unless choosing manual beacon injection, because dashboard injection and build-time injection should not both be enabled.

## Project Documents

- Project index: [trove/Projects/ai-context-as-code/index.md](trove/Projects/ai-context-as-code/index.md)
- Architecture: [trove/Projects/ai-context-as-code/Designs/first-instance-architecture.md](trove/Projects/ai-context-as-code/Designs/first-instance-architecture.md)
- Reader design system: [trove/Projects/ai-context-as-code/Designs/first-instance-reader-design-system.md](trove/Projects/ai-context-as-code/Designs/first-instance-reader-design-system.md)
- Workers deploy prep: [trove/Projects/ai-context-as-code/References/cloudflare-workers-static-assets-deploy-prep.md](trove/Projects/ai-context-as-code/References/cloudflare-workers-static-assets-deploy-prep.md)
