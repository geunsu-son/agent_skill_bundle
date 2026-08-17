# Testing: Velog · Tistory (블로그 플랫폼)

`web-crawler-ver0` Rule·Skill의 **제3 유형** testing 기록입니다.

- **대상:** Velog, Tistory (개발자 블로그 플랫폼)
- **일시:** 2026-08-17
- **상태:** `testing` — 마이그레이션·비교 관점의 수집 가능성 탐색

## 수집 의도 (사용자 맥락)

- 현재 **Tistory**를 주력 블로그로 사용
- 개발자 커뮤니티에서 **Velog** 사용이 많아 이전(마이그레이션)을 고민
- 크롤링으로 확인하고 싶은 것:
  - **자신의 글** 목록·본문·메타를 기계적으로 꺼낼 수 있는지
  - Velog로 옮길 때 **원문(마크다운/HTML) 확보** 경로가 있는지
  - 공개 RSS·API만으로 **무인 E2E**가 되는지

> 본 testing은 **타인 블로그 대량 수집**이 아니라, **자기 글 백업·이전 준비**에 가까운 범위를 가정합니다.

## 수집 경로 요약

| 플랫폼 | 목록 | 본문 | 채택 경로 | Playwright |
|---|---|---|---|---|
| **Velog** | RSS ✅ | RSS `description`(HTML) ✅ / GraphQL `body`(Markdown) ✅ | RSS + GraphQL | 불필요 |
| **Tistory** | RSS ✅ | RSS `description`(HTML) ✅ | RSS | 불필요 |

**생략한 단계:** SPA Network 조사는 RSS·GraphQL로 요구 충족 → HTML·Playwright 생략 (Skill 2단계).

## Velog

### 사전 조사

| 항목 | 결과 |
|---|---|
| robots.txt | `User-agent: *` (빈 파일, 특별 제한 없음) |
| RSS | `https://api.velog.io/rss/@{username}` 또는 `https://v2.velog.io/rss/{username}` — 200 |
| RSS 본문 | `content:encoded` 없음. **`description`에 HTML 본문** (~수천~수만 자) |
| GraphQL | `https://v2.velog.io/graphql` — 공개 조회 가능 |
| GraphQL 본문 | `post(username, url_slug)` → **`body`는 Markdown** |
| GraphQL 목록 | `posts(username, limit)` → id, title, url_slug, tags |
| HTML | Next.js RSC — 초기 HTML에 post JSON(마크다운 body) 임베딩. User-Agent 없으면 빈 응답 가능 |
| 공식 export | 별도 일괄 export API는 확인하지 않음 (RSS·GraphQL로 대체) |

### GraphQL 예시

```graphql
query {
  posts(username: "velopert", limit: 3) {
    id title url_slug released_at tags
  }
  post(username: "velopert", url_slug: "2022.log") {
    id title body released_at tags
  }
}
```

### 마이그레이션 관점

- Velog **입력**은 Markdown 기반이므로, GraphQL `body`가 이전 시 **가장 깔끔한 원문**
- RSS `description` HTML도 백업·변환용으로 사용 가능

## Tistory

### 사전 조사

| 항목 | 결과 |
|---|---|
| robots.txt (개인 블로그) | `Disallow: /manage`, `/admin`, `/search` 등. **RSS·글 URL은 disallow 없음** |
| RSS | `https://{blog}.tistory.com/rss` — 200 |
| RSS 본문 | **`content:encoded` 없음** (jojoldu, toss.tech 확인). **`description`에 HTML 본문** (짧은 글 ~2k, 긴 글 ~15k 자) |
| HTML | 클래식 스킨 — `#article-view` 등 SSR. curl 200 |
| Open API | **2024년 2월까지 순차 종료** ([공지](https://tistory.github.io/document-tistory-apis/)) — 신규 마이그레이션 자동화는 RSS·HTML 중심 |
| 커스텀 도메인 | 예: `https://toss.tech/rss.xml` — `content:encoded` 포함 사례 있음 (회사 블로그) |

### 마이그레이션 관점

- **자기 블로그**는 RSS로 목록+본문 대부분 확보 가능 (스킨·글 길이에 따라 `description`만으로 충분한 경우 많음)
- Open API 종료 → **로그인 백업·비공개 글**은 관리자 UI·별도 export 필요 (본 testing 범위 밖)
- Velog로 옮길 때: HTML → Markdown 변환 파이프라인이 필요할 수 있음

## 스키마

```json
{
  "id": "username/slug | post-id",
  "platform": "velog | tistory",
  "title": "string",
  "url": "string",
  "published_at": "string | null",
  "author": "string | null",
  "description": "string | null",
  "categories": ["string"],
  "body": "string | null",
  "body_char_count": "number",
  "body_source": "rss_description | rss_content_encoded | graphql_markdown",
  "source_feed": "string"
}
```

## 구현

```bash
pip install beautifulsoup4 lxml

cd examples/web-crawler-ver0/scripts

# Velog — RSS 3건
python3 fetch_blog_platform_rss.py --platform velog --target velopert --limit 3

# Velog — RSS + GraphQL 마크다운 본문 샘플 1건
python3 fetch_blog_platform_rss.py --platform velog --target velopert --limit 1 --velog-graphql-body

# Tistory — 서브도메인
python3 fetch_blog_platform_rss.py --platform tistory --target jojoldu --limit 3

# Tistory — 커스텀 도메인 RSS
python3 fetch_blog_platform_rss.py --platform tistory --target toss.tech/rss.xml --limit 2
```

요청 정책: 피드 1회 GET + 기본 1초 간격. GraphQL 옵션 시 추가 1회 POST.

## E2E 결과 (클라우드 VM, 2026-08-17)

| 대상 | 목록 | RSS 본문 | GraphQL 본문 | 비고 |
|---|---|---|---|---|
| `@velopert` | ✅ 3건 | ✅ description HTML | ✅ Markdown | GraphQL 무인 성공 |
| `jojoldu.tistory.com` | ✅ 3건 | ✅ description HTML | — | content:encoded 없음 |
| `toss.tech/rss.xml` | ✅ 2건 | ✅ content:encoded | — | 회사 블로그 패턴 |

## 플랫폼 비교 (크롤링·이전 관점)

| | Velog | Tistory |
|---|---|---|
| 개발자 UX | Markdown 에디터, GitHub 연동 문화 | 스킨·에디터 다양, 비개발 글도 많음 |
| 공개 수집 | RSS + GraphQL, 구조 단순 | RSS(대부분 description), HTML 파싱 |
| 원문 형식 | GraphQL → **Markdown** | RSS/HTML → **HTML** |
| API 안정성 | GraphQL 공개 (스키마 변경 리스크는 존재) | Open API **종료** |
| 비공개·로그인 글 | 본 testing 미검증 | 관리자 백업·수동 export 필요 |
| robots | 관대 | 관리·검색 경로 제한, 글/RSS는 일반적으로 허용 |

**한 줄:** 마이그레이션용 **기계적 백업**은 양쪽 모두 **공개 RSS로 E2E 가능**. Velog는 GraphQL로 **마크다운 원문**까지 무인 확보가 쉽고, Tistory는 HTML 기반이라 **변환 단계**를 계획하는 편이 현실적입니다.

## 한계·미검증

- 사용자 **자신의 Tistory 블로그 URL**으로 재실행 필요 (본 testing은 공개 개발 블로그 샘플)
- 비공개·보호 글, 댓글, 이미지 첨부·CDN URL 만료
- Velog GraphQL rate limit·약관 (공개 읽기 범위 내 사용 가정)
- Tistory 스킨/설정에 따른 RSS 필드 차이
- Velog → Tistory 역방향 이전은 본 testing 범위 밖

## 다음 검증

1. 사용자 실제 Tistory RSS URL로 `fetch_blog_platform_rss.py` 실행
2. 글 수·이미지 비중에 따라 HTML→MD 변환 품질 확인
3. Velog 계정 생성 후 **수동 이전 1건** vs 스크립트 출력 비교

## 관찰 (Rule·Skill)

- **도움이 됐던 것:** yozm와 동일한 RSS 우선 절차가 블로그 플랫폼에도 그대로 적용됨
- **새 패턴:** Velog는 RSS만으로 부족할 때 **공개 GraphQL**이 마크다운 본문 경로 (내부 API 3단계)
- **과한 것 없음:** Playwright·HTML 파싱 생략이 타당
