---
title: 에이전트 런타임 참조
---

# 에이전트 런타임 참조

## 요약

AI Context as Code에는 agent가 직접 읽는 표면이 필요해요.
그 표면의 이름은 `agent-runtime/`이 가장 자연스러워요.

`config`는 너무 넓어요.
`harness`는 test wrapper처럼 들려요.
`agent-runtime`은 폴더의 목적을 바로 말해요. Agent가 작동할 때 읽는 파일들이에요.

## 규칙

Agent-facing instruction은 안정적인 시작점 하나를 가져야 해요.
다른 폴더가 editable source를 소유한다면, 그 시작점은 symlink로 source file을 모아도 돼요.

이 방식은 Obsidian 기반 agent setup에서 skill, memory, command, instruction을 복사하지 않고 runtime에 노출하는 방식과 닮아 있어요.

## 현재 참조

첫 번째 runtime reference는 이것들이에요.

- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

이 파일들은 `conventions/`와 `agents/`로 이어지는 symlink예요.
Agent는 `agent-runtime/`을 먼저 읽고, 사람은 source folder를 계속 편집하면 돼요.

## 앞으로의 모양

Runtime surface는 이렇게 커질 수 있어요.

```text
agent-runtime/
  README.md
  agent-rules.md
  note-format.md
  review-rules.md
  publish-safety.md
  context-rules.md
  commands/
  skills/
  memory/
```

`skills/`는 재사용 가능한 agent procedure를 담아요.
`memory/`는 private context 전체가 아니라 durable note를 가리키는 작은 pointer를 담아요.

## 하지 않을 것

이 구조는 private Obsidian memory를 repo에 복사하지 않아요.
아직 browser에서 agent instruction을 직접 편집하게 만들지는 않아요.
나중에 생성, sync, 검증할 수 있는 runtime entry point를 먼저 만들어요.

## 관련

- [[ai-context-as-code-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
