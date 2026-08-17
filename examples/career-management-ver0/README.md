# Career Management — ver0 Example

요청자가 목표 커리어에 맞춰 최신 트렌드, 이력서 강점, 어필 포인트, 발전 조언을 받을 수 있도록 Agent가 **커리어 매니저** 역할을 수행하는 예시입니다. 필요 시 이력·포트폴리오를 **웹으로 배포**하는 경로(Next.js + Vercel, HTML + Cloudflare)까지 함께 설계·구현합니다.

이 예시는 아직 완성된 제품이 아닙니다. Rule·Skill 분리와 실제 상담·배포 품질을 검증하기 위한 첫 작업물입니다.

## 해결하려는 문제

커리어 조언은 정보 수집, 이력 해석, 시장 트렌드 조사가 섞여 있어 한 번에 처리하면 누락·일반론·낡은 정보가 섞일 수 있습니다. 포트폴리오 웹은 또한 **동일 템플릿**·**스택 선택 부담**·**디자인 방향 부재**로 차별화가 어려울 수 있습니다.

이 예시는 다음 질문에 답하는 것을 목표로 합니다.

1. 목표 커리어에서 지금 강조해야 할 트렌드와 포인트는 무엇인가?
2. 요청자 이력·경험에서 실제로 어필할 수 있는 강점은 무엇인가?
3. 이력서 관점에서 보완·재배치가 필요한 부분은 무엇인가?
4. 다음 3~6개월에 무엇을 하면 커리어 발전에 도움이 되는가?
5. (웹 배포 시) 어떤 스택·디자인으로 어떻게 배포하는가?

## 구성

```text
Rule
→ 커리어 매니저의 판단·표현·윤리·웹 포트폴리오 원칙

Skill — 커리어 상담
→ 시장·트렌드 조사 (career-market-research)
→ 이력·강점·어필 포인트 발굴 (resume-strength-discovery)
→ 전체 상담 오케스트레이션 (career-management-session)

Skill — 웹 포트폴리오
→ 배포 스택 선택 (portfolio-hosting-choice)
→ 디자인 시스템·톤 조사 (portfolio-design-research)
→ 사이트 구현·배포 (portfolio-site-build)
```

- [`rules/career-management.mdc`](rules/career-management.mdc)
- [`skills/career-market-research/SKILL.md`](skills/career-market-research/SKILL.md)
- [`skills/resume-strength-discovery/SKILL.md`](skills/resume-strength-discovery/SKILL.md)
- [`skills/career-management-session/SKILL.md`](skills/career-management-session/SKILL.md)
- [`skills/portfolio-hosting-choice/SKILL.md`](skills/portfolio-hosting-choice/SKILL.md)
- [`skills/portfolio-design-research/SKILL.md`](skills/portfolio-design-research/SKILL.md)
- [`skills/portfolio-site-build/SKILL.md`](skills/portfolio-site-build/SKILL.md)

## 웹 포트폴리오 권장 흐름

```text
어필 포인트·콘텐츠 (resume-strength-discovery 또는 상담)
    ↓
portfolio-hosting-choice (Next+Vercel vs HTML+Cloudflare)
    ↓
portfolio-design-research (다크/라이트, 톤, 참고 브랜드, tokens)
    ↓
portfolio-site-build (구현 + Vercel / Cloudflare 배포)
```

## ver0에서 일부러 하지 않은 것

- 특정 채용 API·이력서 파서 고정
- 자동 이력서 수정·지원
- 연봉·합격 확률의 정량 예측
- 면접 시뮬레이션 전체 플로우
- 상담 기록 저장·추적 자동화
- 단일 공용 포트폴리오 템플릿 저장소
- Netlify·GitHub Pages 등 제3 스택 (ver0는 Next+Vercel, HTML+Cloudflare만)

먼저 Rule과 Skill만으로 상담·배포 품질이 충분한지 확인한 뒤, 반복 수집·정규화는 Script 후보로 분리합니다.

## 추천 확장 Skill (아직 미구현)

| Skill 후보 | 용도 |
|---|---|
| `job-posting-fit` | 특정 JD와 이력·강점의 적합도, 갭 분석 |
| `interview-story-crafting` | 경험을 STAR·행동면접 스토리로 구조화 |
| `profile-optimization` | 이력서·LinkedIn 섹션 재작성 초안 |
| `learning-path-planning` | 갭을 메우는 학습·프로젝트 우선순위 |
| `networking-outreach` | 커피챗·추천 요청 메시지 초안 |
| `compensation-research` | 역할·지역별 보상 범위 조사 (출처 명시) |

ver0에서는 위 Skill을 분리하지 않고, 필요 시 `career-management-session` 안에서 가볍게 다룹니다. 반복 요청이 확인되면 개별 Skill로 승격합니다.

## 관찰할 항목

- 트렌드 조언이 출처·시점과 함께 구분되는가?
- 이력서에 없는 강점을 지어내지 않는가?
- 어필 포인트가 목표 커리어와 연결되는가?
- 조언이 실행 가능한 다음 행동으로 떨어지는가?
- 과도한 확신·합격 보장 표현이 없는가?
- 개인정보·민감 경력을 불필요하게 반복 요청하지 않는가?
- 스택 선택이 요청자 상황에 맞는 근거와 함께 설명되는가?
- 포트폴리오가 템플릿과 동일해 보이지 않는가?
- 웹 콘텐츠가 이력·어필 포인트와 일치하는가?
- 배포 절차·수정 방법이 인수 가능한가?

## 예시 출력 골격

```md
## 한눈에 보기

- 목표 커리어: (요청자가 명시한 역할·산업)
- 현재 포지션 요약: 강점 2~3개, 보완 1~2개
- 지금 강조할 트렌드: 2~3개
- 다음 90일 우선 행동: 2~4개
- (웹 시) 스택·디자인 방향 한 줄

## 시장·트렌드 (출처·시점 구분)

## 이력·경험에서의 어필 포인트

## 이력서·프로필 보완 제안

## 커리어 발전 조언

## 웹 포트폴리오 (해당 시)

- 스택 권장·근거
- 디자인 방향
- 배포·수정 가이드

## 확인·가정

아직 불확실한 정보와 그에 따른 가정을 명시한다.
```

> 예시는 취업·이직 결과를 보장하는 시스템이 아니라, 정보 수집·해석·웹 제작 비용을 줄이는 보조 도구입니다.
