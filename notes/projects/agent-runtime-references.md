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

AI Context as Code needs a direct-read surface for agent configuration.
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

The first config references are:

- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

These are symlinks into `conventions/` and `agents/`.
Agents can read `agent-runtime/` as an index, while humans can still edit the source folders.

## Future Shape

The long-term shape should use familiar names:

```text
AGENTS.md
CLAUDE.md
agents/
  commands/
  shared/
skills/
memory/
conventions/
```

`skills/` should hold reusable agent procedures.
`memory/` should hold compact pointers into durable notes, not full private context.
`AGENTS.md` or `CLAUDE.md` should be generated or linked from the same source rules when this repository needs tool-specific entry files.

## Non-Goals

This does not copy private Obsidian memory into the repository.
It does not make agent instructions editable from the browser yet.
It does not invent a proprietary agent configuration standard.

## Related

- [[ai-context-as-code-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
