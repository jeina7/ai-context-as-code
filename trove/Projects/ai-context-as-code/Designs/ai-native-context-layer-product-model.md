---
type: design
title: "AI-Native Context Layer Product Model"
description: "ACAC product direction, vocabulary, model boundaries, and AI-native context layer decisions"
status: active
created: 2026-06-30
updated: 2026-06-30
visibility: public
id: 4dYzPkCVtG

---

# AI-Native Context Layer Product Model

ACAC is an AI-native context layer for agents and makers.
It gives agents file-speed access to the user's whole context while forcing writes through semantic, auditable actions.
Its core product value is not a document app with AI attached, but a self-evolving context system with durable source, safe writes, human-readable history, and derived relations.
This note captures the product model decisions from the first product-direction grilling session.

## Product Positioning

ACAC is an **AI-native context layer**.
It exists so a solo builder or maker can keep their durable working context in a system that both humans and agents can use well.
The main promise is:

> Agents read the whole context like files, write through safe semantic actions, and leave human-readable history behind.

The product should not be positioned as a generic note app, an Obsidian clone, a Notion clone, a GitHub-backed static site, or a RAG answer engine.
ACAC is a context layer with its own source model, write model, sync model, and agent integration boundary.

## Product Name And Brand

The current product and project name stays **ACAC**, short for AI Context as Code.
The category is AI-native context layer.

**Lapidary** is a future brand candidate.
It fits the product vocabulary because a lapidary cuts and refines rough stone into gems.
That maps well to Quarry, Refine to Trove, Gem, and Trove.
The brand should not be changed yet.
Use the working frame:

> ACAC, potentially branded as Lapidary later.

## Primary User

The first user is a **Claude Code and Codex heavy solo builder or maker**.
This user works with AI agents every day, needs durable project and operating context, and wants agents to read and update that context without manual copy-paste or repeated re-explanation.

The product should keep a future path toward team and organization use, but v1 does not optimize for team governance.
The first version should make one person's AI-native working context feel fast, trusted, and self-improving.

## Independence From Other Document Apps

ACAC product design should stand on its own.
It should not use another document app as its product reference point.

Important boundaries:

- ACAC is not a migration product.
- ACAC does not promise compatibility with another app's plugin system, folder model, graph view, or sync model.
- A user may personally migrate existing notes into ACAC, but that is not a product promise.
- Product copy should avoid "like Obsidian" as a primary explanation.
- ACAC's own model is Account, selectable Forge, selectable Trove, Project, Section, Gem, Quarry, Ledger, Chronicle, Context Graph, and Relations.

## Account Model

ACAC uses a simple account model in v1.

```text
Account
├── <selected-forge>
├── <selected-trove>
├── .acac
└── account settings
```

There is no separate Workspace, Vault, Atelier, Foundry, or Library layer in v1.
One account is one ACAC space.
This keeps hierarchy simple and avoids adding a container that does not carry a distinct user job.

`<selected-forge>` and `<selected-trove>` are selected account resources.
They should not be modeled as literal permanent root folder names such as `Forge/` and `Troves/` in the product hierarchy.
The account can switch the active Trove.
V1 starts with one active Forge, while future Forge Profiles can make Forge selection explicit.

Rejected alternatives:

- `Workspace`: too generic and unnecessary for v1.
- `Vault`: too strongly associated with another document app.
- `Atelier` or `Foundry`: evocative, but the extra hierarchy does not solve a v1 product problem.
- `User -> Troves` with no selected Forge, system store, or history thinking: too simple once Forge, sync, and history are included.

## Pricing Boundary

The v1 pricing boundary is simple:

| Plan area | Free | Paid |
|---|---|---|
| Troves | One Trove | Multiple Troves |
| Forge | One active Forge | Forge Profiles later |
| Desktop App sync | Basic sync | More capacity and history |
| Web publish | Basic publish | Private/shared reader and richer publish controls |
| Import | Not core free value | Import Trove |
| Search and history | Basic | Advanced Chronicle and search |

Future paid or team features:

- Forge Profiles
- team and organization accounts
- shared editing
- synced shared Troves
- origin write-back and review workflow

## Core Vocabulary

### Trove

A **Trove** is the main unit for publish, import, share, sync, and visibility.
It is a collection of canonical Gems organized by project and section.

Trove-level visibility is the v1 boundary.
Gem-level visibility is not part of v1.
If public and private material need different visibility, they should live in different Troves.

### Project

A **Project** is a bounded workstream, subject, or durable context area inside a Trove.
Examples:

- `ai-context-as-code`
- `client-work`
- `personal-finance`
- `product-research`
- `agent-runtime`

Projects are created as content accumulates.
They are not a fixed global taxonomy.
The word Project is preferred over Domain because ACAC is organized around work and context evolution, not abstract knowledge taxonomy.

### Section

A **Section** groups Gems by role inside a Project.
Sections are not Gem classes.
They are placement conventions that help humans and agents decide where a Gem belongs.

Default section candidates:

- `decisions`
- `designs`
- `references`
- `research`
- `meetings`
- `troubleshooting`
- `archive`

The exact default section set should stay compatible with the intended source convention: project first, type or role below it.
Agent refinement should use these section conventions when placing or moving Gems.

### Gem

A **Gem** is an individual canonical markdown document.
It is the product term for a refined, durable note.
The actual file format remains `.md`.

A Gem is not a graph node only, a database row only, or a UI card only.
It is a canonical context unit with markdown source and structured metadata.

### Quarry

A **Quarry** is a Trove-specific raw input space.
Each Trove has its own Quarry.
There is no account-level Unsorted Quarry in v1.

The user can write rough input into a Trove's Quarry.
That input is not a canonical Gem yet.
It becomes useful when the user runs Refine to Trove.

### Refine to Trove

**Refine to Trove** is the main action that turns Quarry input into durable Trove context.
It can:

- absorb a Quarry item into existing Gems
- create a new Gem
- split a rough input into multiple Gems
- update indexes and Relations
- create Ledger Entries
- update Chronicle
- stop as a proposal when a risky change is detected

Refine to Trove is manually triggered.
Quarry items do not automatically process themselves by default.

The loading experience can use progress language such as assaying, polishing, setting into Trove, writing Ledger, and updating Chronicle.
Those words should be treated as UI flavor, not as exposed reasoning steps.

### Forge

**Forge** is account-level agent and system source.
It contains durable operating context that changes agent behavior.

V1 Forge structure:

```text
<forge>/
├── Agents/
├── Skills/
├── Commands/
└── Memory/
```

Meanings:

- `Agents`: runtime entry source markdown
- `Skills`: repeatable agent workflows
- `Commands`: repeatable command procedures
- `Memory`: durable operating context, principles, conventions, and designs

Memory belongs in Forge, not in Trove.
Memory is operating context for agents, while Troves are publishable knowledge collections.

### Forge Profile

**Forge Profile** is a future feature.
V1 starts with one active Forge.

A future account may have several Forge Profiles, such as default, client-safe, and experimental.
That feature should not be included in the first product spec.

### Ledger

A **Ledger** is an append-only structured log.
Each Trove has its own Ledger.
Forge also has its own Ledger.

Ledger is not a Gem and is not shown in the normal Trove tree.
Raw Ledger data lives in the hidden `.acac` system store.
In the user-facing product model, Ledger is a history and audit system, not a content folder.
Ledger is the source of truth for work history.
Human-readable history documents or views are derived from Ledger, not edited as source.

Ledger exists to support:

- audit
- provenance
- validation evidence
- revert
- sync conflict explanation
- Chronicle generation
- trust calibration for automatic actions

### Ledger Entry

A **Ledger Entry** is one meaningful work unit in a Ledger.
It replaces the earlier "transaction" term.

Each Ledger Entry includes:

- intent: why the work happened
- operations: what changed
- evidence: diff, before/after hash, source anchors, affected Gem IDs and paths
- validation: what checks ran and what passed or failed
- actor: human, agent, or system
- approval state: automatic, user-confirmed, blocked, or proposal
- revert data: how to undo the Entry safely

V1 revert is Ledger Entry based.
ACAC does not erase the old Entry.
It creates a new Entry that reverts the effect of a previous Entry.
One-click revert should operate at the Ledger Entry level.

### Chronicle

A **Chronicle** is a human-readable generated history view.
Each Trove has its own Chronicle.

Chronicle is generated from that Trove's Ledger.
It is read-only.
The user should not directly edit Chronicle as source.
Chronicle is not a Gem and is not shown as a normal editable folder inside a Trove.
It is surfaced in the app as a friendly history, activity, or audit view.
Any stored Chronicle artifact is generated output and an implementation detail, not canonical content.

Chronicle should be friendly enough that a person can return weeks later and understand:

- what changed
- why it changed
- what was validated
- which Gems were affected
- what remains open

Forge may also have a Forge Chronicle later, but Trove Chronicle has higher v1 priority.

### Context Graph

The **Context Graph** is a first-class derived layer.
It is not canonical source.
Canonical source remains Gem markdown plus structured metadata.

The graph helps ACAC understand relationships among Gems, concepts, claims, Ledger Entries, Quarry items, Forge items, and external references.
It supports Refine quality, search, stale detection, conflict detection, import, publish, and agent context generation.

### Relations

**Relations** is the user-facing surface for Context Graph.
Users should see useful relationships, not a graph database.

V1 Relations minimum:

- Related Gems
- Supports and Depends On
- Stale and Conflict Signals
- Refine Guidance

V1 should not lead with a graph canvas.

### Claim

**Claim** is an internal Context Graph primitive.
It is not product-facing vocabulary.
Users should not create, edit, approve, or manage Claims directly.

Claim exists to improve:

- search quality
- contradiction detection
- stale context detection
- Refine placement and update quality
- relation inference

Claim rules:

- Claim is hidden by default.
- Claim is not a Gem.
- Claim is not a separate document.
- Claim must have a source Gem anchor.
- Claim must have Ledger provenance.
- LLM-inferred Claims are candidates by default.
- Accepted Claims should be few and limited to clear decisions, constraints, facts, or preferences.
- If Claim quality becomes noisy, reduce extraction scope and schema before exposing more UI.

## Canonical Hierarchy

The v1 canonical content hierarchy is:

```text
Account
├── <selected-forge>/
├── <selected-trove>/
│   ├── Quarry/
│   └── Projects/
│       └── <project>/
│           └── <section>/
│               └── <gem>.md
└── .acac/
    ├── ledger/
    │   ├── troves/
    │   └── forge/
    ├── registry/
    ├── config/
    └── state/
```

`<selected-forge>` and `<selected-trove>` are selected resources, not literal fixed folder names.
The account can switch the active Trove, and future Forge Profiles can switch the active Forge.

`Projects/` replaces the earlier `Domains/` idea.
Project is the correct unit because ACAC context is organized around active work and evolving durable context, not abstract taxonomy.

Ledger and Chronicle are deliberately not normal children of the Trove content tree.
Raw Ledger Entries live under `.acac/ledger/`.
Chronicle is surfaced through the app as a read-only history view derived from Ledger.
It may have generated cache artifacts, but those artifacts are not source and should not define the product hierarchy.

This hierarchy is a product model, not necessarily the exact local filesystem layout.
The local materialized tree should be readable as markdown files.
The cloud source store can use a structured internal model.

## Product Surfaces

### Desktop App

The Desktop App is the primary human write surface.
It should feel like a document workspace, not a developer daemon.

The user should not have to think about localhost, background servers, or process management.
The app may contain an internal local runtime, but that runtime is implementation detail.

Desktop App responsibilities:

- read and edit Gems
- create Quarry items
- run Refine to Trove
- show Refine results
- show Relations
- show Chronicle
- run Revert Ledger Entry
- manage Troves
- manage Forge
- sync local materialized source with ACAC cloud source store
- sync Forge/Agents into Claude Code and Codex managed files

The editor should be markdown/source-aware.
It should not be a Notion-style block editor in v1.

Useful editor affordances:

- markdown editing
- preview
- frontmatter form
- link picker
- validation panel
- semantic action buttons
- relation panel
- Chronicle and Ledger result links

### Web

The Web product is the read, share, publish, and import surface.
It is not the v1 write surface.

Web use cases:

- public proof-of-work
- linkable project or context reader
- agent-readable project handbook
- client-facing delivery room
- published Chronicle
- public/private publish preview
- Trove discovery and import
- future team shared knowledge layer

Published public Troves can be read without login.
Private or shared Troves require login.
Import Trove requires login.

Web v1 should remain read-only for published Troves.
Comments, edit, and review workflow are future features.

### CLI

The CLI is the v1 action interface for agents and power users.
It should expose semantic actions, not low-level file mutation.

V1 uses:

- file-native context reading
- CLI semantic write actions
- managed Claude Code and Codex entry sync

MCP is not needed for v1.
MCP can become a later adapter over the same read and write contract.

### MCP

MCP is future integration, not v1 implementation.
It is useful when ACAC needs to expose semantic actions and read tools to multiple AI apps through a standard protocol.

MCP should not become the primary bulk context read path.
The fast read path is filesystem-style access to the local materialized source.

## Core UX Promise

The core UX promise is:

> Read as filesystem, write through semantic actions.

Agents should read the entire local materialized source at filesystem speed.
They should not fetch every context item through slow tool calls.

Writes should go through semantic actions.
This gives ACAC a chance to validate, record Ledger Entries, update Chronicle, update Relations, and provide revert data.

## Write Model

ACAC-owned writes use a contract-only model.
Agents and UI should not directly mutate canonical source as the normal product path.

This does not mean the user must review every diff.
The cost should be paid by ACAC runtime and adapters, not by the user.

The default principle:

- Low-risk writes can apply automatically.
- Risky writes stop as a proposal.
- Every write creates a Ledger Entry.
- Every write can be explained in Chronicle.
- Every write can be reverted when source state permits it.

## Semantic Write Actions

V1 semantic write actions:

| Action | Meaning |
|---|---|
| Refine to Trove | Turn Quarry input into canonical Trove context. |
| Edit Gem | Modify an existing Gem. |
| Rename Gem | Change a Gem title, slug, or display name. |
| Move Gem | Move a Gem to another section, project, or Trove. |
| Archive Gem | Remove a Gem from the active surface while preserving history. |
| Delete Gem | Remove a Gem from source in limited cases. |
| Import Trove | Bring another published Trove into the user's account as a forked copy. |
| Revert Ledger Entry | Add a new Ledger Entry that reverses a previous Ledger Entry. |

These are product actions.
They are not file operations.

For example, Delete Gem is not a file delete.
It should evaluate links, archive suitability, validation, Ledger recording, Chronicle update, revert data, and safety.

## Archive And Delete

Archive is the normal way to remove a Gem from the active surface.
Delete is restricted.

Archive Gem:

- preserves source history
- keeps enough identity for links, audit, and revert
- removes the Gem from default reader/search surfaces
- can be represented through status, archive section, or store state

Delete Gem:

- is for sensitive accidents, bad imports, or clearly disposable material
- may avoid keeping full content snapshots when privacy requires it
- still records a minimal Ledger Entry
- should not be the ordinary cleanup path

Tombstone is an internal registry concept.
It should not be user-facing product vocabulary.

## Revert Model

The correct action name is **Revert Ledger Entry**.
This aligns with append-only history.

ACAC does not roll back the Ledger itself.
It creates a new Ledger Entry that reverses the earlier Entry's operations.

Before a revert applies, ACAC should check current source hashes.
If affected Gems changed after the target Entry, ACAC should stop with a conflict instead of applying a dangerous revert.

## Refine Result UX

After Refine to Trove, the user should see a result summary, not a raw diff first.

Default result view:

- which Gems were updated
- which Gems were created
- which proposals were blocked
- which Ledger Entry was created
- how the Chronicle will show the change
- whether Relations changed
- one-click Revert Ledger Entry
- optional diff details

Diff is available as detail, not the main user burden.

## Self-Evolution Boundary

ACAC should support self-evolving documents.
New information should not merely pile up.
ACAC should find the right existing Gems, improve them, move context when needed, and leave a record.

Automatic or low-friction behavior:

- add new input to related Gems
- update summaries
- update indexes and relations
- repair simple conventions
- create draft Gems when low risk
- add Chronicle entries

Proposal or explicit approval required:

- visibility changes
- meaning-changing rewrites
- large reorganizations
- deletes
- Forge or agent behavior changes
- public publish
- origin write-back
- team or shared-area changes

## Source Store And Sync

ACAC uses its own cloud source store.
GitHub is not the product storage model.

The cloud source store is canonical.
It stores:

- Gem markdown body
- structured metadata
- Trove, Project, and Section structure
- Quarry items
- Forge source
- Ledger Entries
- registry data
- Context Graph derived data or rebuild inputs

Each device has a full local materialized copy.
Agents read that local copy like files.
The Desktop App syncs local changes to the ACAC cloud source store in the background.

Publish is explicit.
Background sync and public publish are separate operations.

## Local Materialized Source

The local materialized copy should look and behave like a markdown file tree.
This is essential for fast agent access.

Important rules:

- canonical representation must round-trip to markdown
- generated files should be separated from source
- agents should be able to read all Gems directly from the filesystem
- write should still go through semantic actions
- generated agent context should point agents into the file tree instead of duplicating all context

## Sync Model

Sync is background sync.
Publish is explicit.

Conflict behavior:

- different Gem changes should auto-merge
- different sections in the same Gem can auto-merge when safe
- same paragraph, metadata, or visibility conflicts should stop
- conflict UI should explain conflicting Ledger Entries before showing raw diff
- user choices can include keep local, keep remote, manual merge, or revert

## Cloud Database And Telemetry

ACAC cloud database stores canonical source.
It is not only metadata over local files.

ACAC v1 should include live product telemetry for ACAC's own operations.
Telemetry should cover operational quality, not user content.

Allowed telemetry examples:

- sync success and failure
- Refine success and failure
- validation failure categories
- publish, import, and revert events
- Desktop App latency
- agent sync health
- storage usage
- error traces

Do not collect raw Gem body, Quarry text, Forge Memory text, or private content as telemetry.

## `.acac` Hidden System Store

`.acac` is hidden system state.
It should not appear as normal Trove content.

Recommended structure:

```text
.acac/
├── ledger/
│   ├── troves/
│   └── forge/
├── registry/
├── generated/
│   ├── agents/
│   └── indexes/
├── config/
└── state/
```

Meanings:

- `ledger/troves`: raw Trove Ledger Entries
- `ledger/forge`: raw Forge Ledger Entries for Forge changes
- `registry`: stable identity, semantic path, previous paths, origin provenance
- `generated/agents`: generated Claude Code and Codex runtime entries
- `generated/indexes`: search, navigation, and Context Graph indexes
- `config`: user-selected Forge, Trove, sync, publish, and adapter configuration
- `state`: local-only runtime state such as last sync, adapter health, and last generated hash

Chronicle output can be cached under `generated/` if needed, but it should be treated as disposable generated view data.
The product-facing Chronicle is the read-only app view derived from Ledger.

`state` is local-only and should not be source store truth.
`config` may be source-store backed when it represents durable user choices.

## Agent Runtime Sync

ACAC should automatically sync Forge/Agents into Claude Code and Codex runtime entry files.

V1 supported runtimes:

- Claude Code
- Codex

Future runtimes can be adapter-based.

Sync model:

- Forge contains source markdown.
- ACAC App or CLI transforms source into runtime files.
- Runtime output is generated.
- Runtime files are managed files, not managed blocks.
- First run requires user approval.
- Generated marker and source pointer should be written into managed runtime files.
- Manual edits to managed runtime files should be detected as conflicts.

Source model:

```text
<forge>/
└── Agents/
    ├── Common.md
    ├── Codex.md
    └── Claude.md

.acac/
└── generated/
    └── agents/
        ├── AGENTS.md
        └── CLAUDE.md
```

The transformation logic belongs to ACAC App or CLI.
It should not be a user-authored script inside Forge.

## Import Trove

Import Trove lets a logged-in user bring a published Trove into their account.

V1 model:

- import creates a forked copy
- origin provenance is preserved
- the imported Trove becomes the user's own Trove
- subsequent edits happen in the user's copy
- write-back to origin is not included
- synced shared Troves are not included

Import Trove is important for Web's distribution role.
It turns Web from only a reader into a context sharing and adoption surface.

## Web Reader And Publish

Web is read-only for published Troves in v1.
It supports:

- public reader
- invited private reader
- import flow
- published Chronicle
- LLM-readable published context

Published Troves should eventually provide agent-readable manifests, such as a Trove manifest or `llms.txt` style surface.
The exact shape is still open, but the direction fits the product.

## Context Graph Principles

Context Graph is a derived first-class layer.
It exists because flat markdown search is not enough for AI-native context.
Agents need relationships, provenance, stale signals, and contradiction hints.

The graph should support:

- Refine placement
- search
- related Gem suggestions
- stale context detection
- conflict signals
- duplicate signals
- import provenance
- publish manifests
- agent context generation

The graph should not become canonical source.
Do not make graph database nodes the source of truth for documents.

## Context Graph Schema

V1 should use a small typed schema.
Free-form relationship names should be avoided.

Recommended node types:

- `Trove`
- `Project`
- `Section`
- `Gem`
- `QuarryItem`
- `ForgeItem`
- `LedgerEntry`
- `Chronicle`
- `Concept`
- `Claim`
- `ExternalRef`

Recommended edge types:

- `contains`: Trove to Project to Section to Gem
- `links_to`: explicit markdown or wikilink
- `about`: Gem to Concept
- `mentions`: Gem to Concept or ExternalRef
- `cites`: Gem or Claim to ExternalRef
- `derived_from`: Gem or Claim to QuarryItem, import source, or LedgerEntry
- `changed_by`: Gem to LedgerEntry
- `generated_by`: Chronicle to LedgerEntry
- `supersedes`: Gem or Claim replaces another Gem or Claim
- `supports`: Gem or Claim supports a Claim or decision-like Gem
- `contradicts`: Claim conflicts with another Claim
- `depends_on`: Gem depends on another Gem

Every inferred relation should carry metadata:

- `source_kind`: explicit_link, path, ledger, refine, import, or inference
- `source_ref`: Gem ID, Ledger Entry ID, paragraph anchor, or import source
- `status`: accepted, candidate, rejected, or stale
- `confidence`: required for inference
- `valid_from` and `valid_to` where relevant
- `created_by`
- `created_at`

## Relations UX

Relations is how users experience Context Graph.
It should not force users to think in graph terms.

V1 Relations minimum:

- Related Gems
- Supports and Depends On
- Stale and Conflict Signals
- Refine Guidance

V1 should not prioritize:

- graph canvas
- community detection
- full entity map
- graph query language
- GraphRAG answer engine

## Claim Control

Claim is powerful but risky.
If uncontrolled, it will create noise.

V1 control rules:

- Claim is hidden by default.
- Claim is not product-facing vocabulary.
- Claim is not directly edited by users.
- Claim must have a source anchor.
- Claim must have Ledger provenance.
- Claim extraction should be selective.
- LLM-inferred Claims default to candidate.
- Accepted Claims should be limited to clear decisions, constraints, facts, and preferences.
- Accepted Claim count per Gem should stay small.
- Contradiction, stale, duplicate, and unsupported signals should appear as Health Report items, not as unquestioned truth.

If Claim quality is poor, reduce extraction scope and schema.
Do not add more UI for users to clean up noisy Claims.

## Entity Map

Entity Map is a v1-next core feature.
It should not be forced into v1.

Entity Map will extract and connect people, products, projects, technologies, organizations, and concepts.
It can improve search, navigation, stale detection, import, and Refine quality.

V1 Context Graph schema should leave room for Entity Map.
V1 does not need to build the full entity graph.

## AI-Native Research Direction

Several current AI-native document and retrieval ideas support this direction:

- LLM-maintained wikis show that durable markdown context can be updated continuously instead of relying only on one-shot retrieval.[^llm-wiki]
- GraphRAG and LightRAG show that relationships and higher-level structure matter when questions require whole-corpus understanding.[^graphrag][^lightrag]
- Temporal context graphs show that provenance and time validity matter for agent memory.[^graphiti]
- `llms.txt` style publishing suggests that public context should be readable by agents as well as humans.[^llms-txt]
- PROV-O gives a useful model for provenance: derived-from, generated-by, and attributed-to relationships.[^prov-o]

The ACAC interpretation:

- canonical source remains Gem markdown
- Context Graph is derived and auditable
- Ledger provides provenance
- Relations exposes the useful parts to humans
- Claims stay hidden and controlled

## Non-Goals

V1 should not include:

- Notion-style block editor
- public anonymous write API
- Gem-level visibility or permissions
- team or organization permission model
- shared editing
- synced shared Trove
- origin write-back
- uncontrolled memory sync
- MCP implementation
- external user data connectors
- generic app state capture
- Forge Profiles
- productized migration from another document app
- graph database as canonical source
- graph canvas as the main UX
- GraphRAG answer engine as the main product
- user-facing Claim management
- full Entity Map

## Resolved Decisions

- Product category is AI-native context layer.
- Product name remains ACAC for now.
- Lapidary is a future brand candidate.
- Primary user is a Claude Code and Codex heavy solo builder or maker.
- ACAC stands independent from existing document apps.
- Account model has no separate workspace layer in v1.
- V1 starts with one active Forge.
- Troves are the publish, import, share, sync, and visibility unit.
- Multiple Troves are paid.
- Trove hierarchy is Project, Section, Gem.
- Quarry is Trove-specific.
- Refine to Trove is manually triggered.
- Forge contains Agents, Skills, Commands, and Memory.
- Memory belongs in Forge.
- Ledger is append-only hidden system history.
- Trove Ledger is v1 priority; Forge Ledger is system-store history for Forge changes.
- Chronicle is the generated read-only app view from Ledger, not editable source or a Gem tree folder.
- Context Graph is first-class derived layer.
- Relations is the user-facing graph surface.
- Claim is hidden internal primitive.
- Desktop App is the primary write surface.
- Web is read, publish, share, and import surface.
- CLI is v1 semantic action interface.
- MCP is future adapter.
- Read path is filesystem-speed local materialized source.
- Write path is semantic actions.
- ACAC cloud source store is canonical.
- Local markdown tree is materialized working copy.
- Sync is background.
- Publish is explicit.
- Telemetry covers ACAC operations, not user content.

## Remaining Open Questions

- Exact default Project and Section templates for a new Trove.
- Exact local materialized filesystem layout.
- Exact ACAC cloud source store schema.
- Exact Context Graph node and edge schema after prototype validation.
- Exact Relation Health thresholds.
- Exact Claim extraction budget and acceptance rules.
- Exact generated agent context format for Claude Code and Codex.
- Exact Web publish manifest format.
- Pricing limits for free and paid plans.
- Whether Forge Chronicle is needed in v1 or v1-next.
- Whether `llms.txt` support should ship in v1 or v1-next.

## Recommended Next Design Notes

The next durable notes should split this product model into detailed specs:

1. Source Store and Sync Model
2. Semantic Write Actions and Ledger Design
3. Context Graph and Relations Schema
4. Desktop App and Web Surface Design
5. Forge and Agent Runtime Sync Design

## Related Notes

- [[../index|AI Context as Code]]
- [[../../../../forge/_config/index|Forge Source]]
- [[../../../../forge/_config/Memory/MEMORY|ACAC Memory Index]]

[^llm-wiki]: Andrej Karpathy, "LLM Wiki", https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
[^graphrag]: Microsoft GraphRAG documentation, https://microsoft.github.io/graphrag/
[^lightrag]: LightRAG project, https://github.com/HKUDS/LightRAG
[^graphiti]: Graphiti documentation, https://help.getzep.com/graphiti/getting-started/overview
[^llms-txt]: `llms.txt` proposal, https://llmstxt.org/
[^prov-o]: W3C PROV-O, https://www.w3.org/TR/prov-o/

---
<sub>Page: <a href="https://acac.sh/trove/4dYzPkCVtG">https://acac.sh/trove/4dYzPkCVtG</a></sub>
