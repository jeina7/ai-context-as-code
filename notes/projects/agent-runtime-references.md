---
title: Agent Runtime References
type: project
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# Agent Runtime References

## Summary

AI Context as Code needs a direct-read surface for agents.
The best name for that surface is `agent-runtime/`.

`config` is too broad.
`harness` sounds like a test wrapper.
`agent-runtime` says what the folder is for: files that agents read while operating.

## Rule

Agent-facing instructions should have one stable entry point.
That entry point can use symlinks to source files when another folder owns the editable source.

This mirrors the way an Obsidian-backed agent setup can expose skills, memory, commands, and instructions without copying them into every runtime.

## Current References

The first runtime references are:

- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

These are symlinks into `conventions/` and `agents/`.
Agents can read `agent-runtime/` first, while humans can still edit the source folders.

## Future Shape

The runtime surface can grow like this:

```text
agent-runtime/
  README.md
  agent-rules.md
  note-format.md
  review-rules.md
  publish-safety.md
  context-rules.md
  commands/
  skills/
  memory/
```

`skills/` should hold reusable agent procedures.
`memory/` should hold compact pointers into durable notes, not full private context.

## Non-Goals

This does not copy private Obsidian memory into the repository.
It does not make agent instructions editable from the browser yet.
It creates a clear runtime entry point that can later be generated, synced, or checked.

## Related

- [[ai-context-as-code-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
