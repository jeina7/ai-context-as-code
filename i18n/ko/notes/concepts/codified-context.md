---
title: 코드화된 컨텍스트
---

# 코드화된 컨텍스트

## 요약

코드화된 context는 프로젝트 지식, 규칙, 운영 convention을 versioned file로 바꾸는 방식이에요.
그러면 agent는 채팅 history에 의존하지 않고 session을 넘어 context를 이어갈 수 있어요.
이 방식은 반복 설명을 줄이고 실패를 검토하기 쉽게 해요.

## 패턴

코드화된 context에는 보통 이런 것들이 들어가요.

- 오래 남는 노트
- convention
- review rule
- task command
- validation script
- decision record

## 적용

AI Context as Code에서 `notes/`는 재사용 가능한 context를 저장해요.
`conventions/`는 운영 규칙을 저장하고, `scripts/`는 이 context가 배포 가능한 상태인지 검증해요.

## 관련

- [[knowledge-as-code]]
- [[context-engineering]]
- [[agent-maintained-notes]]
