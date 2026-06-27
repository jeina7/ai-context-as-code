---
title: 콘텐츠 구조 계획
---

# 콘텐츠 구조 계획

## 요약

AI Context as Code에는 두 가지 역할이 있어요.
하나는 context as code를 보여주는 제품이에요.
다른 하나는 그 제품이 직접 관리하는 첫 번째 실제 context corpus예요.

노트 구조는 이 두 역할을 쉽게 구분할 수 있어야 해요.
제품 노트는 시스템을 설명해요.
방법 노트는 반복해서 쓸 수 있는 일하는 방식을 설명해요.
Corpus 노트는 이 시스템이 실제로 쓸모 있다는 걸 보여주는 context를 담아요.

## 현재 작성 기준

현재 노트는 이런 기준으로 작성되어 있어요.

- 개인 Obsidian note에 기대지 않고 제품 방향을 설명해요.
- 결정은 chat history가 아니라 오래 남는 context로 보관해요.
- AI가 읽기 쉬운 English를 source of truth로 둬요.
- 사람이 검토할 수 있도록 Korean reading copy를 제공해요.
- 모든 노트는 읽고, 연결하고, 수정하기 쉬운 크기로 유지해요.
- 개인 source material은 이 repo 안에서 독립적으로 읽힐 수 있을 때만 옮겨요.

## 현재 폴더 의미

현재 폴더도 쓸모는 있지만, 경계가 아직 충분히 자연스럽지는 않아요.

- `start/`는 시작점이에요.
- `principles/`는 안정적인 원칙을 담아요.
- `concepts/`는 재사용 가능한 정의를 담아요.
- `workflows/`는 반복 가능한 운영 절차를 담아요.
- `projects/`는 제품과 adoption 계획을 같이 담고 있어요.
- `decisions/`는 왜 특정 선택을 했는지 담아요.
- `research/`는 외부 흐름에서 얻은 field note를 담아요.
- `worklog/`는 구현 이력을 담아요.

어색한 지점은 `projects/`예요.
제품 설계와 이전 계획이 섞여 있어요.
그래서 repo가 working context product라기보다 일반 document system처럼 느껴질 수 있어요.

## 제안 폴더 구조

다음 구조는 product, method, corpus를 분리해야 해요.

```text
notes/
  product/
    overview.md
    interface-map.md
    design-principles.md
    roadmap.md
  runtime/
    agent-runtime-references.md
  method/
    principles/
    concepts/
    workflows/
  corpus/
    obsidian-transition-plan.md
    import-policy.md
    first-pass-import.md
  decisions/
  research/
  worklog/
```

## Obsidian 매핑 규칙

Obsidian note를 검토할 때는 이 기준을 써요.

- 제품 설계, 인터페이스, 로드맵, 시스템 동작은 `product/`로 가요.
- Agent가 직접 읽는 instruction, command, skill, memory reference는 `runtime/`으로 가요.
- 재사용 가능한 사고 패턴과 운영 규칙은 `method/`로 가요.
- 시스템이 실제로 쓸모 있다는 걸 보여주는 imported context는 `corpus/`로 가요.
- 되돌리기 어려운 선택은 `decisions/`로 가요.
- 외부 트렌드 정리는 `research/`로 가요.
- 구현 진행 기록은 `worklog/`로 가요.

## 하지 않을 것

이 구조는 모든 Obsidian note를 옮기지 않아요.
개인 생활 context를 이 repo에 합치지 않아요.
조직 기능을 추가하지 않아요.
오픈소스 제품과 실제 개인 context corpus가 함께 자랄 수 있는 모양을 먼저 잡아요.

## 관련

- [[ai-context-as-code-design]]
- [[agent-runtime-references]]
- [[obsidian-transition-plan]]
- [[publishable-private-context-split]]
