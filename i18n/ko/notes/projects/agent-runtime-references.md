---
title: 에이전트 설정 참조
---

# 에이전트 설정 참조

## 요약

acac.sh에는 에이전트가 바로 읽을 수 있는 설정 표면이 필요해요.
하지만 이것이 별도의 agent framework처럼 보이면 안 돼요.
`AGENTS.md`, `CLAUDE.md`, skill, memory, command 같은 익숙한 구조를 그대로 활용해야 해요.

현재 `agent-runtime/` 폴더는 호환용 시작점일 뿐이에요.
에이전트가 읽을 참조를 모아 보여주는 index예요.
새로운 runtime 모델을 정의하지 않아요.

## 규칙

에이전트 안내문은 이미 익숙한 설정 표면을 써야 해요.
다른 폴더가 편집 가능한 원본을 소유한다면, 에이전트가 읽는 시작점은 symlink로 원본을 가리키면 돼요.

이 방식은 Obsidian 기반 에이전트 설정에서 skill, memory, command, instruction을 복사하지 않고 노출하는 방식과 같아요.

## 현재 참조

현재 설정 참조는 이것들이에요.

- `AGENTS.md`
- `CLAUDE.md`
- `agents/commands/`
- `agents/shared/`
- `skills/`
- `memory/`
- `conventions/`
- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

`agent-runtime/` 안의 항목은 `conventions/`와 `agents/`로 이어지는 호환용 symlink예요.
에이전트는 먼저 `AGENTS.md`나 `CLAUDE.md`를 읽고, 작업에 필요한 command, skill, memory, convention 파일로 이동하면 돼요.

## 현재 모양

이제 저장소는 익숙한 이름을 실제로 써요.

```text
AGENTS.md
CLAUDE.md
agents/
  commands/
  shared/
skills/
memory/
conventions/
agent-runtime/
```

`skills/`는 재사용 가능한 에이전트 절차를 담아요.
`memory/`는 비공개 맥락 전체가 아니라 오래 남길 노트를 가리키는 작은 포인터를 담아요.
`agent-runtime/`은 한 폴더에서 참조를 보고 싶은 도구를 위한 index로만 남겨요.

## 하지 않을 것

이 구조는 비공개 Obsidian 기억을 저장소에 복사하지 않아요.
아직 브라우저에서 에이전트 안내문을 직접 편집하게 만들지는 않아요.
독자적인 agent configuration 표준을 새로 만들지 않아요.

## 관련

- [[acac-sh-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
