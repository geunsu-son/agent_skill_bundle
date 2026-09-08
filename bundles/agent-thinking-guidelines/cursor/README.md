# Cursor implementation

Agent Thinking Guidelines의 공통 지침(`../docs/`)을 Cursor의 Rules / Skills / Agents 구조로 매핑한 공식 구현입니다.

**현재 Agent Thinking Guidelines가 유지하는 실행 target은 Cursor 하나입니다.** 다른 platform 구현은 이 디렉터리와 병렬로 유지하지 않습니다.

기본 적용 모드는 **opt-in**입니다. 설치 직후 `core-principles.mdc`, `worker-conduct.mdc`의 `alwaysApply`는 `false`이며, 필요한 작업에서 명시적으로 호출합니다.

## 구성

```text
cursor/
├── .cursor/
│   ├── rules/
│   │   ├── core-principles.mdc
│   │   ├── worker-conduct.mdc
│   │   ├── analysis-protocol.mdc
│   │   └── design-protocol.mdc
│   ├── skills/
│   │   ├── agent-thinking-guidelines/
│   │   ├── analysis-protocol/
│   │   └── design-protocol/
│   ├── agents/
│   │   ├── orchestrator.md
│   │   └── reviewer.md
│   ├── memory/
│   └── state/
└── README.md
```

| 구성 | 적용 방식 | 역할 |
|---|---|---|
| `agent-thinking-guidelines` | `/agent-thinking-guidelines` | 기본 사고·행동 지침 적용 |
| `core-principles` | opt-in Rule | 모호함 처리, 불확실성 표기, 자체 검토 |
| `worker-conduct` | opt-in Rule | 가정 자기신고, 수정 범위, 체크포인트 규율 |
| `analysis-protocol` | Rule trigger + Skill | 샘플 검증 → 전체 확장, 행 수 추적, 역산 검증 |
| `design-protocol` | Rule trigger + Skill | 구조 먼저, 결정/미결정 구분, 범위 최소화 |
| `orchestrator` | `/orchestrator` | 작업 분해·위험 등급·라우팅 계획 반환 |
| `reviewer` | `/reviewer` | 산출물 체크리스트 검증 |
| `memory/` | 수동 참조 | 프로젝트별 교훈 저장 |
| `state/` | 루프 시 사용 | 반려 횟수·작업 상태 영속화 |

## 호출 방법

1. **`/agent-thinking-guidelines`** — heavy guideline 적용
2. **`@docs/agent-thinking-guidelines.md`** — SSOT 전문 직접 참조
3. **`/reviewer …`** — 결과 검증
4. **`/orchestrator …`** — 큰 작업 계획

항상 적용이 필요할 때만 `core-principles.mdc`, `worker-conduct.mdc`의 `alwaysApply`를 `true`로 바꿉니다.

## 설치

가능하면 Agent Skill Bundle의 **Bundle Catalog gate**를 통해 설치합니다.

수동 설치 기준은 다음과 같습니다.

```bash
# bundle root를 알고 있다는 전제
mkdir -p <your-project>/docs
cp <bundle-root>/docs/agent-thinking-guidelines.md <your-project>/docs/

# .cursor/가 이미 있으면 통째로 덮어쓰지 말고 내용을 병합
cp -r <bundle-root>/cursor/.cursor/* <your-project>/.cursor/
```

### 설치 시 보존

- 같은 이름의 프로젝트 custom Rule / Skill / Agent
- `.cursor/memory/`의 프로젝트별 교훈
- `.cursor/state/loop-status.md`
- 사용자가 직접 조정한 `alwaysApply` 설정

같은 이름의 upstream 파일과 local 파일이 다르면 먼저 diff를 확인하고 사용자가 선택합니다.

## 설치 확인

- `.cursor/rules/`에 4개 guideline rule이 존재하는지 확인
- `.cursor/skills/`에 `agent-thinking-guidelines`, `analysis-protocol`, `design-protocol`이 존재하는지 확인
- `.cursor/agents/`에 `orchestrator.md`, `reviewer.md`가 존재하는지 확인
- `.cursor/memory/`, `.cursor/state/` 규약 파일이 존재하는지 확인
- `docs/agent-thinking-guidelines.md`가 존재하는지 확인
- 기본 opt-in 상태라면 `alwaysApply: false`인지 확인

## 작업 예시

### 데이터 분석

```text
/agent-thinking-guidelines

[목적] 이번 주 팀 회의 공유용
[작업] @sales.csv에서 채널별 매출 변화 분석
[제약] pandas 사용, Markdown 표

먼저 데이터 행 수·컬럼·결측을 확인하고,
샘플로 처리 로직을 검증한 뒤 전체에 적용해.
각 단계 행 수를 기록하고 최종 집계 하나는 원본으로 역산 검증해.
완료되면 reviewer로 검증해.
```

### 설계

```text
/agent-thinking-guidelines

[작업] @schema.sql 기준으로 권한 테이블 설계
[제약] 기존 users 구조는 변경하지 않음

바로 구현하지 말고 먼저 구조와 영향 범위를 제안해.
결정한 것과 미결정인 것을 나누고, 미결정 항목은 옵션과 trade-off를 보여줘.
```

### 대규모 변경

```text
/agent-thinking-guidelines

/orchestrator
src/의 구 API 호출을 신규 API로 옮기는 작업을 분해하고
위험 등급·순서·완료 기준·reviewer 검증 지점을 계획해줘.
```

`orchestrator`는 계획을 반환합니다. 실제 작업·reviewer 호출·상태 추적은 메인 에이전트가 수행합니다.

## 3-agent loop

```text
orchestrator → 계획
      ↓
main agent / Worker → 작업
      ↓
reviewer → 통과 / 반려
      ↓
main agent → 수정·다음 단계·에스컬레이션
```

반려 횟수와 작업 상태는 `.cursor/state/loop-status.md`에 기록합니다. 자세한 규약은 [`../docs/multi-agent-orchestration.md`](../docs/multi-agent-orchestration.md)를 참조합니다.

처음부터 모든 역할을 자동화하기보다 **reviewer부터 사용하고**, 검증 루프가 안정된 뒤 orchestrator를 추가하는 것을 권장합니다.

## 업데이트

upstream bundle이 바뀌면:

1. `../docs/`와 현재 프로젝트 `docs/`를 비교
2. upstream rules / skills / agents를 local과 비교
3. 변경 요약을 먼저 확인
4. upstream 관리 파일만 갱신
5. 프로젝트 memory / runtime state / custom artifact는 보존
6. 설치 상태를 다시 audit

## 운영·보수

1. 원칙 변경은 먼저 `../docs/`에 반영합니다.
2. Rule은 항상 로드될 가능성이 있으므로 짧게 유지합니다.
3. 반복해서 어기는 사례는 나쁨/좋음 대비 예시로 보강합니다.
4. routine edit에는 heavy guideline을 자동 적용하지 않습니다.
5. 되돌리기 어려운 작업은 reviewer와 별개로 사람이 최종 확인합니다.

## 알려진 한계

- guideline은 모델 성능 자체를 높이지 않습니다.
- 같은 모델이 Worker와 reviewer를 맡으면 공통 맹점이 생길 수 있습니다.
- opt-in 상태에서는 호출하지 않으면 지침이 적용되지 않습니다.
- Cursor 기능과 파일 형식은 버전에 따라 달라질 수 있으므로 실제 사용 시점의 Cursor 문서를 확인합니다.
