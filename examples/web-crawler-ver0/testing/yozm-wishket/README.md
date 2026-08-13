# Testing: yozm.wishket.com (요즘IT) 매거진

`web-crawler-ver0` Rule·Skill의 **두 번째 사이트** testing 기록입니다.

- **대상:** https://yozm.wishket.com/ (요즘IT 매거진)
- **일시:** 2026-08-13
- **상태:** `testing` — Investing.com과 비교용

## 수집 요약

- 목적: Rule·Skill이 **차단 약한 사이트**에서도 동일 절차로 E2E 성공하는지 확인
- 대상: 매거진 최신 글
- 범위: RSS 피드 최신 N건 (제목·URL·본문)
- 수집 경로: **공식 RSS** (`content:encoded`에 본문 HTML 포함)
- 출력: `scripts/fetch_yozm_magazine.py` → JSON

## SPA·내부 API 검토

- SPA 여부: Next.js — 상세 URL HTML에도 본문 스니펫 존재 (SSR)
- 내부 API: **RSS로 요구 충족** → Network 조사 생략 (Skill 2단계 조건)
- 채택 경로: `https://yozm.wishket.com/magazine/feed/`
- fallback: 상세 HTML GET + `article` 파싱 (curl 200 확인)

## 사전 조사

| 항목 | 결과 |
|---|---|
| robots.txt | `Allow: /magazine/`, `Crawl-delay: 5`, `Disallow: /api/` |
| RSS | 200, `content:encoded`에 전체 본문 |
| sitemap | `https://yozm.wishket.com/magazine/sitemap.xml` |
| 상세 HTML | 200, 본문 SSR 포함 |
| Playwright | **불필요** (RSS 본문 충분) |

## 스키마

```json
{
  "id": "3898",
  "title": "string",
  "url": "string",
  "published_at": "string | null",
  "author": "string | null",
  "description": "string | null",
  "body": "string | null",
  "body_char_count": "number",
  "body_source": "rss_content_encoded",
  "source_feed": "string"
}
```

## 구현

```bash
pip install beautifulsoup4 lxml

cd examples/web-crawler-ver0/scripts
python3 fetch_yozm_magazine.py --limit 3 --delay 5
```

요청 정책: 피드 1회 GET + robots `Crawl-delay: 5` 준수.

## 검증

| 항목 | 결과 |
|---|---|
| RSS fetch | 통과 |
| 본문 (`content:encoded`) | 통과 — 샘플 4,744자 (article 3898) |
| 무인 E2E (클라우드 VM) | **통과** — Playwright 불필요 |
| 상세 HTML fetch | 통과 (200) — fallback 가능 |

## Investing.com과 비교

| | kr.investing.com | yozm.wishket.com |
|---|---|---|
| 목록 | RSS ✅ | RSS ✅ |
| 본문 | RSS ❌ | RSS `content:encoded` ✅ |
| HTML 자동 fetch | 403 | 200 |
| Playwright | 필요(로컬) | 불필요 |
| robots | 접근 403 | Crawl-delay 5 |

## Rule·Skill 관찰

### 바로 도움이 된 내용

1. 수집 경로 우선순위 → RSS만으로 본문까지 끝 (Skill 생략 조건 실제 적용)
2. robots Crawl-delay를 스크립트 기본값에 반영할 필요 명확
3. 사이트별 Script 분리(investing vs yozm parse)가 적절 — 공통 프레임워크 불필요

### 과했던 내용

1. Investing testing에서 Playwright 단계가 yozm에는 해당 없음 — **경로 확정 후 단계 생략**이 맞음

## 한계

- RSS 피드가 크면(수 MB) 파싱 메모리·시간 부담 — `--limit`로 범위 제한
- HTML fallback 파서는 testing 수준 (레이아웃 변경 시 조정 필요)
- 상업적 재사용은 Wishket 이용약관 확인 필요

## reusable 판단에 대한 메모

이 사이트 testing만으로 `reusable` 승격은 **아직 이르다**.  
[`../REUSABLE_ASSESSMENT.md`](../REUSABLE_ASSESSMENT.md) 참고.
