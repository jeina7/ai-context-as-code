---
title: 왜 Markdown, Git, GitHub Pages인가
---

# 왜 Markdown, Git, GitHub Pages인가

## 요약

첫 버전은 inspectable, forkable, cheap to operate 해야 해요.
Markdown, Git, GitHub Pages는 신뢰할 수 있을 만큼 시스템을 단순하게 유지해요.
더 복잡한 editing layer나 에이전트 execution layer는 나중에 붙일 수 있어요.

## 결정

Markdown file을 원본로 쓰고, Git으로 기록를 남기고, Python script로 메타데이터를 만들고, GitHub Pages로 static hosting해요.

## 이유

이 stack은 core knowledge를 portable하게 유지해요.
또한 첫 safety boundary를 단순하게 만들어요.
`notes/`에 들어간 노트는 검토된 원본라는 뜻이에요.

## 관련

- [[knowledge-as-code]]
- [[acac-sh-design]]
