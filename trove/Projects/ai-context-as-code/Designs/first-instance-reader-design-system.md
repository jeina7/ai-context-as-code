---
name: first-instance-reader-design-system
title: "첫 번째 인스턴스 Reader 디자인 시스템"
description: "ACAC 첫 public-safe context reader의 토큰, 컴포넌트 규칙, 반응형 화면 기준"
type: design
status: active
date: 2026-06-29
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
- 사용자는 `Daily/`, `Projects/`, `_config/`, `_archived/`의 역할을 바로 구분할 수 있어야 해요.
- `_assets/`는 storage라서 navigation, search, dashboard 어디에도 지식 섹션으로 노출하지 않아요.
- `_config/`와 `_archived/`는 숨기지 않고 trove layer로 구분해요.
- 모든 화면은 public-safe, read-only, generated output boundary를 드러내야 해요.

## 색상 토큰

Light mode만 이번 범위예요.
색은 장식보다 상태와 계층을 설명하는 데 써요.

| 역할 | 토큰 | 기준 |
|---|---|---|
| Page background | `--color-bg` | reader 뒤의 조용한 neutral 배경이에요. |
| Reader canvas | `--color-canvas` | 우측 panel과 일부 보조 영역의 바탕이에요. |
| Sidebar | `--color-sidebar` | source tree를 본문과 분리해요. |
| Surface | `--color-surface` | module, input, state card의 기본 면이에요. |
| Muted surface | `--color-surface-muted` | code, table header, 낮은 강조 영역이에요. |
| Text | `--color-text`, `--color-heading` | 본문과 제목의 높은 대비를 유지해요. |
| Muted text | `--color-muted`, `--color-faint` | path, metadata, 설명에만 써요. |
| Accent | `--color-accent` | active link, focus, wikilink, reader identity에 제한적으로 써요. |
| Success | `--color-success` | active/public/read-only처럼 정상 상태에 써요. |
| Warning | `--color-warning` | build warning, broken wikilink, operating layer에 써요. |
| Danger | `--color-danger` | excluded/private 같은 막힌 상태가 필요할 때 써요. |

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

- Sidebar row: 30px 이상 높이를 유지해요.
- Metadata pill: 24px 이상 높이를 유지해요.
- Dashboard module: 16-20px 안쪽 여백을 기본으로 해요.
- Reader page padding: desktop에서는 40px 이상, mobile에서는 16-20px로 줄여요.
- Table과 code block은 가로 scroll을 허용해요.

## Border, Radius, Shadow

ACAC는 작업 도구라서 둥근 장식이 커지면 안 돼요.

- Repeated row: border-top으로 구분해요.
- Sidebar item: 5px radius만 써요.
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
| Module surface | Start here, Build status, Trove layers 같은 의미 block |
| State card | missing, empty, fatal build output 같은 예외 상태 |

카드 안에 또 카드를 넣지 않아요.
반복 문서는 list row로 처리하고, module은 정보 묶음에만 써요.

## Component Rules

### Sidebar

- Brand, search, working context, Trove layers 순서로 둬요.
- `Daily/`와 `Projects/`는 working context예요.
- `_config/`와 `_archived/`는 divider 아래 trove system layer예요.
- Sidebar folder는 chevron으로 접고 펼쳐요.
- Current route가 들어있는 folder는 자동으로 열려 있어야 해요.
- `dir`, `day`, `des`, `dec`, `ref`, `log` 같은 텍스트 badge는 쓰지 않아요.
- `_config`와 `_archived` raw folder name은 1차 navigation label로 노출하지 않고 `Operating layer`, `Archive`를 써요.
- `_assets/`는 보이지 않아야 해요.
- Active route는 accent-soft background와 `aria-current="page"`로 표시해요.

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
- 결과는 title, path, summary, type/status/layer label을 보여줘요.
- `_config/`와 `_archived/` 결과에는 layer label을 붙여요.
- `_assets/`는 검색 결과에 나오면 안 돼요.
- 없는 결과에서 새 문서 만들기를 권하지 않아요. 첫 구현은 read-only예요.

### Home Dashboard

- Home은 product dashboard예요.
- Trove map, Start here, Current project, Today, Trove layers, Build status를 보여줘요.
- Build status는 public note 수, warning 수, repo-injected manual analytics beacon 여부만 작게 보여줘요.
- README는 source boundary 설명으로 보여주되 첫 화면의 주인공이 되지 않게 해요.

### Loading, Empty, Missing

- Loading은 skeleton line으로 짧게 보여줘요.
- Missing note는 route와 home/search entry를 보여줘요.
- Empty trove는 public notes가 거의 없다는 사실과 source boundary를 보여줘요.
- Fatal build output state는 generated JSON을 읽지 못했음을 분명히 말해요.

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
- Dark mode를 만들지 않아요.
- Full graph view, favorites, tabs, presentation mode를 만들지 않아요.
- Private vault reader나 auth gate를 만들지 않아요.

## 확인 기준

- Home, Note, Search, Missing, Loading 상태가 같은 토큰과 컴포넌트 규칙을 써요.
- Desktop에서 3-column layout이 안정적으로 보여요.
- Mobile에서 drawer, reader, context panel이 겹치지 않아요.
- Search result에 layer label이 붙고 `_assets/`는 보이지 않아요.
- Broken wikilink는 warning 상태로 보이고 클릭 가능한 정상 링크처럼 오해되지 않아요.
- `python3 scripts/deploy_check.py`가 통과해야 해요.
