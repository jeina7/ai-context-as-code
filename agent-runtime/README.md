# Agent Runtime

`agent-runtime/` is the direct-read surface for AI agents.

It gathers instructions, commands, review rules, and future skills or memory files in one stable place.
Files in this folder can be symlinks to their source folders when another directory is the canonical editing location.

Current references:

- `agent-rules.md` -> `conventions/agent-rules.md`
- `note-format.md` -> `conventions/note-format.md`
- `review-rules.md` -> `conventions/review-rules.md`
- `publish-safety.md` -> `conventions/publish-safety.md`
- `context-rules.md` -> `agents/shared/context-rules.md`
- `commands/` -> `agents/commands/`

Future references:

- `skills/` for reusable agent procedures
- `memory/` for compact, agent-readable pointers into durable notes
- `profiles/` for runtime-specific agent behavior

The goal is simple: if an agent needs to know how to operate this repository, it should start here.
