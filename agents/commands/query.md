# Query Command

Use this command when answering from the existing context layer.

## Input

- User question
- Optional target note or folder

## Procedure

1. Search `notes/` for relevant existing context.
2. Read the most relevant notes.
3. Answer using only what the context supports.
4. Say when the answer is an inference.
5. If the context is missing or stale, propose a follow-up note update.

## Output

- Answer
- Relevant note links
- Suggested context updates, if any

## Completion Check

The answer should make clear whether the repository already contains enough context.

