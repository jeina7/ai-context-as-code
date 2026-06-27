---
title: 에이전트형 지식 시스템
---

# 에이전트형 지식 시스템

## 요약

에이전트형 지식 시스템은 AI agent가 매 session 처음부터 시작하지 않고 오래 남는 context로 작업하게 도와요.
최근 흐름은 고립된 prompt에서 context engineering, codified context, agent-maintained knowledge layer로 이동하고 있어요.
AI Context as Code는 이 방향의 가볍고 markdown-first인 구현이에요.

## 관찰

관련 업계 용어는 다음과 같아요.

- context engineering
- agentic context engineering
- codified context
- knowledge layer
- agent harness
- Model Context Protocol

이 용어들은 같은 근본 문제를 가리켜요.
AI agent가 안정적으로 행동하려면 구조화되고, 검증되고, 진화하는 context가 필요해요.

## 경계

이 프로젝트는 full agent harness가 아니라 context layer로 시작해요.
tool permission, execution trace, automatic commit 같은 harness 기능은 context source가 신뢰 가능해진 뒤에 붙일 수 있어요.

## 관련

- [[context-engineering]]
- [[agentic-context-engineering]]
- [[codified-context]]
