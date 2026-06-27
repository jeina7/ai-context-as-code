---
title: 공유 가능한 맥락과 private 맥락의 분리
---

# 공유 가능한 맥락과 private 맥락의 분리

## 요약

지식 시스템은 private vault의 직접 복사본이 되면 안 돼요.
private note는 raw context를 담을 수 있지만, 공유 가능한 노트는 review와 generalization이 필요해요.
이 분리는 풍부한 private memory를 유지하면서도 재사용 가능한 지식을 안전하게 드러낼 수 있게 해줘요.

## 패턴

두 공간을 써요.

- raw, sensitive, personal material을 위한 private source space
- 검토되고 일반화된 reusable note를 위한 memory space

자료는 review step을 통해서만 private에서 공유 가능한 쪽으로 이동해요.

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
