# Agent Rules

AI agents working in this repository should treat `notes/` as the publishable source of truth.

## Behavior

1. Search existing notes before creating a new note.
2. Prefer improving an existing note when the concept already exists.
3. Do not copy private source material into `notes/`.
4. Run publish safety and validation checks before publishing.
5. For large structure changes, write a plan before editing.
6. If a correction applies broadly, update the conventions instead of fixing only one note.

## Initial Commands

- `query`: Answer from existing notes.
- `learn`: Add or improve a note from new publishable knowledge.
- `review`: Find stale notes, duplicate concepts, broken links, and safety risks.
- `synthesize`: Combine multiple notes into a clearer durable explanation.
- `import`: Analyze private source material without copying it into `notes/`.
- `promote`: Turn implementation traces into durable publishable context.

See `agents/commands/` for executable command procedures.
