---
type: memory
title: "ACAC Memory Index"
description: "Initial long-term memory index for the ACAC first instance"
status: active
created: 2026-06-28
updated: 2026-06-29
visibility: public
id: qskThSYA1P

---

# ACAC Memory Index

This file is the first long-term memory index for the ACAC trove.
It should point to durable source notes instead of duplicating their full bodies.
When a rule becomes important enough to reuse across sessions, promote it into a focused memory note and link it here.
The current note-writing convention lives in a focused convention note.

## Current Pointers

- Source notes are the source of truth; generated files and runtime memories should point back to source notes.
- `Daily/` holds day-level context and pointers, while project folders hold detailed worklog and decisions.
- `forge/_config/Agents/` source documents generate root entry files for local repository use only.
- [[trove-note-convention]] defines the executable note-writing rules for `trove/**/*.md` and `forge/**/*.md`.

## Promotion Criteria

Create a separate memory note when a rule is reused across multiple sessions, protects against repeated mistakes, or explains how agents should operate on this trove.
Do not create memory notes for one-off implementation details.
