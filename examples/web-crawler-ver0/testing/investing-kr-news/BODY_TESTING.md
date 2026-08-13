# Testing: kr.investing.com 뉴스 본문 수집

`web-crawler-ver0` Rule·Skill의 **본문 수집** testing 기록입니다.

- **선행 testing:** [`README.md`](README.md) (RSS 목록)
- **일시:** 2026-08-13
- **상태:** `testing` — 파이프라인 검증, 무인 자동화 한계 포함

## 수집 요약

- 목적: RSS 헤드라인 + **기사 본문** 수집 파이프라인 검증
- 대상: kr.investing.com 뉴스 상세 페이지
- 범위: 샘플 2건 본문 파싱 성공, RSS 최신 N건 무인 fetch는 403
- 수집 경로: RSS(목록) + **HTML SSR 파싱** (`div[class*='article_WYSIWYG']` 내 `p`)
- fallback: Playwright headless → **403**; GUI 브라우저 저장 HTML → **성공**

## SPA·내부 API 검토

- SPA 여부: Next.js SSR — **초기 HTML에 본문 포함** (내부 API JSON만으로 렌더하지 않음)
- Network JSON API: 자동화 클라이언트에서 별도 본문 API 확인 불가 (HTML도 403)
- 채택 경로: 허용된 클라이언트의 **HTML GET + 파싱**
- fallback: GUI/로컬 브라우저로 HTML 저장 → `--samples-dir` (testing용)

## 사전 조사

| 방법 | 결과 |
|---|---|
| curl / curl_cffi | 403 |
| Playwright headless / headed | 403 |
| undetected-chromedriver | 403 / 드라이버 이슈 |
| GUI Chrome (VM 브라우저) | **200**, 본문 DOM 접근 가능 |
| RSS | 200 (목록만) |

**판단:** 본문은 **봇 차단이 강한 HTML 경로**. 목록은 RSS, 본문은 허용 네트워크·브라우저 세션 필요.

## 스키마 (본문 추가)

```json
{
  "id": "article-93CH-2060007",
  "title": "string",
  "url": "string",
  "published_at": "string | null",
  "author": "string | null",
  "body": "string | null",
  "body_char_count": "number",
  "body_fetch_status": "ok | failed | blocked | parse_failed",
  "body_fetch_errors": ["playwright:blocked_http_403", "sample:used"]
}
```

## 구현

| 파일 | 역할 |
|---|---|
| `scripts/fetch_investing_kr_news_with_body.py` | RSS/URL 목록 → HTML fetch → 본문 파싱 |
| `scripts/investing_kr_parse.py` | HTML → 본문·메타 추출 |
| `testing/investing-kr-news/samples/*.html` | GUI 브라우저로 저장한 검증용 HTML |

의존성 (본문 testing):

```bash
pip install beautifulsoup4 lxml playwright
playwright install chromium
```

실행 예시:

```bash
# 검증된 샘플 2건 (본문 파싱 성공)
cd examples/web-crawler-ver0/scripts
python3 fetch_investing_kr_news_with_body.py \
  --no-playwright \
  --samples-dir ../testing/investing-kr-news/samples \
  --urls \
  "https://kr.investing.com/news/stock-market-news/article-93CH-2060008" \
  "https://kr.investing.com/news/stock-market-news/article-93CH-2060007"

# RSS 최신 + Playwright (이 환경에서는 본문 403 예상)
python3 fetch_investing_kr_news_with_body.py --limit 3 --delay 2
```

요청 정책: 기사당 `--delay` 기본 2초, 식별 User-Agent, 과도한 병렬 없음.

## 검증

| 항목 | 결과 |
|---|---|
| 본문 파싱 (StubHub, 2060008) | 통과 — 1,818자 → 단락 추출 후 정제 |
| 본문 파싱 (Cerebras, 2060007) | 통과 — 1,737자 |
| Playwright 무인 fetch | **실패** — 403 |
| RSS + 무인 본문 E2E | **실패** — 최신 RSS 항목에 샘플 HTML 없음 |
| 파이프라인 (URL + samples) | **통과** — 2/2 본문 |

## 한계와 가정

- 무인 headless로는 이 VM/데이터센터 IP에서 **안정적 본문 수집 불가**
- 로컬 PC·Residential IP에서는 Playwright 성공 가능성 있음 (별도 재검증 필요)
- 본문에 티커 위젯·광고 문구가 섞일 수 있음 — `p` 태그 추출으로 완화
- Investing.com 공식 API 없음, 이용약관·재배포 제한 확인 필요
- `samples/` HTML은 testing용; 프로덕션 캐시로 쓰지 않음

## Rule·Skill 관찰

### 바로 도움이 된 내용

1. RSS 먼저 → HTML fallback 순서가 목록·본문 분리에 맞음
2. **403 시 실패를 숨기지 않고** `body_fetch_errors` 기록 — Skill 출력 템플릿 유용
3. SPA 단계 생략 (SSR HTML에 본문 존재)

### 다음에 바꿀 한 가지

Skill에 **「강한 봇 차단 사이트는 무인 fetch 실패를 완료 조건에 포함」** — 성공/실패를 환경별로 구분 기록.

## 다음 실험

- [ ] 로컬 네트워크에서 Playwright만으로 RSS+본문 E2E
- [ ] 다른 사이트(차단 약한 뉴스)로 Rule·Skill 일반화 testing
- [ ] 본문 정제 규칙 (광고·번역 푸터 제거) Script 후보
