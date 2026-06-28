---
name: first-instance-frame
title: 첫 번째 인스턴스 틀 설계
description: "Initial frame for the ACAC first instance that migrates jeina's local Obsidian into a cloud-based trove root"
type: design
status: active
date: 2026-06-28
created: 2026-06-28
updated: 2026-06-28
visibility: public
id: N_TyCBWLFT

---

# 첫 번째 인스턴스 틀 설계

이 문서는 ACAC 첫 인스턴스의 초기 틀을 정해요.
목표는 local Obsidian을 한 번에 옮기는 것이 아니라, cloud 기반 ACAC가 어떤 구조로 문서를 담고 보여줄지 먼저 고정하는 거예요.
틀이 안정된 뒤 Daily, 프로젝트 문서, special contents를 순서대로 옮겨요.
이 구조는 나중에 더 무거운 context registry로 확장될 수 있어야 해요.

## 설계 입력

이번 틀은 기존 knowledge base reference에서 아래를 가져와요.

- 파일 경로가 문서 정체성을 설명하는 구조
- markdown frontmatter, wikilink, backlink, search, graph를 전제로 한 노트 모델
- `index.md`를 폴더의 진입점으로 쓰는 방식
- 첫 구현부터 영구 ID 기반 route를 붙일 수 있는 구조
- source content와 build output을 분리하는 방식
- 노트 작성 규칙을 한 곳에서 관리하는 방식

그대로 가져오지 않는 것:

- 사내 GitHub Enterprise 전용 설정
- Slack 알림과 팀봇 전용 흐름
- 처음부터 무거운 브라우저 편집기와 Personal Access Token 설정
- 회사 도메인 중심의 노트 타입과 예시

## 현재 구현 기준

아래 기준은 구현자가 별도 decision 문서를 다시 읽지 않아도 따라야 하는 현재 SSOT예요.

| 기준 | 구현 내용 |
|---|---|
| 첫 목표 | 범용 오픈소스 본체가 아니라 jeina의 local Obsidian을 cloud 기반 ACAC 첫 인스턴스로 옮기는 틀을 먼저 만들어요. |
| root folder | ACAC가 관리하는 durable context root는 `trove/`예요. `vault/`나 `context/`를 쓰지 않아요. |
| main context | `trove/Daily/`, `trove/Projects/`가 기본 탐색 영역이에요. |
| special contents | `Memory/`, `Skills/`, `Commands/`, `Agents/`는 모두 `trove/_config/` 아래에 둬요. top-level `Memory/`는 만들지 않아요. |
| special area | `_config/`, `_archived/`는 사이드바 하단 영역이에요. main context처럼 보이게 하지 않아요. |
| hidden storage | `_assets/`는 내부 저장소예요. sidebar와 기본 search 결과에 직접 노출하지 않아요. |
| home | `trove/Home.md`를 만들지 않아요. 첫 화면은 root `README.md`와 `data/home.json`이 담당해요. |
| URL | 문서 canonical public URL은 `/trove/<id>`예요. `/notes/...`나 `/id/<id>` route는 만들지 않아요. |
| ID | build가 10자 URL-safe ID를 생성하고 `data/id-registry.json`으로 source path와 매핑해요. |
| 언어 | `_config/`는 영어 원본, `Daily/`와 `Projects/`는 한국어 원본이에요. |
| deploy | 첫 public deploy target은 Cloudflare Pages예요. |
| route fallback | Cloudflare Pages output에는 `/trove/*`와 `/search`를 app shell로 보내는 `_redirects`를 포함해요. |
| analytics | Cloudflare Web Analytics를 첫 구현 범위에 포함해요. token은 repo에 고정하지 않고 build-time config로 주입해요. |
| seed scope | 첫 seed 문서는 public-safe 최소 문서만 넣어요. 전체 Obsidian migration은 하지 않아요. |
| agent docs | `_config/Agents/`에는 `common.md`, `agent.md`, `claude.md`를 seed로 둬요. |
| agent sync | repo-local agent entry 문서를 생성하는 script는 만들지만, `~/.codex`나 `~/.claude` 같은 외부 runtime config를 자동으로 건드리지는 않아요. |

## 새 repo의 첫 구조

첫 구현은 아래 구조로 시작해요.

```text
ai-context-as-code/
  README.md
  AGENTS.md
  CLAUDE.md
  trove/
    Daily/
      2026-06/
        2026-06-28.md
    Projects/
      ai-context-as-code/
        index.md
        Decisions/
        Designs/
        Worklog/
        References/
        Research/
    _config/
      index.md
      Agents/
        common.md
        agent.md
        claude.md
      Memory/
        MEMORY.md
      Skills/
      Commands/
    _assets/
    _archived/
  site/
  scripts/
  data/
  dist/        # generated Cloudflare Pages output, not source
```

## 폴더 역할

| 폴더                              | 역할                                            | 언어     |
| ------------------- | --------------------------------------------- | ------ |
| `trove/Daily/`    | 하루 단위 context, 작업 요약, project worklog pointer | 한국어 우선 |
| `trove/Projects/` | 프로젝트별 문서, 설계, 결정, 작업 기록, 참고 문서, 조사 결과         | 한국어 우선 |
| `trove/_config/`  | Memory, Skills, Commands 같은 agent-facing special contents | 영어     |
| `trove/_assets/`  | 이미지와 첨부 파일을 뒤에서 저장하는 내부 storage               | 해당 없음  |
| `trove/_archived/` | 현재 기준에서 밀려난 문서                               | 원문 유지  |
| `site/`             | public site shell                             | 코드 기준  |
| `scripts/`          | build, validate, import 스크립트                  | 코드 기준  |
| `data/`             | ID registry, generated metadata               | 코드 기준  |

## 제품 사이드바 표시 규칙

`_config/`, `_archived/`는 main context가 아니에요.
제품에서는 special contents와 과거 기록을 위한 하단 보조 영역으로 취급해요.
`_assets/`는 UI에서 탐색하는 폴더가 아니라 내부 storage로 취급해요.

- 사이드바의 기본 탐색은 `Daily/`, `Projects/`를 먼저 보여줘요.
- `_config/`, `_archived/`는 구분선 아래 맨 아래쪽에 묶어서 보여줘요.
- `_config/` 안의 `Memory/`, `Skills/`, `Commands/`는 special contents로 보여줘요.
- `_archived/`는 기본적으로 접힌 상태로 두고, 검색이나 직접 열기에서 접근하게 해요.
- `_assets/`는 사이드바에 보여주지 않고, 첨부를 가진 문서에서만 간접적으로 접근해요.
- `_config/`와 `_archived/`는 검색과 링크 대상에 포함해요.
- `_assets/`의 파일 자체는 기본 검색 결과로 노출하지 않고, 그 파일을 참조하는 문서를 우선 보여줘요.
- public site에서 `_config/`는 사람이 매일 읽는 main context가 아니라 agent가 쓰는 특수 문서 묶음으로 보여줘요.

## 문서 단위

처음에는 문서 타입을 많이 만들지 않아요.

| 타입 | 위치 예시 | 용도 |
|---|---|---|
| `index` | `trove/Projects/ai-context-as-code/index.md` | 폴더 진입점과 목차 |
| `decision` | `trove/Projects/ai-context-as-code/Decisions/...` | 왜 이 결정을 했는지 보존 |
| `design` | `trove/Projects/ai-context-as-code/Designs/...` | 만들 구조와 설계 |
| `worklog` | `trove/Projects/ai-context-as-code/Worklog/...` | 작업 단위 기록 |
| `reference` | `trove/Projects/<project>/References/...` | 해당 프로젝트에서 다시 찾아볼 설명과 가이드 |
| `research` | `trove/Projects/<project>/Research/...` | 해당 프로젝트의 조사 결과 |
| `daily` | `trove/Daily/YYYY-MM/YYYY-MM-DD.md` | 하루 단위 context와 worklog pointer |
| `memory` | `trove/_config/Memory/...` | 여러 세션과 프로젝트에서 반복해서 쓰는 장기 context |
| `skill` | `trove/_config/Skills/...` | 반복 가능한 agent workflow |
| `command` | `trove/_config/Commands/...` | 반복 가능한 command procedure |
| `agent-entry` | `trove/_config/Agents/...` | agent runtime entry document |
| `principle` | `trove/_config/Memory/Principles/...` | ACAC 인스턴스 전체에 적용할 운영 원칙 |
| `convention` | `trove/_config/Memory/Conventions/...` | 문서 작성, 링크, 번역, 검증 규칙 |
| `context-design` | `trove/_config/Memory/Designs/...` | ACAC 인스턴스 자체의 구조 설계 |

`References/`와 `Research/`는 프로젝트별 하위 폴더로 둬요.
조사 결과가 여러 프로젝트에 반복 적용할 원칙이나 작성 규약으로 굳어지면 `trove/_config/Memory/`로 올려요.
나중에 필요해지면 프로젝트별 `Troubleshooting/`, `Meetings/`를 추가해요.

## Special contents 운영 규칙

`trove/_config/`는 agent-facing special contents를 관리하는 곳이에요.
여기에는 agent가 읽는 장기 기억, 반복 workflow, 반복 command, runtime entry 문서가 함께 들어가요.

초기 하위 폴더:

| 폴더 | 담을 내용 |
|---|---|
| `trove/_config/Agents/` | `common.md`, `agent.md`, `claude.md` 같은 agent entry document source |
| `trove/_config/Memory/` | 여러 세션과 프로젝트에서 반복해서 쓰는 장기 context |
| `trove/_config/Skills/` | 재사용 가능한 agent workflow |
| `trove/_config/Commands/` | 반복 실행할 command procedure |

`Memory/`, `Skills/`, `Commands/`는 모두 markdown content예요.
다만 main context가 아니라 agent가 쓰는 특수 콘텐츠로 다뤄요.

초기 문서:

| 문서 | 담을 내용 |
|---|---|
| `trove/_config/Agents/common.md` | 여러 agent entry가 공유하는 기본 규칙 |
| `trove/_config/Agents/agent.md` | root `AGENTS.md`로 생성될 repo-local agent entry source |
| `trove/_config/Agents/claude.md` | root `CLAUDE.md`로 생성될 Claude entry source |
| `trove/_config/Memory/MEMORY.md` | 장기 기억 index |

아래 문서는 첫 seed 이후에 필요해질 때 추가해요.
처음부터 전부 만들면 구조가 무거워져서, seed에는 포함하지 않아요.

| 후보 문서 | 담을 내용 |
|---|---|
| `trove/_config/Memory/Principles/source-of-truth.md` | context note가 본문 SSOT이고 runtime memory는 pointer라는 원칙 |
| `trove/_config/Memory/Principles/memory-tiers.md` | working, daily, long-term memory를 나누는 규칙 |
| `trove/_config/Memory/Principles/durable-documents.md` | Daily 없이 6개월 뒤에도 읽히는 문서를 만드는 규칙 |
| `trove/_config/Memory/Conventions/daily-and-worklog.md` | detailed worklog + Daily pointer 이중 기록 규칙 |
| `trove/_config/Memory/Conventions/frontmatter.md` | natural-language frontmatter 값은 따옴표로 감싸는 규칙 |
| `trove/_config/Memory/Conventions/wikilinks-and-sources.md` | wikilink, source, archive, reference 사용 규칙 |
| `trove/_config/Memory/Conventions/raw-note-imports.md` | raw note를 정리하고 원본을 처리하는 규칙 |
| `trove/_config/Memory/Conventions/writing-voice.md` | 쉬운 한국어, 해요체, 자체 발명 용어 금지 규칙 |
| `trove/_config/Memory/Designs/context-structure.md` | `Daily/`, `Projects/`, `_config/` 경계 설계 |

Special contents 경계:

- `trove/_config/Memory/`: agent가 장기적으로 재사용해야 하는 원칙, 선호, 판단 기준, 구조 설계를 담아요.
- `trove/_config/Skills/`: 특정 상황에서 반복 실행할 workflow를 담아요.
- `trove/_config/Commands/`: agent나 사람이 반복 실행할 command procedure를 담아요.
- `trove/_config/Agents/`: agent runtime이 처음 읽는 entry document를 담아요.
- 같은 내용이 여러 special contents에 필요하면 `Memory/`가 설명 원본이고, `Skills/`, `Commands/`, `Agents/`는 실행하기 쉬운 형태로 요약해요.

Agent entry sync 기준:

- `trove/_config/Agents/common.md`, `agent.md`, `claude.md`가 source예요.
- root `AGENTS.md`와 root `CLAUDE.md`는 `scripts/sync_agent_docs.py`가 생성하는 output으로 취급해요.
- 생성된 파일에는 직접 수정하지 말라는 header를 넣어요.
- sync script는 repo 안의 entry file만 갱신해요.
- 첫 구현에서는 local machine의 `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, 전역 skill folder를 건드리지 않아요.

## _assets 운영 규칙

`trove/_assets/`는 이미지와 첨부 파일을 저장하는 내부 폴더예요.
사용자가 따로 탐색하거나 관리해야 하는 지식 영역으로 보지 않아요.

- 문서가 이미지나 파일을 참조할 때만 `_assets/`에 저장해요.
- public site 사이드바에는 `_assets/`를 보여주지 않아요.
- 검색 결과에는 파일 자체보다 그 파일을 참조하는 문서를 우선 보여줘요.
- 첨부 파일 이름과 경로는 build/import 도구가 관리할 수 있게 해요.

## Daily 운영 규칙

`trove/Daily/`는 하루 단위 context hub예요.
작업 상세를 모두 여기에 몰아넣지 않고, 그날의 판단과 링크를 모아 다음 세션이 바로 이어받게 해요.

파일 경로:

```text
trove/Daily/YYYY-MM/YYYY-MM-DD.md
```

Daily 최소 템플릿:

```markdown
---
type: daily
title: 2026-06-28
description: "Daily context for 2026-06-28"
status: active
created: 2026-06-28
updated: 2026-06-28
---

# 2026-06-28

오늘의 초점과 이어받을 context를 짧게 정리해요.
자세한 프로젝트 작업 기록은 project worklog로 보내고, 이 문서는 하루 단위의 지도 역할을 해요.

## Today

## Open Context

## Decisions

## Worklog

## Next
```

Daily 문서가 담는 것:

- 오늘의 초점과 열린 질문
- 하루 동안 생긴 중요한 결정과 방향 변경
- 프로젝트별 상세 worklog로 가는 한 줄 pointer
- 다음 세션이 알아야 할 이어받을 context
- 여러 프로젝트에 걸쳐 있어서 아직 특정 프로젝트 문서로 넣기 애매한 짧은 메모

Daily 문서가 담지 않는 것:

- 프로젝트 하나의 상세 작업 기록 전체
- 오래 보존해야 하는 설계나 결정 본문
- agent가 실제로 읽고 실행해야 하는 config 원문

상세 기록 위치:

- 프로젝트 작업 상세: `trove/Projects/<project>/Worklog/YYYY-MM-DD.md`
- 결정 본문: `trove/Projects/<project>/Decisions/...`
- 설계 본문: `trove/Projects/<project>/Designs/...`
- 장기 운영 규칙: `trove/_config/Memory/...`

Daily의 worklog section은 아래처럼 짧게 유지해요.

```markdown
## Worklog

- ACAC 첫 인스턴스 구조에서 `_config/Memory`, `_config/Skills`, `_config/Commands` special contents 경계 정리 [[../../Projects/ai-context-as-code/Worklog/2026-06-28#22:00 — System folder split from Config and project research|#]]
```

## Frontmatter 최소 규칙

모든 markdown 문서는 앞에 frontmatter를 가져요.

```yaml
---
type: design
title: Example Title
description: "One-line description"
status: draft
created: 2026-06-28
updated: 2026-06-28
---
```

초기 필수 필드:

- `type`: 문서의 역할이에요.
- `title`: H1 제목과 같게 써요.
- `description`: 한 줄 설명이에요.
- `status`: `draft`, `active`, `archived` 중 하나로 시작해요.
- `created`: 처음 만든 날짜예요.
- `updated`: 마지막으로 의미 있게 고친 날짜예요.

영구 ID는 사람이 직접 만들지 않아요.
site build가 `data/id-registry.json`으로 자동 관리해요.
문서의 canonical public URL은 `/trove/<id>`예요.
파일 path는 breadcrumb와 registry 내부 매핑으로만 보여줘요.
Hash route는 쓰지 않아요.

## 노트 본문 규칙

- H1 바로 아래에 3~5줄 요약을 둬요.
- 처음 읽는 사람이 전체 그림을 잡은 뒤 세부 내용을 볼 수 있게 써요.
- 파일명과 H1은 같게 맞춰요.
- wikilink는 파일명 기준으로 걸어요.
- 한 문서에는 하나의 주제만 담아요.
- `reference`와 `principle`은 최신 기준으로 다시 쓰는 문서예요.
- `decision`, `design`, `worklog`는 시점과 맥락을 보존하는 문서예요.

## 언어와 번역

`_config/` content는 영어가 원본이에요.

예시:

- `trove/_config/Agents/common.md`
- `trove/_config/Agents/agent.md`
- `trove/_config/Agents/claude.md`
- `trove/_config/Memory/MEMORY.md`
- `trove/_config/Skills/*/SKILL.md`
- `trove/_config/Commands/*.md`

`Projects/`, `Daily/` content는 한국어가 원본이에요.
영어 콘텐츠는 나중에 `en/` 아래에 생성해요.

```text
trove/Projects/ai-context-as-code/Designs/첫 번째 인스턴스 틀 설계.md
en/Projects/ai-context-as-code/Designs/first-instance-frame.md
```

초기에는 번역 자동화를 만들지 않아요.
한국어 원본 구조가 안정된 뒤 번역 생성을 붙여요.

## Public site가 설명해야 하는 것

외부 사람이 `acac.sh`를 봤을 때 아래를 이해해야 해요.

- ACAC 첫 인스턴스가 local Obsidian을 어떻게 cloud 구조로 옮기는지
- Daily, Projects, special contents가 어떤 기준으로 나뉘는지
- `_config/Memory`, `_config/Skills`, `_config/Commands`가 어떻게 함께 관리되는지
- 어떤 문서가 현재 기준이고, 어떤 문서가 archive인지
- 나중에 오픈소스 본체로 분리될 수 있는 부분이 무엇인지

## 구현 순서

1. 빈 repo에 `trove/`, `site/`, `scripts/`, `data/` 기본 구조를 만들어요.
2. `trove/Projects/ai-context-as-code/index.md`를 만들어요.
3. `trove/Daily/YYYY-MM/YYYY-MM-DD.md` 템플릿을 만들어요.
4. `trove/_config/index.md`를 영어로 만들고 special contents의 기준을 적어요.
5. `trove/_config/Agents/common.md`, `agent.md`, `claude.md`를 만들어요.
6. `trove/_config/Memory/MEMORY.md`를 만들고 장기 기억의 승격 기준을 적어요.
7. `scripts/sync_agent_docs.py`로 root `AGENTS.md`, `CLAUDE.md`를 생성해요.
8. `scripts/validate_trove.py`로 frontmatter, H1, visibility, `_assets/` 규칙을 검증해요.
9. `scripts/build_trove.py`로 `data/id-registry.json`, `data/notes.json`, `data/tree.json`, `data/home.json`, `data/search-index.json`, `data/backlinks.json`, `data/build.json`을 만들어요.
10. `scripts/build_trove.py`가 Cloudflare Pages output인 `dist/`를 조립하게 해요.
11. 모든 public 문서가 `/trove/<id>` route를 갖게 해요.
12. site는 먼저 home, sidebar, search, `/trove/<id>` 문서 렌더링만 제공해요.
13. Cloudflare Web Analytics token 주입과 비활성 fallback을 붙여요.
14. 작은 Obsidian 문서 하나를 후보로 골라 public-safe하게 옮겨요.
15. 옮긴 문서를 기준으로 부족한 규칙을 고쳐요.

## 비목표

- 첫 구현에서 모든 Obsidian 폴더를 재현하지 않아요.
- 첫 구현에서 편집기, 로그인, GitHub API 저장 기능을 만들지 않아요.
- 첫 구현에서 repo 밖 agent runtime 동기화를 자동화하지 않아요.
- 첫 구현에서 모든 문서를 한국어와 영어로 동시에 만들지 않아요.
- 첫 구현에서 일반 사용자가 fork해서 바로 쓰는 템플릿까지 만들지 않아요.

## 확인 기준

첫 틀이 끝났다고 볼 수 있는 조건:

- repo root만 봐도 ACAC가 첫 인스턴스 프로젝트라는 점이 보여요.
- root `README.md`와 public site 첫 화면에서 전체 구조와 사용법을 이해할 수 있어요.
- `Daily/`, `Projects/`, `_config/`, `_assets/`, `_archived/`의 역할이 겹치지 않아요.
- `Daily/`가 하루 단위 context hub이고, 상세 worklog는 project folder에 남는다는 기준이 보여요.
- AGENTS와 memory에서 가져온 context 운영 규칙이 `_config/Memory/Principles/`와 `_config/Memory/Conventions/`에 들어갈 위치가 보여요.
- `_config/` content는 영어, `Projects/`, `Daily/` content는 한국어 우선이라는 원칙이 문서와 예시에서 드러나요.
- 이전 설계와 새 설계가 섞이지 않고 archive에서만 확인돼요.
