# Agent Rules

AI agents working in this repository should treat `notes/` as the canonical English source of truth.
Localized files under `i18n/` are for human reading in the site UI.

## Behavior

1. Search existing notes before creating a new note.
2. Prefer improving an existing note when the concept already exists.
3. Do not copy private source material into `notes/`.
4. Run publish safety and validation checks before publishing.
5. For large structure changes, write a plan before editing.
6. If a correction applies broadly, update the conventions instead of fixing only one note.
7. Write AI-facing source context in English under `notes/`.
8. Add or update the Korean translation under `i18n/ko/notes/` when changing a note.
9. Korean translations must follow jeina's AGENTS.md writing voice: short friendly 해요체, plain wording, and no stiff machine-translation phrasing.
10. Explain technical English terms in Korean on first use unless the term is a file name, command, product name, or code identifier.

## Initial Commands

- `query`: Answer from existing notes.
- `learn`: Add or improve a note from new publishable knowledge.
- `review`: Find stale notes, duplicate concepts, broken links, and safety risks.
- `synthesize`: Combine multiple notes into a clearer durable explanation.
- `import`: Analyze private source material without copying it into `notes/`.
- `promote`: Turn implementation traces into durable publishable context.

See `agents/commands/` for executable command procedures.

## Korean Writing Voice

Korean notes should sound like a clear explanation for a vocational-high-school CS student.

- Use short 해요체 sentences.
- Prefer Korean words when they are natural: `검토`, `원본`, `저장소`, `작업 흐름`, `비공개`, `공개해도 되는`.
- Keep technical identifiers in monospace when they refer to concrete files, folders, commands, or product names.
- Avoid literal machine-translation phrasing when a plain Korean phrase works.
- Keep established technical terms such as `harness`, `runtime`, `source of truth`, and `validation` when the English term is clearer than a forced Korean replacement.
- Do not invent compressed labels. Spell out the idea in everyday words.
