# Career Management Session

## 상태

`ver0` 예시. 실제 상담을 통해 단계 순서와 출력 형식을 수정할 예정입니다.

## 목적

커리어 매니저 역할로 시장 조사, 이력 검토, 어필 포인트 발굴, 커리어 발전 조언을 하나의 상담 결과로 통합합니다.

## 사용 시점

- “커리어 조언”, “이력서 검토”, “이직·전환 준비”, “목표 직무 트렌드” 요청
- 시장 맥락과 이력 해석을 한 번에 받고 싶을 때
- 이력·포트폴리오 **웹 배포**까지 경로 설계가 필요할 때 (→ 아래 웹 포트폴리오 Skill 연계)

## 관련 Rule·Skill

- Rule: [`rules/career-management.mdc`](../../rules/career-management.mdc)
- [`career-market-research`](../../skills/career-market-research/SKILL.md)
- [`resume-strength-discovery`](../../skills/resume-strength-discovery/SKILL.md)
- 웹 포트폴리오: [`portfolio-hosting-choice`](../../skills/portfolio-hosting-choice/SKILL.md), [`portfolio-design-research`](../../skills/portfolio-design-research/SKILL.md), [`portfolio-site-build`](../../skills/portfolio-site-build/SKILL.md)
- 지원·성장: [`job-posting-fit`](../../skills/job-posting-fit/SKILL.md), [`interview-story-crafting`](../../skills/interview-story-crafting/SKILL.md), [`profile-optimization`](../../skills/profile-optimization/SKILL.md), [`learning-path-planning`](../../skills/learning-path-planning/SKILL.md), [`networking-outreach`](../../skills/networking-outreach/SKILL.md), [`compensation-research`](../../skills/compensation-research/SKILL.md)

## 입력

- 목표 커리어·직무·산업 (가능하면)
- 이력서·경력 정보 (가능하면)
- 현재 상황·제약·기간 (선택)
- 상담 목적 (이직, 전환, 레벨업, 이력서만, 트렌드만, **웹 포트폴리오**, **특정 공고 지원**, **면접 준비** 등)

## 절차

### 1. 상담 목적·범위 확인

다음이 불명확하면 가정을 명시하거나 한두 가지만 짧게 확인합니다.

- 목표 커리어
- 상담 범위 (트렌드만 / 이력만 / 통합)
- 기간·제약 (예: 3개월 내 이직, 비공개 전환)

이미 제공된 정보는 다시 묻지 않습니다.

### 2. 시장·트렌드 조사

범위에 트렌드가 포함되면 `career-market-research` 절차를 따릅니다.

이력만 요청된 경우에도, 어필 포인트 연결을 위해 **최소한의 시장 맥락**(2~3개 강조 포인트)을 짧게 포함할 수 있습니다. 범위를 넘기면 사용자에게 알립니다.

### 3. 이력·강점 분석

이력이 제공되면 `resume-strength-discovery` 절차를 따릅니다.

시장 조사 결과가 있으면 매칭·갭 분석에 반드시 사용합니다.

### 4. 통합 조언 작성

다음을 연결합니다.

- **지금 강조할 것**: 트렌드 + 이력 강점의 교집합
- **보완·재배치**: 이력서·프로필·스토리 관점
- **갭 메우기**: 학습·프로젝트·네트워킹·지원 전략 (실행 가능한 수준)
- **90일 우선 행동**: 2~4개, 구체적

조언은 Rule의 금지 패턴(합격 보장, 허위 이력 권장 등)을 지킵니다.

### 5. 웹 포트폴리오 연계 (해당 시)

상담 목적에 웹 배포가 포함되면 다음 순서를 권장합니다.

1. (선택) 본 세션까지로 어필 포인트·콘텐츠 우선순위 확정
2. `portfolio-hosting-choice` — Next.js+Vercel vs HTML+Cloudflare
3. `portfolio-design-research` — 톤·다크/라이트·참고 브랜드·디자인 시스템
4. `portfolio-site-build` — 구현·배포

웹만 요청된 경우에도 design-research 없이 템플릿 구현으로 넘어가지 않습니다.

### 6. 지원·성장 Skill 연계 (해당 시)

| 상황 | Skill |
|---|---|
| 특정 공고 fit | `job-posting-fit` |
| 이력서·LinkedIn 문장 | `profile-optimization` |
| 면접·STAR 답변 | `interview-story-crafting` |
| 갭·학습 계획 | `learning-path-planning` |
| 커피챗·추천·follow-up | `networking-outreach` |
| 연봉·기대치 | `compensation-research` |

통합 상담에서는 필요한 Skill만 제안하고, 사용자가 특정 Skill을 요청하면 해당 Skill 절차를 따릅니다.

권장 순서 (특정 공고 지원): `job-posting-fit` → `profile-optimization` / `interview-story-crafting` → (갭) `learning-path-planning` → `networking-outreach` / `compensation-research`

### 7. 불확실성·다음 단계

- 가정과 확인이 필요한 정보
- 다음 상담·Skill 확장 시 유용한 입력 (특정 JD, 면접 일정 등)

## 출력 형식

```md
## 한눈에 보기

- 목표 커리어:
- 현재 포지션 요약: (강점 2~3, 보완 1~2)
- 지금 강조할 트렌드·포인트: 2~3개
- 다음 90일 우선 행동: 2~4개

## 시장·트렌드

(career-market-research 요약, 출처·시점 구분)

## 이력·어필 포인트

(resume-strength-discovery 요약)

## 커리어 발전 조언

### 지금 강조할 메시지
### 보완·재배치
### 갭과 우선 학습·실행
### 지원·네트워킹 (해당 시)
### 웹 포트폴리오 (해당 시)

- 권장 스택·근거
- 디자인 방향 한 줄
- 다음 Skill: hosting-choice → design-research → site-build

### 지원·성장 (해당 시)

- fit 요약 / 다음 Skill 권장

## 확인·가정·한계

## 다음에 도움이 될 정보
```

범위가 “트렌드만” 또는 “이력만”이면 해당 섹션을 깊게, 나머지는 짧게 유지합니다.

## 완료 조건

- Rule 원칙(사실·관측·해석 구분, 허위 강점 금지)을 준수함
- 요청 범위에 맞는 섹션이 포함됨
- 트렌드와 이력이 연결된 조언이 포함됨 (통합 상담 시)
- 다음 90일 행동이 구체적임 (통합·발전 조언 시)
- 합격·연봉 보장 표현이 없음

## 향후 Automation·Script 후보

- 정기 커리어 체크인 (분기별 트렌드·이력 업데이트)
- JD URL 입력 시 fit 분석 Skill과 연동
- 상담 기록 저장·이전 조언과 diff
