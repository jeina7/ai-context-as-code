---
type: convention
title: "Trove Note Convention"
description: "OKF-inspired writing rules for ACAC trove and forge source notes"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: Tx8SwdTFoS

---

# Trove Note Convention

This convention keeps `trove/` and `forge/` readable as durable markdown source.
It adapts the useful parts of the legacy knowledge-base convention into an ACAC-specific OKF profile.[^legacy]
Use this as the single source of truth when creating or editing source notes.

## Must Follow

- Edit source notes under `trove/` or `forge/`; do not hand-edit `data/`, `_build/`, or `dist/`.
- Keep every note public-safe before setting `visibility: public`.
- Use the required OKF frontmatter fields, with `type` first and natural-language values in double quotes.
- Do not create or hand-edit `id`; the build owns `data/id-registry.json`.
- Keep H1 exactly equal to `title`, followed by a 3-5 line summary.
- Write one reusable topic per note.
- Use wikilinks by file stem or intentional relative path, not by H1 text.
- Update the nearest useful index, related notes, and backlinks when adding durable links.
- Use footnotes and public page footers when the note is public and durable.
- Run `python3 scripts/validate_trove.py`; run build/deploy checks when metadata or public output changes.

## Source Boundaries

- `trove/` is the editable user-facing context layer.
- `forge/` is the editable agent-facing and system layer.
- `forge/_config/` source content is English.
- `trove/Daily/` and `trove/Projects/` are Korean-first unless a note has a clear reason to be English.
- Do not copy private Obsidian originals, company-private URLs, credentials, tokens, dashboards, or private collaboration threads into public source.
- Rewrite useful legacy ideas into ACAC terms instead of preserving private tool workflows.

## OKF Profile

Every markdown note starts with this build-facing frontmatter shape.

```yaml
---
type: reference
title: "Example Title"
description: "One-line description for search and summaries"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
---
```

- `status`: `draft`, `active`, or `archived`.
- `visibility`: `public`, `private`, or `internal`.
- `tags`: optional, only for stable domain terms. Avoid broad tags such as `notes`, `docs`, or `general`.
- `ssot: true`: optional, only for `reference`, `research`, `memory`, `principle`, and `convention`.
- Existing `id`: keep it unless the build script updates it.

## Note Types

Use the existing ACAC type set rather than the old `notes/{domain}/{type}` tree.

| Type | Usual location | Behavior |
|---|---|---|
| `project` | `trove/Projects/<project>/index.md` | Project entry point and map. |
| `index` | folder `index.md` | Folder entry point and child-note hub. |
| `daily` | `trove/Daily/YYYY-MM/YYYY-MM-DD.md` | Day-level state and worklog pointers. |
| `worklog` | `trove/Projects/<project>/Worklog/YYYY-MM-DD.md` | Detailed work units with evidence. |
| `decision` | `trove/Projects/<project>/Decisions/YYYY-MM-DD-topic.md` | Decision, reason, tradeoff, follow-up. |
| `design` | `trove/Projects/<project>/Designs/topic.md` | Architecture or implementation design. |
| `reference` | `trove/Projects/<project>/References/topic.md` | Current reusable explanation or guide. |
| `research` | `trove/Projects/<project>/Research/topic.md` | Investigation result and conclusion. |
| `memory` | `forge/_config/Memory/...` | Durable operating context for agents. |
| `principle` | `forge/_config/Memory/Principles/...` | Broad operating principle. |
| `convention` | `forge/_config/Memory/Conventions/...` | Reusable source-writing or operating rule. |
| `context-design` | `forge/_config/Memory/Designs/...` | Design of the context system itself. |
| `agent-entry` | `forge/_config/Agents/...` | Source for generated root agent files. |
| `skill` | `forge/_config/Skills/...` | Repeatable agent workflow. |
| `command` | `forge/_config/Commands/...` | Repeatable command procedure. |

## Evergreen Vs Time-Based

`reference`, `research`, `memory`, `principle`, and `convention` are evergreen.

- Rewrite the body into the current best version when facts change.
- Do not add `Change Log`, `History`, `Latest Update`, or date-stamped patch sections.
- Remove obsolete facts from the main body.
- Keep decision history in `decision` notes, git history, or a short footnote only when it matters.

`decision`, `design`, `worklog`, and `daily` preserve timing and context.

- Do not erase the original constraints or reasoning.
- Add follow-up only when later context changes the status.
- Keep verification evidence near the worklog or decision it supports.

## Naming And Links

File stems are navigation and wikilink targets.

- Prefer descriptive lowercase kebab-case English for public ACAC source paths.
- Use dates for time-based notes: `2026-06-29-cloudflare-workers-static-assets-fallback.md`.
- Avoid opaque labels such as `v1`, `v2`, `final`, `new`, `temp`, or `misc`.
- Avoid duplicate stems unless there is a strong reason.
- H1 must match `title`, not necessarily the file stem.

Wikilink rules:

```markdown
[[trove-note-convention]]
[[2026-06-29-cloudflare-workers-static-assets-fallback|Workers static assets decision]]
```

- Link the first meaningful mention of a related note.
- Use aliases when a dated stem hurts readability.
- Prefer real notes over red-link placeholders in public source.
- Validate links with `python3 scripts/validate_trove.py`.

## Body Structure

Start broad, then move into details.

1. H1 and 3-5 line summary.
2. Short introduction in domain language.
3. Whole flow, architecture, or decision frame.
4. Detailed behavior and implementation notes.
5. Commands, file paths, code references, operations, and verification.
6. Related notes, footnotes, and page footer.

Use prose for context, bullets for actions, tables for comparison, and diagrams only when structure needs a diagram.
Avoid starting with class names, database fields, API paths, command output, or file lists before the reader knows why the note exists.

## Diagrams, Footnotes, Footer

Use Mermaid when visual structure carries information that text would hide.

- Good uses: branching flows, state transitions, sequence handoffs, loops, retries, merges, parallel paths.
- Poor uses: simple linear steps, decorative diagrams, duplicated bullet lists.
- Prefer `flowchart TD` for branching, `flowchart LR` for state transitions, and `sequenceDiagram` for multi-actor handoffs.
- Avoid `stateDiagram-v2` until the public reader renders Mermaid state diagrams reliably.
- Use role/action labels instead of raw endpoint paths.

Use footnotes for sources and small supporting context.

- Good uses: external sources, user constraints, verification notes, public-safe summaries of private evidence.
- Bad uses: empty source placeholders, self-referential convention claims, private URLs, credentials, expiring dashboards, or long explanations.
- Same-repo navigation should be a wikilink, not a footnote.
- Every footnote definition must have a matching marker.

Public durable notes should end with a page footer after footnotes.

```html
---
<sub>Page: <a href="https://acac.sh/trove/{id}">https://acac.sh/trove/{id}</a></sub>
```

- Use `/trove/<id>`, not a source path route.
- Do not invent an `id`; run the build first for new notes.
- Omit this footer for `visibility: private` or `visibility: internal`.

## Indexes And Backlinks

- Project `index.md` files should route readers to decisions, designs, references, research, and worklogs.
- `forge/_config/index.md` should explain the agent-facing source surface.
- Memory indexes should point to focused memory notes instead of duplicating their bodies.
- Add new durable notes to the nearest useful index in reading order.
- Do not expose `_assets/` as a knowledge section.

Use `## Related Notes` near the bottom only when meaningful neighbors exist.
Do not create an empty related-notes section.

When adding a durable wikilink:

- Add a backlink in the target note's `Related Notes` when it helps future navigation.
- Skip backlinks for one-off Daily pointers unless the target note becomes easier to navigate.
- If a new note supersedes or clarifies an older note, update the older note to point forward.

## Before Commit

- Run `python3 scripts/validate_trove.py`.
- Run `python3 scripts/build_trove.py` when IDs, metadata, search, payloads, or public note content change.
- Run `python3 scripts/deploy_check.py` before deploy or after structural changes.
- Review `git status --short` and do not stage unrelated dirty changes.
- Commit source changes and required generated metadata together.
- Use a short imperative commit message.
- Do not add AI-generated signatures or co-author lines.
- Deploy through `origin/main` push or an authenticated Wrangler deploy.

## Related Notes

- [[legacy-knowledge-base-principles]]
- [[worklog-note-convention]]
- [[../MEMORY|ACAC Memory Index]]
- [[../../../../trove/Projects/ai-context-as-code/index|AI Context as Code]]

[^legacy]: This note adapts a private legacy knowledge-base convention. The private source is intentionally not linked from the public ACAC repo.

---
<sub>Page: <a href="https://acac.sh/trove/Tx8SwdTFoS">https://acac.sh/trove/Tx8SwdTFoS</a></sub>
