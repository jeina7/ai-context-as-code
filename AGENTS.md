# Agent Instructions

This repository stores AI Context as Code.
Agents should treat `notes/` as the canonical English context source and `i18n/ko/notes/` as the Korean reading copy.

## Start Here

1. Read `README.md` for the product boundary.
2. Read `conventions/agent-rules.md` before editing notes.
3. Read `conventions/note-format.md` before creating or changing notes.
4. Use `agents/commands/` for repeatable operations.
5. Use `memory/` for compact pointers into durable context.

## Operating Rules

- Do not copy private Obsidian content directly into this repository.
- Keep publishable notes useful without private source context.
- Prefer small, explicit changes that can be reviewed in Git.
- Run `python3 scripts/review_context.py` before committing content changes.
- Update Korean reading copies when public-facing note content changes.

## Agent Config Surfaces

- `AGENTS.md`: general agent instructions for this repository.
- `CLAUDE.md`: Claude-specific entry instructions.
- `agents/commands/`: repeatable command procedures.
- `skills/`: reusable agent procedures that can later become tool skills.
- `memory/`: compact context pointers, not private memory dumps.
- `conventions/`: durable writing, review, safety, and note-format rules.
