---
title: 실행 환경 검증
---

# 실행 환경 검증

## 요약

workflow는 script가 존재한다고 증명되지 않아요.
중요한 환경에서 script가 실행되고, 그 결과를 확인할 때 증명돼요.
AI가 관리하는 시스템에는 실제 사용과 가까운 검증이 필요해요.

## 패턴

자동화되거나 생성되는 시스템을 바꾼 뒤에는 세 층을 검증해요.

- source check가 통과해야 해요.
- generated artifact를 다시 만들어야 해요.
- user-facing path가 결과를 load할 수 있어야 해요.

static knowledge system에서는 note validation, metadata rebuild, site loading 확인이 여기에 해당해요.

## 적용

`scripts/review_context.py`는 이 repo의 local runtime verification entrypoint예요.
safety check, note validation, metadata build를 한 번에 실행해요.

## 관련

- [[reviewable-ai-workflows]]
- [[single-source-of-truth]]
- [[operating-routine]]
