---
title: 왜 만드는 과정도 context가 되는가
---

# 왜 만드는 과정도 context가 되는가

## 요약

AI Context as Code를 만드는 과정 자체도 시스템의 일부가 되어야 해요.
구현 선택, validation failure, naming decision, import rule은 모두 재사용 가능한 context예요.
이것들이 chat이나 private log에만 남으면 미래의 agent가 같은 맥락을 반복해서 다시 찾아야 해요.

## 결정

유용한 build history를 note, decision, convention, script로 승격해요.

## 이유

이 프로젝트는 사용을 통해 좋아지는 context를 만들려는 프로젝트예요.
첫 번째 증명은 프로젝트가 만들어지는 동안 자신의 context를 포착하고 개선할 수 있는지예요.

## 관련

- [[self-evolving-context-loop]]
- [[operating-routine]]
- [[2026-06-27-initial-build]]
