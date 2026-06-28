# Agent Configuration Index

`agent-runtime/` is a compatibility index for AI agents.
It is not a separate framework or a proprietary runtime model.

It gathers recognizable agent configuration surfaces in one stable place.
The source of truth should still be common files and folders such as `AGENTS.md`, `CLAUDE.md`, `agents/`, `skills/`, `memory/`, and `conventions/`.
Files in this folder can be symlinks when another directory is the canonical editing location.

Current references:

- `../AGENTS.md`
- `../CLAUDE.md`
- `../skills/`
- `../memory/`
- `agent-rules.md` -> `conventions/agent-rules.md`
- `note-format.md` -> `conventions/note-format.md`
- `review-rules.md` -> `conventions/review-rules.md`
- `publish-safety.md` -> `conventions/publish-safety.md`
- `context-rules.md` -> `agents/shared/context-rules.md`
- `commands/` -> `agents/commands/`

The goal is simple: if an agent needs to know how to operate this repository, it can start here without learning a custom structure.
