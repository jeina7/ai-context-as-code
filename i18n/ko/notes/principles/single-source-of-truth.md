---
title: 단일 출처
---

# 단일 출처

## 요약

AI 에이전트는 행동하기 전에 확인할 안정적인 장소가 필요해요.
중요한 맥락이 채팅, 초안, 메모 조각에 흩어져 있으면 매 세션이 추측으로 시작돼요.
context system은 오래 남길 출처를 찾고, 검토하고, 업데이트하기 쉽게 만들어야 해요.

## 원칙

반복되는 결정이나 workflow에는 서로 다른 참고 자료가 충돌할 때 이기는 하나의 오래 남는 출처가 있어야 해요.

메모리 파일, 요약, 생성된 index는 lookup을 빠르게 할 수 있어요.
하지만 그것들이 출처 자체는 아니에요.
출처는 사람이 읽을 수 있고, versioned 되어야 하며, 그것을 바꾼 결정과 연결되어야 해요.

## 적용

AI Context as Code는 `notes/`, `conventions/`, `agents/`를 오래 남는 source file로 다뤄요.
생성된 JSON은 site와 agent를 위해 존재하지만, 언제든 source에서 다시 만들 수 있어요.

## 관련

- [[knowledge-as-code]]
- [[agent-maintained-notes]]
- [[runtime-verification]]
