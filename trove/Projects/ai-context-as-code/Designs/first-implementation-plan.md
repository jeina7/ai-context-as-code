---
type: design
title: "첫 구현 최종 스펙"
description: "ACAC 첫 인스턴스 아키텍처를 repo의 작동하는 최소 구조로 옮기는 최종 구현 기준"
status: active
created: 2026-06-28
updated: 2026-06-29
visibility: public
id: zxhIW0jU5O

---

# 첫 구현 최종 스펙

이 문서는 비어 있는 `ai-context-as-code` repo에 ACAC 첫 인스턴스의 최소 작동 구조를 만드는 최종 구현 기준이에요.
목표는 예쁜 사이트를 먼저 만드는 것이 아니라, `trove/` source가 검증되고 build되고 site에서 읽히는 한 흐름을 완성하는 거예요.
첫 구현은 ACAC 자체 프로젝트 문서를 예시로 삼고, 공개 가능한 작은 문서만 넣어요.
private Obsidian migration, 브라우저 편집기, 외부 runtime config sync는 이 흐름이 안정된 뒤에 해요.
Cloudflare Workers static assets와 Cloudflare Web Analytics는 첫 구현 범위에 포함해요.

## 구현 원칙

- `trove/` source가 먼저예요. site는 그 source를 보여주는 결과물이에요.
- 첫 commit부터 public-safe content만 넣어요.
- hash route를 쓰지 않고 실제 URL path route로 시작해요.
- 문서의 canonical public URL은 `/trove/<id>`예요.
- 파일 path는 URL이 아니라 breadcrumb와 registry 매핑에만 써요.
- validator가 실패하면 build와 deploy를 멈춰요.
- 기능은 읽기, 탐색, 검색, 검증 순서로 붙여요.
- 편집 기능은 첫 구현에 넣지 않아요.
- Cloudflare Workers static assets deploy output은 `dist/`예요.
- Cloudflare Web Analytics는 dashboard automatic setup을 우선하고, manual beacon token은 source에 고정하지 않아요.
- repo-local agent entry sync script는 만들지만, `~/.codex`나 `~/.claude`를 자동 수정하지 않아요.

## 1단계: repo 기본 구조 만들기

목표는 빈 repo에 ACAC 첫 인스턴스의 뼈대를 만드는 거예요.
이 단계에서 top-level `Memory/`, `Assets/`, `Config/`, `System/`, `Archive/`, `Home.md`는 만들지 않아요.

만들 파일과 폴더:

```text
README.md
AGENTS.md
CLAUDE.md
trove/
  Daily/
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
    Skills/
    Commands/
  _assets/
  _archived/
site/
scripts/
data/
dist/
```

초기 문서:

| 문서 | 내용 |
|---|---|
| `README.md` | ACAC 첫 인스턴스가 무엇인지, `trove/`가 무엇인지 설명해요. |
| `AGENTS.md` | `trove/_config/Agents/agent.md`와 `common.md`에서 생성되는 repo-local agent entry예요. |
| `CLAUDE.md` | `trove/_config/Agents/claude.md`와 `common.md`에서 생성되는 Claude entry예요. |
| `trove/Projects/ai-context-as-code/index.md` | 첫 프로젝트의 진입점이에요. |
| `trove/Daily/YYYY-MM/YYYY-MM-DD.md` | 하루 단위 context 예시예요. |
| `trove/_config/index.md` | special contents의 영어 설명이에요. |
| `trove/_config/Memory/MEMORY.md` | 장기 기억 index예요. |
| `trove/_config/Agents/common.md` | 여러 agent entry가 공유하는 영어 원본 규칙이에요. |
| `trove/_config/Agents/agent.md` | root `AGENTS.md` 생성을 위한 영어 원본이에요. |
| `trove/_config/Agents/claude.md` | root `CLAUDE.md` 생성을 위한 영어 원본이에요. |

확인 기준:

- `find trove -maxdepth 3 -type d`로 기본 구조가 보여요.
- root `README.md`만 읽어도 첫 인스턴스 목표가 보여요.
- `trove/Home.md`는 없어요.
- `_assets/`에는 지식 문서가 없어요.
- `dist/`는 generated output이라 source 문서처럼 편집하지 않아요.

## 2단계: special contents seed 만들기

목표는 현재 AGENTS와 memory에 있는 운영 규칙을 `_config/`의 영어 markdown content로 옮길 자리를 만드는 거예요.
처음부터 모든 내용을 옮기지 않고, agent가 반복해서 써야 하는 핵심 규칙만 넣어요.

첫 seed Memory:

| 파일 | 내용 |
|---|---|
| `trove/_config/Memory/MEMORY.md` | 장기 기억 index와 첫 원칙 pointer |

첫 seed Agents:

| 파일 | 내용 |
|---|---|
| `trove/_config/Agents/common.md` | 여러 agent entry가 공유할 기본 규칙 |
| `trove/_config/Agents/agent.md` | root `AGENTS.md`로 생성될 entry source |
| `trove/_config/Agents/claude.md` | root `CLAUDE.md`로 생성될 entry source |

첫 구현 이후 추가할 Memory 후보:

| 파일 | 내용 |
|---|---|
| `trove/_config/Memory/Principles/source-of-truth.md` | source note가 진실이고 runtime memory는 pointer라는 원칙 |
| `trove/_config/Memory/Principles/memory-tiers.md` | working, daily, long-term context 기준 |
| `trove/_config/Memory/Principles/durable-documents.md` | Daily 없이도 읽히는 지속 문서 기준 |
| `trove/_config/Memory/Conventions/daily-and-worklog.md` | detailed worklog와 Daily pointer 이중 기록 |
| `trove/_config/Memory/Conventions/frontmatter.md` | frontmatter 필드와 따옴표 규칙 |
| `trove/_config/Memory/Conventions/wikilinks-and-sources.md` | wikilink, source, backlink 기준 |
| `trove/_config/Memory/Conventions/writing-voice.md` | 쉬운 한국어, 해요체, 자체 발명 용어 금지 |
| `trove/_config/Memory/Designs/context-structure.md` | Daily, Projects, `_config` 경계 |

확인 기준:

- `_config/` 문서는 영어로 작성돼요.
- 같은 원칙이 여러 파일에 길게 중복되지 않아요.
- root `AGENTS.md`와 `CLAUDE.md`는 생성물이고, 자세한 설명은 `_config/Memory/`를 가리켜요.

## 2.5단계: agent entry sync script 만들기

목표는 `_config/Agents/`의 markdown source를 repo root의 agent entry file로 반영하는 거예요.
이 script는 ACAC repo 안에서만 동작해요.
jeina의 전역 `~/.codex`, `~/.claude`, vault-backed runtime config는 건드리지 않아요.

파일:

```text
scripts/sync_agent_docs.py
```

입력과 출력:

| 입력 | 출력 |
|---|---|
| `trove/_config/Agents/common.md` + `trove/_config/Agents/agent.md` | `AGENTS.md` |
| `trove/_config/Agents/common.md` + `trove/_config/Agents/claude.md` | `CLAUDE.md` |

생성 기준:

- root output에는 `GENERATED FILE. Do not edit directly.` header를 넣어요.
- source 파일이 없으면 error로 멈춰요.
- output을 만들 때 기존 파일을 통째로 덮되, repo 밖 파일은 수정하지 않아요.
- sync는 build 전에 한 번 실행해도 되고, agent 문서가 바뀔 때 수동 실행해도 돼요.
- `AGENTS.md`와 `CLAUDE.md`도 public content로 읽힐 수 있지만, canonical note route는 `_config/Agents/*.md` source 문서가 가져요.

## 3단계: validator 만들기

목표는 문서가 쌓이기 전에 최소 품질선을 자동으로 잡는 거예요.

파일:

```text
scripts/validate_trove.py
```

검사 항목:

| 수준 | 검사 |
|---|---|
| error | frontmatter 없음 |
| error | `type`, `title`, `description`, `status`, `created`, `updated`, `visibility` 누락 |
| error | `title`과 H1 불일치 |
| error | H1 바로 아래 3-5줄 요약 없음 |
| error | 허용되지 않은 `type`, `status`, `visibility` |
| error | `_assets/` 아래 markdown 문서 발견 |
| error | public 문서인데 `/trove/<id>` route를 만들 수 없음 |
| error | 같은 `id`가 두 source file에서 발견됨 |
| warning | 깨진 wikilink 후보 |
| warning | `index.md`에 하위 문서 링크 누락 |
| warning | `description`이 너무 길거나 비어 있음 |
| warning | frontmatter `id`와 registry `id`가 달라 source 복원이 필요함 |

확인 기준:

- 정상 fixture에서 exit code `0`을 반환해요.
- 일부러 frontmatter를 깨면 exit code가 `1`이 돼요.
- error와 warning이 파일 경로와 함께 출력돼요.

## 4단계: metadata build 만들기

목표는 site가 source markdown을 직접 뒤지지 않아도 되도록 데이터를 만드는 거예요.

파일:

```text
scripts/build_trove.py
```

생성물:

| 파일 | 내용 |
|---|---|
| `data/tree.json` | sidebar tree |
| `data/notes.json` | note id, route, path, title, type, status metadata |
| `data/search-index.json` | 검색 대상 |
| `data/backlinks.json` | wikilink 기반 역링크 |
| `data/home.json` | home view 데이터 |
| `data/id-registry.json` | 문서 이동에도 살아 있는 ID registry |
| `data/build.json` | build 시각, public 문서 수, warning 수, analytics 설정 상태 |
| `_build/trove/` | site가 읽을 markdown payload |
| `dist/` | Cloudflare Workers static assets가 배포할 최종 output |

첫 구현 규칙:

- build 전에 validator를 실행해요.
- `visibility: public` 문서만 public payload에 넣어요.
- `_assets/`는 tree에서 제외해요.
- `_config/`와 `_archived/`는 special section으로 표시할 metadata를 붙여요.
- `data/id-registry.json`은 첫 metadata build에 포함해요.
- 모든 public 문서는 `/trove/<id>` route를 가져요.
- 누락된 ID는 build가 생성하고 source frontmatter에 써요.
- ID 충돌은 build error로 처리해요.

확인 기준:

- `python3 scripts/build_trove.py` 실행 후 `data/*.json`이 생성돼요.
- `tree.json`에서 `_assets/`가 보이지 않아요.
- `notes.json`에 `visibility: public` 문서만 들어가요.
- wikilink가 `backlinks.json`에 반영돼요.
- `id-registry.json`에서 `id -> currentPath`, `path -> id`, `route: /trove/<id>`를 확인할 수 있어요.
- source markdown frontmatter에 생성된 `id`가 들어가요.

ID 생성 세부 기준:

| 항목 | 기준 |
|---|---|
| ID 길이 | 10자 |
| 문자 | URL-safe alphabet: `0-9`, `A-Z`, `a-z`, `_`, `-` |
| 생성 방식 | Python `secrets.choice` 기반 |
| 충돌 처리 | registry에 이미 있으면 다시 생성 |
| 중복 감지 | 같은 ID가 두 source file에 있으면 error |
| source 반영 | missing ID는 frontmatter에 삽입 |
| 이동 감지 | 기존 ID의 path가 바뀌면 `currentPath` 갱신, 과거 path는 `previousPaths`에 추가 |

build 처리 순서:

1. `trove/` markdown 파일 목록을 만들어요.
2. `_assets/`와 public build 제외 파일을 제거해요.
3. frontmatter와 H1, 3-5줄 summary를 읽어요.
4. 기존 `data/id-registry.json`을 읽어요.
5. 문서마다 ID를 결정해요.
6. missing ID나 registry 복원 ID를 source frontmatter에 써요.
7. `data/id-registry.json`을 갱신해요.
8. `data/notes.json`에 `id`, `route`, `path`, `title`, `type`, `status`, `visibility`, `summary`, `updated`를 써요.
9. `data/tree.json`, `data/search-index.json`, `data/backlinks.json`, `data/home.json`, `data/build.json`을 생성해요.
10. `_build/trove/`에 site가 읽을 markdown payload를 복사해요.
11. `site/` 정적 앱, `data/`, `_build/trove/` payload를 `dist/`에 조립해요. Workers fallback은 `wrangler.jsonc`가 담당해요.

첫 구현에서 route는 아래 세 종류만 만들어요.

| route | source |
|---|---|
| `/` | root `README.md` + `data/home.json` |
| `/trove/<id>` | `data/id-registry.json`의 `currentPath` |
| `/search?q=<query>` | `data/search-index.json` |

`/notes/...`와 `/id/<id>`는 만들지 않아요.

## 5단계: static reader 만들기

목표는 public site에서 ACAC의 실제 사용 구조가 보이게 하는 거예요.
첫 화면은 marketing page가 아니라 문서 reader예요.

파일 후보:

```text
site/
  index.html
  assets/
    style.css
    app.js
```

초기 화면:

| 영역 | 동작 |
|---|---|
| Home view | root `README.md` 요약과 `Daily/`, `Projects/`, `_config/` 설명을 보여줘요. |
| Sidebar | `Daily/`, `Projects/`를 위에, `_config/`, `_archived/`를 아래에 보여줘요. |
| Note view | markdown 문서를 렌더링해요. |
| Search | title, description, summary 중심으로 검색해요. |
| Backlinks | note 하단이나 오른쪽 영역에 역링크를 보여줘요. |

처음에는 CDN 기반 markdown renderer를 써도 돼요.
단, build와 source 구조가 renderer에 종속되지는 않게 해요.

확인 기준:

- local server에서 home view가 열려요.
- sidebar ordering이 설계와 같아요.
- `_assets/`는 보이지 않아요.
- `trove/Projects/ai-context-as-code/index.md`를 `/trove/<id>` route로 열 수 있어요.
- 긴 제목과 설명이 모바일 폭에서 겹치지 않아요.
- Workers static assets 설정에는 `/trove/*`와 `/search`가 `index.html` app shell로 들어가는 `not_found_handling: single-page-application`이 있어요.

## 6단계: 첫 문서 마이그레이션

목표는 구조가 실제 콘텐츠를 담을 수 있는지 작은 단위로 검증하는 거예요.

순서:

1. ACAC 자체 프로젝트 문서부터 `trove/Projects/ai-context-as-code/`에 넣어요.
2. 공개 가능한 Obsidian 문서 하나를 골라 `References/`나 `Research/`에 넣어요.
3. private 정보가 있는지 사람이 한 번 검토해요.
4. validator와 build를 다시 돌려요.
5. site에서 문서, 검색, backlink가 자연스러운지 확인해요.

확인 기준:

- 첫 migration 문서는 `visibility: public`이에요.
- 문서 하나만 봐도 배경과 결론이 이해돼요.
- 관련 프로젝트 `index.md`에서 새 문서로 갈 수 있어요.
- site 검색으로 찾을 수 있어요.

## 7단계: Cloudflare Workers static assets deploy 연결

목표는 acac.sh에서 첫 인스턴스가 실제로 보이게 하는 거예요.
local 검증이 먼저 끝난 뒤 deploy를 붙여요.

확정 deploy 기준:

| 항목 | 기준 |
|---|---|
| provider | Cloudflare Workers |
| domain | `acac.sh` |
| build command | `python3 scripts/build_trove.py` |
| deploy command | `npx wrangler deploy` |
| static assets directory | `./dist` in `wrangler.jsonc` |
| route fallback | `not_found_handling: single-page-application` |
| deploy blocker | validator error, duplicate ID, public payload safety error |
| preview deploy | Workers preview versions를 사용해 main 배포 전 확인 |

공식 문서 확인:

- Cloudflare Workers static assets SPA fallback: https://developers.cloudflare.com/workers/static-assets/routing/single-page-application/
- Cloudflare Web Analytics automatic setup: https://developers.cloudflare.com/web-analytics/get-started/

확인 기준:

- deploy 전 local build가 성공해요.
- public site에 private 문서가 없어요.
- `acac.sh` 첫 화면에서 ACAC가 무엇을 할 수 있는지 보여요.
- 외부 사람이 `Projects/ai-context-as-code` 예시를 따라가며 구조를 이해할 수 있어요.
- `/trove/<id>`와 `/search` 실제 URL이 정적 배포 fallback을 통해 app shell로 들어와요.
- Cloudflare Web Analytics에서는 `/trove/<id>` page view가 문서별 방문으로 잡혀요.

## 8단계: Cloudflare Web Analytics 연결

목표는 `acac.sh` 방문과 `/trove/<id>` 문서별 page view를 가장 작게 측정하는 거예요.
첫 구현에서는 제품 analytics를 복잡하게 만들지 않고 Cloudflare Web Analytics만 붙여요.

구현 기준:

- 기본 방식은 Cloudflare dashboard automatic setup이에요.
- `ACAC_CF_WEB_ANALYTICS_TOKEN`은 manual beacon injection을 선택한 경우에만 환경 변수에서 읽어요.
- token이 없으면 analytics script를 넣지 않고 `data/build.json`에 `analytics.enabled: false`, `analytics.manualBeacon: false`를 기록해요.
- token이 있으면 `site/index.html`의 analytics placeholder에 Cloudflare beacon script를 주입하고 `analytics.manualBeacon: true`를 기록해요.
- SPA 측정은 Cloudflare Web Analytics의 History API 추적에 맡겨요.
- Hash route를 쓰지 않기 때문에 `/trove/<id>` 이동이 문서별 page view로 잡힐 수 있어요.
- dashboard automatic setup과 manual token injection을 중복으로 켜지 않아요.

공식 문서 확인:

- Cloudflare Web Analytics SPA tracking: https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/
- Cloudflare Web Analytics setup: https://developers.cloudflare.com/web-analytics/get-started/

확인 기준:

- local build에서 token이 없을 때도 site가 정상 동작해요.
- token을 넣고 build하면 output HTML에 Cloudflare beacon script가 들어가요.
- `/`, `/trove/<id>`, `/search?q=...` 이동이 실제 History API route로 남아요.
- Cloudflare dashboard에서 배포 후 page view가 들어오는지 확인할 수 있어요.

## 다음 단계로 미룰 것

아래는 중요하지만 첫 구현의 성공 조건은 아니에요.

- graph view
- browser editor
- GitHub API 저장
- clipboard image paste
- note move/delete modal
- 전체 Obsidian import 자동화
- private trove와 public trove 분리
- repo 밖 agent runtime config 자동 sync
- Cloudflare Analytics 외의 product analytics
- 한국어 원본의 영어 번역 자동 생성

## 첫 구현 완료 기준

첫 구현은 아래가 모두 되면 끝난 것으로 봐요.

- repo에 `trove/`, `site/`, `scripts/`, `data/` 구조가 있어요.
- `trove/Projects/ai-context-as-code/`가 첫 실제 프로젝트 예시로 작동해요.
- `_config/Memory`, `_config/Skills`, `_config/Commands`, `_config/Agents`의 역할이 문서로 보여요.
- `scripts/validate_trove.py`가 기본 문서 오류를 잡아요.
- `scripts/build_trove.py`가 site용 metadata를 만들어요.
- site에서 home, sidebar, `/trove/<id>`, `/search` route가 작동해요.
- Cloudflare Workers static assets output인 `dist/`가 생성돼요.
- Cloudflare Web Analytics token이 있으면 manual beacon script가 output에 들어가고, 없으면 manual beacon off 상태가 build metadata에 남아요.
- `_config/Agents/common.md`, `agent.md`, `claude.md`에서 root `AGENTS.md`, `CLAUDE.md`를 생성할 수 있어요.
- public site에 들어간 문서는 모두 public-safe예요.
- 첫 화면과 README를 보면 ACAC가 “cloud에서 durable context를 관리하는 방식”이라는 점이 이해돼요.
