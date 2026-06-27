---
title: AI Context as Code 설계
---

# AI Context as Code 설계

## 요약

AI Context as Code는 사람과 AI agent를 위한 markdown-first context system이에요.
처음에는 개인용 context layer로 시작해요.
나중에는 core source format을 바꾸지 않고도 조직용 context system으로 커질 수 있어요.

## 설계

시스템에는 다섯 layer가 있어요.

- authoring layer: `notes/`와 `conventions/`
- safety layer: `private-staging/`, safety check, validation
- build layer: metadata, link, backlink, search, generated JSON
- serving layer: static GitHub Pages site
- agent layer: rule, command, review loop, future skill

## 경계

이 시스템은 private vault의 직접 mirror가 아니에요.
검토되고 일반화되어 외부에 보여도 안전한 material만 담아요.

## 관련

- [[why-build-ai-context-as-code]]
- [[publishable-private-context-split]]
- [[context-engineering]]
