---
title: Knowledge as Code
---

# Knowledge as Code

## 요약

Knowledge as Code는 오래 남길 노트를 software project처럼 다루는 방식이에요.
노트는 version control 안에 있고, convention을 따르며, 배포 전에 validation을 통과해요.
이렇게 하면 사람과 agent가 지식을 더 쉽게 재사용할 수 있어요.

## 패턴

plain file을 source of truth로 두고, 그 위에서 index와 view를 생성해요.

```text
markdown notes
→ metadata build
→ validation
→ static site
→ agent review
```

## 관련

- [[agent-maintained-notes]]
- [[why-build-ai-context-as-code]]
