---
title: 컨텍스트 엔지니어링
---

# 컨텍스트 엔지니어링

## 요약

컨텍스트 엔지니어링은 AI 시스템이 판단에 쓰는 정보 환경을 설계하는 일이에요.
prompt 작성보다 넓은 개념이에요.
source 선택, 구조, 검증, retrieval, update rule, 출처 추적까지 포함해요.

## 패턴

AI 시스템에는 이런 context가 필요해요.

- task와 관련 있어야 해요.
- 판단에 충분해야 해요.
- 관련 없는 noise와 분리되어야 해요.
- runtime limit에 들어갈 만큼 경제적이어야 해요.
- 출처를 추적할 수 있어야 해요.
- 현실이 바뀌면 업데이트할 수 있어야 해요.

## 적용

AI Context as Code는 markdown note와 convention을 context infrastructure로 다뤄요.
목표는 agent가 매번 다시 발견하지 않아도 재사용할 수 있을 만큼 유용한 context를 오래 남기는 거예요.

## 관련

- [[ai-native-expertise]]
- [[codified-context]]
- [[agentic-context-engineering]]
