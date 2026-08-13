# Testing: kr.investing.com 뉴스 크롤러

`web-crawler-ver0` Rule·Skill을 실제 대상에 적용한 첫 `testing` 기록입니다.

- **대상:** https://kr.investing.com/ (한국어 금융 뉴스)
- **일시:** 2026-08-13
- **상태:** `testing` — Rule·Skill 검증용, 정답 구현 아님

## 1. 요청 정리

| 항목 | 내용 |
|---|---|
| 목적 | Rule·Skill testing + 한국 Investing.com 최신 뉴스 목록 수집 |
| 레코드 단위 | 뉴스 1건 (제목, URL, 발행 시각, 작성자, 썸네일 URL) |
| 완료 | RSS에서 N건 파싱·JSON 출력 |
| 실패 | HTTP 오류, 0건, 필수 필드 누락 |

**가정:** 본문(full article text)까지는 이번 testing 범위 밖. 목록·메타데이터만 수집.

## 수집 요약

- 목적: 최신 금융 뉴스 헤드라인 모니터링 (testing)
- 대상: kr.investing.com 뉴스
- 범위: 공개 RSS 피드 최신 10건 (본문 HTML 미수집)
- 수집 경로: **RSS** (공식 피드)
- 출력: JSON (`scripts/fetch_investing_kr_news_rss.py`)

## SPA·내부 API 검토

- SPA 여부: 뉴스 **목록·상세 HTML**은 JS·광고·DFP 로딩이 많은 동적 페이지로 추정. 단, **목록 데이터는 RSS로 이미 제공**.
- 관찰한 엔드포인트:
  - `GET https://kr.investing.com/rss/news.rss` — 한국어 「모든 뉴스」
  - `GET https://kr.investing.com/rss/news_285.rss` — 「많이 본 기사」
  - 공식 RSS 목록: https://kr.investing.com/webmaster-tools/rss
- 채택 경로: **RSS 우선** — Skill 단계 2에서 HTML·SPA·브라우저 검토 전에 피드로 충분함을 확인
- fallback: 본문·카테고리 필터가 RSS에 없을 때만 HTML/내부 API 재검토. 현 환경에서 HTML은 403

내부 API Network 관찰은 **HTML 접근이 403**이라 브라우저 세션 없이는 이번 testing에서 수행하지 않음.

## 사전 조사

| 항목 | 결과 |
|---|---|
| robots.txt | 자동화 클라이언트에서 `403` (접근 차단) |
| 이용약관 | 별도 법무 검토 필요 — RSS는 webmaster-tools에 공개 제공 |
| HTML `/news`, 기사 URL | `403` (curl + 브라우저 UA, 클라우드 IP) |
| RSS 피드 | `200`, XML 정상 |
| 차단 신호 | HTML 경로 강한 봇·지역/IP 차단 추정 |

**판단:** 목록 수집은 RSS가 적절. HTML 크롤은 차단·약관 리스크를 동반하므로 기본 경로로 채택하지 않음.

## 스키마

```json
{
  "id": "article-93CH-2060008",
  "title": "string",
  "url": "string",
  "published_at": "string (RSS pubDate)",
  "author": "string | null",
  "image_url": "string | null",
  "source_feed": "string",
  "fetched_at": "ISO-8601"
}
```

식별 키: `url` (또는 URL suffix `id`)

## 구현

- 도구: Python 3 stdlib (`urllib`, `xml.etree`)
- 추출: RSS XML 파싱
- 요청 정책: 단일 GET, 식별 User-Agent, 피드 1회/실행
- 페이지네이션: RSS 최신 N건만 (피드에 포함된 범위)

실행:

```bash
python3 examples/web-crawler-ver0/scripts/fetch_investing_kr_news_rss.py --limit 5
```

## 검증

| 항목 | 결과 |
|---|---|
| RSS fetch | 통과 (`200`) |
| 필드 완전성 (title, url, pubDate) | 통과 (샘플 10건) |
| 기사 HTML fetch | **실패** (`403`) — 본문 수집 불가 |
| 한국어 제목·국내 기사 포함 | 통과 (예: 코스피 마감체크 기사) |
| 중복 | URL 기준 unique |

## 한계와 가정

- RSS에 **본문(description/content) 없음** — 헤드라인·링크·메타만
- 카테고리별 피드는 webmaster-tools에서 별도 RSS URL 선택 필요
- HTML·robots.txt 접근 불가 환경에서는 본문 크롤 검증 미완
- Investing.com HTML 차단은 IP·헤더·쿠키에 따라 달라질 수 있음
- 상업적 재배포·대량 수집은 이용약관 확인 필요

## Rule·Skill 관찰 (testing 결과)

### 바로 도움이 된 내용

1. **수집 경로 우선순위** — HTML 시도 전 RSS 확인으로 올바른 경로를 빠르게 선택
2. **SPA·내부 API 단계** — 「RSS로 충분하면 Network 조사 생략 가능」이 명시되면 좋겠음 (아래 개선 제안)
3. **출력 템플릿** — 한계·fallback 기록이 403 상황 설명에 유용

### 불필요하거나 과했던 내용

1. SPA Network 관찰 체크리스트가 **RSS만으로 충분한 경우**에도 부담으로 느껴질 수 있음
2. 9단계 절차 전체를 짧은 testing에 매번 풀어쓰면 장문 보고가 됨 — **경로 확정 후 단계 생략 규칙**이 있으면 좋음

### 다음에 바꿀 한 가지

**Skill에 「수집 경로가 RSS/공식 API로 확정되면 SPA·HTML 단계는 기록만 하고 생략 가능」** 조건을 추가.

## 다음 실험

- [ ] 카테고리 RSS (주식, 외환, 암호화폐) 매핑 표
- [ ] 로컬·허용 IP에서 기사 HTML 403 재현 여부
- [ ] 본문이 필요할 때만 Playwright + rate limit fallback (별도 testing)
