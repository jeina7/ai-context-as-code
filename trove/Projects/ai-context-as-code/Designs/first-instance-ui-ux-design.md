---
name: first-instance-ui-ux-design
title: 첫 번째 인스턴스 UI/UX 설계
description: "ACAC 첫 인스턴스 public reader의 화면 구성, 탐색 방식, 시각 디자인 기준"
type: design
status: active
date: 2026-06-28
created: 2026-06-28
updated: 2026-06-29
visibility: public
id: z1hXOfY1w6

---

# 첫 번째 인스턴스 UI/UX 설계

ACAC 첫 인스턴스의 화면은 landing page가 아니라 실제 context reader로 시작해요.
방문자는 첫 화면에서 `trove/` 구조, 현재 프로젝트 예시, special contents가 어떻게 쓰이는지 바로 볼 수 있어야 해요.
기본 화면은 좌측 navigation, 가운데 문서 reader, 우측 context panel로 구성해요.
시각 디자인은 화려한 소개 사이트보다 조용하고 밀도 있는 작업 도구에 가까워야 해요.

## 제품 경험 목표

ACAC의 UI는 문서를 예쁘게 보여주는 것보다 durable context를 읽고 이어받게 하는 것이 중요해요.
그래서 첫 화면부터 실제 구조와 문서를 보여주고, 설명은 그 구조를 이해하는 데 필요한 만큼만 둬요.

핵심 목표:

- 사람이 `acac.sh`를 열었을 때 ACAC가 무엇을 관리하는지 30초 안에 이해해요.
- jeina가 다음 작업을 이어받을 때 `Daily/`, `Projects/`, `_config/` 중 어디를 봐야 하는지 바로 판단해요.
- 외부 방문자가 첫 인스턴스를 보고 ACAC가 어떤 제품이 될 수 있는지 상상할 수 있어요.
- agent-facing special contents가 숨겨진 설정 파일이 아니라 관리 가능한 markdown content로 보여요.
- UI가 더 많은 산출물을 만들게 하기보다, 좋은 source와 검증된 context를 찾게 해요.

## 사용자 기준

첫 구현은 세 사용자를 동시에 만족해야 해요.
다만 우선순위는 jeina의 실제 사용, 외부 방문자의 이해, agent context 확인 순서예요.

| 사용자 | 필요한 일 | UI가 도와야 하는 방식 |
|---|---|---|
| jeina | 오늘의 context를 보고 다음 작업을 이어감 | `Daily/`, 최근 project worklog, 열린 decision을 빠르게 보여줘요. |
| 외부 방문자 | ACAC가 어떤 제품인지 이해함 | 실제 `Projects/ai-context-as-code` 예시와 구조 설명을 첫 화면에 보여줘요. |
| agent 사용자 | agent가 읽는 memory, skill, command 구조를 확인함 | `_config/`를 하단 special contents로 보여주되 검색과 링크에는 포함해요. |

## 전체 화면 구조

Desktop 기본 구조는 세 영역이에요.

```text
+----------------------+--------------------------------------+-----------------------+
| Left navigation      | Main reader                          | Right context panel   |
|                      |                                      |                       |
| Brand / search       | Home or note content                 | Current note metadata |
| Daily                | Breadcrumb                           | Table of contents     |
| Projects             | H1 + 3-5 line summary                | Backlinks             |
|                      | Markdown body                        | Related context       |
| Special contents     |                                      | Build / visibility    |
+----------------------+--------------------------------------+-----------------------+
```

Layout 기준:

| 영역 | desktop 기준 | 역할 |
|---|---:|---|
| 좌측 navigation | 260-300px | 전체 구조와 검색 진입점 |
| 가운데 reader | 남는 폭 전체 | Home view와 note view |
| 우측 context panel | 280-340px | 현재 문서의 메타 정보, 목차, backlinks |

작은 화면에서는 세 영역을 한 줄에 모두 유지하지 않아요.
좌측 navigation은 drawer로 접고, 우측 context panel은 문서 하단 section 또는 bottom drawer로 내려요.

## 첫 화면

첫 화면은 `trove/Home.md`가 아니라 root `README.md`와 `data/home.json`으로 만들어요.
marketing hero가 아니라 “이 인스턴스가 실제로 어떻게 구성되어 있는지”를 보여주는 dashboard예요.

첫 화면 구성:

| 영역 | 내용 |
|---|---|
| 상단 intro | `AI Context as Code` 이름, 한 줄 설명, 현재 인스턴스가 first instance라는 점 |
| Structure summary | `Daily/`, `Projects/`, `_config/`, `_archived/` 역할 |
| Start here | 처음 보는 사람이 열어야 할 문서 3-5개 |
| Current project | `Projects/ai-context-as-code`의 index, 최신 design, 최신 decision |
| Today | 오늘 Daily가 있으면 link와 짧은 요약 |
| Special contents | `_config/Memory`, `_config/Skills`, `_config/Commands`가 무엇인지 짧게 설명 |
| Build status | 마지막 build 시각, public 문서 수, warning 수 |

첫 화면의 모든 문서 링크는 `/trove/<id>`를 사용해요.
화면에는 문서의 source path를 작게 보여줄 수 있지만, 링크 주소 자체는 path를 드러내지 않아요.

첫 화면에서 하지 않을 것:

- 큰 hero 이미지나 marketing copy 중심 화면을 만들지 않아요.
- 기능 소개 카드만 나열하지 않아요.
- 실제 문서로 들어가는 길 없이 제품 설명만 하지 않아요.
- private Obsidian migration을 완료한 것처럼 보이게 하지 않아요.

## 좌측 navigation

좌측 navigation은 “이 trove가 어떻게 생겼는지”를 보여주는 지도예요.
Obsidian처럼 폴더 tree를 보여주되, ACAC의 main context와 special contents를 시각적으로 분리해요.

구성:

| 영역 | 내용 |
|---|---|
| Header | `ACAC` 또는 `AI Context as Code`, home link |
| Search button | `Search` 입력 또는 버튼. keyboard shortcut은 나중 단계 |
| Main context | `Daily/`, `Projects/` |
| Special contents | 구분선 아래 `_config/`, `_archived/` |
| Hidden storage | `_assets/`는 표시하지 않음 |

표시 규칙:

- `Daily/`와 `Projects/`는 항상 먼저 보여줘요.
- `_config/`와 `_archived/`는 구분선 아래에 보여줘요.
- `_config/`는 접을 수 있지만 완전히 숨기지는 않아요.
- `_archived/`는 기본 접힘 상태예요.
- `_assets/`는 sidebar에 나오지 않아요.
- `visibility: private` 또는 `internal` 문서는 public build에서 sidebar에 나오지 않아요.

Navigation item은 단순한 텍스트 목록이어야 해요.
각 문서가 card처럼 보이면 문서 tree를 훑기 어려워져요.

## 가운데 reader

가운데 영역은 가장 중요해요.
여기서 ACAC가 실제 durable context를 어떻게 읽게 하는지 결정돼요.

Note view 구성:

| 순서 | 요소 | 역할 |
|---:|---|---|
| 1 | breadcrumb | 현재 문서가 `trove/` 어디에 있는지 보여줘요. |
| 2 | metadata strip | type, status, visibility, updated를 작게 보여줘요. |
| 3 | H1 | 문서 제목이에요. |
| 4 | 3-5줄 summary | 문서 핵심을 먼저 보여줘요. |
| 5 | body | markdown 본문이에요. |
| 6 | related/backlinks entry | 우측 panel이 없는 화면에서 연결 문서를 보여줘요. |

Reader 기준:

- 본문 폭은 너무 넓히지 않아요. 긴 줄은 읽기 어렵기 때문에 최대 폭을 둬요.
- 표와 코드 블록은 가로 scroll을 허용해요.
- heading anchor를 지원해요.
- wikilink는 일반 링크와 다르게 표시하되 과하게 튀지 않게 해요.
- 깨진 wikilink는 흐린 점선 스타일로 보여주고, 나중에 validator warning과 연결해요.
- `visibility`는 public site에서 주로 내부 검증용이지만, 문서 상단에 작게 보여줘요.
- canonical URL은 항상 `/trove/<id>`예요.
- source path는 breadcrumb와 metadata에서만 보여줘요.

## 우측 context panel

우측 panel은 현재 문서의 주변 맥락을 보여줘요.
문서 본문을 읽으면서 “이 문서가 어디에 연결되는지”를 확인하는 영역이에요.

초기 section:

| section | 내용 |
|---|---|
| Document | type, status, updated, path, visibility |
| Table of contents | 현재 문서 heading |
| Backlinks | 이 문서를 가리키는 문서 |
| Outgoing links | 이 문서가 가리키는 문서 |
| Related context | 같은 project의 index, latest decision, latest worklog |

표시 기준:

- 우측 panel은 보조 정보예요. 본문보다 시각적으로 강하면 안 돼요.
- Graph는 첫 구현에서 full view로 만들지 않아요.
- 대신 backlinks와 outgoing links를 list로 먼저 보여줘요.
- panel은 접을 수 있어야 해요.
- mobile에서는 문서 하단으로 내려요.

## Search

Search는 첫 구현의 핵심 기능이에요.
ACAC는 folder를 탐색하는 도구이면서, 오래된 context를 다시 찾는 도구이기 때문이에요.

초기 search modal:

| 요소 | 기준 |
|---|---|
| 입력창 | 화면 상단 modal 또는 command style overlay |
| 결과 ranking | title, filename, description, summary, body snippet 순서 |
| 필터 | type, folder, status, visibility |
| 결과 표시 | title, path, summary 1-2줄 |

Search UX 기준:

- `_assets/` 파일은 직접 검색 결과로 보여주지 않아요.
- `_config/`와 `_archived/`는 검색에 포함하되, 결과에서 special label을 붙여요.
- 검색 결과는 folder tree보다 빨라야 해요.
- 없는 결과에서는 “새 문서 만들기”를 보여주지 않아요. 첫 구현은 read-only예요.
- 검색 결과 item의 primary link는 `/trove/<id>`예요.
- 검색 결과에는 title, source path, summary를 함께 보여줘요.

## Visual style

ACAC는 SaaS marketing page보다 작업 도구에 가까워야 해요.
조용하고 신뢰감 있는 화면, 적당한 밀도, 명확한 hierarchy가 중요해요.

시각 원칙:

- 배경은 거의 흰색에 가까운 neutral tone으로 둬요.
- 강조색은 하나만 과하게 쓰지 않고, link와 active state에만 제한적으로 써요.
- 카드 남발을 피하고, 반복 item과 작은 status block에만 얕은 surface를 써요.
- 큰 radius를 피하고, 6-8px 정도의 절제된 radius를 써요.
- hero-scale typography는 첫 화면 상단 이름에만 제한해요.
- 문서 본문은 읽기 좋은 크기와 line-height를 우선해요.
- `_config`, `_archived` 같은 special area는 색보다 위치와 label로 구분해요.

색 역할:

| 역할 | 느낌 |
|---|---|
| Background | warm-neutral 또는 neutral white |
| Text | 높은 대비의 near-black |
| Muted text | metadata와 path |
| Accent | active link, focused search, current item |
| Warning | validator warning, broken wikilink |
| Archived | 흐린 neutral label |

첫 구현에서는 dark mode를 만들지 않아도 돼요.
먼저 light mode의 정보 밀도와 문서 가독성을 맞춰요.

## Interaction states

첫 구현에서 필요한 상태만 만들어요.
상태가 적어야 구현이 단순하고, 사용자가 헷갈리지 않아요.

필수 상태:

| 상태 | 화면 |
|---|---|
| Loading | `data/*.json`을 읽는 중임을 짧게 보여줘요. |
| Empty trove | 문서가 거의 없을 때 scaffold와 다음 행동을 보여줘요. |
| Missing note | route의 문서를 찾지 못했을 때 path와 home link를 보여줘요. |
| Build warning | validator warning 수와 자세히 볼 수 있는 link를 보여줘요. |
| Private excluded | public build에서 제외된 문서는 route에 나오지 않아요. |
| Broken wikilink | 클릭은 막고 validator warning과 연결해요. |

편집 상태, 저장 상태, 삭제 확인 modal은 첫 구현에 넣지 않아요.

## Mobile behavior

Mobile은 “모든 기능을 작은 화면에 억지로 넣는 것”이 아니에요.
문서 읽기와 검색을 우선하고, 구조 탐색은 drawer로 보조해요.

Mobile 기준:

- 상단 bar에는 home, current path, search, menu만 둬요.
- 좌측 navigation은 full-height drawer로 열어요.
- 우측 context panel은 문서 하단 section으로 내려요.
- table과 code block은 가로 scroll을 허용해요.
- tap target은 작게 만들지 않아요.
- 긴 path는 말줄임하되, breadcrumb 전체는 별도 행에서 볼 수 있게 해요.

첫 구현 QA는 desktop과 mobile width를 모두 봐야 해요.
문서 제목, summary, sidebar item이 겹치지 않아야 해요.

## 정보 구조와 data 계약

UI는 build output을 기준으로 그려요.
site가 `trove/` 파일 시스템을 직접 추측하지 않게 해요.

필요 data:

| 파일 | UI 사용처 |
|---|---|
| `data/tree.json` | 좌측 navigation |
| `data/notes.json` | `/trove/<id>` route, metadata strip, latest lists |
| `data/search-index.json` | search modal |
| `data/backlinks.json` | right context panel |
| `data/home.json` | first screen |
| `data/id-registry.json` | `/trove/<id>` route와 source path 매핑 |
| `data/build.json` | build status, public 문서 수, warning 수, analytics 설정 상태 |
| `_build/trove/` | markdown body |

`data/tree.json`에는 UI 표시용 grouping이 있어야 해요.

```json
{
  "main": ["Daily", "Projects"],
  "special": ["_config", "_archived"],
  "hidden": ["_assets"]
}
```

이 grouping은 hard-coded UI 취향이 아니라 ACAC의 context 철학이에요.
main context와 special contents가 다르게 보이는 이유를 data에도 드러내요.

## URL route 기준

ACAC는 hash route를 쓰지 않아요.
Analytics, 공유 링크, 브라우저 주소, 배포 로그가 같은 path를 바라보게 하기 위해 실제 URL route를 써요.
문서의 canonical URL은 `/trove/<id>`예요.
파일 path는 URL이 아니라 breadcrumb와 metadata로 보여줘요.

초기 route:

| route | 화면 |
|---|---|
| `/` | Home view |
| `/trove/<id>` | ID 기반 note view |
| `/search?q=<query>` | search result view |

UI 표시 기준:

- breadcrumb는 registry의 `currentPath`를 기준으로 보여줘요.
- 공유 버튼은 `/trove/<id>`를 복사해요.
- 주소창에는 `/trove/<id>`를 유지해요.
- `id`가 없는 문서는 build warning으로 봐요.
- hash route와 `/notes/...` 형태의 링크는 만들지 않아요.

## Analytics 기준

Analytics는 제품 화면의 주인공이 아니에요.
첫 구현에서는 Cloudflare Web Analytics로 page view만 확인하고, 별도 product event tracking은 만들지 않아요.

측정 기준:

| 항목 | 기준 |
|---|---|
| tool | Cloudflare Web Analytics |
| route | `/`, `/trove/<id>`, `/search?q=<query>` |
| SPA tracking | History API route change를 사용해요. |
| token | build-time config로 주입하고 repo source에는 고정하지 않아요. |
| UI exposure | analytics token이나 tracking 설정을 화면에 보여주지 않아요. |

첫 구현에서 추적하지 않는 것:

- 검색어별 custom event
- sidebar click event
- reading depth
- outbound link click
- user identity

필요한 화면 표시:

- Home의 Build status에는 analytics가 enabled인지 disabled인지만 작게 보여줘요.
- analytics가 꺼져 있어도 reader 기능은 모두 정상 동작해야 해요.

## 첫 구현 범위

첫 구현에 넣을 것:

- Home view
- 좌측 navigation
- 가운데 markdown reader
- 우측 context panel
- Search modal
- responsive mobile drawer
- loading, empty, missing note, build warning 상태

첫 구현에서 뺄 것:

- browser editor
- GitHub API 저장
- 새 노트 생성 modal
- 삭제, 이동, 이름 변경 modal
- full graph view
- favorites
- tabs
- presentation mode
- dark mode
- private auth gate

## 확인 기준

UI/UX 첫 구현은 아래가 되면 통과예요.

- `acac.sh` 첫 화면이 landing page가 아니라 실제 reader로 보여요.
- 첫 화면에서 `Daily/`, `Projects/`, `_config/`, `_archived`의 역할을 이해할 수 있어요.
- sidebar에서 main context와 special contents가 분리되어 보여요.
- `_assets/`는 보이지 않아요.
- `Projects/ai-context-as-code` 예시 문서를 열 수 있어요.
- note view에서 title, summary, metadata, body, backlinks가 자연스럽게 이어져요.
- search로 문서를 찾을 수 있어요.
- mobile에서 navigation, reader, context panel이 서로 겹치지 않아요.
- UI가 “문서 사이트”가 아니라 “context를 이어받는 작업 도구”처럼 느껴져요.

## 구현 디자인 시스템

구체적인 토큰, 컴포넌트 규칙, responsive 기준은 [[first-instance-reader-design-system]]에 둬요.
이 문서는 제품 경험과 정보 구조를 설명하고, 디자인 시스템 문서는 `site/` 구현이 따라야 하는 세부 규칙을 설명해요.

## 비목표

- 첫 구현에서 제품 marketing page를 만들지 않아요.
- 첫 구현에서 Obsidian의 모든 UI를 복제하지 않아요.
- 첫 구현에서 편집 가능한 CMS를 만들지 않아요.
- 첫 구현에서 개인 private vault reader를 만들지 않아요.
- 첫 구현에서 visual polish를 build, validation, information architecture보다 앞세우지 않아요.
