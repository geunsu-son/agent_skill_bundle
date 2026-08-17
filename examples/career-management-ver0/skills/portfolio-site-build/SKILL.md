# Portfolio Site Build

## 상태

`ver0` 예시. 실제 Next·Cloudflare 배포를 통해 절차와 체크리스트를 수정할 예정입니다.

## 목적

디자인 방향과 선택된 스택에 따라 **이력·포트폴리오 웹 사이트를 구현**하고 **Vercel 또는 Cloudflare에 배포**할 수 있도록 돕습니다.

## 사용 시점

- “포트폴리오 웹 만들어줘”, “이력서 웹 배포”, “Next + Vercel”, “HTML + Cloudflare” 요청
- `portfolio-hosting-choice`·`portfolio-design-research` 완료 후 구현 단계

## 관련 Rule·Skill

- Rule: [`rules/career-management.mdc`](../../rules/career-management.mdc)
- [`portfolio-hosting-choice`](../../skills/portfolio-hosting-choice/SKILL.md) — 스택 미정 시
- [`portfolio-design-research`](../../skills/portfolio-design-research/SKILL.md) — **구현 전 필수**
- (선택) [`resume-strength-discovery`](../../skills/resume-strength-discovery/SKILL.md) — 콘텐츠
- (선택) [`career-management-session`](../../skills/career-management-session/SKILL.md) — 어필 메시지

## 입력

- 이력·프로젝트·연락처 등 **사이트 콘텐츠** (이력서 텍스트 또는 구조화 목록)
- 스택: `nextjs-vercel` | `html-cloudflare` (미정이면 hosting-choice 먼저)
- `portfolio-design-research` 출력 (없으면 본 Skill 내에서 design-research 절차를 먼저 수행)
- 저장소·프로젝트 경로 (기존 repo 또는 새 생성 위치)
- 커스텀 도메인 계획 (선택)

## 절차

### 1. 선행 Skill 확인

| 조건 | 행동 |
|---|---|
| 스택 미정 | `portfolio-hosting-choice` 실행 후 사용자 확정 또는 권장안 채택 |
| 디자인 스펙 없음 | `portfolio-design-research` 실행 |
| 콘텐츠만 흩어져 있음 | `resume-strength-discovery`로 섹션·우선순위 정리 |

### 2. 프로젝트 구조 결정

**Next.js + Vercel**

```text
권장 (ver0): App Router, TypeScript, CSS Modules 또는 Tailwind (디자인 스펙에 맞게)
- app/layout.tsx, app/page.tsx
- app/globals.css — design tokens (CSS variables)
- components/ — design-research의 components
- public/ — 정적 자산
- package.json, next.config (필요 최소)
```

**HTML + Cloudflare**

```text
권장 (ver0): 빌드 없는 정적 구조
- index.html
- styles/ (variables.css, main.css)
- scripts/ (선택, main.js — 토글·스무스 스크롤 등 최소)
- assets/
- (선택) projects/*.html — 멀티 페이지 시
```

단일 템플릿 파일을 복사하지 않고, **design-research 스펙**으로 레이아웃·토큰을 새로 작성합니다.

### 3. 콘텐츠 구현

- 이력서에 없는 경력·수치를 넣지 않습니다.
- design-research의 **콘텐츠 우선순위**대로 섹션 순서를 배치합니다.
- 필수 섹션 (요청·직무에 따라 조정):
  - Hero (포지셔닝 + CTA: 이력 PDF / 연락 / GitHub)
  - Highlights / 어필 포인트
  - Experience 또는 Projects
  - Skills (해당 시)
  - Contact

### 4. 디자인 시스템 적용

- tokens를 CSS 변수(또는 Tailwind theme)로 구현
- 다크/라이트: 스펙대로 (class `data-theme`, `prefers-color-scheme`, 토글 버튼)
- focus·대비·heading 계층·모바일 퍼스트
- design-research의 **차별화 포인트** 1개 이상 코드에 반영

### 5. 로컬 확인

- 로컬에서 빌드·미리보기
  - Next: `npm run dev` / `npm run build`
  - HTML: 정적 파일 열기 또는 `npx serve`
- 모바일 너비·다크/라이트 전환·링크·메타(title, description) 확인

### 6. 배포

#### Next.js + Vercel

1. Git 저장소에 push (또는 Vercel CLI)
2. Vercel에서 Import — Framework Preset: Next.js
3. Build: `next build`, Output: Next 기본
4. 환경 변수: ver0에서는 비밀 없이 진행; 필요 시 Vercel 대시보드에만 설정
5. 배포 URL 확인 · (선택) 커스텀 도메인 DNS

#### HTML + Cloudflare

1. **Cloudflare Pages** — Git 연동 또는 Direct Upload
2. Git 연동 시: 빌드 명령 없음, Output directory: `/` (또는 프로젝트 루트)
3. Direct Upload: `index.html` 포함 정적 폴더 업로드
4. (선택) 커스텀 도메인 — Cloudflare DNS에서 CNAME
5. HTTPS·캐시는 Cloudflare 기본 설정 활용

배포 자격 증명을 코드·커밋·공개 문서에 넣지 않습니다.

### 7. 배포 후 체크

- 공개 URL에서 콘텐츠·다크모드·모바일 확인
- 이력서·어필 포인트와 내용 일치 확인
- `robots`·개인정보(전화·이메일 노출 범위) 요청자 의도와 일치

### 8. 인수 문서

요청자에게 짧게 전달:

- 저장소 구조·수정 방법 (어디를 고치면 되는지)
- 재배포 방법 (git push / Pages 재업로드)
- 도메인 연결 시 DNS 요약
- 다음에 콘텐츠만 바꿀 때 vs 디자인 바꿀 때 진입 파일

## 출력 형식

구현 완료 시:

```md
## 빌드·배포 요약

- 스택: Next.js + Vercel | HTML + Cloudflare
- 디자인 방향: (한 줄)
- 로컬 경로 / 저장소:
- 배포 URL: (배포 완료 시)

## 수정 가이드

- 콘텐츠 수정: ...
- 스타일·토큰: ...
- 재배포: ...

## 확인 체크리스트

- [ ] 콘텐츠 = 이력 근거
- [ ] 다크/라이트 (해당 시)
- [ ] 모바일
- [ ] 메타·favicon (해당 시)
- [ ] 비밀·키 없음
```

## 완료 조건

- design-research 스펙이 코드에 반영됨
- 단일 공용 템플릿과 동일한 결과가 아님 (차별화 포인트 존재)
- 선택한 스택으로 구현·(가능 시) 배포 절차가 문서화됨
- 이력에 없는 허위 콘텐츠 없음
- Rule 금지 패턴 준수

## 향후 Script 후보

- Vercel / Cloudflare Pages deploy CLI 래퍼
- design tokens JSON → CSS 생성
- 이력서 Markdown → 섹션 JSON
