---
title: 옮기기 전 검토 workflow
---

# 옮기기 전 검토 workflow

## 요약

private note는 context layer로 바로 이동하면 안 돼요.
분석, risk detection, rewriting, validation이 필요해요.
import process는 copy operation이 아니라 filter예요.

## workflow

```text
private source
→ dry-run import report
→ risk review
→ rewrite into durable note
→ validate links and frontmatter
→ safety check
→ commit
```

## 규칙

- import report는 `private-staging/`에 남겨요.
- raw private source는 `notes/`에 들어가지 않아요.
- 다시 쓴 노트는 private event가 아니라 재사용 가능한 idea를 보존해야 해요.
- safety check는 실수를 줄이지만 판단을 대체하지 않아요.

## 관련

- [[publishable-private-context-split]]
- [[why-not-full-obsidian-migration]]
- [[ai-context-as-code-design]]
