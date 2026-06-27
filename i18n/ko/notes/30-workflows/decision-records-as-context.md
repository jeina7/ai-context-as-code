---
title: 결정 기록을 컨텍스트로 쓰기
---

# 결정 기록을 컨텍스트로 쓰기

## 요약

결정은 단순한 history가 아니에요.
미래의 agent가 같은 질문을 근거 없이 다시 열지 않게 하는 context예요.
좋은 decision record는 선택, 버린 대안, 당시 그 선택이 타당했던 이유를 설명해요.

## 패턴

시스템의 형태를 바꾸는 선택이 생기면 decision note를 써요.

노트는 아래 질문에 답해야 해요.

- 무엇이 바뀌었나요?
- 왜 이 선택인가요?
- 무엇을 의도적으로 하지 않았나요?
- 미래의 agent가 바꾸기 전에 무엇을 확인해야 하나요?

## 적용

이 repo는 naming, local-first 구현, GitHub Pages, build process가 context가 되는 이유 같은 프로젝트 선택을 `notes/50-decisions/`에 남겨요.

## 관련

- [[why-context-as-code]]
- [[why-build-process-becomes-context]]
- [[reviewable-ai-workflows]]
