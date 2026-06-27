---
title: 컨텍스트와 하네스의 경계
---

# 컨텍스트와 하네스의 경계

## 요약

context layer와 agent harness는 관련이 있지만 같은 것은 아니에요.
context layer는 오래 남길 지식과 규칙을 저장해요.
harness는 agent를 tool, permission, observation, verification, execution state로 감싸는 실행 환경이에요.

## 경계

AI Context as Code는 context layer로 시작해요.

아래 기능을 관리하기 시작할 때 harness에 가까워져요.

- tool access
- task state
- execution trace
- verification report
- permission boundary
- intervention record
- commit 또는 pull request workflow

## 의미

context source가 신뢰할 수 있기 전에는 harness 기능을 먼저 붙이지 않아요.
약한 context layer는 execution layer를 디버깅하기 더 어렵게 만들어요.

## 관련

- [[context-engineering]]
- [[agentic-context-engineering]]
- [[ai-context-as-code-design]]
