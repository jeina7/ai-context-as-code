---
type: design
title: "ACAC Visual Design System Core Direction"
description: "Core visual direction, surface rules, and design-system boundaries for ACAC"
status: active
created: 2026-06-30
updated: 2026-06-30
visibility: public
id: afMXXdr8qE

---

# ACAC Visual Design System Core Direction

ACAC's visual design system starts from the product model, not from the current reader implementation.
The existing `site/` UI, CSS, layout, and earlier reader design-system notes are not design references for this direction.
This note defines the durable visual baseline that future token, layout, and component specs should inherit.

ACAC is an AI-native context layer.
Humans and agents share readable context source.
Reads should feel as fast and legible as a filesystem.
Writes should pass through named semantic actions, validation, Chronicle history, and Ledger-backed evidence.
The visual system should make that model feel precise, trustworthy, and workable.

## Visual Positioning

ACAC is a **precise crafted tool and technical context system**.
Still-life and jewel concepts can inform the vocabulary and iconography, but they are not the product identity sentence.
The jewel language helps explain `Quarry`, `Refine to Trove`, `Gem`, and `Trove`; it should never push the interface into decorative fantasy.

Core visual promise:

> ACAC turns rough context into durable, validated, readable source for humans and agents.

This promise implies four visual requirements:

- Work surfaces should feel calm, exact, and highly usable.
- Reading surfaces should be scannable like a filesystem.
- Write surfaces should expose semantic actions, validation, and history.
- AI-native activity should look like accountable system work, not magic.

Rejected framing:

- Do not describe ACAC as having "still-life and jewel materiality."
- That wording overstates the metaphor and can make the product sound ornamental.
- The correct frame is: ACAC may reference still-life and jewel concepts, but its identity is a precise crafted tool and technical context system.

## Surface Strategy

Desktop App and Web should feel like the same product, but they should not share the same layout.
They should share tokens, icon rules, state language, typography principles, and semantic-action vocabulary.
They should differ in density, navigation, panel structure, and primary job.

### Desktop App

Desktop App is the trusted write and agent workspace.
It should be dense, source-aware, and action-heavy without feeling like a developer daemon.

Desktop rules:

- Start at Account Home.
- Open a Trove into Trove Home.
- Open a Gem into the filesystem tree, Gem editor/reader, and right trust panel.
- Treat Forge as a technical agent workspace, not as another Trove reader.
- Present write operations as named semantic actions, not hidden file operations.

### Web

Web is the read, publish, share, and import surface.
It is not a read-only clone of Desktop.
It should act as a public proof-of-work reader for published Troves.

Web rules:

- Make published Troves readable and trustworthy.
- Keep file tree and reader affordances, but reduce density compared with Desktop.
- Emphasize published Chronicle, import action, provenance, publish state, and shareability.
- Begin with Trove identity and reader access, not a marketing hero.

## Navigation Model

Gem reading should use a normal filesystem-like tree.
The tree must not hard-code a fixed `Project` or `Section` hierarchy.
Different Troves may use different folder depths, names, and conventions.

Tree rules:

- The left tree shows canonical markdown context only.
- A `Gem` appears as a file-like canonical context unit inside a Trove.
- Ordinary folders and Gem rows should be compact, quiet, and easy to scan.
- `.acac`, raw Ledger data, generated indexes, and system state should not appear in the normal tree.
- Project and Section meaning can appear in breadcrumbs, metadata, filters, and validation context when useful.

Surfaces outside the Gem tree:

- `Quarry`: raw input that is not canonical yet.
- `Chronicle`: human-readable generated history.
- `Relations`: the user-facing surface for Context Graph.
- `Ledger`: system log and audit substrate.

## Object Hierarchy

The UI should not flatten every product model into peer navigation items.
Objects should be distinguished by job.

Primary places:

- `Trove`: the unit of publish, import, share, sync, and visibility.
- `Forge`: the account-level agent and system source workspace.

Trove internal units:

- `Quarry`: raw input before it becomes canonical context.
- `Gem`: refined, durable markdown context source.
- `Chronicle`: generated history that explains what changed and why.

Trust layers:

- `Relations`: related Gems, supports, depends on, stale/conflict signals, and Refine guidance.
- `Health`: validation, stale state, conflict state, proposal state, and blocked state.
- `Ledger`: evidence detail, not ordinary user-facing content.

## Home And Overview

Home is not a generic dashboard.
It is an operational overview: what to continue, what needs attention, and what changed recently.

### Account Home

Account Home is the first screen of the Desktop App.
It should combine "continue working" with "attention needed."

Account Home should show:

- recent meaningful work
- recently opened Gems
- recent Quarry inputs
- blocked proposals
- conflicts
- stale signals
- sync and publish issues
- Trove list
- Forge status

### Trove Home

Trove Home appears after selecting a Trove.
It should describe the current health and recent evolution of that Trove.

Trove Home should show:

- Trove name
- sync status
- publish status
- validation health
- Quarry items ready to refine
- blocked proposals
- conflicts and stale items
- Chronicle summary
- recent Ledger-backed activity
- affected Gems

Primary Trove actions:

- `New Quarry Item`
- `Refine to Trove`
- `Open Gem Tree`
- `Publish Preview`

History rules:

- Recent history is not a file-view log.
- History rows should represent meaningful work units such as `Ledger Entry`, `Refine result`, `Gem edit`, `Publish`, `Import`, and `Revert`.
- Recently viewed files can exist, but they are secondary.

## Right Trust Panel

Desktop should keep the right trust panel always reachable.
The panel can collapse for focus or narrow viewports, but it should not disappear as a hidden advanced feature.

Panel groups:

- `Relations`: related Gems, supports, depends on
- `Health`: validation, stale, conflict, proposal, blocked state
- `Ledger Context`: affected paths, actor, entry link, revert availability
- `Refine Guidance`: placement hints, merge suggestions, unresolved issues

This panel is not a graph canvas.
The user should see context safety and useful relationships, not a graph database.

## Ledger And Chronicle

Ledger and Chronicle should be visually distinct.
They describe the same underlying work from different levels of abstraction.

Chronicle:

- Human-facing history.
- Written in readable summaries.
- Explains what changed, why it changed, what was validated, which Gems were affected, and what remains open.
- Appropriate for Home, Trove Home, and Web reader contexts.

Ledger:

- Not normal user-facing content.
- System log and audit substrate.
- Used for evidence detail, conflict explanation, revert confirmation, and provenance.
- Should look structured, compact, and technical.
- Should not appear in the normal navigation tree.

Chronicle explains the story.
Ledger provides the evidence.

## AI-Native State

AI-native state should look accountable.
The interface should not imply that the user is watching model reasoning.

Refine loading rules:

- Combine real product operation phases with crafted status phrases.
- Use phrases such as `Assaying input`, `Finding matching Gems`, `Polishing changes`, `Setting into Trove`, `Writing Ledger`, `Updating Chronicle`, and `Checking conflicts`.
- Treat those phrases as product operation status, not chain-of-thought.
- If the process fails or blocks, stop the ambient loading language and show validation result, blocked reason, affected Gems, and available actions.

State badge vocabulary:

- `Synced`
- `Published`
- `Draft`
- `Proposal`
- `Conflict`
- `Stale`
- `Validated`
- `Blocked`
- `Reverted`

Use plain system state labels by default.
Reserve crafted language for Refine loading and result moments.

## Color Direction

Color should prioritize state interpretation over model identity.
Do not assign loud permanent colors to every model object.
Use icon, position, label, and surface hierarchy to distinguish `Trove`, `Quarry`, `Forge`, `Chronicle`, and `Gem`.

Base direction:

- Light-first technical workspace.
- Readable body and editor surfaces.
- Slate, graphite, and muted border tones for structure.
- Teal, green, amber, rust, and blue-green accents for states and actions.

Surface-specific rules:

- Desktop may use darker graphite side surfaces to support a workbench feel.
- Web should stay brighter and easier to read.
- Dark mode is a power-user option, not the product identity.

Status color priority:

- Success and validated: teal or green.
- Publish and sync: blue-green.
- Warning and proposal: amber.
- Conflict and blocked: rust or restrained crimson.
- Neutral and system: slate or graphite.

## Surface Depth And Radius

The UI itself is not 3D.
3D belongs to the prepared icon assets.
Panels, rows, logs, and editor surfaces should stay flat, exact, and quiet.

Depth rules:

- Use borders, background tone, and spacing before shadows.
- Keep shadows subtle when needed.
- Do not use glassmorphism, neumorphism, glossy buttons, or jewel-like cards.

Radius rules:

- Use a soft but controlled rounded technical UI.
- Panels should generally sit around 10-12px radius.
- Rows should generally sit around 8px radius.
- Badges and pills are allowed for state expression, not as the dominant shape language.
- Avoid large rounded cards filling the screen.

## Icon System

Use the prepared icon assets.
Do not invent new concept icons for this baseline.

Current core icon source assets:

- `forge/_assets/icons/trove-jewel-casket-source-chroma.png`
- `forge/_assets/icons/gem-teal-source-chroma.png`
- `forge/_assets/icons/quarry-raw-shard-source-chroma.png`
- `forge/_assets/icons/forge-workshop-alcove-icon-source-chroma-magenta.png`
- `forge/_assets/icons/chronicle-imperial-open-folio-source-chroma.png`

Icon usage rules:

- Treat 3D icons as top-level concept markers.
- Use them in concept explanations, empty states, result summaries, onboarding moments, and sidebar section headers.
- Do not repeat the Gem icon on every Gem row.
- Keep normal folders and file rows quiet and filesystem-like.
- Do not expose chroma source backgrounds in product UI.
- Product UI should use background-removed or masked derivatives of the source assets.

Sidebar rules:

- `Trove`, `Quarry`, `Forge`, and `Chronicle` section headers may use concept icons.
- `Gem` icon should be reserved for Gem concept explanation, creation completion, and Refine result summary moments.

## Component Grammar

The base grammar is **panels, rows, and logs**.
Cards are limited tools, not the default layout pattern.

Core components:

- Gem file row
- Gem editor surface
- Gem reader surface
- Frontmatter renderer
- Trove switcher
- Quarry item row
- Refine to Trove action
- Refine result summary
- Chronicle entry
- Ledger Entry detail
- Relations panel group
- Health and validation row
- Status badge
- Sync state row
- Publish state row
- Import state row
- Revert Ledger Entry confirmation
- Revert result summary

Card rules:

- Use cards only when a bounded object needs a framed preview, such as Trove switcher, publish/import preview, or empty state.
- Do not build the product as a grid of oversized cards.
- Do not put cards inside cards.

## Markdown Rendering

Gem body and Web reader surfaces should optimize for markdown readability.
Surrounding tool UI should remain denser and more operational.

Required markdown rendering components:

- headings
- paragraphs
- links
- ordered lists
- unordered lists
- task lists
- blockquote
- callout
- inline code
- code block
- table
- image
- horizontal rule
- footnote and reference
- frontmatter display and form

Gem body rules:

- Gem body is a pure markdown renderer.
- Do not introduce ACAC-specific block syntax inside the Gem body.
- If ACAC creates content through semantic action, that content should still render as normal markdown once it is inside a Gem.

Tool surface rules:

- `Refine result`, `Validation/Conflict`, `Ledger Entry detail`, `Chronicle entry`, `Relations`, and `Frontmatter form` are tool components outside the markdown body.
- The UI should visually distinguish source markdown from ACAC-managed tool surfaces.

## Frontmatter Rendering

Frontmatter should be visible by default.
It should not render as a raw YAML block in normal reading mode.
Use a readable metadata renderer at the top of the Gem.

Always-visible fields:

- `title`
- `type`
- `status`
- `updated`
- `visibility`

Conditional fields:

- `tags`
- `project`
- `section`
- `source`
- `related`

Collapsed fields:

- `id`
- generated fields
- hashes
- internal registry fields
- internal provenance fields

Source mode may expose raw frontmatter.
Web reader should show only public-safe metadata.

## Quarry Direction

Quarry is a pre-canonical input surface.
Do not describe it as a "raw material bench."
That phrase makes the metaphor too heavy and less precise.

Quarry rules:

- A Quarry item is not yet a canonical Gem.
- Quarry should feel clear like an inbox.
- `Refine to Trove` is the primary Quarry action.
- A Quarry item may become a new Gem, be absorbed into an existing Gem, or be split across multiple Gems.
- The UI should clearly signal that Quarry content is not canonical source yet.

Quarry state candidates:

- `Raw`
- `Ready`
- `Refining`
- `Proposal`
- `Absorbed`
- `Split`
- `Blocked`

## Forge Direction

Forge is not a Trove reader.
Forge is a technical agent workspace.

Forge rules:

- Organize around `Agents`, `Skills`, `Commands`, and `Memory`.
- Allow source-like reading and editing, but emphasize runtime sync and validation state.
- Treat Forge changes as higher risk because they can change agent behavior.
- Require proposal or confirmation for risky Forge changes.
- Use the Forge icon strongly in sidebar section headers and Forge overview.

## Non-Goals

Avoid these visual directions:

- Notion clone.
- Obsidian clone.
- Generic document app clone.
- Generic AI gradient.
- Graph canvas-first UI.
- Over-fantasy jewel UI.
- Marketing hero-first Web.
- Oversized card dashboard.
- Low-density dashboard.
- Chat-like Quarry.
- Glossy 3D controls.
- Ledger as a pretty user-facing timeline.
- ACAC-specific block syntax inside Gem markdown.

## Resolved Decisions

- ACAC's visual identity is a precise crafted tool and technical context system.
- Still-life and jewel concepts are reference material, not the product identity sentence.
- Desktop and Web share tokens, state language, icon rules, and typography principles, but not layout density.
- Desktop starts with Account Home, then Trove Home, Gem workspace, or Forge workspace.
- Web is a public proof-of-work reader, not a read-only clone of Desktop.
- Gem reading uses a normal filesystem-like tree.
- Quarry, Chronicle, Relations, and Ledger live outside the Gem tree.
- The right trust panel is always accessible and collapsible.
- Ledger is system log and audit substrate, not normal user-facing content.
- Chronicle is human-readable generated history.
- Colors prioritize state, not model identity.
- UI surfaces are flat; 3D belongs to prepared icon assets.
- Radius is soft but controlled.
- Core component grammar is panels, rows, and logs.
- Markdown body is pure markdown rendering.
- ACAC tool components live outside the markdown body.
- Frontmatter is visible by default through a readable metadata renderer.

## Remaining Open Questions

- Exact color token values and contrast ratios.
- Exact light and dark mode token mapping.
- Exact Account Home layout.
- Exact Trove Home layout.
- Exact right trust panel information architecture.
- Exact markdown renderer spacing, table styling, code styling, and callout styling.
- Exact icon processing pipeline for chroma source assets.
- Exact Web public reader entry layout.
- Exact animation timing and phrase rotation rules for Refine loading.

## Recommended Next Design Notes

1. Design Token Spec
2. Account Home And Trove Home Layout Spec
3. Desktop Gem Workspace Layout Spec
4. Web Reader And Publish Spec
5. Right Trust Panel Spec
6. Markdown Renderer Component Spec
7. Icon Usage And Asset Processing Spec

## Related Notes

- [[ai-native-context-layer-product-model]]
- [[acac-visual-direction-grill-qna-extract]]
