# AI Context as Code

Project name confirmed: `AI Context as Code`.

AI Context as Code is a markdown-based publishable knowledge system for notes that are safe to publish, easy for humans to browse, and structured enough to become durable context for AI agents to read, review, and improve.

## Goals

- Keep publishable knowledge in plain markdown.
- Support wikilinks, backlinks, search, and a folder tree.
- Publish as a static GitHub Pages site.
- Separate private staging from publishable notes.
- Add safety checks before anything is published.
- Evolve toward agent-assisted note creation, review, and synthesis.
- Record the design and implementation process as the system's first publishable knowledge.
- Become a publishable context brain that can support personal use first and organizational use later.

## Current Features

- Static GitHub Pages workspace.
- Three-pane reading layout with search, filters, outline, backlinks, and status.
- Wikilink hover previews.
- Mermaid diagram rendering.
- Local and full knowledge graph views.
- Browser draft editing with localStorage.
- Patch export for reviewing browser edits locally before committing.
- Light and dark themes.
- Generated reports for broken links, orphan notes, and hub notes.

## Non-Goals

- This is not a full private Obsidian migration.
- This does not publish private journals, company notes, finance notes, family context, or sensitive strategy.
- This does not include auth, team permissions, or organization management.
- Browser editing does not silently commit to GitHub. It drafts locally and exports patches.

## Structure

```text
notes/                 publishable markdown notes
private-staging/       ignored local staging area for private source material
conventions/           note, safety, and agent rules
agents/                command procedures for AI-assisted work
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
python3 -m http.server 8000 --directory site
```

The site expects generated JSON under `site/_build/`. `build_meta.py` writes there automatically for local preview.

## Import Dry Run

Private Obsidian material must be analyzed before it is rewritten into `notes/`.

```bash
python3 scripts/import_from_obsidian.py /path/to/candidate.md
```

The importer writes a dry-run report under `private-staging/`. It never writes directly into `notes/`.
