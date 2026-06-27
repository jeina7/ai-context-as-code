# Note Format

Every publishable note uses YAML frontmatter followed by readable markdown.

```md
---
title: Example Note
type: pattern
status: active
visibility: publishable
created: 2026-06-26
updated: 2026-06-26
---

# Example Note

## Summary

Three to five lines that let a reader understand the note quickly.

## Body

The durable content.

## Related

- [[another-note]]
```

## Required Fields

- `title`: Human-readable title.
- `type`: One of `principle`, `pattern`, `research`, `decision`, `project`, `worklog`, `reference`.
- `status`: `draft`, `active`, or `archived`.
- `visibility`: Must be `publishable` for files in `notes/`.
- `created`: Creation date.
- `updated`: Last meaningful update date.

## Writing Rules

- Prefer durable explanations over chat-like fragments.
- Add new notes only when they introduce a distinct concept.
- Update existing notes when the new material strengthens an existing concept.
- Use wikilinks for related notes.
- Keep private context out of publishable notes.
- Keep Korean translations in short friendly 해요체.
- Korean translations should not read like literal English translations.
- When a technical English term must remain, explain it briefly or keep it as a concrete code/file term.
