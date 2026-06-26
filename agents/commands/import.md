# Import Command

Use this command when private Obsidian material may contain publishable knowledge.

## Input

- One or more private markdown source paths

## Procedure

1. Run `python3 scripts/import_from_obsidian.py <paths...>`.
2. Read `private-staging/import-report.md`.
3. Do not copy raw source into `notes/`.
4. Rewrite only the reusable idea into a publishable note.
5. Run required checks.

## Output

- Import report path
- Created or updated publishable note path
- Risks found
- Checks run

## Completion Check

Raw private source remains outside `notes/`.

