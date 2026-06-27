---
title: 외부 영향 전 승인
---

# 외부 영향 전 승인

## 요약

어떤 행동은 실행하기 쉽지만 되돌리기 어려워요.
배포, 메시지 전송, 비용 지출, 권한 변경, 외부 연락은 agent가 할 수 있다는 이유만으로 실행되면 안 돼요.
시스템은 local preparation과 external action을 분리해야 해요.

## 패턴

agent는 합의된 workspace 안에서 local artifact를 자유롭게 준비할 수 있어요.

하지만 외부 세계에 영향을 주는 행동 전에는 명시적인 승인이 필요해요.

- remote repository 생성 또는 변경
- site 배포
- outbound message 전송
- access 권한 부여
- 비용 지출
- 오래 남는 기록 삭제

## 적용

AI Context as Code는 local에서 전부 만들고 검토할 수 있어요.
GitHub remote 생성과 Pages 배포는 승인 후에만 진행해요.

## 관련

- [[publishable-import-workflow]]
- [[reviewable-ai-workflows]]
- [[why-markdown-git-github-pages]]
