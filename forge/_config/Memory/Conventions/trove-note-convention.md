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
It adapts the legacy knowledge-base note rules into an ACAC-specific OKF profile without private infrastructure assumptions.[^legacy]
Use it when creating or editing `trove/**/*.md` or `forge/**/*.md`, then verify the result with the local trove scripts.

## Scope

- `trove/` is the editable user-facing context source layer.
- `forge/` is the editable agent-facing and system source layer.
- `data/`, `_build/`, and `dist/` are generated outputs unless a script explicitly says otherwise.
- `forge/_config/` source content is written in English.
- `trove/Daily/` and `trove/Projects/` content stays Korean-first unless a note has a clear reason to be English.
- Do not import private Obsidian originals, company-private URLs, credentials, tokens, dashboards, or private collaboration threads into public source.

## Quality Bar

ACAC source notes should read like chapters in a small operating manual, not like loose scratch notes.

- Each note answers one reusable question.
- Each folder index is an entry point, not a dump of links.
- A reader should understand the topic from the summary and first sections before meeting low-level paths, classes, settings, or commands.
- Durable notes should be understandable six months later without opening a Daily note first.
- Public notes should be safe to publish as-is.

## OKF Profile

ACAC uses an OKF-inspired document model with stricter build-facing fields.
Every markdown note starts with YAML frontmatter.

Required fields:

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

- Put `type` first.
- Keep natural-language values such as `title` and `description` in double quotes.
- Use `status: draft`, `active`, or `archived`.
- Use `visibility: public`, `private`, or `internal`; public builds expose only public notes.
- Do not create or edit `id` manually. The build assigns and preserves it through `data/id-registry.json`.
- If a built note already has `id`, keep it unless the build script updates it.
- Optional `tags` may be added only when they are stable domain terms. Do not add broad tags such as `notes`, `docs`, `system`, or `general`.
- Optional `ssot: true` is allowed only for `reference`, `research`, `memory`, and `convention` notes that are intended to be the current source of truth.

## Note Types

Use the existing ACAC type set rather than copying the old domain/type tree literally.

| Type | Usual location | Behavior |
|---|---|---|
| `project` | `trove/Projects/<project>/index.md` | Project entry point and map. |
| `index` | folder `index.md` | Folder entry point and child-note hub. |
| `daily` | `trove/Daily/YYYY-MM/YYYY-MM-DD.md` | Day-level state and pointers. Preserve timing. |
| `worklog` | `trove/Projects/<project>/Worklog/YYYY-MM-DD.md` | Detailed work units. Preserve timing and evidence. |
| `decision` | `trove/Projects/<project>/Decisions/YYYY-MM-DD-topic.md` | Decision, reason, tradeoff, follow-up. Preserve context. |
| `design` | `trove/Projects/<project>/Designs/topic.md` | Architecture or implementation design. Preserve the design frame and constraints. |
| `reference` | `trove/Projects/<project>/References/topic.md` | Current reusable explanation or guide. Rewrite into the current best version. |
| `research` | `trove/Projects/<project>/Research/topic.md` | Investigation output from multiple sources. Rewrite when the conclusion changes. |
| `memory` | `forge/_config/Memory/...` | Durable operating context for agents. Rewrite as the current best rule. |
| `convention` | `forge/_config/Memory/Conventions/...` | Reusable source-writing or operating convention. Rewrite as the current rule. |
| `principle` | `forge/_config/Memory/Principles/...` | Broad operating principle. Rewrite as the current rule. |
| `context-design` | `forge/_config/Memory/Designs/...` | Design of the context system itself. Preserve the design frame. |
| `agent-entry` | `forge/_config/Agents/...` | Source for generated root agent entry files. Keep executable and scoped. |
| `skill` | `forge/_config/Skills/...` | Repeatable agent workflow. Keep concrete and trigger-based. |
| `command` | `forge/_config/Commands/...` | Repeatable command procedure. Keep runnable and verifiable. |

## Evergreen And Time-Based Notes

`reference`, `research`, `memory`, `principle`, and `convention` describe the current best understanding.

- Rewrite the section naturally when facts change.
- Do not append `Change Log`, `History`, `Latest Update`, or date-stamped patch sections.
- Remove obsolete facts from the main body.
- Keep decision history in `decision` notes, git history, or a short footnote when the context matters.

`decision`, `design`, `worklog`, and `daily` preserve time, constraints, and reasoning from the moment they record.

- Do not rewrite away the original decision context.
- Add follow-up sections only when later context changes the status.
- Keep verification evidence close to the worklog or decision it supports.

## File Names

The file stem is the wikilink target and should be stable.
The H1 must match `title`, not necessarily the file name.

- Use descriptive, durable slugs.
- Prefer lowercase kebab-case English for public ACAC source paths: `cloudflare-workers-static-assets-deploy-prep.md`.
- Use dates when the note is time-based: `2026-06-29-cloudflare-workers-static-assets-fallback.md`.
- Do not use opaque labels such as `v1`, `v2`, `final`, `new`, `temp`, or `misc`.
- Do not create duplicate stems in different folders unless there is a strong reason; stem-only wikilinks become ambiguous for humans.

Type-specific patterns:

| Type | Filename pattern |
|---|---|
| `daily` | `YYYY-MM-DD.md` under `trove/Daily/YYYY-MM/` |
| `worklog` | `YYYY-MM-DD.md` under the project `Worklog/` folder |
| `decision` | `YYYY-MM-DD-short-topic.md` |
| `design` | `short-topic-design.md` or a clear existing project slug |
| `reference` | `short-topic.md` |
| `research` | `short-topic-research.md` when the research nature is not obvious |
| `memory`, `principle`, `convention`, `context-design` | concise kebab-case under the matching `forge/_config/Memory/` subfolder |
| `agent-entry`, `skill`, `command` | stable executable names used by scripts or agents |

## Body Shape

- H1 must exactly match the `title` frontmatter value.
- H1 is followed immediately by a 3-5 line summary.
- The summary should say what the note is, why it matters, and what the current conclusion or preserved context is.
- Start with the durable context before implementation details.
- Put low-level identifiers, paths, settings, commands, and code references after the reader has the overall picture.
- Use prose for context, bullets for lists and actions, tables for comparisons, and diagrams only when structure needs a diagram.

## Progressive Disclosure

Technical notes move from broad context to details.

Recommended order:

1. H1 and 3-5 line summary.
2. Short introduction in domain language.
3. Whole flow, architecture, or decision frame.
4. Detailed behavior and implementation notes.
5. Commands, file paths, code references, operations, and verification.
6. Related notes, footnotes, and page footer.

Avoid these patterns:

- Starting with class names, database fields, API paths, or command output before the reader knows why the note exists.
- Listing endpoints or files without a flow.
- Mixing unrelated topics because they happened in the same session.
- Adding a time-based update section to an evergreen note.

## Mermaid

Use Mermaid when visual structure carries information that prose or a table would hide.

Use Mermaid for:

- Branching flows.
- State transitions.
- Sequence or handoff between systems.
- Loops, retries, merges, or parallel paths.
- Two modes whose control flow differs.

Do not use Mermaid for:

- A simple linear sequence that fits in a numbered list.
- Decorative diagrams.
- A diagram that repeats the same information as the surrounding bullet list.

Rules:

- Prefer `flowchart TD` for branching and `flowchart LR` for state transitions.
- Prefer `sequenceDiagram` for multi-actor handoffs.
- Avoid `stateDiagram-v2` until the public reader renders Mermaid state diagrams reliably.
- Labels should describe roles and actions, not raw endpoint paths.
- If a Mermaid diagram is important to understanding the note, verify the public reader output before sharing.

## Wikilinks

Wikilinks use the target file stem, not the H1 text.

```markdown
[[trove-note-convention]]
[[2026-06-29-cloudflare-workers-static-assets-fallback|Workers static assets decision]]
```

Rules:

- Link the first meaningful mention of a related note.
- Use aliases when a dated stem would make the sentence hard to read.
- Prefer a real note over a red-link placeholder in public source.
- When a link intentionally points to a not-yet-created note, mention that the target is planned.
- Check links with `python3 scripts/validate_trove.py`; possible broken wikilinks should be resolved before committing.

## Indexes

Every important folder should have an entry point when it contains more than incidental files.

- Project `index.md` files should introduce the project and route readers to decisions, designs, references, research, and worklogs.
- `forge/_config/index.md` should explain the agent-facing source surface.
- Memory indexes should point to focused memory notes rather than duplicating their full bodies.
- Add new notes to the nearest useful index or hub in a reading order that helps a new reader.
- Do not expose `_assets/` as a knowledge section in navigation, search, or index notes.

## Related Notes

Use `## Related Notes` near the bottom of durable notes when meaningful neighbors exist.
Place it before footnotes and before the page footer.

Rules:

- Link the nearest project index or memory index when it helps navigation.
- Link sibling decisions, designs, references, or conventions that a reader should inspect next.
- Do not create an empty `Related Notes` section.
- Do not pad the section with weak associations.

Example:

```markdown
## Related Notes

- [[AI Context as Code]]
- [[legacy-knowledge-base-principles]]
- [[2026-06-29-cloudflare-workers-static-assets-fallback|Cloudflare Workers static assets decision]]
```

## Backlinks

When adding a durable wikilink, consider whether the target note should also link back.

- Add a backlink in the target note's `Related Notes` section when the relationship is durable and useful.
- Do not add backlinks for one-off Daily pointers unless the target note would become easier to navigate.
- If a new note becomes the current rule for an older note, update the older note to point forward.
- If a note is moved or renamed, update affected indexes and high-value related-note links.

## Footnotes

Footnotes carry sources and small supporting context.

Use footnotes for:

- External sources.
- User decisions or constraints that matter but would interrupt the main text.
- Small caveats, examples, or verification notes.
- Private-source acknowledgements that cannot expose a private URL or title.

Do not use footnotes for:

- Empty source placeholders.
- Self-referential convention claims.
- Internal private URLs, expiring dashboards, credentials, tokens, or private thread links.
- Long explanations that belong in the main body.
- Same-repo navigation that should be a wikilink instead.

If a source is private, summarize only the public-safe fact and say that the private source is intentionally not linked when that context is necessary.
Every footnote definition must have a matching marker in the body.

## Public Page Footer

Public durable notes should end with a public page footer after footnotes.
Existing notes can be backfilled gradually, but new or meaningfully touched public notes should include it once the note has a build-managed `id`.

Format:

```html
---
<sub>Page: <a href="https://acac.sh/trove/<id>">https://acac.sh/trove/<id></a></sub>
```

Rules:

- Use the `/trove/<id>` route, not a source path route.
- Do not invent an `id` to create the footer. Run the build first if the note is new.
- Omit the public footer for `visibility: private` or `visibility: internal` notes.
- Keep the footer as the last block in the file.

## Commit And Deploy Workflow

Before committing a meaningful source-note change:

1. Run `python3 scripts/validate_trove.py`.
2. Run `python3 scripts/build_trove.py` when metadata, IDs, search, or public payloads may change.
3. Run `python3 scripts/deploy_check.py` before deploy or after structural changes.
4. Review `git status --short` and do not stage unrelated dirty changes.
5. Commit source changes and required generated metadata together.

Commit rules:

- Use a short imperative commit message.
- Do not add AI-generated signatures or co-author lines.
- Keep unrelated UI, content, and generated-output changes out of the same commit unless the build requires them together.
- Direct `main` commits are acceptable for small ACAC source updates; use a branch or PR for broad migrations.
- Deploy currently happens through `origin/main` push or an authenticated Wrangler deploy.

## Edit Checklist

Before finishing a source note edit:

- Required frontmatter fields are present and ordered with `type` first.
- Natural-language frontmatter values use double quotes.
- `title` and H1 match exactly.
- H1 has a 3-5 line summary directly below it.
- The note's file name is descriptive and stable.
- Evergreen notes read as the current best version, not an append-only history.
- Time-based notes preserve dates, constraints, evidence, and context.
- Wikilinks resolve by file stem or intentional relative path.
- Useful indexes, related notes, and backlinks are updated.
- Footnotes are paired, useful, and public-safe.
- Mermaid diagrams are used only where they improve understanding.
- Public notes that have an `id` include the public page footer when newly created or meaningfully touched.
- `python3 scripts/validate_trove.py` passes.

## What This Will Not Do

- It does not import the full private Obsidian vault.
- It does not define live Claude Code, MCP, hook, or automatic memory sync behavior.
- It does not require private legacy infrastructure, internal Pages links, or private dashboard references.
- It does not replace the validator; it explains what the source should look like before the validator and build run.

## Related Notes

- [[legacy-knowledge-base-principles]]
- [[../MEMORY|ACAC Memory Index]]
- [[../../../../trove/Projects/ai-context-as-code/index|AI Context as Code]]

[^legacy]: This note adapts a private legacy knowledge-base convention. The private source is intentionally not linked from the public ACAC repo.

---
<sub>Page: <a href="https://acac.sh/trove/Tx8SwdTFoS">https://acac.sh/trove/Tx8SwdTFoS</a></sub>
