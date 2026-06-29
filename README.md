# AI Context as Code

AI Context as Code, or ACAC, is an AI-native context layer for agents and makers.
The current public reader is a small deployed surface for the source notes that remain in this repository.
The product direction is now captured in one canonical model note rather than spread across earlier first-instance planning documents.

Live reader: [https://acac.sh](https://acac.sh/)

## Start Here

- Product model: [AI-Native Context Layer Product Model](trove/Projects/ai-context-as-code/Designs/ai-native-context-layer-product-model.md)
- Project index: [trove/Projects/ai-context-as-code/index.md](trove/Projects/ai-context-as-code/index.md)
- Forge index: [forge/_config/index.md](forge/_config/index.md)

## Current Source Shape

```text
trove/
  Daily/
  Projects/
    ai-context-as-code/
      index.md
      Designs/
        ai-native-context-layer-product-model.md
      Worklog/
forge/
  _config/
    Agents/
    Memory/
  _assets/
site/
scripts/
data/
dist/
```

## Source And Output

- `trove/` contains public-safe product and project source notes.
- `forge/` contains repo-local agent-facing source and internal assets.
- `site/` contains the current static reader shell.
- `scripts/` contains validation, build, deploy-check, local serving, and source-write helpers.
- `data/id-registry.json` is committed for stable note identity.
- Other `data/*.json`, `_build/`, and `dist/` are generated output.

## Local Commands

Validate source notes:

```bash
python3 scripts/validate_trove.py
```

Build generated metadata, payloads, and `dist/`:

```bash
python3 scripts/build_trove.py
```

Run the local predeploy check:

```bash
python3 scripts/deploy_check.py
```

Serve the built `dist/` output locally:

```bash
python3 scripts/serve_dist.py --port 4173
```

Regenerate repo-local agent entry files:

```bash
python3 scripts/sync_agent_docs.py
```

## Deployment

The current public reader deploys from `origin/main`.
Push to `main` triggers the hosted build path for `acac.sh`.
