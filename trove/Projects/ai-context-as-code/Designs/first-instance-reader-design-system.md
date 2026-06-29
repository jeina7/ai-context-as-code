---
type: design
title: "첫 번째 인스턴스 Reader 디자인 시스템"
description: "ACAC 첫 public-safe context reader의 토큰, 컴포넌트 규칙, 반응형 화면 기준"
status: active
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: ReaderDS01

---

# 첫 번째 인스턴스 Reader 디자인 시스템

ACAC 첫 public reader는 landing page가 아니라 읽기 가능한 context 작업 화면이에요.
이 문서는 `site/index.html`, `site/assets/style.css`, `site/assets/app.js`가 따라야 하는 디자인 기준을 설명해요.
목표는 개인 문서 모음을 예쁘게 감싸는 것이 아니라, public-safe context operating system reader처럼 보이게 하는 거예요.
첫 구현은 vanilla HTML, CSS, JavaScript만 사용하고, 외부 런타임 연결 없이 generated JSON과 markdown payload만 읽어요.

## 제품 표면 원칙

- 첫 화면은 제품 소개 hero가 아니라 dashboard예요.
- 사용자는 `Daily/`, `Projects/`, `forge/_config/`, `forge/_archived/`의 역할을 바로 구분할 수 있어야 해요.
- `forge/_assets/`는 storage라서 navigation, search, dashboard 어디에도 지식 섹션으로 노출하지 않아요.
- `forge/_config/`와 `forge/_archived/`는 숨기지 않고 FORGE layer로 구분해요.
- 모든 화면은 public-safe, read-only, generated output boundary를 드러내야 해요.

## 색상 토큰

Light mode가 현재 구현 기준이에요.
Dark mode는 아직 runtime 적용 범위가 아니지만, 같은 semantic token 이름으로 쓸 palette draft를 같이 보관해요.
색은 장식보다 상태와 계층을 설명하는 데 써요.
TROVE icon의 확정 색상은 teal 계열이므로, reader identity도 teal을 primary로 써요.
Tailwind CSS 기본 팔레트의 teal, cyan, slate, emerald, amber, rose 계열을 참고해서 더 선명한 색감을 써요.[^tailwind-colors]

`weak`는 글자색이 아니라 약한 배경 tint를 뜻해요.
낮은 강조 글자는 `muted`나 `faint`를 써요.
`primary`는 제품감 있는 면과 icon-adjacent accent에 쓰고, 일반 링크와 작은 텍스트에는 접근성 대비가 더 좋은 `primary-strong`을 써요.

### Primitive Palette

Primitive palette는 색 원재료예요.
컴포넌트는 가능하면 아래 값을 직접 쓰지 않고 semantic token을 써요.

| Token | Hex | Use |
|---|---|---|
| `--teal-10` | `#f8fffe` | near-white sidebar surface |
| `--teal-50` | `#f0fdfa` | primary faint background |
| `--teal-100` | `#ccfbf1` | primary weak background |
| `--teal-200` | `#99f6e4` | soft selected state |
| `--teal-300` | `#5eead4` | primary line and bright edge |
| `--teal-400` | `#2dd4bf` | vivid hover accent or icon support |
| `--teal-500` | `#14b8a6` | living product primary |
| `--teal-600` | `#0d9488` | filled action hover |
| `--teal-700` | `#0f766e` | accessible primary text and link |
| `--teal-800` | `#115e59` | pressed or high-emphasis primary |
| `--teal-900` | `#134e4a` | deep primary surface |
| `--cyan-500` | `#06b6d4` | small spark, graph/data highlight only |
| `--slate-50` | `#f8fafc` | page background |
| `--slate-100` | `#f1f5f9` | muted surface |
| `--slate-200` | `#e2e8f0` | default line |
| `--slate-300` | `#cbd5e1` | strong line |
| `--slate-400` | `#94a3b8` | faint text |
| `--slate-500` | `#64748b` | muted text |
| `--slate-600` | `#475569` | secondary text |
| `--slate-700` | `#334155` | body text |
| `--slate-900` | `#0f172a` | heading text |
| `--slate-950` | `#020617` | dark preview background |

### Semantic Tokens

Semantic tokens are the names components should use.
The first CSS implementation can keep existing `accent` aliases while migrating them to `primary`.

| Role | Token | Hex | Use |
|---|---|---:|---|
| Page background | `--color-bg` | `#f8fafc` | reader 뒤의 깨끗한 slate 배경이에요. |
| Reader canvas | `--color-canvas` | `#ffffff` | 우측 panel과 일부 보조 영역의 바탕이에요. |
| Sidebar | `--color-sidebar` | `#f8fffe` | `teal-10` near-white surface예요. Sidebar 구분은 border와 selected row가 맡아요. |
| Surface | `--color-surface` | `#ffffff` | module, input, state card의 기본 면이에요. |
| Muted surface | `--color-surface-muted` | `#f1f5f9` | code, table header, 낮은 강조 영역이에요. |
| Primary | `--color-primary` | `#14b8a6` | product accent, active surface, icon-adjacent detail에 써요. |
| Primary strong | `--color-primary-strong` | `#0f766e` | link, focus, selected text처럼 작은 글자에 써요. |
| Primary weak | `--color-primary-weak` | `#ccfbf1` | selected row, soft badge, search result hover에 써요. |
| Primary line | `--color-primary-line` | `#5eead4` | primary 관련 border와 subtle divider에 써요. |
| Primary spark | `--color-primary-spark` | `#06b6d4` | relation map, graph point, 순간적인 highlight에 제한적으로 써요. |
| Text | `--color-text` | `#334155` | 본문 텍스트예요. |
| Heading | `--color-heading` | `#0f172a` | 제목과 가장 높은 대비 텍스트예요. |
| Muted text | `--color-muted` | `#64748b` | path, metadata, 설명에 써요. |
| Faint text | `--color-faint` | `#94a3b8` | placeholder와 낮은 우선순위 meta에만 써요. |
| Line | `--color-line` | `#e2e8f0` | 기본 border예요. |
| Strong line | `--color-line-strong` | `#cbd5e1` | control border, panel split에 써요. |
| Success | `--color-success` | `#047857` | active, public, read-only처럼 정상 상태에 써요. |
| Success weak | `--color-success-weak` | `#d1fae5` | success 상태의 약한 배경이에요. |
| Warning | `--color-warning` | `#facc15` | yellow mango warning icon, badge fill, attention accent에 써요. |
| Warning strong | `--color-warning-strong` | `#a16207` | broken wikilink text, dotted underline, warning text에 써요. |
| Warning weak | `--color-warning-weak` | `#fef9c3` | warning 상태의 약한 배경이에요. |
| Danger | `--color-danger` | `#e11d48` | excluded/private 같은 막힌 상태가 필요할 때 써요. |
| Danger weak | `--color-danger-weak` | `#ffe4e6` | danger 상태의 약한 배경이에요. |

`primary`인 `#14b8a6`는 product color라서 생동감이 좋아요.
하지만 흰 surface 위 작은 텍스트에는 대비가 부족하므로, 링크와 focus text는 `primary-strong`인 `#0f766e`를 기본으로 써요.
`warning`도 같은 방식이에요.
`#facc15`는 yellow mango warning accent로 쓰고, 작은 warning text에는 `warning-strong`인 `#a16207`를 써요.

### Dark Mode Semantic Tokens

Dark mode도 같은 semantic token 이름을 써요.
값만 바꿔서 component code가 light/dark를 따로 알 필요 없게 해요.
아직 실제 CSS 적용이나 theme toggle은 만들지 않아요.

| Role | Token | Hex | Use |
|---|---|---:|---|
| Page background | `--color-bg` | `#020617` | 가장 바깥의 deep slate 배경이에요. |
| Reader canvas | `--color-canvas` | `#0f172a` | reader panel의 기본 바탕이에요. |
| Sidebar | `--color-sidebar` | `#031f1e` | dark mode의 깊은 teal sidebar예요. |
| Surface | `--color-surface` | `#111827` | module, input, state card의 기본 면이에요. |
| Muted surface | `--color-surface-muted` | `#1e293b` | code, table header, 낮은 강조 영역이에요. |
| Primary | `--color-primary` | `#2dd4bf` | dark surface 위 product accent예요. |
| Primary strong | `--color-primary-strong` | `#99f6e4` | link, focus, selected text처럼 작은 글자에 써요. |
| Primary weak | `--color-primary-weak` | `#134e4a` | selected row, soft badge, search result hover에 써요. |
| Primary line | `--color-primary-line` | `#0d9488` | primary 관련 border와 subtle divider에 써요. |
| Primary spark | `--color-primary-spark` | `#22d3ee` | relation map, graph point, 순간적인 highlight에 제한적으로 써요. |
| Text | `--color-text` | `#e2e8f0` | 본문 텍스트예요. |
| Heading | `--color-heading` | `#f8fafc` | 제목과 가장 높은 대비 텍스트예요. |
| Muted text | `--color-muted` | `#94a3b8` | path, metadata, 설명에 써요. |
| Faint text | `--color-faint` | `#64748b` | placeholder와 낮은 우선순위 meta에만 써요. |
| Line | `--color-line` | `#1e293b` | 기본 border예요. |
| Strong line | `--color-line-strong` | `#334155` | control border, panel split에 써요. |
| Success | `--color-success` | `#34d399` | active, public, read-only처럼 정상 상태에 써요. |
| Success weak | `--color-success-weak` | `#022c22` | success 상태의 어두운 약한 배경이에요. |
| Warning | `--color-warning` | `#facc15` | yellow mango warning icon, badge fill, attention accent에 써요. |
| Warning strong | `--color-warning-strong` | `#fde047` | broken wikilink text, dotted underline, warning text에 써요. |
| Warning weak | `--color-warning-weak` | `#422006` | warning 상태의 어두운 약한 배경이에요. |
| Danger | `--color-danger` | `#fb7185` | excluded/private 같은 막힌 상태가 필요할 때 써요. |
| Danger weak | `--color-danger-weak` | `#4c0519` | danger 상태의 어두운 약한 배경이에요. |

Dark mode에서는 `primary`가 `#2dd4bf`라서 light mode보다 밝아요.
다크 표면 위에서는 색이 더 어두워 보이므로, 작은 링크와 selected text는 `primary-strong`인 `#99f6e4`를 써요.
`warning`은 light mode와 같은 yellow mango를 유지하고, warning text만 더 밝은 `#fde047`로 올려요.

## State Tokens

상태는 색 하나로만 설명하지 않아요.
배경, border, text, icon을 같이 써서 작은 화면과 낮은 대비 환경에서도 의미가 남아야 해요.
상태 이름은 component가 쓰는 의미 이름이고, light/dark mode에서는 같은 이름에 다른 값을 넣어요.

| State | Token pattern | 기준 |
|---|---|---|
| Default | `surface`, `text`, `line` | 일반 row, module, panel의 기본 상태예요. |
| Hover | `surface-muted`, `line-strong` | 클릭 가능한 영역임을 살짝 보여줘요. |
| Selected | `primary-weak`, `primary-strong` | active route, selected search result, chosen filter에 써요. |
| Focus | `primary`, `primary-line` | keyboard focus ring과 input focus에 써요. |
| Success | `success-weak`, `success` | public, active, read-only, passed 상태에 써요. |
| Warning | `warning-weak`, `warning-strong`, `warning` | broken wikilink, build warning, attention 상태에 써요. |
| Danger | `danger-weak`, `danger` | private, excluded, fatal, destructive affordance에 써요. |
| Disabled | `surface-muted`, `faint`, `line` | 지금은 불가능하지만 설명이 필요한 control에 써요. |
| Loading | `surface-muted`, `line` | skeleton line만 짧게 보여주고 shimmer는 쓰지 않아요. |

`weak` 배경 위에 같은 계열 strong text를 올리는 조합을 기본으로 해요.
`warning`처럼 밝은 accent는 text color로 바로 쓰지 않고, 작은 글자는 `warning-strong`을 써요.

## Typography

Reader는 긴 설명보다 빠른 판단과 문서 읽기를 우선해요.
큰 글자는 첫 화면 이름과 note title에만 써요.

| 역할 | 크기 | 기준 |
|---|---:|---|
| Micro label | 11px | section label, uppercase label |
| Metadata | 12-13px | path, pill, context meta |
| UI body | 14px | sidebar, list, panel text |
| Document body | 16px | markdown paragraph |
| Small heading | 18px | h3, compact heading |
| Section heading | 22px | document h2 |
| Page title | 30px | Home, Note, Search title |

Line-height는 본문 1.7 안팎, UI text 1.45 안팎으로 둬요.
글자 간격은 0으로 두고, viewport width에 따라 font size를 키우지 않아요.

## Spacing

간격은 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48px scale을 써요.
반복 item은 촘촘하게, reader header와 dashboard module 사이는 넉넉하게 둬요.

- Sidebar row: 26px 안팎으로 촘촘하게 유지하고, chevron 칸과 depth padding은 제목 폭을 침범하지 않게 최소화해요.
- Metadata pill: 24px 이상 높이를 유지해요.
- Dashboard module: 16-20px 안쪽 여백을 기본으로 해요.
- Reader page padding: desktop에서는 40px 이상, mobile에서는 16-20px로 줄여요.
- Table과 code block은 가로 scroll을 허용해요.

## Density Rules

Reader는 반복해서 훑어보는 작업 화면이에요.
정보는 촘촘해야 하지만, clickable target과 읽기 흐름은 안정적이어야 해요.

| Area | Density 기준 |
|---|---|
| Sidebar tree | row height 26-30px, title 우선, icon 최소화예요. |
| Sidebar controls | search, submit, collapse, close button은 34-40px target을 유지해요. |
| Note header | breadcrumb와 metadata는 작게, H1과 summary는 넉넉하게 둬요. |
| Markdown body | paragraph line-height는 1.65-1.75 안팎으로 둬요. |
| Context panel | 보조 정보라서 card보다 list rhythm을 우선해요. |
| Search palette | 결과 row는 64-76px 안에서 title, path, snippet을 안정적으로 담아요. |
| Status pill | height 24px 이상, label은 1줄 유지가 기본이에요. |
| Mobile | 좌우 padding은 16-20px, row text는 말줄임보다 줄바꿈을 먼저 고려해요. |

작은 버튼은 icon-only일 때 더 안전해요.
텍스트 버튼은 명령이 분명할 때만 쓰고, label이 길어지면 줄바꿈보다 짧은 동사로 바꿔요.

## Border, Radius, Shadow

ACAC는 작업 도구라서 둥근 장식이 커지면 안 돼요.
다만 sidebar controls는 제품 표면처럼 보여야 하므로, 작은 버튼과 input에는 더 부드러운 rounded surface를 써요.

- Repeated row: border-top으로 구분해요.
- Sidebar item: compact한 8-10px radius를 써요.
- Sidebar control: search, shortcut hint, submit, collapse, close button은 같은 soft rounded surface를 써요.
- Module과 state card: 8px 이하 radius를 써요.
- Shadow는 drawer와 중요한 state card에만 제한적으로 써요.
- Section 자체를 큰 floating card처럼 만들지 않아요.

## Surface 계층

`surface`는 화면의 의미 계층이에요.
단순 장식 박스가 아니어야 해요.

| 계층 | 쓰임 |
|---|---|
| Background | 전체 reader의 조용한 바탕 |
| Sidebar surface | source tree와 search entry |
| Reader surface | 문서와 dashboard의 주 작업 영역 |
| Module surface | Start here, Build status, FORGE 같은 의미 block |
| State card | missing, empty, fatal build output 같은 예외 상태 |

카드 안에 또 카드를 넣지 않아요.
반복 문서는 list row로 처리하고, module은 정보 묶음에만 써요.

## Icon System

Icon은 장식이 아니라 ACAC 개념을 구분하는 작은 물성 언어예요.
Top-level concept만 product icon을 쓰고, 일반 file/folder row에는 큰 아이콘을 넣지 않아요.
아이콘은 18-24px에서도 실루엣과 색으로 읽혀야 해요.

### Icon Grammar

- Style: polished 3D emoji-like product icon이에요.
- View: three-quarter front/top angle을 기본으로 해요.
- Shape: squat, compact, stable silhouette을 우선해요.
- Surface: large facets, soft bevels, clean highlights만 써요.
- Background source: generated source는 flat `#ff00ff` chroma-key 배경으로 만들어요.
- Detail: text, glyph, rune, letter, internal stripe, busy decoration은 쓰지 않아요.
- QA: 18px, 24px, 32px preview에서 역할이 읽히는지 확인해요.

### Concept Icons

| Concept | Visual metaphor | 기준 |
|---|---|---|
| Quarry item | raw shard | 아직 정제 전 raw input이라 거칠고 임시적인 조각처럼 보여요. 확정 source asset은 `forge/_assets/icons/quarry-raw-shard-source-chroma.png`예요. |
| Quarry | shallow sorting basin | raw input이 잠시 머무는 곳이라 open tray나 basin 느낌이에요. |
| Gem | polished teal emerald memory gem | Trove 안의 canonical knowledge unit이에요. 확정 source asset은 `forge/_assets/icons/gem-teal-source-chroma.png`예요. |
| Trove | curated gem vessel | 정리된 canonical notes가 들어가는 보관함/컬렉션이에요. Treasure chest처럼 보이면 안 돼요. 확정 source asset은 `forge/_assets/icons/trove-jewel-casket-source-chroma.png`예요. |
| Note | markdown unit | Trove 안의 개별 문서예요. Sidebar row에서는 icon보다 title 공간을 우선해요. |
| Forge | dark system-forge block | agent 규칙과 도구 문서가 있는 system 영역이에요. Gear나 hammer icon으로 가지 않아요. |
| Ledger | transaction record block | 변경 transaction의 SSOT라서 정확하고 단단한 기록면처럼 보여요. |
| Chronicle | readable history view | Ledger에서 생성된 사람용 기록 view라서 layered reading surface 느낌이에요. 확정 source asset은 `forge/_assets/icons/chronicle-story-folio-source-chroma.png`예요. |

Trove와 Forge는 sidebar section heading에서 icon + label 조합으로 보여줘요.
Gem, Quarry item, Ledger, Chronicle은 dashboard, relation preview, future workflow view에서 쓰는 개념 icon이에요.

## Dark Mode Rules

Dark mode는 단순히 light mode를 반전하지 않아요.
같은 역할의 token 이름을 유지하고, surface depth와 accent brightness를 dark surface에 맞게 다시 정해요.

- Background는 `slate-950`, reader canvas는 `slate-900` 계열로 둬요.
- Sidebar는 deep teal을 써서 Trove identity가 남게 해요.
- Text는 `heading`, `text`, `muted`, `faint`의 4단계만 써요.
- Primary는 light mode보다 밝게 올리고, text link는 `primary-strong`을 써요.
- Weak state는 어두운 tint예요. Light mode처럼 밝은 tint를 쓰지 않아요.
- Warning은 yellow mango identity를 유지하되, text에는 더 밝은 `warning-strong`을 써요.
- Shadow는 더 줄이고, depth는 surface color와 border로 구분해요.
- Runtime theme toggle, OS preference sync, persisted preference는 이번 범위가 아니에요.

## Component Rules

### Sidebar

- Brand, search, TROVES, FORGE 순서로 둬요.
- Brand mark는 단순한 글자 박스가 아니라 ACAC의 context/gem/route 느낌을 담은 작은 logo-like mark로 보여줘요.
- `Daily/`와 `Projects/`는 TROVES예요.
- `forge/_config/`와 `forge/_archived/`는 divider 아래 FORGE예요.
- Sidebar folder는 chevron으로 접고 펼쳐요.
- Current route가 들어있는 folder는 자동으로 열려 있어야 해요.
- `dir`, `day`, `des`, `dec`, `ref`, `log` 같은 텍스트 badge는 쓰지 않아요.
- TROVES와 FORGE section heading은 emoji가 아닌 inline SVG icon과 label 조합으로 보여줘요.
- TROVES icon은 trove/gem/treasure 느낌, FORGE icon은 making/system layer 느낌이어야 해요.
- File/folder row에는 큰 아이콘을 넣지 않아요. 긴 제목 공간을 우선해요.
- `forge/_config`와 `forge/_archived` raw folder name은 1차 navigation label로 노출하지 않고 `Operating layer`, `Archive`를 써요.
- `forge/_assets/`는 보이지 않아야 해요.
- Active route는 accent-soft rounded selected state와 `aria-current="page"`로 표시해요.
- Desktop에서는 drawer close X를 보이지 않게 하고, collapse/expand button만 보여줘요.
- Mobile drawer에서는 close X를 유지하되 search, shortcut, submit, collapse button과 같은 visual language를 써요.

### Reader

- Note 화면은 breadcrumb, metadata strip, H1, summary, markdown body 순서예요.
- Source path는 breadcrumb와 metadata에서만 작게 보여줘요.
- H1은 source markdown의 frontmatter `title`과 같아야 해요.
- Summary는 H1 아래 3-5줄 context preview로 보여주고, 본문에서는 중복 표시를 줄여요.
- Wikilink는 일반 link보다 살짝 더 문서 연결처럼 보여요.
- Broken wikilink는 warning 색과 dotted underline으로 표시해요.

### Context Panel

- Context panel은 보조 정보예요.
- Document metadata, table of contents, connection counts, 1-hop relation map, backlinks, outgoing links, related context 순서로 보여줘요.
- Mobile과 tablet에서는 reader 아래로 내려가요.
- Full graph view는 이번 범위가 아니에요.
- Relation map은 `data/graph.json`에서 현재 문서 주변 1-hop 관계만 읽어요.

### Search

- Search는 `/search?q=<query>` route를 써요.
- Header search trigger와 mobile search button은 quick navigation palette를 열어요.
- Desktop shortcut은 macOS에서 `Cmd+K`, Windows/Linux에서 `Ctrl+K`예요.
- Palette는 `role="dialog"` 기반 modal로 열고, input이 첫 focus를 가져요.
- Palette 결과 목록은 fixed-height scroll 영역을 쓰고, `ArrowDown`/`ArrowUp`/`Enter`/`Esc` keyboard flow를 지원해요.
- Input이 비어 있으면 recent 또는 suggested public notes를 보여줘요.
- Palette에서 focused result가 없을 때 `Enter`를 누르면 `/search?q=<query>` full results view로 이동해요.
- 결과는 title, path, summary, type/status/layer label을 보여줘요.
- `forge/_config/`와 `forge/_archived/` 결과에는 layer label을 붙여요.
- `forge/_assets/`는 검색 결과에 나오면 안 돼요.
- 없는 결과에서 새 문서 만들기를 권하지 않아요. 첫 구현은 read-only예요.

### Home Dashboard

- Home은 product dashboard예요.
- Trove map, Start here, Current project, Today, FORGE, Build status를 보여줘요.
- Build status는 public note 수, warning 수, repo-injected manual analytics beacon 여부만 작게 보여줘요.
- README는 source boundary 설명으로 보여주되 첫 화면의 주인공이 되지 않게 해요.

### Loading, Empty, Missing

- Loading은 실제 reader body와 같은 width, 같은 시작점에서 skeleton line으로 짧게 보여줘요.
- Missing note는 route와 home/search entry를 보여줘요.
- Empty trove는 public notes가 거의 없다는 사실과 source boundary를 보여줘요.
- Fatal build output state는 generated JSON을 읽지 못했음을 분명히 말해요.

## Component Examples

이 예시는 component가 token을 어떤 조합으로 써야 하는지 보여주는 기준이에요.
실제 CSS class 이름은 구현하면서 달라질 수 있지만, 의미 조합은 유지해요.

| Component | Token use | 기준 |
|---|---|---|
| Active sidebar row | `primary-weak` bg, `primary-strong` text | 현재 route를 보여줘요. |
| Sidebar section heading | `muted` text, concept icon | TROVES와 FORGE를 구분해요. |
| Search input | `surface`, `line`, focus `primary-line` | 입력 가능한 control임을 보여줘요. |
| Search result hover | `primary-weak` bg, `heading` text | 결과 row가 선택 가능함을 보여줘요. |
| Metadata pill | `surface-muted` bg, `muted` text | 낮은 강조 정보예요. |
| Success pill | `success-weak` bg, `success` text | public, active, passed 상태예요. |
| Warning callout | `warning-weak` bg, `warning` border, `warning-strong` text | broken wikilink와 build warning에 써요. |
| Danger callout | `danger-weak` bg, `danger` text | private, excluded, fatal 상태에 써요. |
| Primary button | `primary` bg, white or dark readable text | 명확한 주요 command에만 써요. |
| Soft action button | `surface` bg, `primary-line` border, `primary-strong` text | 보조 command에 써요. |

Component example은 기능 설명 문구로 화면에 노출하지 않아요.
사용자는 설명을 읽어서 쓰는 것이 아니라, 배치와 상태 표현만 보고 이해해야 해요.

## Responsive 기준

Desktop은 3-column layout이에요.

```text
sidebar 296px | reader flexible | context panel 320px
```

Tablet은 2-column에 가까워져요.
좌측 sidebar와 reader를 유지하고, context panel은 reader 아래로 내려요.

Mobile은 reader-first예요.

- Top bar에는 menu, home brand, search entry만 둬요.
- Sidebar는 full-height drawer로 열어요.
- Drawer search button은 drawer를 연 뒤 search input으로 focus를 보내요.
- Context panel은 문서 하단 section처럼 보여요.
- 긴 path, title, pill은 줄바꿈하거나 말줄임하고 겹치지 않게 해요.

## Data Boundary

UI는 `trove/` 파일 시스템을 직접 추측하지 않아요.
아래 generated data만 읽어요.

- `data/tree.json`
- `data/notes.json`
- `data/search-index.json`
- `data/backlinks.json`
- `data/graph.json`
- `data/home.json`
- `data/build.json`
- `content/trove/<id>.md`

`scripts/build_trove.py`는 Home dashboard에 필요한 최신 Daily, Design, Decision, Worklog pointer를 `home.json`에 넣어요.
이것은 runtime feature가 아니라 build-time metadata예요.

`data/graph.json`은 bounded relation preview용 static data예요.
초기 계약은 note `nodes[]`, `wikilink`/`backlink`/`folder`/`project` `edges[]`, layer/project/folder `clusters`를 포함해요.
UI는 이것으로 현재 note 주변 1-hop relation map만 보여주고, full interactive graph는 만들지 않아요.

## 이번에 하지 않을 것

- Marketing landing page를 만들지 않아요.
- Editable CMS, 새 노트 생성, 삭제, 이동, rename을 만들지 않아요.
- Claude Code live connection, MCP, hooks, automatic memory sync를 만들지 않아요.
- Dark mode runtime theme toggle과 CSS 적용은 만들지 않아요. Palette draft만 design note에 보관해요.
- Full graph view, favorites, tabs, presentation mode를 만들지 않아요.
- Private vault reader나 auth gate를 만들지 않아요.

## 확인 기준

- Home, Note, Search, Missing, Loading 상태가 같은 토큰과 컴포넌트 규칙을 써요.
- Desktop에서 3-column layout이 안정적으로 보여요.
- Mobile에서 drawer, reader, context panel이 겹치지 않아요.
- Search result에 layer label이 붙고 `forge/_assets/`는 보이지 않아요.
- Broken wikilink는 warning 상태로 보이고 클릭 가능한 정상 링크처럼 오해되지 않아요.
- `python3 scripts/deploy_check.py`가 통과해야 해요.

[^tailwind-colors]: Tailwind CSS current color docs define a default palette with `50` through `950` steps and CSS theme variables. The hex values here use the official Tailwind v3 default color palette reference for teal, cyan, slate, emerald, amber, and rose.

---
<sub>Page: <a href="https://acac.sh/trove/ReaderDS01">https://acac.sh/trove/ReaderDS01</a></sub>
