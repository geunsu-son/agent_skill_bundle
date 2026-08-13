# Web Crawler Craft — ver0 Example

웹에서 데이터를 수집하거나 크롤러를 만들 때, Agent가 매번 다른 방식으로 접근하지 않도록 **법·안정성·유지보수** 기준과 **실행 절차**를 나눈 예시입니다.

이 예시는 완성된 크롤러 프레임워크가 아닙니다. Rule·Skill 분리가 실제 크롤 작업에서 도움이 되는지 검증하는 첫 작업물입니다.

## 해결하려는 문제

Agent에게 크롤·스크래핑을 맡기면 다음이 반복적으로 발생합니다.

- 공식 API나 RSS를 확인하지 않고 곧바로 HTML 파싱을 시도함
- SPA·동적 페이지에서 Network 관찰 없이 브라우저 자동화부터 설계함
- `robots.txt`, 요청 빈도, 이용약관을 확인하지 않음
- 사이트 구조 변경에 취약한 선택자만 사용함
- 페이지네이션·에러·빈 결과를 일관되게 처리하지 않음
- 수집 범위와 출력 스키마가 요청마다 달라져 재사용이 어려움

이 예시는 다음 질문에 답하는 것을 목표로 합니다.

1. 이 대상은 크롤이 적절한가, 더 나은 수집 경로가 있는가?
2. SPA인 경우 내부 API 직접 호출이 가능한가?
3. 어떤 범위까지, 어떤 형식으로 수집해야 하는가?
4. 어떤 도구와 추출 전략이 이 사이트에 맞는가?
5. 결과를 어떻게 검증하고 한계를 기록하는가?

## 상태

`testing` — kr.investing.com 뉴스 RSS testing 완료. [`testing/investing-kr-news/`](testing/investing-kr-news/README.md) 참고.

## 구성

```text
Rule
→ 크롤 작업 전반에서 지켜야 할 판단·윤리·품질 원칙

Skill
→ 대상 정의, 사전 조사, 구현, 검증까지의 절차
```

- [`rules/crawler-craft.mdc`](rules/crawler-craft.mdc)
- [`skills/web-crawler-craft/SKILL.md`](skills/web-crawler-craft/SKILL.md)
- [`docs/api-direct-call-guideline.md`](docs/api-direct-call-guideline.md) — SPA·내부 API 검토 참고
- [`scripts/fetch_investing_kr_news_rss.py`](scripts/fetch_investing_kr_news_rss.py) — testing용 RSS 수집
- [`scripts/fetch_investing_kr_news_with_body.py`](scripts/fetch_investing_kr_news_with_body.py) — RSS + 본문 파이프라인 (testing)
- [`scripts/investing_kr_parse.py`](scripts/investing_kr_parse.py) — HTML 본문 파서
- [`testing/investing-kr-news/README.md`](testing/investing-kr-news/README.md) — 첫 testing 관찰 기록 (RSS)
- [`testing/investing-kr-news/BODY_TESTING.md`](testing/investing-kr-news/BODY_TESTING.md) — 본문 수집 testing

## ver0에서 일부러 하지 않은 것

- 특정 라이브러리(Playwright, Scrapy 등) 고정
- 공통 크롤러 런타임·설정 파일 표준화
- 대규모 분산 크롤·스케줄링 인프라
- CAPTCHA·로그인 우회 절차
- 수집 결과 저장·백테스트 자동화

먼저 실제 크롤 요청에서 Rule과 Skill이 충분히 유용한지 확인한 뒤, 반복되는 수집·정규화 로직만 Script로 분리합니다.

## 관찰할 항목

- API·RSS·SPA 내부 API 등 대안을 먼저 검토했는가?
- SPA에서 브라우저 자동화 전에 Network 관찰을 했는가?
- 수집 범위가 요청보다 넓어지지 않았는가?
- 요청 빈도와 예의 있는 접근이 명시되었는가?
- 선택자·파싱 전략이 사이트 구조 변경에 어느 정도 견딜 수 있는가?
- 빈 결과·HTTP 오류·페이지네이션 끝을 구분했는가?
- 출력 스키마와 한계·가정이 함께 기록되었는가?
- 같은 사이트를 다시 크롤할 때 절차가 재사용되는가?

## 예시 출력 골격

```md
## 수집 요약

- 대상: ...
- 범위: ...
- 수집 경로: 공식 API / 내부 API / RSS / HTML / 브라우저
- 도구: ...
- 요청 정책: ...

## SPA·내부 API 검토

- SPA 여부, 관찰한 엔드포인트, 채택 경로, fallback

## 사전 조사

- robots.txt / 이용약관 메모
- 페이지 구조·페이지네이션·동적 렌더 여부
- 반복 요청·차단 신호

## 구현 메모

- 추출 전략과 선택자
- 정규화 스키마
- 재시도·백오프·캐시

## 검증

- 샘플 N건과 엣지 케이스
- 실패·빈 결과 처리

## 한계와 가정

- 수집하지 않은 항목
- 구조 변경 시 깨질 지점
```

> 예시는 모든 사이트를 자동으로 크롤할 수 있는 시스템이 아니라, Agent가 크롤 작업을 **더 일관되고 책임 있게** 수행하는 보조 도구입니다.
