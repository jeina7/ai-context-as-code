---
title: acac.sh 리브랜딩과 도메인 설정
---

# acac.sh 리브랜딩과 도메인 설정

## 요약

제품 이름을 설명형 이름인 `AI Context as Code`에서 공개 제품명 `acac.sh`로 바꿨어요.
사이트 껍데기, README, 활성 제품 노트, 결정 노트, runtime pointer, QA 기준이 이제 `acac.sh`를 사용해요.
GitHub Pages custom domain은 `acac.sh`로 설정했지만, 실제 접속은 도메인 등록과 DNS 레코드 추가가 끝나야 열려요.

## 완료

- GitHub Pages custom domain을 `acac.sh`로 설정했어요.
- `site/CNAME`을 추가했어요.
- 사이트에 보이는 brand, browser title, dashboard product label을 `acac.sh`로 바꿨어요.
- 핵심 설계/결정 노트를 `acac-sh-design`, `why-build-acac-sh`, `why-acac-sh`로 옮겼어요.
- 영어 원본 노트와 한국어 읽기 copy에서 제품명을 `acac.sh`로 맞췄어요.
- 예전 slug는 `data/aliases.json`에 남겨서 build 중 오래된 참조가 새 노트로 풀릴 수 있게 했어요.

## 검증

- `python3 scripts/check_publish_safety.py`
- `python3 scripts/validate_notes.py`
- `python3 scripts/build_meta.py`
- `python3 scripts/review_context.py`
- `node --check site/app.js`
- `python3 scripts/qa_viewports.py`

## 남은 외부 작업

`acac.sh`를 등록한 뒤 DNS를 GitHub Pages로 연결해야 해요.

## 관련

- [[why-acac-sh]]
- [[acac-sh-design]]
- [[why-markdown-git-github-pages]]
