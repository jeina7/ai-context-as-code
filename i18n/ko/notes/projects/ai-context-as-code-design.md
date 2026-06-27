---
title: AI Context as Code 설계
---

# AI Context as Code 설계

## 요약

AI Context as Code는 사람과 AI agent를 위한 markdown-first context system이에요.
처음에는 제품 repo로 시작하고, 자기 자신의 개발 맥락을 첫 번째 corpus로 삼아요.
나중에는 core source format을 바꾸지 않고도 조직용 context system으로 커질 수 있어요.

## 설계

시스템에는 다섯 layer가 있어요.

- authoring layer: `notes/`와 `conventions/`
- safety layer: `private-staging/`, safety check, validation
- build layer: metadata, link, backlink, search, generated JSON
- serving layer: static GitHub Pages site
- agent runtime layer: symlink된 rule, command, review loop, future skill 또는 memory reference

## 경계

이 repo는 UI가 붙은 private vault처럼 보이면 안 돼요.
자기 자신의 검토된 context를 첫 dataset으로 가진 제품처럼 보여야 해요.

그래서 product code, product decision, example context는 함께 있을 수 있지만 역할이 분리되어야 해요.

- product code는 시스템을 실제로 쓸 수 있음을 보여줘요.
- product decision은 시스템이 왜 존재하는지 설명해요.
- context corpus는 시간이 지나며 유용한 지식을 어떻게 포착하는지 보여줘요.
- agent runtime은 agent가 작동할 때 무엇을 직접 읽을 수 있는지 보여줘요.

이 corpus는 private vault의 전체 mirror가 아니에요.
private source 없이도 이해되는, 검토되고 일반화된 material만 담아요.

## 관련

- [[why-build-ai-context-as-code]]
- [[agent-runtime-references]]
- [[publishable-private-context-split]]
- [[context-engineering]]
