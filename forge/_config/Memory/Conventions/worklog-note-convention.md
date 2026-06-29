---
type: convention
title: "Worklog Note Convention"
description: "Rules for writing ACAC worklog notes and Daily pointers"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: tH4apLCCnu

---

# Worklog Note Convention

This convention defines when ACAC work gets a durable worklog note.
Detailed work units live under `trove/Projects/ai-context-as-code/Worklog/`, while `trove/Daily/` keeps one-line navigation pointers.
The goal is to preserve implementation context, evidence, and follow-up without turning short lookups into noise.
Use this together with [[trove-note-convention]] when editing worklog or Daily markdown source.

## Scope

This convention applies to ACAC project worklog notes inside this repository.
It lives in `forge/_config/Memory/Conventions/` because worklog behavior is an agent-facing operating rule, not a public project decision or a reader feature.

- Detailed project worklog files live at `trove/Projects/ai-context-as-code/Worklog/YYYY-MM-DD.md`.
- Daily pointers live in `trove/Daily/YYYY-MM/YYYY-MM-DD.md` under `## Worklog`.
- Worklog and Daily notes are Korean-first unless a specific note has a clear reason to be English.
- `forge/_config` convention content is written in English.

## When To Record

Create or update a worklog entry when the work changes durable project state or future context.

- Record meaningful implementation, deployment, documentation, structure changes, verification passes, incident response, and decision cleanup.
- Record audits that change the canonical operating rule or identify where future records should live.
- Record external checks such as live URL verification when they prove deployment or public behavior.
- Do not record simple file reads, quick status lookups, short question answers, or routine explanation that does not change project state.
- Do not create a worklog entry only because a chat turn was long; record the effect, not the conversation length.

## Detailed Worklog Entry

Each detailed entry uses this shape.
Keep the body Korean-first for ACAC project worklogs.

```markdown
## HH:MM — Clear Title

Write one or two sentences of work context.
Explain why this record will matter later.

- Core change 1
- Core change 2
- Core change 3

Verification:

- `python3 scripts/validate_trove.py` passed.
- Confirmed the related commit, live URL check, thread final, or existing record.

Remaining Decisions:

- Add follow-up only when needed.
```

Rules:

- The heading must be `## HH:MM — <clear title>`.
- Use KST for `HH:MM`.
- Keep the title specific enough to distinguish it from nearby entries.
- Start with one or two context sentences before implementation bullets.
- Use bullets for core changes.
- Include verification bullets or a `Verification:` section.
- Add remaining decisions or follow-up only when they are actionable.

## Daily Pointer

The Daily note keeps navigation, not detailed history.
Add one line to `## Worklog` for each detailed worklog entry that should be visible from the day view.

```markdown
- ACAC source write apply-create 구현 [[../../Projects/ai-context-as-code/Worklog/2026-06-29#20:07 — Apply Create Local Source Write Implemented|#]]
```

Rules:

- Use one short summary plus the wikilink pointer only.
- Do not copy detailed bullets into the Daily note.
- Use the relative path from the Daily file to the project worklog.
- If the detailed worklog entry already exists and only the Daily pointer is missing, add only the pointer.

## Time Basis

Use KST for all worklog headings.
The heading time should be the time the meaningful unit started or the evidence-backed time for a backfilled record.

- For current work, use the current KST `HH:MM`.
- For backfill, use the time supported by evidence such as commit time, final answer time, live check time, or an existing private record.
- If the time is estimated, keep the heading in `HH:MM` format and state in the first context sentence or verification section that it is estimated.
- Do not silently invent precise times when evidence only supports an approximation.

## Public-Safe Boundary

ACAC worklogs are public-safe source unless the note visibility says otherwise.
Record what happened without copying private material.

- Do not copy private Obsidian design notes, private source text, credentials, tokens, internal URLs, private dashboard details, personal filesystem paths, or private collaboration threads.
- Summarize private-source decisions as public-safe facts when needed.
- Use wording such as "private vault design으로 분리했다" when detailed private context belongs outside this repository.
- Keep public URLs only when they are intended project surfaces such as `https://acac.sh/`.

## Evidence

Each meaningful worklog entry should say how the result was verified.
Use concise evidence instead of long raw output.

- Git commits: record the short hash and purpose when the commit exists; use `git log`, `git show --stat`, or `git show --name-only` as evidence when checking prior work.
- Thread finals: use the final answer as evidence for what was reported, but do not copy private thread contents into public source.
- Validation output: record the command and pass/fail summary, such as `python3 scripts/deploy_check.py` passed.
- Live URL checks: record the public URL, HTTP status, build metadata, or asset check that proves the deployed behavior.
- Existing worklog and Daily pointers: use them to avoid duplicate records and to confirm a prior unit already has durable context.

## Duplicate Avoidance

Before writing, inspect the target worklog and Daily file.

- If the same `## HH:MM — <title>` heading already exists, strengthen that entry instead of creating a duplicate.
- If the worklog entry exists and the Daily pointer is missing, add only the pointer.
- If the Daily pointer exists but points to a renamed heading, update the pointer rather than adding a second line.
- Keep one durable entry per meaningful unit unless two units have different scope, evidence, or follow-up.

## Concurrent Sessions

Multiple local and remote sessions may touch the same repository.
Read current state before writing shared records.

- Check `git status` before editing shared worklog, Daily, memory, or agent files.
- If another thread has changed the same target file, read the diff and append or edit around it without overwriting.
- Do not revert changes outside the current task.
- If a concurrent edit makes the target ambiguous, stop and report the conflict instead of guessing.

## Generated Output

Worklog convention follows the repository source/output boundary.

- Do not hand-edit `data/`, `_build/`, or `dist/`.
- Build scripts may update generated outputs and `data/id-registry.json`; review those changes after running the script.
- If generated output changes only because the source changed, keep it as script output rather than editing it manually.
- If generated output changes unexpectedly, inspect the source cause before accepting it.

## Deploy, Commit, And Push

Worklog and convention changes do not imply deployment.

- Do not deploy only because a convention was edited.
- Commit, push, or deploy only when the user explicitly asks for that action.
- If a commit or deploy already happened as part of the work, record it as evidence with the command or commit hash.
- Keep verification separate from deployment; `python3 scripts/deploy_check.py` is a local check, not a deploy.

## Related Notes

- [[trove-note-convention]]
- [[ACAC Memory Index]]
