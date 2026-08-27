# Collect Blog Corpus

## 상태

`ver0` draft. 실제 블로그 URL 수집은 아직 이 예시에서 돌리지 않았습니다. 크롤 절차는 Web Crawler Craft에 맡깁니다.

## 목적

작성자 **본인** 공개 블로그에서 스타일 학습에 쓸 글을 모아, 소비 프로젝트에 재사용 가능한 코퍼스와 인덱스를 남깁니다.

## 사용 시점

- 스타일 팩을 처음 만들 때
- 최근 글이 쌓여 팩을 갱신해야 할 때
- “내 블로그 글을 모아줘”처럼 수집만 요청된 때

## 관련 Rule·Skill

- 이 번들 Rule: [`rules/blog-style-writing.mdc`](../../rules/blog-style-writing.mdc)
- 크롤: [`examples/web-crawler-ver0/skills/web-crawler-craft/SKILL.md`](../../../web-crawler-ver0/skills/web-crawler-craft/SKILL.md)
- 크롤 Rule: [`examples/web-crawler-ver0/rules/crawler-craft.mdc`](../../../web-crawler-ver0/rules/crawler-craft.mdc)

설치본을 쓰는 소비 프로젝트에서는 `.cursor/skills/web-crawler-craft/SKILL.md`를 따른다.

## 입력

- 블로그 베이스 URL 또는 글 목록 URL (요청자가 본인 글이라고 지정)
- 있으면: 포함할 태그·카테고리, 제외할 URL, 최대 편수
- 저장 위치. 없으면 소비 프로젝트의 `blog-style/corpus/` 를 가정하고 한 줄로 적는다

이미 제공된 URL을 다시 묻지 않는다. 본인 글인지 모호하고 구현이 막히면 그때만 짧게 확인한다.

## 기본값 (가정)

- 최근 글 **8~15편**. 전체 아카이브는 명시 요청이 있을 때만
- 본문 텍스트·제목·발행일·원문 URL. 댓글·추천 수·사이드바는 수집하지 않음
- 출력 스키마는 아래 JSON. 플랫폼은 고정하지 않음

## 절차

### 1. 범위 고정

한 문장씩 적는다.

- 누구의 어떤 블로그인가
- 레코드 단위는 글 1편인가
- 최대 편수와 제외 범위

요청자가 지정하지 않은 다른 블로그·검색 결과로 범위를 넓히지 않는다.

### 2. Web Crawler Craft로 수집

`web-crawler-craft` 절차를 그대로 따른다. 여기서 robots·SPA·선택자를 다시 설계하지 않는다.

블로그에 자주 해당하는 경로만 상기한다.

- Velog, Tistory, 많은 개인 블로그: RSS·Atom을 먼저 본다
- Velog: GraphQL 등 내부 API가 확인되면 HTML보다 그걸 쓴다
- 피드 `description`만 짧으면 상세 본문을 최소 요청으로 보완한다

채택 경로와 생략한 단계를 한 줄로 남긴다.

### 3. 스키마에 맞추기

각 글:

```json
{
  "id": "string",
  "source_url": "string",
  "fetched_at": "ISO-8601",
  "title": "string",
  "published_at": "ISO-8601 | null",
  "tags": ["string"],
  "body_text": "string",
  "char_count": "number"
}
```

- `id`는 URL 또는 플랫폼 고유키. 중복을 이걸로 제거한다
- `body_text`는 본문. 내비게이션·푸터·공유 버튼을 본문으로 넣지 않는다
- 원문과 정규화(공백 정리 등)를 구분할 수 있으면 한 줄로 적는다

소비 프로젝트 저장 예:

```text
blog-style/corpus/
├── index.md          # 아래 인덱스 형식
└── posts/<id>.md     # 글 1편
```

이 공방 `examples/` 아래에는 실제 원문을 쓰지 않는다. 절차 확인용은 [`fixtures/sample-corpus/`](../../fixtures/sample-corpus/)만 사용한다.

### 4. 인덱스 작성

[`templates/style-pack/corpus-index.md`](../../templates/style-pack/corpus-index.md) 형식을 채운다.

최소 확인:

- 요청 편수 대비 실제 건수
- 본문이 비었거나 피드 요약만인 글
- 중복 URL
- 작성자가 아닌 글이 섞였는지 (게스트·번역 전재가 보이면 제외하고 기록)

### 5. 출력

크롤 Skill 9단계 요약에 더해, 스타일 작업에 필요한 한 줄만 보탠다.

## 출력 형식

```md
## 수집 요약

- 목적: 스타일 학습용 본인 글 코퍼스
- 대상: ...
- 범위: 최근 N편 / 제외 ...
- 수집 경로: 공식 API / 내부 API / RSS / HTML / 브라우저
- 저장: ...
- 다음: `build-style-context` 로 스타일 팩 생성 또는 갱신

## SPA·내부 API 검토

## 사전 조사

## 스키마

## 구현

## 검증

- 샘플 N건, 본문 비어 있음 / 요약만 / 중복

## 한계와 가정
```

## 완료 조건

- 본인 공개 글로 범위가 고정됨
- Web Crawler Craft 절차를 따름 (우회·범위 확장 없음)
- 스키마와 인덱스가 있음
- 본문 공백·중복·작성자 불명이 구분됨
- 실제 원문이 이 예시 번들에 커밋되지 않음

## 향후 Script 후보

- 피드 글 목록 → 상세 본문 보강
- `char_count`·중복 URL 검사

같은 블로그·같은 스키마가 반복될 때만 분리한다.
