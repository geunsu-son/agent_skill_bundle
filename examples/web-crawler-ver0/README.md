# Web Crawler Craft — ver0 Example

웹에서 데이터를 수집하거나 크롤러를 만들 때, Agent가 매번 다른 방식으로 접근하지 않도록 **법·안정성·유지보수** 기준과 **실행 절차**를 나눈 예시입니다.

완성된 크롤러 프레임워크가 아니라, **Rule·Skill로 크롤 작업을 일관되게 수행**하는지 검증한 `ver0` draft입니다.

## 해결하려는 문제

Agent에게 크롤·스크래핑을 맡기면 다음이 반복적으로 발생합니다.

- 공식 API나 RSS를 확인하지 않고 곧바로 HTML 파싱을 시도함
- SPA·동적 페이지에서 Network 관찰 없이 브라우저 자동화부터 설계함
- `robots.txt`, 요청 빈도, 이용약관을 확인하지 않음
- 사이트 구조 변경에 취약한 선택자만 사용함
- 페이지네이션·에러·빈 결과를 일관되게 처리하지 않음
- 수집 범위와 출력 스키마가 요청마다 달라져 재사용이 어려움

## 상태

`draft` — Investing.com, yozm.wishket.com, Velog·Tistory 등 **3가지 수집 패턴**으로 Rule·Skill 절차를 검증했습니다.  
사이트별 fetch 스크립트·testing 기록은 제거했습니다. 실제 크롤 요청 시 Skill 절차와 아래 출력 골격을 따르면 됩니다.

## 구성

```text
Rule   → 크롤 작업 전반의 판단·윤리·품질 원칙
Skill  → 대상 정의, 사전 조사, 구현, 검증까지의 절차
Doc    → SPA·내부 API 검토 참고 (Skill에서 참조)
```

- [`rules/crawler-craft.mdc`](rules/crawler-craft.mdc)
- [`skills/web-crawler-craft/SKILL.md`](skills/web-crawler-craft/SKILL.md)
- [`docs/api-direct-call-guideline.md`](docs/api-direct-call-guideline.md)

## 검증에서 확인한 것 (요약)

| 패턴 | 대표 사례 | 채택 경로 | Skill에서의 시사점 |
|---|---|---|---|
| 강한 차단 | kr.investing.com | RSS 목록 + HTML 본문(환경 의존) | 피드 우선, 실패·fallback·한계 기록 필수 |
| RSS 본문 충분 | yozm.wishket.com | `content:encoded` | SPA·HTML·Playwright 생략 가능 |
| 블로그 플랫폼 | Velog, Tistory | RSS `description` / Velog GraphQL | 내부 API·피드 필드 차이 확인 후 최단 경로 |

## ver0에서 일부러 하지 않은 것

- 특정 라이브러리(Playwright, Scrapy 등) 고정
- 공통 크롤러 런타임·사이트별 스크립트 저장소
- 대규모 분산 크롤·스케줄링 인프라
- CAPTCHA·로그인 우회 절차

같은 사이트·같은 스키마가 **반복**될 때만 Script 분리를 검토합니다.

## 예시 출력 골격

Skill 9단계와 동일. 크롤 결과·관찰 기록은 요청 단위로 아래 형식을 사용합니다.

```md
## 수집 요약

- 목적: ...
- 범위: ...
- 수집 경로: 공식 API / 내부 API / RSS / HTML / 브라우저
- 요청 정책: ...

## SPA·내부 API 검토

- SPA 여부, 관찰한 엔드포인트, 채택 경로, fallback

## 사전 조사

- robots.txt / 이용약관 / 구조·차단 신호

## 스키마

- 필드 정의, 식별 키

## 구현

- 도구, 추출 전략, 페이지네이션

## 검증

- 샘플 N건, 통과·실패 구분

## 한계와 가정

- 수집하지 않은 항목, 구조 변경 시 취약 지점
```

> 이 예시는 모든 사이트를 자동 크롤하는 시스템이 아니라, Agent가 크롤 작업을 **더 일관되고 책임 있게** 수행하는 보조 도구입니다.
