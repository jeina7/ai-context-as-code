---
title: 구현 로드맵 검토
---

# 구현 로드맵 검토

## 요약

현재 제품에는 정적 context workspace, 한국어 읽기 모드, graph view, 브라우저 임시 편집, modal search, 생성된 검색 metadata, 익숙한 agent config 표면이 들어가 있어요.

이번에 가장 크게 비어 있던 부분은 agent 설정 구조였어요.
이제 `AGENTS.md`, `CLAUDE.md`, `skills/`, `memory/`가 실제 저장소 구조로 존재해요.
`agent-runtime/`은 호환용 index로만 남겨요.

## 이번 패스에서 완료한 것

- 루트 `AGENTS.md`를 추가했어요.
- 루트 `CLAUDE.md`를 추가했어요.
- 재사용 가능한 agent 절차 후보를 담는 `skills/`를 추가했어요.
- 오래 남길 맥락을 가리키는 작은 포인터를 담는 `memory/`를 추가했어요.
- navbar 검색을 짧은 trigger로 바꿨어요.
- 검색 modal에 command 그룹, note snippet, 키보드 이동, 빈 상태, ranking을 추가했어요.
- `Interface Design Direction`을 추가했어요.
- agent runtime 문서를 agent configuration 문서로 다시 설명했어요.
- command/search modal이 생성된 검색 metadata를 쓰도록 연결했어요.
- 브라우저 patch export에 section 단위 검토 블록을 추가했어요.
- graph insight가 가장 중요한 연결 이유를 설명하도록 바꿨어요.
- Obsidian import report에 위험도, 목적지, rewrite checklist, rewrite prompt를 추가했어요.
- desktop과 mobile screenshot을 남기는 viewport QA script를 추가했어요.

## 더 만들 가치가 있는 것

- 현재 topic 폴더를 product, method, corpus, research, operations로 나누는 콘텐츠 구조 migration
- 기존 note slug를 옮기기 전 필요한 alias와 redirect 지원
- 정적 index로 부족해졌을 때 붙일 semantic search나 embedding 기반 검색
- 끊긴 링크, 오래된 문구, 번역 차이를 기준으로 묶어 보여주는 더 풍부한 review queue
- 여러 Obsidian 후보를 비교하고 하나의 rewritten note outline을 제안하는 import report

## 제품 경계가 바뀌어서 미룬 것

- 브라우저에서 GitHub API로 직접 commit하기
- 로그인과 권한 관리
- 조직 단위 workspace
- 비공개 Obsidian 전체 이전
- 비공개 원본을 자동 publish하는 기능

## 관련

- [[ai-context-as-code-design]]
- [[interface-design-direction]]
- [[agent-runtime-references]]
- [[content-structure-plan]]
