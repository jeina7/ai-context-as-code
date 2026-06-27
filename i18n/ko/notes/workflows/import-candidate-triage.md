---
title: 가져올 후보 선별
---

# 가져올 후보 선별

## 요약

유용한 private note가 모두 옮길 만한 노트는 아니에요.
어떤 노트는 private fact를 담고 있지만, 그 안에 재사용 가능한 idea가 있을 수 있어요.
triage는 그 idea를 건너뛸지, 다시 쓸지, 병합할지, 승격할지 결정해요.

## 선별

각 후보는 네 가지 결과 중 하나로 분류해요.

- skip: 가치가 private detail에 의존해요.
- extract: private detail 없이 재사용 가능한 idea로 다시 써요.
- merge: insight를 기존 노트에 추가해요.
- promote: idea가 분명히 독립적이면 새 노트를 만들어요.

기본값은 skip 또는 extract여야 해요.
직접 promote는 드물어야 해요.

## 적용

Obsidian vault를 스캔할 때 AI Context as Code는 folder를 복사하지 않아야 해요.
dry-run report를 만들고, 재사용 가능한 pattern을 찾은 뒤, target context에 맞게 다시 쓴 후에만 durable note를 작성해야 해요.

## 관련

- [[publishable-import-workflow]]
- [[publishable-private-context-split]]
- [[approval-before-external-side-effects]]
