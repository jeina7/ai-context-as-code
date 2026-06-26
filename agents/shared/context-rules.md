# Shared Context Rules

Agents working in AI Context as Code must treat `notes/` as the publishable source of truth.

## Core Rules

1. Search before writing.
2. Improve existing notes before creating new ones.
3. Never copy private source material into `notes/`.
4. Use `private-staging/` only for dry-run reports and local review.
5. Run checks before considering work complete.
6. If feedback repeats, update `conventions/` or scripts.
7. Large structure changes require a decision note.

## Required Checks

```bash
python3 scripts/check_publish_safety.py
python3 scripts/validate_notes.py
python3 scripts/build_meta.py
```

## Output Destinations

- durable concept: `notes/principles/`, `notes/patterns/`, or `notes/reference/`
- external research: `notes/research/`
- why a choice was made: `notes/decisions/`
- project design: `notes/projects/`
- implementation trace: `notes/worklog/`
- recurring process rule: `conventions/`
- deterministic check: `scripts/`

