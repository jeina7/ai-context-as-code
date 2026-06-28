---
title: 옮기기 전 검토 작업 흐름
---

# 옮기기 전 검토 작업 흐름

## 요약

비공개 노트는 맥락 층으로 바로 옮기면 안 돼요.
먼저 위험한 내용이 있는지 보고, 필요한 부분만 다시 써야 해요.
가져오기는 복사가 아니라 선별이에요.

## 작업 흐름

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

- 가져오기 보고서는 `private-staging/`에 남겨요.
- 날것의 비공개 원본은 `notes/`에 들어가지 않아요.
- 다시 쓴 노트는 개인 사건이 아니라 재사용 가능한 아이디어를 보존해야 해요.
- 안전 점검은 실수를 줄이지만 판단을 대체하지 않아요.

## 관련

- [[publishable-private-context-split]]
- [[why-not-full-obsidian-migration]]
- [[acac-sh-design]]
