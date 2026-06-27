---
title: 인터페이스 디자인 방향
---

# 인터페이스 디자인 방향

## 요약

AI Context as Code는 일반 문서 사이트보다 잘 다듬어진 개발자 도구에 가까워야 해요.
Tailwind CSS 문서의 선명함은 참고할 수 있지만, 브랜드 자체를 따라 하지는 않아요.

목표는 맥락을 읽고, 찾고, 검토하고, 편집하기 좋은 조용하고 정확한 작업면이에요.

## 원칙

- 색보다 정렬이 먼저예요.
- 반복되는 표면은 같은 간격 규칙을 써야 해요.
- 검색은 긴 navbar 입력창보다 모달 중심이어야 해요.
- 대시보드는 노트가 아니라 운영 상태 화면처럼 보여야 해요.
- 문서 화면은 읽기 좋은 본문 폭과 유용한 옆 맥락을 함께 가져야 해요.
- 그래프는 장식이 아니라 관계를 요약해야 해요.

## 시각 방향

graphite 바탕에 하나의 강한 accent만 써요.
border는 약하게 두고, shadow는 overlay, modal, floating preview에만 써요.

인터페이스는 이런 요소를 가져야 해요.

- navbar의 짧은 검색 trigger
- 중앙 command/search modal
- 노트 snippet과 명령을 함께 보여주는 검색 결과
- 화면별로 흔들리지 않는 좌우 inset
- 작지만 읽기 쉬운 label
- 절제된 hover 상태
- 반복 item이나 tool panel에만 쓰는 card

## 검색 방향

검색은 시스템 안에서 가장 빠르게 이동하는 방법이어야 해요.
navbar 검색창은 입구일 뿐이고, 실제 상호작용은 modal이 맡아요.

modal은 이것을 지원해야 해요.

- 노트 제목, 경로, 타입, 본문 검색
- 명령 실행
- 키보드 이동
- 노트 snippet 표시
- 나중에는 backlink, 최근 변경, review 상태를 반영한 ranking

## 하지 않을 것

이 화면은 marketing landing page가 아니에요.
Tailwind CSS의 시각 정체성을 그대로 복사하지 않아요.
장식용 gradient나 과한 hero layout을 추가하지 않아요.
그래프가 판단을 돕지 않는다면 그래프를 화면의 주인공으로 만들지 않아요.

## 관련

- [[ai-context-as-code-design]]
- [[system-interface-map]]
- [[agent-runtime-references]]
