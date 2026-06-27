---
title: 에이전트 런타임 참조
---

# 에이전트 런타임 참조

## 요약

AI Context as Code에는 에이전트가 바로 읽을 수 있는 기준 위치가 필요해요.
그 위치의 이름은 `agent-runtime/`이 가장 자연스러워요.

`config`는 너무 넓어요.
`harness`는 테스트용 실행 장치처럼 들려요. 한국어로는 하네스라고 부를 수 있어요.
`agent-runtime`은 폴더의 목적을 바로 말해요. 에이전트가 작동할 때 읽는 파일들이에요.

## 규칙

에이전트가 읽는 안내문은 안정적인 시작점 하나를 가져야 해요.
다른 폴더가 편집 가능한 원본을 소유한다면, 그 시작점은 symlink로 원본 파일을 모아도 돼요.

이 방식은 Obsidian 기반 에이전트 설정에서 스킬, 기억, 명령, 안내문을 복사하지 않고 한곳에 드러내는 방식과 닮아 있어요.

## 현재 참조

첫 번째 실행 기준은 이것들이에요.

- `agent-runtime/agent-rules.md`
- `agent-runtime/note-format.md`
- `agent-runtime/review-rules.md`
- `agent-runtime/publish-safety.md`
- `agent-runtime/context-rules.md`
- `agent-runtime/commands/`

이 파일들은 `conventions/`와 `agents/`로 이어지는 symlink예요.
에이전트는 `agent-runtime/`을 먼저 읽고, 사람은 원본 폴더를 계속 편집하면 돼요.

## 앞으로의 모양

실행 기준 모음은 이렇게 커질 수 있어요.

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

`skills/`는 재사용 가능한 에이전트 절차를 담아요.
`memory/`는 비공개 맥락 전체가 아니라 오래 남길 노트를 가리키는 작은 포인터를 담아요.

## 하지 않을 것

이 구조는 비공개 Obsidian 기억을 저장소에 복사하지 않아요.
아직 브라우저에서 에이전트 안내문을 직접 편집하게 만들지는 않아요.
나중에 생성, 동기화, 검증할 수 있는 실행 기준 시작점을 먼저 만들어요.

## 관련

- [[ai-context-as-code-design]]
- [[content-structure-plan]]
- [[agent-maintained-notes]]
