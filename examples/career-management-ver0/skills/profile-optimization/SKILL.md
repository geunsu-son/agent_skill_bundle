# Profile Optimization

## 상태

`ver0` 예시. 실제 이력서·LinkedIn 수정 피드백으로 섹션 템플릿을 수정할 예정입니다.

## 목적

이력서·LinkedIn 등 **프로필 섹션**을 목표 커리어·(선택) JD에 맞게 **재작성 초안**을 제공합니다. 사실을 바꾸지 않고 표현·구조·우선순위만 최적화합니다.

## 사용 시점

- 이력서·LinkedIn 문장이 약하거나 산만할 때
- `job-posting-fit`·`resume-strength-discovery` 후 구체 수정이 필요할 때
- `portfolio-site-build` 전 웹용 한 줄 소개·요약 필요

## 관련 Rule·Skill

- Rule: [`rules/career-management.mdc`](../../rules/career-management.mdc)
- [`resume-strength-discovery`](../../skills/resume-strength-discovery/SKILL.md)
- (선택) [`job-posting-fit`](../../skills/job-posting-fit/SKILL.md)
- (선택) [`career-market-research`](../../skills/career-market-research/SKILL.md)

## 입력

- 현재 이력서·LinkedIn 텍스트 (섹션별 가능)
- 목표 직무·산업
- (선택) JD 또는 `job-posting-fit` 출력
- (선택) 어필 포인트·강조할 프로젝트
- 형식: 이력서 PDF용 / LinkedIn / 둘 다
- 톤: 격식 / 테크 업계 간결 / 국문 / 영문

## 절차

### 1. 현재 상태 진단

섹션별로 짧게:

- **강점**: 잘 드러난 부분
- **약점**: 맥락 부족, 수치 없음, 키워드 누락, 우선순위 혼란
- **유지**: 건드리지 않을 사실·문장

### 2. 섹션 우선순위

목표·JD에 맞게 **상단·강조 순서**를 제안합니다.

예: Summary → Experience → Projects → Skills (직무에 따라 조정)

### 3. 재작성 초안

다음 원칙을 따릅니다.

- **사실 추가·변경 금지** — 없는 스킬·성과·기간을 넣지 않음
- **구체화**: 가능한 범위에서 수치·범위·Before/After (이력에 있거나 사용자 확인 가능한 것만)
- **키워드**: JD·시장 조사 키워드를 **사실에 맞는 범위**에서 반영
- **한 줄 포지셔닝**: 헤드라인·Summary 1~2문장
- **Experience**: 역할 한 줄 + 불릿 2~4개 (행동·결과)
- **LinkedIn**: About, Headline, Featured 힌트 (해당 시)

각 초안에 **변경 의도**를 한 줄로 붙입니다.

### 4. 삭제·축소 제안

목표와 거리가 멀거나 공간만 차는 항목 (근거와 함께)

### 5. 확인 요청

수치·범위가 이력에 없어 보강이 필요한 불릿에 **사용자에게 물을 질문** 2~5개

## 출력 형식

```md
## 진단 요약

## 권장 섹션 순서·구조

## 재작성 초안

### Headline / Summary
(초안 + 변경 의도)

### Experience — (회사·역할)
(불릿 초안 + 변경 의도)

### Projects / Skills / LinkedIn About (해당 시)

## 삭제·축소 제안

## 확인이 필요한 정보 (수치·맥락 보강)

## 금지 사항 준수 확인

- 사실 변경 없음 / 허위 서술 없음
```

## 완료 조건

- 초안이 목표·(선택) JD와 연결됨
- 사실 변경·허위 서술 없음
- 섹션별 변경 의도가 있음
- 확인 질문 또는 한계가 명시됨
- Rule 금지 패턴 준수

## 향후 Script 후보

- 불릿 길이·키워드 커버리지 체크
- LinkedIn 글자 수 제한 검증
