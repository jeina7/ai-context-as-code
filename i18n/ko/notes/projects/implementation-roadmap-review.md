---
title: 구현 로드맵 검토
---

# 구현 로드맵 검토

## 요약

현재 제품에는 정적 context workspace, 한국어 읽기 모드, graph view, 브라우저 임시 편집, modal search, 익숙한 agent config 표면이 들어가 있어요.

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

## 더 만들 가치가 있는 것

- 현재 topic 폴더를 product, method, corpus, research, operations로 나누는 콘텐츠 구조 migration
- 브라우저 안 계산이 아니라 생성된 index를 쓰는 검색 ranking
- 노트 section 단위로 더 구조적인 patch를 만드는 브라우저 편집
- 연결이 있다는 사실뿐 아니라 왜 중요한지 설명하는 graph insight
- 실제 viewport 측정 기반의 더 체계적인 mobile QA
- Obsidian 후보를 위한 더 나은 import review report

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
