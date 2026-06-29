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

ACAC의 visual design system은 기존 reader app을 개선하는 작업이 아니에요.
현재 `site/` 구현, 기존 CSS, 기존 reader layout, 이전 reader design system 문서는 기준점으로 삼지 않아요.
이 문서는 ACAC 제품 모델에서 새 visual direction을 뽑아낸 core design 기준이에요.

ACAC는 AI-native context layer예요.
사람과 agent가 같은 context source를 읽고, 변경은 의미 있는 action과 검증 가능한 history를 통해 남겨요.
시각 방향은 이 제품 모델을 먼저 보여줘야 해요.

## Visual Positioning

ACAC의 본질은 **정교한 제작 도구이자 technical context system**이에요.
정물이나 보석 컨셉은 참고할 수 있지만, 제품의 중심 표현은 아니에요.
보석 컨셉은 `Quarry`, `Refine to Trove`, `Gem`, `Trove` 같은 모델을 설명하는 보조 은유로만 써요.

Core visual promise:

> ACAC helps people and agents turn rough context into durable, validated, readable context source.

이 약속은 다음 기준으로 화면에 나타나야 해요.

- 작업면은 조용하고 정교해야 해요.
- 읽기 surface는 filesystem처럼 빠르게 훑을 수 있어야 해요.
- 쓰기 surface는 semantic action, validation, history를 분명히 보여줘야 해요.
- AI-native 상태는 마법처럼 보이면 안 되고, 검증 가능한 작업 흐름처럼 보여야 해요.

Rejected wording:

- “정물/보석의 물성을 가진다”는 표현은 쓰지 않아요.
- 이 표현은 컨셉과 제품 본질을 섞어서 ACAC를 장식적인 UI로 오해하게 만들 수 있어요.

## Product Surface Split

Desktop App과 Web은 같은 제품처럼 느껴져야 하지만, 같은 layout을 공유하지 않아요.
공유할 것은 token, icon usage, 상태 표현, typography 원칙, semantic action 표현이에요.
분리할 것은 density, navigation, panel structure, primary job이에요.

### Desktop App

Desktop App은 write and agent workspace예요.
밀도 있고, source-aware하고, action-heavy해야 해요.

Desktop visual rules:

- Account Home에서 시작해요.
- Trove를 선택하면 Trove Home을 보여줘요.
- Gem을 선택하면 file tree, Gem editor/reader, right trust panel이 중심이 돼요.
- Forge는 Trove reader가 아니라 technical agent workspace로 보여줘요.
- Semantic actions는 숨은 file operation이 아니라 명명된 action으로 보여줘요.

### Web

Web은 read, publish, share, import surface예요.
Desktop editor의 read-only 복제가 아니라 public proof-of-work reader예요.

Web visual rules:

- Published Trove를 읽고 신뢰할 수 있게 해야 해요.
- File tree와 reader는 유지하되 Desktop보다 density를 낮춰요.
- Published Chronicle, import action, provenance, publish state가 중요해요.
- Web 첫 화면은 marketing hero가 아니라 Trove identity와 reader로 바로 이어져야 해요.

## Navigation Model

Gem 읽기는 일반 폴더 기반 filesystem tree처럼 보여야 해요.
Tree는 `Project`나 `Section` 의미에 고정 종속되지 않아요.
Trove마다 folder depth와 naming이 달라질 수 있어요.

Tree rules:

- 왼쪽 tree는 canonical markdown context만 보여줘요.
- `Gem`은 Trove 안의 file-like canonical context unit이에요.
- 일반 folder와 Gem row는 조용하고 촘촘하게 보여줘요.
- `.acac`, raw Ledger, generated indexes는 normal tree에 노출하지 않아요.
- Project와 Section 의미가 필요하면 breadcrumb, metadata, filter, validation context에서 보조로 보여줘요.

Tree 밖에 있어야 하는 surfaces:

- `Quarry`: 정제 전 입력함이에요.
- `Chronicle`: 사람이 읽는 generated history view예요.
- `Relations`: Context Graph를 사람이 이해하는 right panel이에요.
- `Ledger`: system log and audit substrate예요.

## Core Object Hierarchy

ACAC UI는 모델을 동등한 메뉴 항목으로 나열하지 않아요.
역할에 따라 위계를 나눠요.

Primary places:

- `Trove`: publish, import, share, sync, visibility의 단위예요.
- `Forge`: agent and system source workspace예요.

Trove internal units:

- `Quarry`: 아직 canonical Gem이 아닌 raw input이에요.
- `Gem`: refined, durable markdown context source예요.
- `Chronicle`: Gem 변경과 Refine 결과를 사람이 읽을 수 있게 보여주는 history예요.

Trust layers:

- `Relations`: related Gems, depends on, supports, stale/conflict, Refine guidance를 보여줘요.
- `Health`: validation, stale, conflict, proposal 상태를 보여줘요.
- `Ledger`: 사용자가 일반적으로 탐색하는 content가 아니라 evidence detail이에요.

## Home And Overview

Home은 일반 dashboard가 아니에요.
ACAC의 Home은 “지금 이어서 무엇을 해야 하는지”와 “어디가 막혀 있는지”를 보여주는 operational overview예요.

Account Home:

- 앱 첫 화면이에요.
- 상단은 continue working과 attention needed를 함께 보여줘요.
- 여러 Trove, Forge sync, 최근 의미 있는 작업, blocked proposal, conflict, stale signal을 보여줘요.

Trove Home:

- Trove를 선택하면 먼저 볼 수 있는 surface예요.
- Trove name, sync status, publish status, validation health를 보여줘요.
- Quarry items ready to refine, blocked proposals, conflicts, stale items를 보여줘요.
- Chronicle summary와 recent Ledger-backed activity를 보여줘요.
- 주요 action은 `New Quarry Item`, `Refine to Trove`, `Open Gem Tree`, `Publish Preview`예요.

History rules:

- 최근 history는 단순 file view log가 아니에요.
- `Ledger Entry`, `Refine result`, `Gem edit`, `Publish`, `Import`, `Revert` 같은 의미 있는 작업 단위 중심이에요.
- Recently viewed files는 보조 영역으로 낮춰요.

## Right Trust Panel

Desktop App의 오른쪽 panel은 항상 접근 가능해야 해요.
다만 사용자가 접었다 펼 수 있어야 해요.
좁은 화면이나 집중 읽기에서는 collapsed rail로 보여줄 수 있어요.

Panel groups:

- `Relations`: related Gems, supports, depends on
- `Health`: validation, stale, conflict, proposal, blocked state
- `Ledger Context`: affected paths, actor, entry link, revert availability
- `Refine Guidance`: placement hints, merge suggestions, unresolved issues

이 panel은 graph canvas가 아니에요.
사용자는 graph database를 보는 것이 아니라 context safety와 related context를 읽어야 해요.

## Ledger And Chronicle Visual Split

`Ledger`와 `Chronicle`은 강하게 다르게 보여야 해요.

Chronicle:

- user-facing history예요.
- 문장형 summary, 날짜 흐름, intent, result, remaining work를 보여줘요.
- Home, Trove Home, Web reader에서 노출될 수 있어요.

Ledger:

- user-facing content가 아니에요.
- system log and audit substrate예요.
- evidence detail, conflict explanation, revert confirmation에서 구조화된 log처럼 보여요.
- 일반 navigation tree에 노출하지 않아요.

같은 사건을 보더라도 Chronicle은 “무슨 일이 있었는지”를 설명하고, Ledger는 “무엇이 근거인지”를 보여줘야 해요.

## AI-Native State

AI-native state는 검증 가능한 작업 기록처럼 보여야 해요.
사용자가 AI reasoning을 보는 느낌을 주면 안 돼요.

Refine loading rules:

- 실제 작업 단계와 crafted status phrase를 함께 써요.
- 예시는 `Assaying input`, `Finding matching Gems`, `Polishing changes`, `Setting into Trove`, `Writing Ledger`, `Updating Chronicle`, `Checking conflicts`예요.
- 이 문구는 model chain-of-thought가 아니라 ACAC product operation state예요.
- 실패하거나 멈추면 바로 검증 결과와 blocked reason으로 전환해요.

State badges:

- 일반 상태어를 우선 써요.
- 기본 후보는 `Synced`, `Published`, `Draft`, `Proposal`, `Conflict`, `Stale`, `Validated`, `Blocked`, `Reverted`예요.
- Refine 주변에서만 crafted phrase를 허용해요.

## Color Direction

색은 모델 구분보다 상태 판단에 우선 써요.
`Trove`, `Quarry`, `Forge`, `Chronicle`, `Gem`을 각각 강한 색으로 고정하면 화면이 빨리 산만해져요.
모델 구분은 icon, section position, label, surface hierarchy로 해요.

Base direction:

- 기본 작업면은 light-first technical workspace예요.
- 본문과 editor surface는 읽기 쉬운 밝은 base를 써요.
- Slate, graphite, muted border tone으로 구조를 만들어요.
- Teal, green, amber, rust, blue-green 계열은 상태와 action에 신중하게 써요.

Surface-specific color rules:

- Desktop은 graphite workbench 느낌의 어두운 side surface를 일부 쓸 수 있어요.
- Web은 더 밝고 읽기 좋은 public proof-of-work surface여야 해요.
- Dark mode는 제품 정체성이 아니라 power-user option이에요.

Status color priority:

- Success and validated: teal or green
- Publish and sync: blue-green
- Warning and proposal: amber
- Conflict and blocked: rust or restrained crimson
- Neutral and system: slate or graphite

## Surface Depth And Radius

UI 자체는 3D가 아니에요.
3D는 icon asset의 역할이에요.
Panels, rows, logs, editor surface는 flat하고 정교해야 해요.

Depth rules:

- Shadow를 과하게 쓰지 않아요.
- Border, background tone, spacing으로 hierarchy를 만들어요.
- Glassmorphism, neumorphism, glossy button은 쓰지 않아요.
- 보석처럼 반짝이는 card UI는 쓰지 않아요.

Radius rules:

- 부드러운 rounded technical UI로 가요.
- Panels는 10-12px 정도를 기준으로 해요.
- Rows는 8px 안팎을 기준으로 해요.
- Badges and pills는 상태 표현에만 제한적으로 써요.
- 큰 rounded card가 화면을 채우는 dashboard 느낌은 피해야 해요.

## Icon System

Icon은 새로 만들지 않고 준비된 asset을 기준으로 써요.
현재 core icon source assets:

- `forge/_assets/icons/trove-jewel-casket-source-chroma.png`
- `forge/_assets/icons/gem-teal-source-chroma.png`
- `forge/_assets/icons/quarry-raw-shard-source-chroma.png`
- `forge/_assets/icons/forge-workshop-alcove-icon-source-chroma-magenta.png`
- `forge/_assets/icons/chronicle-imperial-open-folio-source-chroma.png`

Icon usage rules:

- 3D icon은 top-level concept marker예요.
- 개념 설명, empty state, result summary, onboarding, sidebar section header에 써요.
- Gem row마다 반복하지 않아요.
- 일반 folder와 file row는 filesystem처럼 조용해야 해요.
- Chroma source asset은 그대로 제품 UI에 노출하지 않아요.
- Product UI에는 배경 제거 또는 mask 처리된 파생 asset을 써야 해요.

Sidebar usage:

- `Trove`, `Quarry`, `Forge`, `Chronicle` 같은 section header 앞에 icon을 둘 수 있어요.
- `Gem` icon은 Gem 개념 설명, 생성 완료, Refine result summary 같은 중요한 순간에만 써요.

## Component Grammar

ACAC의 기본 component 문법은 cards가 아니에요.
기본은 **panels, rows, logs**예요.

Core components:

- Gem file row
- Gem editor and reader surface
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
- Sync, publish, import state row
- Revert Ledger Entry confirmation and result

Card rules:

- Card는 Trove switcher, publish/import preview, empty state처럼 묶음 단위가 필요할 때만 써요.
- 큰 card를 반복해서 dashboard처럼 만들지 않아요.
- Card 안에 card를 넣지 않아요.

## Markdown Rendering

Gem body와 Web reader는 markdown document readability를 우선해요.
주변 UI는 tool information density를 유지해요.

Required markdown rendering components:

- headings
- paragraphs
- links
- ordered and unordered lists
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

- Gem body는 순수 markdown renderer예요.
- ACAC 전용 block syntax를 새로 만들지 않아요.
- ACAC가 semantic action으로 내용을 만들더라도 Gem 안에 들어가면 markdown으로 보여요.

Tool surface rules:

- `Refine result`, `Validation/Conflict`, `Ledger Entry detail`, `Chronicle entry`, `Relations`, `Frontmatter form`은 body 밖 tool component예요.
- Source markdown과 ACAC-generated tool surface는 시각적으로 구분되어야 해요.

## Frontmatter Rendering

Frontmatter는 기본 노출해요.
하지만 raw YAML block처럼 보이면 안 돼요.
Gem 상단에서 가독성 좋은 metadata renderer로 보여줘야 해요.

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

Source mode에서는 raw frontmatter를 볼 수 있어요.
Web reader에서는 public-safe metadata만 노출해요.

## Quarry Direction

Quarry는 정제 전 입력함이에요.
`raw material bench` 같은 표현은 쓰지 않아요.
그 표현은 ACAC UI를 과하게 은유적으로 만들 수 있어요.

Quarry rules:

- Quarry item은 아직 canonical Gem이 아니에요.
- Quarry UI는 inbox처럼 명확해야 해요.
- `Refine to Trove`가 Quarry의 main action이에요.
- Quarry item은 새 Gem이 되거나, 기존 Gem에 흡수되거나, 여러 Gem으로 나뉠 수 있어요.
- UI는 “아직 canonical source가 아니다”를 시각적으로 구분해야 해요.

Quarry state candidates:

- `Raw`
- `Ready`
- `Refining`
- `Proposal`
- `Absorbed`
- `Split`
- `Blocked`

## Forge Direction

Forge는 Trove와 같은 reader가 아니에요.
Forge는 technical agent workspace예요.

Forge visual rules:

- `Agents`, `Skills`, `Commands`, `Memory`를 중심으로 보여줘요.
- 문서처럼 읽고 편집할 수 있지만, runtime sync와 validation state가 더 중요해요.
- Forge 변경은 agent behavior를 바꿀 수 있으므로 위험한 변경은 proposal 또는 confirmation이 필요해요.
- Forge icon은 sidebar section header와 Forge overview에서 강하게 쓸 수 있어요.

## Non-Goals

ACAC visual design system은 다음 방향을 피해야 해요.

- Notion clone
- Obsidian clone
- generic document app clone
- generic AI gradient
- graph canvas-first UI
- over-fantasy jewel UI
- marketing hero-first Web
- oversized card dashboard
- low-density dashboard
- chat app처럼 보이는 Quarry
- glossy 3D UI controls
- Ledger를 예쁜 user-facing timeline으로 포장하는 것
- Markdown body 안에 ACAC 전용 block system을 만드는 것

## Resolved Decisions

- Visual identity is a precise crafted tool and technical context system.
- Still-life and jewel concepts are reference material, not the product identity sentence.
- Desktop and Web share tokens, state language, icon rules, and typography principles, but not layout density.
- Desktop starts with Account Home, then Trove Home, Gem workspace, or Forge workspace.
- Web is a public proof-of-work reader, not a read-only clone of Desktop.
- Gem reading uses a normal filesystem-like tree.
- Quarry, Chronicle, Relations, and Ledger live outside the Gem tree.
- Right trust panel is always accessible and collapsible.
- Ledger is system log / audit substrate, not normal user-facing content.
- Chronicle is human-readable generated history.
- Colors prioritize state, not model identity.
- UI is flat technical surface; 3D belongs to prepared icon assets.
- Radius is soft but controlled.
- Core component grammar is panels, rows, and logs.
- Markdown body is pure markdown rendering.
- ACAC tool components live outside the markdown body.
- Frontmatter is visible by default through a readable metadata renderer.
- Next durable design artifact after this note should be a design token spec or a layout spec.

## Remaining Open Questions

- Exact color token values and contrast ratios.
- Exact light and dark mode token mapping.
- Exact Account Home and Trove Home layout.
- Exact right trust panel information architecture.
- Exact markdown renderer spacing, table, code, and callout styling.
- Exact product-ready icon processing pipeline for chroma source assets.
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
