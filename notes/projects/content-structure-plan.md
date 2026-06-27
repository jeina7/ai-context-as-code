---
title: Content Structure Plan
type: project
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# Content Structure Plan

## Summary

AI Context as Code has two jobs.
It is a product that demonstrates context as code.
It is also the first real context corpus maintained by that product.

The note structure should make those two jobs easy to tell apart.
Product notes explain the system.
Method notes explain reusable ways of working.
Corpus notes hold the actual context that proves the system is useful.

## Current Writing Criteria

The current notes were written with these criteria:

- explain the product direction without depending on private Obsidian notes
- preserve decisions as durable context, not chat history
- make AI-readable English the source of truth
- provide Korean reading copies for human review
- keep every note small enough to inspect, link, and revise
- avoid importing personal source material unless it can stand alone inside this repo

## Current Folder Meaning

The current folders are useful, but the boundaries are not natural enough yet.

- `start/` is an entry point.
- `principles/` stores stable beliefs.
- `concepts/` stores reusable definitions.
- `workflows/` stores repeatable operating steps.
- `projects/` stores product and adoption plans.
- `decisions/` stores why a choice was made.
- `research/` stores field notes from outside sources.
- `worklog/` stores implementation history.

The awkward part is `projects/`.
It mixes product design with migration/adoption notes.
That makes the repo feel like a document system instead of a working context product.

## Proposed Folder Structure

The next structure should separate product, method, and corpus:

```text
notes/
  product/
    overview.md
    interface-map.md
    design-principles.md
    roadmap.md
  runtime/
    agent-runtime-references.md
  method/
    principles/
    concepts/
    workflows/
  corpus/
    obsidian-transition-plan.md
    import-policy.md
    first-pass-import.md
  decisions/
  research/
  worklog/
```

## Obsidian Mapping Rule

When reviewing Obsidian notes, use this rule:

- product design, interface, roadmap, and system behavior go to `product/`
- agent-readable instructions, commands, skills, and memory references go to `runtime/`
- reusable thinking patterns and operating rules go to `method/`
- actual imported context that proves the system works goes to `corpus/`
- irreversible choices go to `decisions/`
- external trend notes go to `research/`
- implementation progress goes to `worklog/`

## Non-Goals

This structure does not move every Obsidian note.
It does not merge private life context into this repo.
It does not add organization features.
It gives the repo a shape that can support both an open source product and a real personal context corpus.

## Related

- [[ai-context-as-code-design]]
- [[agent-runtime-references]]
- [[obsidian-transition-plan]]
- [[publishable-private-context-split]]
