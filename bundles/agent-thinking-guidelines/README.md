# Agent Thinking Guidelines

> 기존 `agent-thinking-guidelines` 저장소에서 이관되었습니다. 현재 canonical source는 `agent_skill_bundle/bundles/agent-thinking-guidelines/`입니다.

AI 에이전트가 설계·분석·대규모 변경 작업을 더 정확하고 검증 가능하게 수행하도록 만드는 **heavy protocol bundle**입니다.

## 지원 환경

**현재 공식 구현 target은 Cursor입니다.**

- `docs/`는 사고·검증·오케스트레이션 원칙의 SSOT입니다.
- 실제 실행 artifact는 `cursor/.cursor/`에만 둡니다.
- Claude Code 등 다른 platform용 배포본은 현재 유지하지 않습니다.
- 다른 platform 지원이 실제로 필요해지면 `docs/`를 기준으로 해당 platform 구현을 새로 추가합니다.

이 구분은 공통 원칙과 특정 IDE 구현을 섞지 않기 위한 것입니다.

```text
docs/
= 무엇을 지켜야 하는지

cursor/.cursor/
= Cursor에서 그 원칙을 어떻게 실행할지
```

## 기본 적용 모드: 호출 시에만 (옵트인)

지침은 품질을 높이지만 토큰·리소스 비용이 큽니다. 설치 직후 기본값은 **항상 자동 적용이 아니라 필요할 때 호출**하는 방식입니다.

| 호출 방법 | 예시 | 효과 |
|---|---|---|
| 지침 Skill | `/agent-thinking-guidelines` | 핵심 사고·행동 원칙 적용 |
| 전문 지침 참조 | `@docs/agent-thinking-guidelines.md` | SSOT 전문을 직접 참조 |
| 검증 Agent | `/reviewer …` | 산출물을 별도 관점에서 체크리스트 검증 |
| 계획 Agent | `/orchestrator …` | 큰 작업의 분해·위험 등급·라우팅 계획 |

항상 적용이 필요하면 `core-principles.mdc`, `worker-conduct.mdc`의 `alwaysApply`를 `true`로 바꿉니다. 기본값은 `false`입니다.

## 이 지침이 하는 것

- **모호함 처리 기준**: 틀렸을 때 재작업이 필요한가를 기준으로 질문/가정을 판단
- **불확실성 표기**: 확인됨 / 추정 / 가정을 구분
- **검증 프로토콜**: 샘플 검증 → 전체 확장, 행 수 추적, 집계 역산 검증
- **범위 규율**: 요청한 범위만 수정하고 unrelated cleanup은 분리
- **검증자 분리**: reviewer가 작성 과정과 분리된 관점에서 산출물을 판정
- **큰 작업 계획**: orchestrator가 분해·위험 등급·라우팅 계획을 반환

하지 못하는 것: 모델의 판단 능력 자체를 올리지는 못합니다. 이 bundle은 행동 패턴과 검증 절차를 보강합니다.

## 구조

```text
agent-thinking-guidelines/
├── README.md
├── docs/                                  # 사고·검증 원칙 SSOT
│   ├── agent-thinking-guidelines.md
│   ├── multi-agent-orchestration.md
│   └── agent-system-overview.md
└── cursor/
    ├── README.md
    └── .cursor/
        ├── rules/
        │   ├── core-principles.mdc
        │   ├── worker-conduct.mdc
        │   ├── analysis-protocol.mdc
        │   └── design-protocol.mdc
        ├── skills/
        │   ├── agent-thinking-guidelines/
        │   ├── analysis-protocol/
        │   └── design-protocol/
        ├── agents/
        │   ├── orchestrator.md
        │   └── reviewer.md
        ├── memory/
        └── state/
```

## 역할 구조

3-에이전트 구조에서 실제 루프를 라우팅하는 주체는 **메인 에이전트**입니다.

```text
사용자
  ↓
메인 에이전트
  ├─ /orchestrator → 작업 분해·위험 등급·라우팅 계획
  ├─ Worker 역할 → 실제 작업 수행
  └─ /reviewer → 결과 검증
```

`orchestrator`는 다른 Agent를 직접 호출하는 실행 엔진이 아니라 **계획 반환자**입니다. 실제 Worker 진행·reviewer 호출·상태 추적은 메인 에이전트가 수행합니다.

## 설치

Agent Skill Bundle을 사용하는 프로젝트에서는 **Bundle Catalog gate를 통한 설치를 권장**합니다. 전체 source repo를 소비 프로젝트 안에 복사하지 않고 필요한 Cursor artifact만 가져옵니다.

수동으로 확인할 경우 기준 경로는 다음과 같습니다.

```text
bundles/agent-thinking-guidelines/cursor/.cursor/rules/*
  → .cursor/rules/*

bundles/agent-thinking-guidelines/cursor/.cursor/skills/*
  → .cursor/skills/*

bundles/agent-thinking-guidelines/cursor/.cursor/agents/*
  → .cursor/agents/*

bundles/agent-thinking-guidelines/cursor/.cursor/memory/*
  → .cursor/memory/*

bundles/agent-thinking-guidelines/cursor/.cursor/state/*
  → .cursor/state/*

bundles/agent-thinking-guidelines/docs/*
  → docs/*
```

설치 시 다음은 무단 덮어쓰지 않습니다.

- 같은 이름의 프로젝트 custom Rule / Skill / Agent
- `.cursor/memory/`의 프로젝트별 교훈
- `.cursor/state/loop-status.md` 런타임 상태
- 사용자가 이미 `alwaysApply`를 조정한 경우 그 설정

자세한 Cursor 설치·사용법은 [`cursor/README.md`](cursor/README.md)를 봅니다.

## AI 채팅으로 설치

대상 Cursor 프로젝트에서 다음처럼 요청할 수 있습니다.

```text
이 프로젝트에 Agent Thinking Guidelines를 설치해줘.

소스: https://github.com/geunsu-son/agent_skill_bundle

1. Bundle Catalog gate가 있으면 먼저 설치 상태를 조사해
2. Agent Thinking Guidelines 원본은 bundles/agent-thinking-guidelines/를 사용해
3. cursor/.cursor/의 rules, skills, agents, memory, state를 현재 프로젝트 .cursor/에 필요한 것만 반영해
4. docs/agent-thinking-guidelines.md를 프로젝트 docs/에 반영해
5. 같은 이름의 custom 파일은 덮어쓰지 말고 차이를 보여줘
6. .cursor/state/loop-status.md와 프로젝트 memory는 보존해
7. 기본 모드는 opt-in(alwaysApply: false)으로 유지해
8. 완료 후 /agent-thinking-guidelines, /reviewer, /orchestrator 사용법을 알려줘
```

## 업데이트

upstream이 갱신되면 source와 소비 프로젝트를 파일별로 비교한 뒤 필요한 파일만 갱신합니다.

**갱신 대상**

- `docs/`의 공통 지침
- upstream에 존재하는 rules / skills / agents
- memory/state의 README와 example template

**보존 대상**

- 프로젝트 전용 memory 파일
- `.cursor/state/loop-status.md`
- upstream에 없는 프로젝트 custom artifact

## SSOT 동기화 체크리스트

`docs/`의 기준을 바꾸면 관련 Cursor 구현도 함께 확인합니다.

| SSOT 변경 | Cursor 구현 |
|---|---|
| 핵심 원칙·금지 행동 | `cursor/.cursor/rules/core-principles.mdc` |
| 작업 규율·진행 보고 | `cursor/.cursor/rules/worker-conduct.mdc` |
| 옵트인 안내·호출법 | `cursor/.cursor/skills/agent-thinking-guidelines/SKILL.md` |
| 분석 프로토콜 | `cursor/.cursor/skills/analysis-protocol/SKILL.md` |
| 설계 프로토콜 | `cursor/.cursor/skills/design-protocol/SKILL.md` |
| 오케스트레이션 | `cursor/.cursor/agents/orchestrator.md` |
| 검증 | `cursor/.cursor/agents/reviewer.md` |
| 메모리 규약 | `cursor/.cursor/memory/README.md` |
| 루프 상태표 | `cursor/.cursor/state/README.md` |

## 요구 사항

- Cursor Rules / Skills를 지원하는 환경
- Cursor 서브에이전트(`.cursor/agents/`)를 사용할 경우 해당 기능을 지원하는 Cursor 버전

기능 지원 여부나 버전별 동작은 실제 사용 시점의 Cursor 문서를 확인합니다.

## 운영 원칙

1. **SSOT**: 기준 변경은 `docs/`에 먼저 반영하고 Cursor artifact로 내려보냅니다.
2. **어긴 항목은 예시로 승격**: 반복 위반은 나쁨/좋음 대비 예시로 보강합니다.
3. **짧게 유지**: 항상 로드되는 Rule은 특히 짧게 유지합니다.
4. **heavy workflow는 opt-in**: 일상적인 수정까지 reviewer/orchestrator를 자동 동원하지 않습니다.
5. **다른 platform은 필요할 때 추가**: 사용하지 않는 구현체를 미리 병렬 유지하지 않습니다.

## 알려진 한계

- 지침은 행동 패턴을 교정하지만 모델의 판단 능력 자체를 올리지는 못합니다.
- reviewer와 Worker가 같은 모델이면 맹점을 공유할 수 있습니다.
- 되돌리기 어려운 작업은 reviewer 통과와 별개로 사람이 최종 확인해야 합니다.
- opt-in 상태에서는 명시적으로 호출하지 않으면 heavy guideline이 적용되지 않습니다.
