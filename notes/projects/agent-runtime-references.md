---
title: Agent Configuration References
type: project
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# Agent Configuration References

## Summary

acac.sh needs a direct-read surface for agent configuration.
That surface should not become a custom agent framework.
It should mirror common agent files and folders such as `AGENTS.md`, `CLAUDE.md`, skills, memory, and commands.

The current `agent-runtime/` folder is only a compatibility entry point.
It gathers references that agents can read.
It does not define a new runtime model.

## Rule

Agent-facing instructions should use recognizable config surfaces.
When another folder owns the editable source, the agent-readable entry point can use symlinks instead of copying content.

This follows the same pattern as an Obsidian-backed agent setup exposing skills, memory, commands, and instructions without copying them into every tool.

## Current References

The current config references are:

- `AGENTS.md`
- `CLAUDE.md`
- `agents/commands/`
- `agents/shared/`
- `skills/`
- `memory/`
- `conventions/`
- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

The `agent-runtime/` entries are compatibility symlinks into `conventions/` and `agents/`.
Agents can read `AGENTS.md` or `CLAUDE.md` first, then follow the command, skill, memory, or convention file required by the task.

## Current Shape

The repository now uses familiar names:

```text
AGENTS.md
CLAUDE.md
agents/
  commands/
  shared/
skills/
memory/
conventions/
agent-runtime/
```

`skills/` should hold reusable agent procedures.
`memory/` should hold compact pointers into durable notes, not full private context.
`agent-runtime/` remains only an index for tools that benefit from one folder of references.

## Non-Goals

This does not copy private Obsidian memory into the repository.
It does not make agent instructions editable from the browser yet.
It does not invent a proprietary agent configuration standard.

## Related

- [[acac-sh-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
