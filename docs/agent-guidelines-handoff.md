# Agent 가이드 핸드오프

이 문서는 현재 두 번들의 사용 경계를 설명한다.

## 어떤 것을 사용할까?

```text
일상적인 수정·버그·작은 기능
  → Core User Rule
  → 필요하면 minimal-implementation 또는 actionable-response

설계·대규모 변경·다단계 분석·고위험 작업
  → /agent-thinking-guidelines
  → implementation-protocol + 필요한 analysis/design protocol
  → orchestrator / reviewer
```

## 일상 작업

Core User Rule은 기본적으로 다음을 요구한다.

- 요청과 직접 관련된 최소 변경
- 기존 구현과 표준 기능 우선
- 불확실한 사실을 추측하지 않기
- 변경에 맞는 가장 작은 검증
- 결론과 다음 행동이 먼저인 답변

구현 범위가 과한지 검토하려면 다음처럼 요청한다.

```text
minimal-implementation을 사용해서 이 변경의 과잉 구현 여부를 검토해줘.
관련 caller, 재사용 가능한 기존 기능, 안전성, 최소 검증을 확인해줘.
```

긴 설명이나 오류 보고를 실행 가능한 형식으로 바꾸려면:

```text
actionable-response를 사용해서 다음 행동부터 보이도록 정리해줘.
단계는 번호로 나누고, 마지막에는 다음 행동 하나만 남겨줘.
```

## 큰 작업

먼저 작업의 목적·결과·제약을 적고 지침을 호출한다.

```text
/agent-thinking-guidelines
/implementation-protocol

[목적] 팀 공유용 인증 마이그레이션
[작업] 기존 인증 호출을 새 API로 교체
[자료] src/auth/, tests/auth/
[제약] public API 유지, 단계별 검증 후 확장
```

필요한 경우 추가한다.

```text
/analysis-protocol       # 데이터·집계·대량 처리
/design-protocol         # 설계·구조 변경·스키마
/orchestrator            # 작업 분해와 순서 계획
/reviewer                # 완성 산출물 검증
```

## 진행 방식

1. `orchestrator`로 작업을 나누고 위험도·완료 조건을 정한다.
2. 각 단계를 작은 산출물과 검증으로 수행한다.
3. 구현 단계에서는 `implementation-protocol`의 최소 구현 사다리를 적용한다.
4. 중간 상태를 보고하고 다음 행동 하나만 제시한다.
5. 완료 후 `reviewer`로 요청 충족·논리·수치·가정·형식을 점검한다.
6. 고위험 변경은 reviewer 통과 후에도 사람이 최종 확인한다.

## 출처와 적용 범위

- [Ponytail](https://github.com/DietrichGebert/ponytail): YAGNI, 기존 기능 재사용,
  최소 구현, 단순화의 안전선
- [i-have-adhd](https://github.com/ayghri/i-have-adhd): 결론 우선, 번호 단계,
  상태 표시, 오류의 위치·원인·수정, 다음 행동

두 저장소를 그대로 설치하거나 새 번들로 복제하지 않았다. 일반 원칙은
`core/user-rule`, 대규모 작업 절차는 `agent-thinking-guidelines`의 기존
SSOT·Skill·Agent 구조에 반영했다.
