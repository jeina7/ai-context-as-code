---
type: research
title: "ACAC Visual Direction Grill Q&A Extract"
description: "Meaningful Q&A extraction from the ACAC visual direction grill transcript"
status: active
created: 2026-06-30
updated: 2026-06-30
visibility: public
id: mz9Mw6b6aE

---

# ACAC Visual Direction Grill Q&A Extract

이 문서는 ACAC visual design system grill 원문에서 visual direction을 바꾼 Q&A만 추출한 기록이에요.
원문 전체 보존은 raw transcript가 맡고, 이 문서는 왜 이런 visual direction이 되었는지 읽기 쉽게 설명해요.
각 항목은 원문 turn 번호를 남겨서 필요하면 원문으로 되돌아갈 수 있게 해요.
구현 계획이 아니라 visual promise, layout rule, color rule, component rule, interaction rule, non-goal을 고정하는 문서예요.

## Source And Method

- Source: [[acac-visual-direction-grill-raw-transcript]]
- Product model context: [[ai-native-context-layer-product-model]]
- Scope: 첫 visual design direction prompt부터 정물/보석 표현을 “컨셉 참고”로 수정한 답변까지
- Included: visual direction을 바꾼 질문, 사용자 보정, 용어 수정, surface rule, layout rule, non-goal
- Excluded: tool 진행 안내, 단순 확인 메시지, 원문 보존 자체에 대한 후속 작업

## Visual Positioning

### Q01. 기존 reader design을 기준점으로 삼을 것인가?  
Source turns: 1-8

**Question extracted:** ACAC visual design system을 기존 reader app, CSS, layout, 이전 reader design system 없이 새로 잡아야 하나?

**Answer extracted:** 맞아요. 기준점은 현재 구현이 아니라 AI-native context layer product model과 준비된 icon asset이에요.

**Decision:** Visual direction은 기존 reader 개선 작업이 아니에요. 기존 `site/` 구현, reader CSS/layout, 이전 reader design system은 reference가 아니에요.

### Q02. ACAC의 시각 성격은 무엇인가?  
Source turns: 8-10, 85-88

**Question extracted:** ACAC는 technical infra, calm document workspace, crafted maker tool, jewel/lapidary 세계관 중 무엇에 가까운가?

**Answer extracted:** 정물/보석 컨셉은 참고하되, 본질은 정교한 제작 도구이자 technical context system이에요.

**Decision:** ACAC visual promise는 “raw input을 검증 가능한 context artifact로 다듬는 정교한 tool”이에요. 정물/보석은 개념적 재료일 뿐, UI 정체성의 중심 문구는 아니에요.

**Rejected wording:** “정물/보석의 물성을 가진다”는 표현은 애매해서 쓰지 않아요.

### Q03. Desktop과 Web은 같은 visual language를 써야 하나?  
Source turns: 10-12

**Question extracted:** Desktop App과 Web은 같은 visual system을 공유해야 하나, 아니면 surface별로 달라야 하나?

**Answer extracted:** 공통 token과 개념 surface는 공유하고, layout과 density는 분리해요.

**Decision:** Desktop은 dense, source-aware, action-heavy workspace예요. Web은 readable, publish/share/import 중심 surface예요.

## Model And Navigation

### Q04. Core model hierarchy는 어떻게 보여야 하나?  
Source turns: 12-16

**Question extracted:** Trove, Gem, Quarry, Chronicle을 동등한 메뉴처럼 보여야 하나?

**Answer extracted:** 아니요. `Gem`은 `Trove` 하위 canonical context unit이에요. `Quarry` input은 `Refine to Trove`를 통해 Gem으로 승격되거나 기존 Gem에 흡수되고, 그 변경이 `Chronicle`에 기록돼요.

**Decision:** `Trove`와 `Forge`가 primary place예요. `Gem`은 Trove 안의 파일 같은 읽기/쓰기 단위예요. `Chronicle`은 승격과 변경의 generated history view예요.

### Q05. Gem tree는 Domain/Section 구조에 종속되어야 하나?  
Source turns: 17-21

**Question extracted:** 읽기는 Obsidian처럼 tree 중심이어야 하지만, Domain/Section 구조를 고정 tree로 보여도 되나?

**Answer extracted:** 아니요. 일반 폴더 기반 파일시스템처럼 보여야 해요. Domain/Section 구조는 Trove마다 변할 수 있어서 tree UI를 고정 taxonomy에 종속하면 안 돼요.

**Decision:** Gem tree는 일반 file tree예요. Domain/Section 의미는 breadcrumb, metadata, filter, validation context에서 보조적으로만 보여요.

### Q06. Quarry, Chronicle, Relations, Ledger는 tree 안에 들어가야 하나?  
Source turns: 21-23

**Question extracted:** 시스템 surface들을 Gem file tree 안에 섞어야 하나?

**Answer extracted:** 아니요. Gem tree는 canonical markdown context만 보여줘야 해요.

**Decision:** `Quarry`, `Chronicle`, `Relations`, `Ledger`는 tree 밖 전용 surface예요. `.acac`, raw ledger, generated indexes는 normal tree에 노출하지 않아요.

## Icons And Visual Assets

### Q07. 3D icon asset은 어디에 써야 하나?  
Source turns: 23-25

**Question extracted:** 준비된 3D icon을 작은 row icon처럼 반복해서 써도 되나?

**Answer extracted:** 아니요. 개념을 설명하는 순간과 sidebar section header에서 써요.

**Decision:** 3D icon은 top-level concept marker예요. `Quarry`, `Forge`, `Chronicle`, `Trove` 같은 section header 앞에는 쓸 수 있지만, Gem row마다 반복하지 않아요.

**Asset rule:** Chroma magenta source asset은 그대로 UI에 노출하지 않고, 배경 제거 또는 마스킹된 product asset으로 처리해야 해요.

## AI-Native State And Trust

### Q08. Refine loading은 어떻게 보여야 하나?  
Source turns: 26-29

**Question extracted:** Loading UI에 CoT처럼 보이는 `...ing` 문구를 둘 수 있나?

**Answer extracted:** 실제 model reasoning은 노출하지 않고, ACAC가 수행하는 제품 작업 상태로 보여주면 돼요.

**Decision:** Refine loading은 실제 작업 단계와 crafted status phrase를 섞어요. 예시는 `Assaying input`, `Finding matching Gems`, `Polishing changes`, `Setting into Trove`, `Writing Ledger`, `Updating Chronicle`, `Checking conflicts`예요.

**Non-goal:** 실제 chain-of-thought, 의미 없는 magic animation, generic AI gradient는 쓰지 않아요.

### Q09. Relations와 validation은 어디에 있어야 하나?  
Source turns: 37-41

**Question extracted:** Relations는 항상 보이는 surface인가, 필요할 때만 여는 surface인가?

**Answer extracted:** Desktop에서는 항상 접근 가능한 오른쪽 panel이어야 해요. 다만 접었다 펼 수 있어야 해요.

**Decision:** Right panel은 `Relations`, `Health`, `Ledger context`, `Refine Guidance`를 담는 collapsible trust panel이에요.

### Q10. Ledger와 Chronicle은 같은 history UI인가?  
Source turns: 41-43

**Question extracted:** Ledger와 Chronicle을 timeline처럼 비슷하게 보여도 되나?

**Answer extracted:** 아니요. Ledger는 user-facing content가 아니라 system log / audit substrate예요. Chronicle은 사용자가 읽는 history예요.

**Decision:** Chronicle은 사람이 이해하는 generated history view예요. Ledger는 evidence/detail로 들어갔을 때 system log 형식으로 보여요.

## Home And Surface Layout

### Q11. 기본 Desktop workspace는 무엇 중심인가?  
Source turns: 29-31

**Question extracted:** Desktop App의 기본 작업면은 Gem editor 중심인가, Trove overview 중심인가?

**Answer extracted:** 기본 작업면은 Gem editor 중심이에요. 하지만 첫 Home/Overview는 별도 기획이 필요해요.

**Decision:** Desktop의 core workspace는 file tree, Gem editor/reader, right trust panel이에요. Home/Overview는 제품의 세계관과 현재 작업 상태를 보여주는 별도 surface예요.

### Q12. Home/Overview는 무엇을 보여야 하나?  
Source turns: 30-35, 62-67

**Question extracted:** Home은 최근 작업 재개인가, health command center인가?

**Answer extracted:** 둘 다 필요해요. Account-level Home과 Trove Home을 분리해요.

**Decision:** 앱 첫 화면은 Account-level Home이에요. Trove를 선택하면 Trove Home을 보여줘요. Home의 상단은 continue working과 attention needed가 중심이에요.

### Q13. Recent history는 파일 열람 기록인가, 의미 있는 작업 단위인가?  
Source turns: 32-35

**Question extracted:** 최근 작업 history는 단순히 최근 열어본 파일 목록인가?

**Answer extracted:** 아니요. `Ledger Entry`, `Refine result`, `Gem edit`, `Publish`, `Import`, `Revert` 같은 의미 있는 작업 단위 중심이어야 해요.

**Decision:** Home history는 “다시 이어서 일하기 위한 최근 활동”이에요. 단순 file click history는 보조 surface로 낮춰요.

### Q14. Web은 Desktop reader의 복제인가?  
Source turns: 35-37

**Question extracted:** Web surface는 Desktop의 read-only 버전인가?

**Answer extracted:** 아니요. Web은 public proof-of-work reader예요.

**Decision:** Web은 published Trove를 읽고, 신뢰하고, 공유하고, import할 수 있게 해야 해요. Desktop editor를 그대로 막아둔 화면이 아니에요.

## Component And Markdown Rules

### Q15. 기본 component 문법은 cards인가?  
Source turns: 44-47

**Question extracted:** ACAC UI는 card 중심 dashboard로 가야 하나?

**Answer extracted:** 아니요. 기본 문법은 panels, rows, logs예요.

**Decision:** `Gem`, `Quarry item`, `Chronicle entry`, `Ledger Entry`, `Relations`는 compact row/log 중심으로 보여요. Card는 Trove switcher, publish/import preview, empty state 같은 묶음 단위에만 제한적으로 써요.

### Q16. Typography와 Markdown renderer는 무엇을 우선해야 하나?  
Source turns: 47-51

**Question extracted:** 문서 가독성과 tool 정보 밀도 중 무엇을 우선해야 하나?

**Answer extracted:** Gem body와 Web reader는 문서 가독성을 우선하고, 주변 UI는 tool 정보 밀도를 유지해요.

**Decision:** Markdown 기본 렌더링 컴포넌트는 design system에 포함해야 해요. Headings, paragraphs, links, lists, blockquote, callout, inline code, code block, table, image, horizontal rule, task list, footnote/reference, frontmatter display/form이 필요해요.

### Q17. ACAC tool component는 Markdown body 안에 들어가나?  
Source turns: 50-53

**Question extracted:** “ACAC가 만든 block”이란 무엇이고, Gem 본문 안에 ACAC 전용 block을 만들자는 뜻인가?

**Answer extracted:** 아니요. Gem body는 순수 Markdown renderer예요. ACAC의 검증, 기록, 관계, 결과 UI는 body 바깥 tool surface예요.

**Decision:** `Refine result`, `Validation/Conflict`, `Ledger Entry detail`, `Chronicle entry`, `Relations`, `Frontmatter form`은 Markdown body 밖의 tool component예요.

### Q18. Frontmatter는 기본 노출인가?  
Source turns: 53-57

**Question extracted:** Frontmatter는 접어두고 metadata mode에서만 보여야 하나?

**Answer extracted:** 아니요. 기본 노출이에요. 다만 raw YAML 덩어리가 아니라 가독성 좋은 metadata renderer로 보여줘야 해요.

**Decision:** Gem 상단에 frontmatter summary를 보여줘요. `title`, `type`, `status`, `updated`, `visibility`처럼 판단에 필요한 필드를 우선 표시하고, `id`, generated fields, hashes, internal registry/provenance fields는 접어요.

## Quarry, Forge, Color, Surface

### Q19. Quarry는 어떻게 보여야 하나?  
Source turns: 57-61

**Question extracted:** Quarry를 “raw material bench”처럼 설명해도 되나?

**Answer extracted:** 아니요. 그 표현은 애매해요. Quarry는 정제 전 입력함이에요.

**Decision:** Quarry UI는 inbox처럼 명확해야 해요. 아직 canonical source가 아니라는 점만 시각적으로 구분해요.

### Q20. Forge는 Trove와 같은 reader인가?  
Source turns: 59-61

**Question extracted:** Forge UI는 Trove와 같은 문서 tree처럼 보여야 하나?

**Answer extracted:** 아니요. Forge는 technical agent workspace예요.

**Decision:** Forge는 `Agents`, `Skills`, `Commands`, `Memory` 중심이며, runtime sync와 validation 상태를 잘 보여줘야 해요.

### Q21. 색은 모델 구분에 쓰나, 상태 구분에 쓰나?  
Source turns: 67-69

**Question extracted:** `Trove`, `Quarry`, `Forge`, `Chronicle`, `Gem`마다 강한 색을 줄까?

**Answer extracted:** 아니요. 색은 상태 판단에 우선 써요.

**Decision:** Model 구분은 icon, section position, label로 해요. 색은 `validated`, `conflict`, `stale`, `proposal`, `published`, `synced` 같은 상태에 우선 사용해요.

### Q22. UI surface는 3D인가, flat인가?  
Source turns: 69-71

**Question extracted:** 준비된 3D icon의 물성을 UI surface에도 넣을까?

**Answer extracted:** 아니요. UI 자체는 3D가 아닌 flat technical surface예요.

**Decision:** 3D는 icon asset 역할이에요. Panels, rows, logs, editor surface는 flat하고 정교해야 해요.

### Q23. Radius는 작고 단단한가, 부드러운가?  
Source turns: 71-75

**Question extracted:** Rounded radius는 작은 tool 느낌이 맞나?

**Answer extracted:** 최종적으로는 부드럽게 가요. 단, 말랑한 SaaS가 아니라 정교한 rounded technical UI여야 해요.

**Decision:** Panels는 10-12px 정도, rows는 8px 안팎을 기준으로 해요. 큰 rounded card가 화면을 채우는 dashboard 느낌은 피해야 해요.

## Non-Goals And Next Artifact

### Q24. 1순위 visual non-goal은 무엇인가?  
Source turns: 75-77

**Question extracted:** ACAC에서 절대 피해야 할 시각 방향은 무엇인가?

**Answer extracted:** 기존 문서 앱 clone처럼 보이는 것이 1순위 non-goal이에요.

**Decision:** Notion/Obsidian/doc app clone, generic AI gradient, graph canvas-first UI, over-fantasy jewel UI, marketing hero-first site, oversized cards, low-density dashboard, chat app처럼 보이는 Quarry는 피해야 해요.

### Q25. 가장 작은 다음 산출물은 무엇인가?  
Source turns: 77-88

**Question extracted:** 다음에 바로 token spec이나 implementation plan을 만들면 되나?

**Answer extracted:** 아니요. 먼저 Visual Positioning Note가 필요해요.

**Decision:** 다음 산출물은 Visual Positioning Note예요. 그다음 Design Token Spec, Desktop/Trove Home/Gem workspace layout spec, Component inventory, Icon usage spec으로 내려가요.

## Important Shifts During The Grill

- “정물/보석의 물성”에서 “정물/보석 컨셉을 참고하되 본질은 정교한 제작 도구이자 technical context system”으로 바뀌었어요.
- Domain/Section 고정 tree에서 일반 폴더 기반 file tree로 바뀌었어요.
- Gem을 Trove와 같은 top-level place로 두지 않고 Trove 하위 canonical context unit으로 정리했어요.
- Quarry flow를 `Quarry → Domain/Section/Gem → Chronicle`이 아니라 `Quarry → Gem으로 승격/흡수 → Chronicle에 기록`으로 고쳤어요.
- 3D icon을 row마다 반복하는 방향에서 concept 설명과 sidebar section header 중심으로 바뀌었어요.
- Loading UI는 실제 reasoning 노출이 아니라 product operation status phrase로 정리했어요.
- Home은 단순 dashboard가 아니라 Account Home과 Trove Home으로 분리된 operational overview가 되었어요.
- Ledger는 user-facing history가 아니라 system log / audit substrate로 정리됐어요.
- Markdown body 안의 ACAC block idea는 폐기하고, tool component는 body 바깥 surface에 두기로 했어요.
- Frontmatter는 접힘 기본이 아니라 가독성 좋은 기본 노출로 바뀌었어요.
- `raw material bench` 표현은 폐기하고 Quarry를 정제 전 입력함으로 정리했어요.
- Radius는 작고 단단한 방향에서 부드러운 rounded technical UI로 수정됐어요.

## Resulting Visual Promise

ACAC is a precise crafted tool and technical context system for AI-native context work.
It can reference still-life and jewel concepts, but those concepts must not become decorative fantasy UI.
Humans read Gems through a fast filesystem-like tree.
Writes and AI-native changes happen through named semantic actions, visible validation, Chronicle history, and Ledger-backed evidence.
Desktop is the dense write and agent workspace.
Web is the readable public proof-of-work, publish, share, and import surface.

## Follow-Up Design Notes

1. Visual Positioning Note
2. Design Token Spec
3. Desktop App Layout Spec
4. Trove Home And Account Home Layout Spec
5. Web Reader And Publish Spec
6. Component Inventory
7. Icon Usage Spec
