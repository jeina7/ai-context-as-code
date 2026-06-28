---
name: reader-tree-and-relational-context-map-follow-up
title: "Reader Tree와 Relational Context Map 개선 요구사항"
description: "ACAC reader의 sidebar tree, trove layer naming, loading skeleton, graph-based context map 후속 개선 범위"
type: design
status: draft
date: 2026-06-29
created: 2026-06-29
updated: 2026-06-29
visibility: public
id: TreeCtxM01

---

# Reader Tree와 Relational Context Map 개선 요구사항

이 문서는 ACAC public reader 배포 후 확인된 sidebar tree와 relational context map 후속 개선 요구사항을 기록해요.
목표는 현재 제품형 reader의 큰 구조를 유지하면서, 문서 트리를 Obsidian처럼 읽고 조작하기 쉬운 탐색 surface로 개선하는 거예요.
또한 기존 ACAC 설계가 전제한 graph 기반 문서 indexing과 relational context map을 다음 구현 범위로 올려요.
이 작업은 read-only static reader 범위 안에서 진행하고, 외부 런타임 연결이나 편집 기능은 추가하지 않아요.

## 배경

현재 reader는 product dashboard와 note/search/missing 상태를 갖춘 첫 public-safe reader로 배포됐어요.
다만 sidebar tree는 아직 `dir`, `day`, `des`, `ref` 같은 텍스트 badge가 앞에 붙고, 폴더가 항상 펼쳐져 있어요.
첨부된 현재 화면 기준으로는 badge가 가로 공간을 많이 차지해서 긴 제목이 잘려 보이고, folder와 note의 시각적 차이가 제품답게 정리되지 않았어요.
또한 `_config`, `_archived` 같은 실제 폴더명이 그대로 드러나면 ACAC의 trove 개념보다 파일 시스템 구현 디테일이 먼저 보이는 문제가 있어요.

## 반드시 반영할 요구사항

### Obsidian-like collapsible tree

- Sidebar 문서 트리는 Obsidian처럼 폴더를 접었다 펼칠 수 있어야 해요.
- Folder row에는 expand/collapse affordance가 있어야 해요.
- Current route가 안에 있는 folder는 자동으로 열려 있어야 해요.
- 사용자가 직접 펼친 상태는 최소한 현재 브라우저 세션 안에서 유지되면 좋아요.
- Link가 있는 folder index와 expand action은 서로 헷갈리지 않게 분리해야 해요.

### Badge 제거와 title 가독성 개선

- `dir`, `day`, `des`, `dec`, `ref`, `log` 같은 텍스트 badge는 sidebar tree에서 제거해요.
- Badge 때문에 제목이 짧아 보이거나 말줄임되는 현재 문제를 해결해요.
- 제목 텍스트가 tree row의 주인공이어야 해요.
- 긴 제목은 필요한 경우 자연스럽게 말줄임하되, badge가 공간을 잡아먹어서 말줄임되는 구조는 피해야 해요.

### Icon-based visual language

- 텍스트 badge 대신 icon을 써도 좋아요.
- Folder, note, daily, decision, design, reference, worklog, system-layer item을 아이콘으로 구분할 수 있어요.
- Icon은 장식이 아니라 빠른 scan을 돕는 용도여야 해요.
- Vanilla HTML/CSS/JS 구조를 유지하되, 외부 icon package를 새로 도입할지는 구현 전 판단해요.
- 새 package 없이 구현한다면 inline symbol, CSS mask, compact text-free glyph를 사용해도 돼요.

### Main context와 system layer naming

- `Special contents`라는 이름은 너무 trivial해서 다음 구현에서 바꿔요.
- ACAC의 `trove` 개념을 살린 이름을 사용해요.
- 후보는 구현 전에 짧게 비교해요.
  - `Trove layers`
  - `Trove system`
  - `System layer`
  - `Operating layer`
  - `Agent layer`
- 단순히 `_config`, `_archived`를 special이라고 부르는 방식은 피하고, 이 영역이 trove의 운영/agent/system layer라는 느낌을 줘야 해요.

### Underscore folder display abstraction

- `_config`, `_archived`처럼 `_`로 시작하는 folder는 내부적으로 special/system layer로 취급해요.
- 하지만 사용자에게 실제 raw folder name을 그대로 노출하는 것은 피하고 싶어요.
- 예를 들어 `_config`는 `System config`, `Agent memory`, `Operating config` 같은 user-facing label로 바꿀 수 있어요.
- `_archived`는 `Archive` 또는 `Dormant context`처럼 의미 기반 label로 바꿀 수 있어요.
- 실제 source path는 breadcrumb나 metadata에서 필요한 수준으로만 확인 가능하면 돼요.
- Navigation의 1차 label은 구현 디테일보다 제품 개념을 보여줘야 해요.

### Loading skeleton layout

- 현재 skeleton 자체는 괜찮아요.
- 다만 loading skeleton이 중앙의 좁은 card처럼 잡혀서 실제 reader body width와 다르게 느껴져요.
- Loading skeleton은 원래 reader layout width와 같은 폭감으로 보여야 해요.
- Home loading, note loading, search loading이 같은 layout container를 써야 해요.
- Skeleton은 sidebar/context shell과도 어색하게 분리되지 않아야 해요.

### Graph-based indexing and relational context map

- 기존 ACAC 문서들은 markdown frontmatter, wikilink, backlink, search, graph를 전제로 한 note model을 말하고 있어요.
- 현재 first reader는 backlinks와 outgoing links를 list로만 보여주고, full graph view는 첫 구현 비목표였어요.
- 다음 단계에서는 graph 기반 문서 indexing과 relational context map을 구현 범위에 추가해요.
- 이 작업은 먼저 read-only static data로 시작해요.
- 후보 data output:
  - `data/graph.json`
  - nodes: note id, title, type, status, visibility, display layer, path
  - edges: wikilink, backlink, folder relation, project relation
  - derived clusters: Daily, Projects, system layer, archive, project folder
- UI 후보:
  - 우측 context panel에 작은 relational context map preview
  - Home dashboard에 trove topology summary
  - Note view에서 현재 문서 중심의 1-hop relation map
- Full interactive graph는 범위가 커질 수 있으므로, 첫 graph step은 static, bounded, readable preview로 시작해요.

## 이번 후속 구현에서 하지 않을 것

- Browser editor, note create, delete, rename, move 기능을 만들지 않아요.
- Claude Code live connection, MCP, hooks, automatic memory sync를 만들지 않아요.
- Private auth gate를 만들지 않아요.
- Full Obsidian clone을 만들지 않아요.
- Graph layout이 과도하게 제품의 주인공이 되게 하지 않아요.
- 현재 public-safe boundary와 generated output boundary를 넘지 않아요.

## 구현 순서 제안

1. Sidebar tree naming과 data mapping을 먼저 정해요.
2. `_` prefix folder를 user-facing layer label로 표시하는 helper를 만들어요.
3. Tree row에서 text badge를 제거하고 icon, chevron, title, active state 구조로 바꿔요.
4. Collapsible folder state를 구현해요.
5. Loading skeleton이 reader width를 따르도록 state component를 고쳐요.
6. `graph.json`의 최소 data contract를 설계해요.
7. 우측 context panel 또는 Home에 작은 relational context map preview를 추가해요.
8. Desktop/mobile에서 tree, drawer, search, note, missing route를 다시 검증해요.

## 검증 기준

- Sidebar에서 `dir` 같은 badge가 보이지 않아야 해요.
- Folder는 접고 펼칠 수 있어야 해요.
- Current note가 있는 folder path는 열려 있어야 해요.
- Main context와 trove system layer가 시각적으로 분리되지만, `Special contents`라는 이름은 쓰지 않아야 해요.
- `_config`, `_archived` 같은 raw underscore folder name은 navigation 1차 label로 노출되지 않아야 해요.
- `_assets`는 여전히 navigation과 search에 노출되지 않아야 해요.
- Loading skeleton은 reader body layout width와 어울려야 해요.
- Graph 기반 relational context map은 read-only static data에서 시작해야 해요.
- `python3 scripts/deploy_check.py`가 통과해야 해요.
- Desktop과 mobile drawer에서 텍스트 겹침과 가로 overflow가 없어야 해요.

## 새 세션 시작 프롬프트

```text
/Users/jeina/ai-context-as-code 에서 ACAC reader 후속 개선을 진행해줘.

먼저 아래 파일을 반드시 읽고 현재 의도와 제약을 파악해줘.

- AGENTS.md
- README.md
- trove/Projects/ai-context-as-code/index.md
- trove/Projects/ai-context-as-code/Designs/first-instance-ui-ux-design.md
- trove/Projects/ai-context-as-code/Designs/first-instance-reader-design-system.md
- trove/Projects/ai-context-as-code/Designs/reader-tree-and-relational-context-map-follow-up.md
- site/index.html
- site/assets/style.css
- site/assets/app.js
- scripts/build_trove.py
- scripts/deploy_check.py

목표:

ACAC public reader의 sidebar 문서 트리를 제품 수준으로 개선해줘.
현재 `dir`, `day`, `des`, `dec`, `ref`, `log` 같은 텍스트 badge 때문에 제목이 짤려 보이고, folder/note 구분도 제품답지 않아.
Obsidian처럼 folder를 접었다 펼칠 수 있게 만들고, 텍스트 badge 대신 icon/chevron 중심의 시각 언어를 사용해줘.

반드시 반영할 것:

- Vanilla HTML/CSS/JS 구조를 유지해줘.
- 새 frontend framework를 도입하지 마.
- Sidebar folder는 collapsible이어야 해.
- Current route가 들어있는 folder는 자동으로 열려 있어야 해.
- 사용자가 펼친 tree state는 최소한 현재 브라우저 세션에서 유지되면 좋아.
- `dir` 같은 텍스트 badge는 제거해줘.
- Folder/note/type 구분은 icon이나 시각적 row state로 처리해줘.
- `Special contents`라는 용어는 쓰지 말고, ACAC의 `trove` 컨셉을 살린 이름으로 바꿔줘.
- `_config`, `_archived`처럼 `_`로 시작하는 raw folder name은 navigation의 1차 label로 그대로 노출하지 말아줘.
- `_config`와 `_archived`는 내부적으로 system/special layer로 취급하되, 사용자에게는 의미 기반 label로 보여줘.
- `_assets`는 계속 navigation/search에 노출하지 마.
- Loading skeleton은 중앙의 좁은 card가 아니라 reader body layout width에 맞게 보여줘.
- 기존 public-safe/read-only/generated-output boundary를 넘지 마.
- Claude Code live connection, MCP, hooks, automatic memory sync는 구현하지 마.

추가 설계 범위:

기존 ACAC 문서에서 graph, backlinks, relational context가 다음 단계로 언급돼 있어.
이번 작업에서 최소한 graph-based indexing과 relational context map의 다음 구현 범위를 설계해줘.
가능하면 read-only static data인 `data/graph.json` 계약까지 제안하고, 작게 구현 가능한 1-hop relation map preview를 어디에 둘지 판단해줘.
단, full interactive graph를 과하게 만들지는 마.

작업 방식:

1. 먼저 현재 UI를 짧게 진단해줘.
2. sidebar tree와 trove layer naming 설계를 제안해줘.
3. 구현 계획과 검증 기준을 짧게 작성해줘.
4. 그 다음 실제 코드와 필요한 문서를 수정해줘.
5. `python3 scripts/deploy_check.py`를 실행해줘.
6. 가능하면 로컬 정적 서버와 브라우저로 desktop/mobile을 확인해줘.
7. 변경 내용을 worklog와 Daily pointer에 남겨줘.

완료 기준:

- ACAC sidebar가 문서 사이트 tree가 아니라 context operating system의 trove navigator처럼 보여야 해.
- Folder 접기/펼치기가 동작해야 해.
- Badge 때문에 제목이 잘리는 문제가 없어야 해.
- Trove system layer naming이 `Special contents`보다 제품답게 바뀌어야 해.
- Loading skeleton layout이 reader body width와 맞아야 해.
- Graph 기반 relational context map은 최소한 다음 구현 가능한 data/UI 계약으로 기록되어야 해.
```
