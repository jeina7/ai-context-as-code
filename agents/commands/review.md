# Review Command

Use this command to inspect the health of the context layer.

## Procedure

1. Run publish safety checks.
2. Run note validation.
3. Run metadata build.
4. Review broken links, duplicate concepts, weak summaries, stale notes, and missing related links.
5. Propose targeted fixes.

## Output

- Findings ordered by severity
- Fixes applied
- Fixes deferred
- Checks run

## Completion Check

The repository should have zero broken links and no known publish safety findings.

## Shortcut

```bash
python3 scripts/review_context.py
```
