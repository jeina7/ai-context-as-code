---
title: 검토 가능한 AI workflow
---

# 검토 가능한 AI workflow

## 요약

AI output은 근거를 남길 때 더 유용해져요.
검토 가능한 workflow는 어떤 source를 썼고, 어떤 check를 실행했고, 어떤 decision이 뒤따랐는지 보여줘요.
그래야 AI 작업을 더 쉽게 신뢰하고, 고치고, 재사용할 수 있어요.

## 패턴

AI workflow는 의미 있는 변경마다 아래 내용을 남기도록 설계해요.

- input context
- generated output
- validation result
- 필요할 때의 human decision
- durable record

기록이 길 필요는 없어요.
다음 독자가 무엇이 왜 바뀌었는지 이해할 만큼이면 돼요.

## 적용

이 프로젝트에서 검토 가능한 AI workflow는 agent가 명시적인 file update로 노트를 고치고, `scripts/review_context.py`를 실행하고, 의미 있는 변경이면 worklog를 남기는 것을 뜻해요.

## 관련

- [[ai-native-expertise]]
- [[self-evolving-context-loop]]
- [[decision-records-as-context]]
