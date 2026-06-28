# AI Context as Code

Project name confirmed: `AI Context as Code`.

AI Context as Code is a markdown-based context system for knowledge that is easy for humans to browse and structured enough for AI agents to read, review, and improve.

This repository has two roles:

- the product code and design for AI Context as Code
- the first context corpus that demonstrates the product on its own development history

That corpus is not a private life vault. It is the reviewed example dataset that makes the product useful, inspectable, and resume-ready.

## Goals

- Keep reviewed knowledge in plain markdown.
- Support wikilinks, backlinks, search, and a folder tree.
- Publish as a static GitHub Pages site.
- Separate private staging from reviewed notes.
- Add safety checks before anything is published.
- Evolve toward agent-assisted note creation, review, and synthesis.
- Record the design and implementation process as the system's first context corpus.
- Become a context brain that can support personal use first and organizational use later.

## Current Features

- Static GitHub Pages workspace.
- Three-pane reading layout with search, filters, outline, backlinks, and status.
- Compact navbar search trigger with a command/search modal.
- Generated search index used by the command/search modal.
- Wikilink hover previews.
- Mermaid diagram rendering.
- Context map with relationship reasons, not only node links.
- Browser draft editing with localStorage.
- Section-aware patch export for reviewing browser edits locally before committing.
- Light and dark themes.
- Korean and English reading modes.
- Generated reports for broken links, orphan notes, and hub notes.
- Viewport QA script for desktop and mobile screenshots.

## Non-Goals

- This is not a full private Obsidian migration.
- This does not publish private journals, company notes, finance notes, family context, or sensitive strategy.
- This does not include auth, team permissions, or organization management.
- Browser editing does not silently commit to GitHub. It drafts locally and exports patches.

## Structure

```text
notes/                 canonical English context corpus
i18n/                  localized reading copies; notes/ remains canonical English
private-staging/       ignored local staging area for private source material
AGENTS.md              general agent entry instructions
CLAUDE.md              Claude-specific entry instructions
conventions/           note, safety, and agent rules
agents/                command procedures for AI-assisted work
skills/                reusable agent procedures
memory/                compact pointers into durable context
agent-runtime/         compatibility index for agent-readable config
scripts/               build and validation scripts
site/                  static GitHub Pages app
data/                  persistent registries
_build/                generated data
```

## Local Build

```bash
python3 scripts/check_publish_safety.py
python3 scripts/validate_notes.py
python3 scripts/build_meta.py
python3 scripts/review_context.py
python3 scripts/qa_viewports.py
python3 -m http.server 8000 --directory site
```

The site expects generated JSON under `site/_build/`. `build_meta.py` writes there automatically for local preview.
The viewport QA script writes screenshots and a JSON report under ignored `private-staging/qa/`.

## Language Model

`notes/` is the canonical English source for AI agents and automation.
Korean reading copies live under `i18n/ko/notes/` with the same slug.
The site defaults to Korean for human reading, while generated metadata keeps the English source body available for AI-facing use.

## Import Dry Run

Private Obsidian material must be analyzed before it is rewritten into `notes/`.

```bash
python3 scripts/import_from_obsidian.py /path/to/candidate.md
```

The importer writes a dry-run report under `private-staging/`. It never writes directly into `notes/`.
The report includes risk level, recommended destination, rewrite checklist, and a standalone rewrite prompt.
