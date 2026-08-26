# Blog Style Writing — ver0 Example

이미 블로그를 쓰는 사람이, 자기 글 문체를 Agent가 재사용하도록 **스타일 프롬프트와 콘텍스트를 만들고**, 그걸로 **초고·첨삭까지** 해 게시용 원고를 받는 예시입니다.

완성된 글쓰기 제품이 아닙니다. Web Crawler Craft로 글을 모으고, 문체를 팩으로 남기고, 원고를 쓰는지 시험하는 `ver0` draft입니다.

## 해결하려는 문제

Agent에게 글을 맡기면 흔히 다음이 일어납니다.

- 기존 글과 다른 일반 AI 문체가 나온다
- “내 말투로”만 있고 재사용 프롬프트가 안 남는다
- 글을 붙여 넣어도 다음 글에 스타일이 이어지지 않는다
- 초고와 게시 가능 원고가 구분되지 않는다

이 예시는 다음 질문에 답하는 것을 목표로 합니다.

1. 본인 공개 글을 어디에 어떤 스키마로 모을 것인가?
2. 문체 주장을 어떤 근거와 함께 프롬프트로 남길 것인가?
3. 그 팩을 로드한 초고는 어떻게 쓰는가?
4. 첨삭이 문체를 지우지 않고 게시용 원고가 되는가?

## 상태

`draft` — Rule·Skill·템플릿·fixture만 있습니다. 실제 블로그 URL 수집과 게시 품질은 아직 이 저장소에서 돌리지 않았습니다.

의존: [Web Crawler Craft](../web-crawler-ver0/README.md). 크롤 절차는 여기 복제하지 않습니다.

## 구성

```text
Rule
→ 문체는 코퍼스 근거, 내용은 지어내지 않기, 미게시

Skill — 오케스트레이션
→ 수집 → 팩 → 초고·첨삭 순서 (blog-style-writing)

Skill — 단계
→ 본인 글 수집 (collect-blog-corpus)
→ 스타일 프롬프트·근거 팩 (build-style-context)
→ 초고와 첨삭 (write-blog-manuscript)
```

- [`rules/blog-style-writing.mdc`](rules/blog-style-writing.mdc)
- [`skills/blog-style-writing/SKILL.md`](skills/blog-style-writing/SKILL.md)
- [`skills/collect-blog-corpus/SKILL.md`](skills/collect-blog-corpus/SKILL.md)
- [`skills/build-style-context/SKILL.md`](skills/build-style-context/SKILL.md)
- [`skills/write-blog-manuscript/SKILL.md`](skills/write-blog-manuscript/SKILL.md)
- 템플릿: [`templates/style-pack/`](templates/style-pack/)
- 절차 확인용 가상 글: [`fixtures/sample-corpus/`](fixtures/sample-corpus/)
- 같은 글로 한 번 추출한 팩(정답 아님): [`fixtures/sample-style-pack/`](fixtures/sample-style-pack/)

## 권장 흐름

```text
collect-blog-corpus     (Web Crawler Craft)
        ↓
build-style-context     (profile.md + evidence.md)
        ↓
write-blog-manuscript   (초고 → 첨삭, 사람 확인)
```

수집만, 팩만, 첨삭만 요청되면 해당 Skill만 실행합니다.

소비 프로젝트 저장 가정:

```text
blog-style/
├── corpus/
└── style-pack/
    ├── profile.md
    ├── evidence.md
    └── corpus-index.md
```

## ver0에서 일부러 하지 않은 것

- 특정 블로그 플랫폼 SDK·게시 API
- 글 미세조정·외부 스타일 학습 서비스
- 이 저장소에 실제 저자 원문 보관
- `.cursor/` 승격
- 맞춤법 검사 스크립트

같은 블로그 스키마·문장 길이 집계가 반복될 때만 Script를 검토합니다.

## 가정

- 대상은 요청자가 지정한 **본인** 공개 글
- 기본 수집은 최근 8~15편
- 언어·말투는 코퍼스를 따른다 (이 공방 문서는 한국어)
- 게시는 사람이 한다

## 관찰할 항목

1. 바로 도움이 된 내용
2. 불필요하거나 과도했던 내용
3. 다음 실행에서 바꿀 한 가지

추가로 본다.

- 팩이 일반 작법 문장으로 채워지지 않는가
- 초고가 팩을 건너뛰지 않는가
- 첨삭이 합니다체·“마무리하며”로 평탄화하지 않는가
- 없는 경험·숫자가 본문에 안 생기는가
- 크롤 범위가 본인 글 밖으로 안 나가는가

## 이 예시에서 절차 확인하는 법

실제 URL 없이 Skill 단계만 보려면:

1. `fixtures/sample-corpus/` 세 글을 코퍼스로 넣는다
2. `build-style-context`로 `profile`·`evidence`를 채운다. 이미 추출한 표본은 `fixtures/sample-style-pack/`
3. 주제를 하나 주고 `write-blog-manuscript`로 초고+첨삭을 한다

통과 대략:

- 해요체, 짧은 문단, 실패·장면으로 시작, 교과서 맺음 없음이 근거와 함께 나온다
- 초고에 fixture에 없는 SLA·회사명이 사실처럼 안 붙는다

실패:

- “명확하고 친절한 기술 블로그” 같은 프롬프트만 나온다
- 합니다체 보고서가 최종 원고가 된다

## 예시 출력 골격

오케스트레이션 Skill과 동일합니다.

```md
## 한눈에 보기

- 수행한 단계: 수집 / 팩 / 초고 / 첨삭
- 스타일 팩: ...
- 원고: ...
- 게시: 사람 확인 남김 (미게시)

## 수집

## 스타일 팩

## 원고

## 사람 확인

## 한계와 가정
```

> 이 예시는 모든 블로그에 글을 대신 올리는 시스템이 아니라, 이미 쓰는 사람의 문체를 **근거 있게 재사용**하도록 돕는 보조 도구입니다.
