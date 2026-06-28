---
title: Interface Design Direction
type: project
status: active
visibility: publishable
created: 2026-06-28
updated: 2026-06-28
---

# Interface Design Direction

## Summary

AI Context as Code should feel closer to a polished developer tool than a generic document site.
The interface can borrow the clarity of Tailwind CSS documentation without copying its brand.

The target is a quiet, precise surface for reading, searching, reviewing, and editing context.

## Principles

- Alignment matters as much as color.
- Repeated surfaces should share one spacing scale.
- Search should be modal-first, not a long navbar input.
- The dashboard should show operational state, not behave like a note.
- The dashboard and workspace chrome should stay English by default.
- Korean and English switching should belong to individual note reading, not the whole app.
- Document pages should keep a focused reading column with useful side context.
- Graphs should summarize relationships, not decorate the page.

## Visual Direction

Use a compact graphite base with one expressive accent.
Keep borders subtle and use shadow only for overlays, modals, and floating previews.

The interface should use:

- a short search trigger in the navbar
- a centered command/search modal
- grouped search results with note snippets and command actions
- consistent left and right page insets
- small but legible labels
- restrained hover states
- cards only for repeated items or tool panels

## Search Direction

Search should become the fastest way to move through the system.
The navbar search field is only an entry point.
The modal owns the real interaction.

The modal should support:

- generated index search across note title, path, type, headings, and body
- localized Korean text search for human reading
- command actions
- keyboard navigation
- visible note snippets
- ranking by title match, path, type, body, backlinks, recency, and review state
- empty state feedback when nothing matches

## QA Direction

Every layout change should keep desktop and mobile insets aligned.
When possible, use `scripts/qa_viewports.py` to capture dashboard and note screens before publishing.

## Non-Goals

This is not a marketing landing page.
It should not copy Tailwind CSS visual identity directly.
It should not add decorative gradients or oversized hero layouts.
It should not make graphs the main visual object unless the graph explains a decision.

## Related

- [[ai-context-as-code-design]]
- [[system-interface-map]]
- [[agent-runtime-references]]
