# Claude Instructions

Claude should use the same repository rules as other agents.
Start with `AGENTS.md`, then follow the task-specific command or convention file.

## Default Workflow

1. Search existing notes before writing new context.
2. Edit the English canonical note in `notes/`.
3. Update the Korean reading copy in `i18n/ko/notes/` when the note is reader-facing.
4. Run `python3 scripts/review_context.py`.
5. Leave a worklog note when the change is meaningful.

## Source Boundaries

- `notes/` is the durable source for publishable context.
- `i18n/ko/notes/` is a reading layer, not a separate source of truth.
- `private-staging/` is not safe to publish.
- `memory/` should point to durable context instead of storing private raw details.

## Useful Entry Points

- `conventions/agent-rules.md`
- `conventions/note-format.md`
- `conventions/publish-safety.md`
- `agents/commands/review.md`
- `skills/README.md`
- `memory/README.md`
