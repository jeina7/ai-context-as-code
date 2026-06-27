---
title: 운영 루틴
---

# 운영 루틴

## 요약

AI Context as Code가 건강하게 유지되려면 작고 반복 가능한 routine이 필요해요.
의미 있는 변경은 write, link, validate, build, review를 지나야 해요.
그래야 context layer를 사람과 agent가 모두 쓸 수 있어요.

## 루틴

새 노트나 변경마다 아래 순서로 진행해요.

1. 기존 노트를 검색해요.
2. 가장 작은 유용한 노트를 쓰거나 업데이트해요.
3. 관련 wikilink를 추가해요.
4. `python3 scripts/review_context.py`를 실행해요.
5. safety, validation, broken link 문제를 고쳐요.
6. check가 통과한 뒤에만 commit해요.

## 주간 리뷰

일주일에 한 번 확인해요.

- 중복 concept 찾기
- 약한 summary 개선하기
- 낡은 decision 확인하기
- 유용한 worklog를 durable note로 승격하기
- 실수가 반복되면 convention 업데이트하기

## 관련

- [[self-evolving-context-loop]]
- [[agent-maintained-notes]]
- [[publishable-import-workflow]]
