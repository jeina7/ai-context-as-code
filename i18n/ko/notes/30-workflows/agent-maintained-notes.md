---
title: 에이전트가 관리하는 노트
---

# 에이전트가 관리하는 노트

## 요약

AI agent는 knowledge system 관리를 도울 수 있지만, 규칙과 review가 필요해요.
유용한 loop는 자동 작성만이 아니에요.
검색하고, 제안하고, 검증한 뒤 shared memory를 개선하는 loop가 중요해요.

## 패턴

agent가 관리하는 note system은 이렇게 동작해야 해요.

- 새로 쓰기 전에 기존 노트를 검색해요.
- 같은 개념이 있으면 새 노트보다 기존 노트 개선을 우선해요.
- 배포 전에 validation을 실행해요.
- 민감한 context를 노트 밖에 둬요.
- 같은 feedback이 반복되면 convention을 업데이트해요.

## 관련

- [[knowledge-as-code]]
- [[publishable-private-context-split]]
