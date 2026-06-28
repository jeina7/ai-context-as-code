# Publishable Import Skill

Use this when an agent evaluates whether private-source material should become part of this repository.

## Inputs

- Candidate source path or summary
- Publish safety rules
- Target note type and folder

## Steps

1. Treat the source as private by default.
2. Extract the reusable idea, not the private event.
3. Decide whether to skip, rewrite, or create a new note.
4. Write into `notes/` only after removing private details.
5. Add or update the Korean reading copy when the note is reader-facing.
6. Run the review command.

## Verification

- `conventions/publish-safety.md`
- `conventions/note-format.md`
- `python3 scripts/review_context.py`
