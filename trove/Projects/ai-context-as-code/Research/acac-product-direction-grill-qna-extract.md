---
type: research
title: "ACAC Product Direction Grill Q&A Extract"
description: "Meaningful Q&A extraction from the ACAC product direction grill transcript"
status: active
created: 2026-06-30
updated: 2026-06-30
visibility: public
id: sOkKpZBKqF

---

# ACAC Product Direction Grill Q&A Extract

이 문서는 ACAC 제품 방향 grill 원문에서 제품 결정을 바꾼 Q&A만 추출한 기록이에요.
원문 전체 보존은 raw transcript가 맡고, 이 문서는 왜 이런 제품 모델이 되었는지 읽기 쉽게 설명해요.
각 항목은 원문 turn 번호를 남겨서 필요하면 원문으로 되돌아갈 수 있게 해요.
구현 계획이 아니라 제품 약속, UX, 저장 모델, agent boundary, 비목표를 고정하는 문서예요.

## Source And Method

- Source: [[acac-product-direction-grill-raw-transcript]]
- Canonical model after extraction: [[ai-native-context-layer-product-model]]
- Scope: 첫 제품 방향 prompt부터 “다음 단계는 구현 계획이 아니라 결정 문서화가 맞아요.” 답변까지
- Included: 제품 결정을 바꾼 질문, 재검토, 용어 확정, scope cut, 위험 제어
- Excluded: 단순 동의, tool 진행 안내, 배포/정리 작업 로그, 원문 보존 자체에 대한 후속 작업

## Product Frame

### Q01. ACAC는 어떤 제품으로 확장되어야 하나?  
Source turns: 1-5

**Question extracted:** ACAC를 AI-native document layer로 확장하려면 먼저 무엇을 날카롭게 해야 하나?

**Answer extracted:** 구현 계획보다 먼저 제품 정체성, UX 약속, 저장 모델, agent boundary, 비목표를 정해야 해요.

**Decision:** ACAC는 문서 앱이 아니라 AI-native context layer예요. 사람과 agent가 같은 source를 다루되, agent write는 semantic action과 audit을 통과해야 해요.

### Q02. 첫 핵심 사용자는 누구인가?  
Source turns: 6-7

**Question extracted:** 개인 지식관리 사용자, solo builder, 팀, Claude Code/Codex heavy user 중 누구를 먼저 잡아야 하나?

**Answer extracted:** 첫 사용자는 Claude Code와 Codex를 매일 쓰는 solo builder 또는 maker예요. 팀/조직 공유 layer는 확장 방향으로 남겨요.

**Decision:** V1은 solo builder/maker를 최적화해요. 팀 permission, SSO, 조직 governance, 실시간 협업은 v1 비목표예요.

### Q03. 매번 diff 승인하는 UX는 맞나?  
Source turns: 8-9

**Question extracted:** 모든 변경마다 사람이 diff를 확인하면 과부하가 크지 않나?

**Answer extracted:** ACAC는 매번 diff 승인을 요구하는 제품이 아니어야 해요. 안전한 범위의 변경은 agent가 자동 적용하고, 검증과 기록과 되돌리기를 제공해야 해요.

**Decision:** Product promise는 “알아서 잘 동작하되, 검증 가능하고 되돌릴 수 있다”예요. Diff는 항상 남지만 사용자가 매번 읽는 절차는 아니에요.

### Q04. 새 기록은 문서를 쌓는 것인가, 문서가 스스로 진화하는 것인가?  
Source turns: 10-13

**Question extracted:** 새로 기록할 때 기존 문서를 보강하거나 재구조화하는 self-evolution layer가 되어야 하지 않나?

**Answer extracted:** 맞아요. ACAC의 핵심 약속은 새 입력을 기존 context에 흡수하고, 필요하면 구조를 정리하며, 검증 가능한 기록을 남기는 것이에요.

**Decision:** ACAC는 raw note accumulation 제품이 아니에요. Refine 과정에서 기존 Gem 보강, 새 Gem 생성, split, move, relation update가 일어나야 해요.

## Human Write UX

### Q05. Web은 read-only인가, 사람이 직접 쓸 수 있어야 하나?  
Source turns: 14-17

**Question extracted:** Web은 read 중심이어도 edit, archive, delete, create가 가능해야 하지 않나?

**Answer extracted:** Web은 기본적으로 reader지만 사람이 직접 edit/archive/delete 할 수 있어야 해요. 다만 create는 canonical Gem이 아니라 임시 입력으로 시작해요.

**Decision:** Human create는 Quarry item이에요. Agent가 format, convention, placement를 검수한 뒤 existing Gem update나 new Gem promotion을 수행해요.

### Q06. ACAC는 local clone 기반인가, single source of truth인가?  
Source turns: 18-19

**Question extracted:** GitHub/local clone을 전제로 삼지 말고 single source of truth로 기능해야 하지 않나?

**Answer extracted:** 맞아요. GitHub는 MVP backend일 수 있지만 제품 저장 모델이 아니에요. ACAC 자체 source store가 canonical truth가 되어야 해요.

**Decision:** ACAC cloud source store가 canonical source예요. Local materialized copy는 빠른 read/write와 agent access를 위한 working copy예요.

### Q07. Web URL은 random ID인가, folder path인가?  
Source turns: 20-25

**Question extracted:** Stable random note ID보다 folder path를 그대로 보여주는 URL이 낫지 않나?

**Answer extracted:** 사람용 URL은 semantic path가 좋고, system identity는 stable ID가 필요해요.

**Decision:** ACAC는 semantic path와 stable ID를 모두 가져요. Path는 사람과 URL을 위한 이름이고, ID는 rename, move, backlink, audit, relation graph를 위한 identity예요.

## Ledger And Chronicle

### Q08. Logging은 일반 문서인가, 시스템화된 로그인가?  
Source turns: 26-29

**Question extracted:** Worklog는 단순 markdown note가 아니라 시스템화된 logging이어야 하지 않나?

**Answer extracted:** 맞아요. ACAC가 self-evolving layer가 되려면 logging은 document type이 아니라 structured system event log여야 해요.

**Decision:** Work history의 SSOT는 append-only structured log예요. 사람이 읽는 문서는 그 위에서 생성되는 view예요.

### Q09. Worklog의 목적은 commit log와 같은 것인가?  
Source turns: 28-29

**Question extracted:** Worklog의 본질은 어떤 작업이 언제 수행됐는지, audit과 future lookup을 위해 남기는 것 아닌가?

**Answer extracted:** 맞아요. Git commit log의 AI-native 버전으로 볼 수 있어요. 다만 agent safety를 위해 provenance, validation, rollback 기준, trust calibration도 필요해요.

**Decision:** ACAC log는 audit, provenance, rollback, conflict explanation, Chronicle generation의 기반이에요.

### Q10. Worklog보다 좋은 이름은 무엇인가?  
Source turns: 30-35

**Question extracted:** Worklog 대신 Trove/Forge 계열에 맞는 이름은 무엇인가?

**Answer extracted:** SSOT event log는 Ledger가 맞고, 사람이 읽는 history view는 Chronicle이 좋아요.

**Decision:** Ledger는 append-only structured event log예요. Chronicle은 Ledger에서 생성되는 human-readable view예요.

### Q11. Chronicle은 편집 가능한 문서인가?  
Source turns: 36-37

**Question extracted:** Chronicle은 Ledger 기반으로 일방향 생성되므로 read-only여야 하지 않나?

**Answer extracted:** 맞아요. Chronicle은 사람이 읽기 좋은 read-only view여야 해요.

**Decision:** Chronicle은 editable Gem이 아니에요. App에서 보는 friendly history/activity/audit view예요.

### Q12. Ledger의 기본 단위는 edit인가, intent인가?  
Source turns: 38-45

**Question extracted:** Edit level은 너무 큰가? Intent level만으로 audit과 rollback이 충분한가?

**Answer extracted:** Intent만으로는 약해요. Ledger unit은 intent와 operations를 함께 가져야 해요.

**Decision:** Ledger Entry는 intent, operations, evidence, validation, actor, approval state, revert data를 담아요.

### Q13. Rollback은 무엇을 기준으로 가능한가?  
Source turns: 44-47

**Question extracted:** Intent와 operation이 합쳐진 하나의 transaction 단위로 rollback해야 하지 않나?

**Answer extracted:** 맞아요. V1 rollback은 Ledger Entry 단위가 맞아요.

**Decision:** One-click revert는 Ledger Entry 단위로 동작해요. Ledger를 지우지 않고 Revert Ledger Entry를 새로 추가해 이전 Entry의 효과를 되돌려요.

## Product Surfaces

### Q14. Local daemon은 제품 UX로 괜찮은가?  
Source turns: 48-51

**Question extracted:** 사용자가 local daemon을 직접 띄워야 한다면 너무 개발자 도구 같지 않나?

**Answer extracted:** 맞아요. 사용자는 daemon을 인식하지 않아야 해요. ACAC App이 내부 runtime을 숨기는 방식이 좋아요.

**Decision:** Desktop App이 write, local trust boundary, sync, rollback, agent integration을 담당해요. Local runtime은 implementation detail이에요.

### Q15. Desktop App과 Web이 둘 다 필요한가?  
Source turns: 52-61

**Question extracted:** Desktop App이 있으면 Web이 왜 필요한가?

**Answer extracted:** Desktop App과 Web은 역할이 달라요. Desktop App은 trusted write surface이고, Web은 read, publish, share, import surface예요.

**Decision:** ACAC has two primary surfaces. Desktop App is for private writing and agent integration. Web is for reader, publish, sharing, and import.

### Q16. Web App의 구체적 use case는 무엇인가?  
Source turns: 61-65

**Question extracted:** Desktop App은 개인 workspace인데, Web은 어떤 상황에서 쓰이나?

**Answer extracted:** Web은 특정 folder/project를 URL로 읽게 하고, 다른 user에게 배포 가능한 context package처럼 전달하는 surface예요.

**Decision:** Trove 또는 project-like unit은 publish/share/import 가능한 context package가 될 수 있어요.

### Q17. Write copy import도 필요한가?  
Source turns: 65-67

**Question extracted:** 다른 사람이 배포한 context를 내 쪽으로 write-copy import할 수 있어야 하지 않나?

**Answer extracted:** 맞아요. Import는 read-only subscribe가 아니라 forked copy에 가까워요. Origin provenance는 남겨야 해요.

**Decision:** Import Trove는 logged-in user가 published Trove를 자기 account로 가져오는 기능이에요. Shared editing과 origin write-back은 v1 이후예요.

## Quarry And Refine

### Q18. Inbox라는 용어는 제품 세계관에 맞나?  
Source turns: 69-73

**Question extracted:** Inbox는 좋지만 Trove/Forge/Ledger와 결이 맞는 단어가 필요하지 않나?

**Answer extracted:** Raw input space는 Quarry가 좋아요. 아직 Gem이 되기 전의 원석 공간이라는 뜻이에요.

**Decision:** 새 human create는 Quarry로 들어가요. Quarry는 Trove별 raw input surface예요.

### Q19. Quarry 처리 action의 이름은 무엇인가?  
Source turns: 73-80

**Question extracted:** Process 버튼의 제품 용어는 무엇이 좋나?

**Answer extracted:** Refine이 가장 적절하고, 결과 목적지까지 포함하면 Refine to Trove가 좋아요.

**Decision:** Main action name is Refine to Trove. Loading copy can use mining/lapidary words later, but exposed reasoning steps는 아니에요.

## Semantic Write Actions

### Q20. 모든 write는 contract를 거쳐야 하나?  
Source turns: 85-88

**Question extracted:** 매번 큰 contract 비용이 들면 너무 무겁지 않나?

**Answer extracted:** User-visible cost는 낮춰야 하지만, internal semantic contract는 필요해요.

**Decision:** V1은 contract-only model로 잡아요. User에게 매번 복잡한 diff를 요구하지 않고, action contract와 validation으로 safety를 확보해요.

### Q21. Delete Note는 단순 file delete인가?  
Source turns: 89-90

**Question extracted:** Delete도 link 정리, Ledger 기록, validation을 거치는 semantic edit이어야 하지 않나?

**Answer extracted:** 맞아요. Delete는 file delete가 아니라 semantic action이에요.

**Decision:** Delete Gem은 links, references, archive suitability, validation, Ledger Entry, Chronicle explanation, revert data를 포함해야 해요.

### Q22. Import Package보다 Import Trove가 나은가?  
Source turns: 91-94

**Question extracted:** Product 용어로 Import Package보다 Import Trove가 더 직관적이지 않나?

**Answer extracted:** 맞아요. ACAC에서 publish/import/share의 단위는 Trove예요.

**Decision:** Action name is Import Trove.

### Q23. Rename과 Move는 분리해야 하나?  
Source turns: 93-98

**Question extracted:** Move Note와 Rename Note는 같은 action인가, 다른 action인가?

**Answer extracted:** 사용자 의도와 validation이 다르므로 분리하는 게 좋아요.

**Decision:** Rename Gem과 Move Gem은 별도 semantic actions예요. Rename은 title/slug/display name, Move는 section/project/Trove placement를 바꿔요.

### Q24. Archive와 Delete는 어떻게 구분하나?  
Source turns: 99-105

**Question extracted:** Archive와 tombstone 같은 단어가 섞이면 헷갈리지 않나?

**Answer extracted:** Product action은 Archive와 Delete로 충분해요. Tombstone은 내부 구현 표현으로만 가능해요.

**Decision:** Archive Gem은 active surface에서 숨기되 history를 보존해요. Delete Gem은 제한적으로 source에서 제거하되 Ledger Entry는 남겨요.

### Q25. Note라는 단어를 계속 써야 하나?  
Source turns: 101-105

**Question extracted:** Trove가 보관함인지 note인지 헷갈린다. 개별 note도 세계관 용어가 필요하지 않나?

**Answer extracted:** Trove는 보관함/collection이고, 개별 canonical document는 Gem이 좋아요.

**Decision:** Product vocabulary uses Trove for collection and Gem for individual canonical markdown document.

### Q26. Rollback Transaction은 어떤 이름이 맞나?  
Source turns: 105-115

**Question extracted:** Rollback Transaction, Rollback Ledger, Revert Ledger Entry 중 무엇이 정확한가?

**Answer extracted:** Git처럼 Revert가 정확해요. Transaction 대신 Ledger Entry가 더 직관적이에요.

**Decision:** Action name is Revert Ledger Entry. Ledger Entry replaces transaction in product vocabulary.

## Source Hierarchy

### Q27. Trove 내부 단위는 무엇인가?  
Source turns: 117-128

**Question extracted:** Trove 아래에 nested hierarchy가 필요하고, section convention도 agent refine에 필요하지 않나?

**Answer extracted:** Trove 안에는 project/domain-like grouping과 section convention이 필요해요. Gem은 class가 아니라 개별 문서 instance예요.

**Decision:** Current product model uses Trove -> Projects -> Section -> Gem. Sections are placement conventions, not Gem classes.

### Q28. Quarry, Ledger, Chronicle은 Trove tree 안에 들어가나?  
Source turns: 131-135

**Question extracted:** Ledger와 Chronicle은 Trove content tree와 같은 flat hierarchy인가, 별도 system/history layer인가?

**Answer extracted:** Ledger는 Gem tree가 아니라 hidden system log예요. Chronicle은 Ledger에서 파생되는 read-only app view예요.

**Decision:** Quarry is a Trove raw input surface. Ledger lives under `.acac/ledger/`. Chronicle is a read-only app history view, not editable source or a content folder.

### Q29. Forge source와 generated runtime files는 어디에 있어야 하나?  
Source turns: 135-143

**Question extracted:** Forge에는 common source만 있고 generated Claude/Codex files는 `.acac` 아래가 맞지 않나?

**Answer extracted:** 맞아요. Forge는 source markdown을 가지고, runtime output은 generated artifact여야 해요.

**Decision:** Forge/Agents remains markdown source. `.acac/generated/agents/` can hold generated AGENTS.md and CLAUDE.md. Transformation belongs to ACAC App or CLI.

### Q30. Config, cache, state는 무엇을 담나?  
Source turns: 147-151

**Question extracted:** `.acac/config`, cache, state에는 구체적으로 무엇이 들어가나?

**Answer extracted:** Durable user choices는 config, generated/rebuildable data는 cache/generated, local runtime facts는 state로 나누는 게 좋아요.

**Decision:** `.acac/config` can be source-store backed for durable settings. `.acac/state` is local-only runtime state and should not be source truth.

## Agent Integration

### Q31. MCP는 왜 필요한가?  
Source turns: 159-165

**Question extracted:** Desktop App과 CLI가 있으면 MCP까지 필요한가?

**Answer extracted:** CLI는 빠른 deterministic local action에 좋고, MCP는 agent tool discovery와 external tool integration에 좋아요. 하지만 v1 구현 우선순위는 아니에요.

**Decision:** MCP is future adapter. V1 should design MCP-friendly contracts but not implement MCP first.

### Q32. Native document context layer 속도는 어떻게 얻나?  
Source turns: 163-177

**Question extracted:** MCP가 느릴 수 있는데, file system 수준으로 빠른 전체 문서 접근은 어떻게 보장하나?

**Answer extracted:** Agents should read local materialized markdown files directly. Writes still go through semantic actions.

**Decision:** Read path is filesystem-speed local materialized source. Write path is semantic action through ACAC App or CLI.

### Q33. Storage backend는 GitHub인가, 자체 cloud인가?  
Source turns: 173-179

**Question extracted:** GitHub backend를 전제로 하면 안 되고, 자체 cloud storage를 둬야 하지 않나?

**Answer extracted:** 맞아요. GitHub is not product storage. ACAC needs its own cloud source store.

**Decision:** ACAC cloud source store is canonical. Sync model is background sync plus explicit publish.

## Account And Pricing

### Q34. 회원 체계와 Trove 수는 어떻게 잡나?  
Source turns: 187-193

**Question extracted:** User -> Trove 구조가 맞나? 여러 Trove는 paid feature인가?

**Answer extracted:** Account owns Troves. Multiple Troves can be a paid subscription boundary.

**Decision:** V1 has one account space, one active Forge, and one or more Troves. Multiple Troves are paid.

### Q35. Workspace 같은 상위 계층이 필요한가?  
Source turns: 193-209

**Question extracted:** Trove, Ledger, Forge를 묶는 workspace 계층이 필요한가?

**Answer extracted:** V1에서는 별도 workspace/foundry/atelier layer가 필요 없어요. Account 아래에서 selected Forge와 selected Trove를 조합하면 충분해요.

**Decision:** No separate Workspace/Vault/Atelier/Foundry layer in v1. Forge Profile은 future feature예요.

## Category And Data Boundary

### Q36. 제품 카테고리는 무엇인가?  
Source turns: 213-214

**Question extracted:** AI-native document layer보다 더 정확한 category는 무엇인가?

**Answer extracted:** AI-native context layer가 더 정확해요.

**Decision:** ACAC category is AI-native context layer.

### Q37. External DB, telemetry, memory sync는 어떻게 구분하나?  
Source turns: 217-223

**Question extracted:** External DB와 telemetry를 v1에 넣을지, memory는 어디에 둘지 어떻게 잡나?

**Answer extracted:** ACAC's own canonical source DB는 v1에 포함돼요. Live product telemetry도 v1에 포함돼요. User external connectors와 uncontrolled memory sync는 비목표예요.

**Decision:** Cloud DB stores ACAC canonical source. Telemetry covers ACAC operations, not raw private content. Memory belongs in Forge.

### Q38. Visibility와 Quarry/Refine scope는 어느 단위인가?  
Source turns: 227-237

**Question extracted:** Visibility, Quarry, Refine은 account-level인가 Trove-level인가?

**Answer extracted:** Trove-level이 먼저 맞아요.

**Decision:** Trove is the publish, import, share, sync, visibility, Quarry, and Refine boundary in v1.

### Q39. 기존 document app과의 관계는 어떻게 잡나?  
Source turns: 237-238

**Question extracted:** ACAC 설계에서 기존 앱을 고려해야 하나?

**Answer extracted:** 아니요. ACAC는 독립 제품이어야 해요. 개인 migration은 user action이지 product promise가 아니에요.

**Decision:** ACAC product design stands independent from other document apps.

## Context Graph And AI-Native Research

### Q40. LLM-wiki나 graph 기반 문서 트렌드를 반영해야 하나?  
Source turns: 239-244

**Question extracted:** Document-native 제품이라면 LLM-maintained wiki, GraphRAG, graph 기반 문서 관리 흐름을 검토해야 하지 않나?

**Answer extracted:** 맞아요. 핵심 제품 가치가 되어야 해요. 다만 canonical source는 markdown이고 graph는 derived layer예요.

**Decision:** Context Graph is a first-class derived layer. Relations is the user-facing surface.

### Q41. Typed schema는 어느 정도 필요하나?  
Source turns: 246-248

**Question extracted:** 작은 typed schema를 처음부터 solid하게 설계해야 하지 않나?

**Answer extracted:** 맞아요. Free-form relation names는 피하고, 작은 node/edge schema를 가져야 해요.

**Decision:** V1 Context Graph uses typed nodes and edges with provenance, source_ref, confidence, status, valid time, creator, timestamp.

### Q42. Claim node는 무엇인가?  
Source turns: 249-253

**Question extracted:** Claim은 단일 문서가 아니라 graph에 섞이는 internal node인가?

**Answer extracted:** Claim은 product-facing note가 아니라 Context Graph 내부 primitive예요. Gem source anchor와 Ledger provenance가 있어야 해요.

**Decision:** Claim is hidden internal graph primitive, not user-authored content.

### Q43. Claim noise는 어떻게 통제하나?  
Source turns: 254-262

**Question extracted:** Claim이 많아지면 noise가 될 텐데 어떻게 막나?

**Answer extracted:** Claim은 hidden by default, selective extraction, candidate status, source anchor, Ledger provenance, small accepted count로 통제해야 해요.

**Decision:** Users should not manage Claims directly. Claim exists to improve internal quality, not to create a new user task.

### Q44. Entity Map은 v1인가 v1-next인가?  
Source turns: 264-267

**Question extracted:** Community detection과 full entity map은 무엇이고 제품에 넣을 만한가?

**Answer extracted:** Entity Map은 유용하지만 v1에는 크고, v1-next core feature가 맞아요.

**Decision:** Entity Map goes to v1-next. V1 schema leaves room for entities without building full entity graph.

## Naming And Documentation

### Q45. Product name은 ACAC로 유지하나, 바꾸나?  
Source turns: 272-275

**Question extracted:** Trove, Quarry, Forge 세계관이면 제품명도 바꿔야 하나?

**Answer extracted:** ACAC는 지금 유지하고, Lapidary는 future brand candidate로 두는 게 좋아요.

**Decision:** Product name remains ACAC for now. Lapidary is a future brand candidate.

### Q46. 최종 용어는 무엇인가?  
Source turns: 276-277

**Question extracted:** 지금까지의 용어를 한 번 정리하면 무엇인가?

**Answer extracted:** Account, Trove, Project/Section/Gem, Quarry, Refine to Trove, Forge, Ledger, Ledger Entry, Chronicle, Context Graph, Relations, Claim으로 정리해요.

**Decision:** 이 vocabulary가 product model의 기준이에요. 이후 문서와 UI는 이 용어를 기준으로 맞춰야 해요.

### Q47. 다음 단계는 무엇인가?  
Source turns: 278-279

**Question extracted:** 이제 다음 단계로 구현 계획을 만들면 되나?

**Answer extracted:** 아니요. 다음 단계는 구현 계획이 아니라 결정 문서화예요.

**Decision:** First durable artifact is the Product Positioning + Core Model Note. 세부 구현 설계는 Source Store and Sync, Semantic Write Actions and Ledger, Context Graph and Relations 순서로 나눠요.

## Important Shifts During The Grill

- Diff approval product에서 automatic safe write product로 바뀌었어요.
- GitHub-backed MVP에서 ACAC-owned cloud source store로 바뀌었어요.
- Note 중심 vocabulary에서 Trove/Gem/Quarry/Forge/Ledger/Chronicle vocabulary로 바뀌었어요.
- Worklog document에서 Ledger SSOT와 Chronicle generated view로 바뀌었어요.
- Local daemon UX에서 Desktop App with hidden local runtime으로 바뀌었어요.
- MCP-first integration에서 filesystem-speed local read plus semantic write actions로 바뀌었어요.
- Domain taxonomy에서 Project-based Trove hierarchy로 바뀌었어요.
- Graph feature에서 Context Graph as core derived layer로 바뀌었어요.
- User-facing Claim feature가 아니라 hidden internal quality primitive로 바뀌었어요.
- Separate workspace/foundry layer 없이 Account with selected Forge and selected Trove로 바뀌었어요.

## Resulting Product Promise

ACAC is an AI-native context layer for solo builders who work with Claude Code and Codex every day.
Agents read local materialized context at filesystem speed.
Writes go through semantic actions that validate, record Ledger Entries, update Relations, and can be reverted.
Humans read and publish through Web, write and refine through Desktop App, and see Chronicle as a friendly read-only history.
Trove is the main unit for visibility, publish, import, sync, Quarry, and Refine.

## Follow-Up Design Notes

1. Source Store and Sync Model
2. Semantic Write Actions and Ledger Design
3. Context Graph and Relations Schema
4. Desktop App and Web Surface Design
5. Forge and Agent Runtime Sync Design
