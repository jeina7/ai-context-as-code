# AGENTS.md instructions

<!-- GENERATED FILE. Do not edit directly. -->
<!-- Source: forge/_config/Agents/agent.md + forge/_config/Agents/common.md -->
<!-- Regenerate: python3 scripts/sync_agent_docs.py -->

# Codex Agent Entry

This entry points Codex toward the current ACAC product model.
The repository keeps only minimal source documents after the product direction reset.
Future work should start from the product model and avoid reviving removed scaffold notes.

## Start Here

1. Read the root `README.md`.
2. Read `trove/Projects/ai-context-as-code/Designs/ai-native-context-layer-product-model.md`.
3. Read `trove/Projects/ai-context-as-code/index.md`.
4. Read `forge/_config/index.md`.

## Current Scope

This repository now keeps a minimal source set for the ACAC product direction.
Do not revive removed first-instance, deploy-prep, or legacy reference notes unless the user explicitly asks for that historical material.
Use `scripts/sync_agent_docs.py` after changing files in `forge/_config/Agents/`.

# Common Agent Rules

These rules apply to agents working inside this repository.
The current durable product direction is the AI-native context layer product model.
Keep new work aligned with that model unless the user explicitly changes the product direction.

## Source And Output

- Treat `trove/` as the editable public-safe product and project source layer.
- Treat `forge/` as the editable repo-local agent-facing source layer.
- Treat `data/`, `_build/`, and `dist/` as generated output unless a script explicitly says otherwise.
- Treat `forge/_assets/` as internal asset storage, not a knowledge section.
- Do not create new durable project notes unless they strengthen the new ACAC product model or a requested design spec.

## Safety

- Keep source content public-safe before setting `visibility: public`.
- Do not modify user-level runtime paths such as `~/.codex`, `~/.claude`, MCP config, or hooks from this repository.
- Do not add external runtime integration, MCP, hosted sync, or automatic memory sync unless the user explicitly asks for that implementation step.

## Writing

- Keep frontmatter values that contain natural language in double quotes.
- Keep H1 equal to the `title` frontmatter value.
- Do not create or hand-edit `id`; the build manages it through `data/id-registry.json`.
- Prefer updating the nearest canonical design note over creating parallel notes.
- If a meaningful unit of work changes durable project state, record a concise project worklog entry and Daily pointer.
