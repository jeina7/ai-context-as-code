---
title: 공유 가능한 맥락과 비공개 맥락의 분리
---

# 공유 가능한 맥락과 비공개 맥락의 분리

## 요약

지식 시스템은 비공개 볼트의 직접 복사본이 되면 안 돼요.
비공개 노트는 raw 맥락을 담을 수 있지만, 공유 가능한 노트는 검토와 generalization이 필요해요.
이 분리는 풍부한 비공개 기억를 유지하면서도 재사용 가능한 지식을 안전하게 드러낼 수 있게 해줘요.

## 패턴

두 공간을 써요.

- raw, sensitive, personal 자료를 위한 비공개 원본 space
- 검토되고 일반화된 reusable note를 위한 기억 space

자료는 검토 step을 통해서만 비공개에서 공유 가능한 쪽으로 이동해요.

```text
private source
→ private staging
→ safety review
→ rewrite
→ notes
```

## 관련

- [[why-build-ai-context-as-code]]
- [[agent-maintained-notes]]
