# Agent Skill Bundle

Agent에게 일을 맡기는 **기본 규칙, 재사용 가능한 번들, 실험 중인 아이디어와 관리 도구**를 한 곳에서 관리하는 개인 Agent toolkit monorepo입니다.

이 저장소의 목표는 Rule·Skill을 많이 만드는 것이 아니라, 실제 작업에서 반복해서 유용한 패턴을 **한 곳에서 개선하고 필요한 프로젝트에 선택적으로 적용**하는 것입니다.

## 공식 지원 환경

**현재 공식 target은 Cursor입니다.**

- `core/`, `workshop-kit/`, `examples/`, `bundles/`에서 관리하는 실행 artifact는 Cursor의 `.cursor/` 구조를 기준으로 합니다.
- 각 bundle의 `docs/`는 가능한 한 플랫폼에 종속되지 않는 사고 원칙·설계 문서를 SSOT로 유지합니다.
- 실제 설치·배포 가능한 구현은 `cursor/.cursor/`만 관리합니다.
- Claude Code 등 다른 환경용 구현은 현재 유지하지 않습니다. 필요해지는 시점에 공통 `docs/`를 기준으로 별도 target을 다시 추가합니다.

```text
기본 작업 원칙
        ↓
core/

큰 작업에 필요한 재사용 프로토콜
        ↓
bundles/

새 Agent 작업 아이디어
        ↓
workshop/ → examples/ → 검증 → bundles/
                         ↑
                  workshop-kit/
```

## Bundle overview

GitHub 첫 화면에서도 현재 가지고 있는 bundle을 바로 확인할 수 있도록 상태별로 정리합니다. 상세 구성과 설치 metadata의 SSOT는 [`workshop-kit/catalog.md`](workshop-kit/catalog.md)입니다.

### Stable

| Bundle | 위치 | 용도 |
|---|---|---|
| [Agent Thinking Guidelines](bundles/agent-thinking-guidelines/README.md) | `bundles/agent-thinking-guidelines/` | 대규모·장기·다단계·고위험 작업의 사고·검증·review/orchestration |

### Testing

| Bundle | 위치 | 용도 |
|---|---|---|
| [Session Market Briefing](examples/session-market-briefing/) | `examples/session-market-briefing/` | 세션 경제 브리핑 |
| [Domain Data Analysis](examples/domain-data-analysis/) | `examples/domain-data-analysis/` | 도메인 기반 데이터 분석 설계·보고 |
| [MCP Server Craft](examples/mcp-server-craft-ver0/) | `examples/mcp-server-craft-ver0/` | MCP 서버 설계·권한·구현·연결 |

### Draft

| Bundle | 위치 | 용도 |
|---|---|---|
| [Web Crawler Craft](examples/web-crawler-ver0/) | `examples/web-crawler-ver0/` | 웹 크롤러 제작 |
| [Blog Style Writing](examples/blog-style-writing-ver0/) | `examples/blog-style-writing-ver0/` | 기존 블로그 문체 팩 구축·초고·첨삭 |
| [Career Management](examples/career-management-ver0/) | `examples/career-management-ver0/` | 커리어 상담·이력 강점 발굴·포트폴리오 지원 |

`Bundle Catalog`와 `Agent Skill Workshop`은 위 업무 번들을 만들고 설치·관리하기 위한 **공방 키트**이므로 별도 상태 목록으로 분리하지 않습니다.

## Repository structure

```text
.
├── core/
│   └── user-rule/                         # 가볍게 유지하는 개인 기본 Agent rule
│       ├── README.md
│       └── user_rule.md
│
├── bundles/                               # 검증·승격된 재사용 번들 원본
│   └── agent-thinking-guidelines/
│       ├── README.md
│       ├── docs/                          # 사고·검증 지침 SSOT
│       └── cursor/                        # Cursor 배포본
│
├── workshop-kit/                          # Bundle Catalog gate와 공방 관리 도구의 원본
├── workshop/                              # 아직 구조가 확정되지 않은 아이디어·작업 노트
├── examples/                              # 실제 사용을 시험하는 draft/testing 번들
├── docs/                                  # 공통 개념 문서
└── .cursor/                               # 이 monorepo 자체에서 활성화된 공방 관리 도구
```

### `core/` — 항상 가까이 두는 기본 원칙

[`core/user-rule/user_rule.md`](core/user-rule/user_rule.md)는 일상적인 Cursor/AI coding 작업에서 지킬 최소 원칙입니다.

- 생각하고 코딩하기
- 최소한의 변경
- 검증 가능한 목표
- notebook → verify → script 승격
- 불필요한 heavy workflow 억제
- PR 작성 시 diff 기반·일관된 형식 (`pull-request` skill)

자세한 배경과 변경 관리 방식은 [`core/user-rule/README.md`](core/user-rule/README.md)를 봅니다.

### `bundles/` — 검증되어 승격된 재사용 번들

반복해서 사용할 가치가 확인된 Rule·Skill·Agent 세트의 **SSOT**입니다.

`bundles/` 아래 원본은 소비 프로젝트에 직접 실행되는 파일이 아닙니다. Bundle Catalog를 통해 필요한 Cursor artifact만 대상 프로젝트의 `.cursor/` 등에 설치합니다.

### `workshop/` + `examples/` — 실험 공간

새 Agent 작업 아이디어는 바로 정식 번들로 만들지 않습니다.

```text
Agent 작업 아이디어
→ workshop에서 작업 정의
→ Rule / Skill / Script / Automation 분리
→ examples에서 작은 구현·실사용 테스트
→ 관찰과 수정
→ 반복 가치가 확인되면 bundles/로 승격
```

- `workshop/`: 인터뷰, 범위 정의, 설계 메모
- `examples/`: 아직 `draft` / `testing` 상태인 실제 번들 후보
- `bundles/`: 안정적으로 재사용할 정식 원본

## Core rule과 heavy bundle의 관계

일상 작업과 큰 작업을 같은 무게로 처리하지 않습니다.

```text
core/user-rule
= 평소의 가벼운 기본 행동 규칙

agent-thinking-guidelines bundle
= 필요할 때만 가져와 사용하는 heavy protocol
```

`user_rule.md`는 routine edit에 무거운 multi-agent workflow를 자동 적용하지 않습니다. 대신 작업이 **크고, 오래 걸리고, 여러 단계이거나, 되돌리기 어렵고 검증 비용이 큰 경우** `agent-thinking-guidelines` 번들 사용을 제안합니다.

번들이 현재 프로젝트에 없으면 자동으로 설치하지 않고, Bundle Catalog gate를 통해 가져올 것을 제안합니다.

## Bundle Catalog로 Cursor 프로젝트에 연결

작업 중인 다른 Cursor 저장소에서 이 toolkit의 번들을 사용할 때는 전체 repo를 소비 프로젝트 안에 복사하지 않습니다.

먼저 Bundle Catalog gate를 설치·점검한 다음, 필요한 번들만 선택합니다.

```text
지금 작업 중인 이 저장소에 Agent Skill Bundle을 연결해줘.
번들 소스: https://github.com/geunsu-son/agent_skill_bundle

1. Bundle Catalog gate를 먼저 설치하거나 보완해
2. audit-installed-bundles로 현재 .cursor/ 설치 상태를 조사해
3. 이번 연결 turn 안에서만 추가 설치할 번들을 물어봐
4. 내가 선택한 번들만 설치해
5. 설치 후 catalog와 실제 파일 상태를 다시 확인해
```

가져올 수 있는 목록과 상태는 [`workshop-kit/catalog.md`](workshop-kit/catalog.md)에서 관리합니다.

## Bundle Catalog gate

Bundle Catalog는 별도 제품이 아니라 **Cursor 프로젝트에 bundle을 설치·업데이트·제거하기 위한 관리용 bundle**입니다.

| 구성 | 역할 |
|---|---|
| `bundle-catalog.mdc` | 설치·업데이트·삭제 판단과 gate 원칙 |
| `audit-installed-bundles` | 현재 `.cursor/` 설치 상태 조사 |
| `manage-agent-bundles` | 선택한 bundle의 설치·업데이트·제거 |
| `report-bundle-feedback` | 사용 중 발견한 개선점을 source repo로 되돌리는 선택적 피드백 절차 |

원본은 `workshop-kit/`에 있고, 루트 `.cursor/`의 같은 파일은 **이 저장소 자체에서 실제로 사용하는 활성 복사본**입니다.

```text
workshop-kit/      = 관리 도구 SSOT
       ↓ sync
.cursor/           = 이 monorepo에서 활성화된 복사본

bundles/.../cursor/.cursor/
                   = 소비 Cursor 프로젝트에 배포할 bundle 원본
```

세 위치를 같은 것으로 취급하지 않습니다.

## 기본 관점: Rule → Skill → Script

- **Rule**: Agent가 지속적으로 지켜야 할 판단 기준, 역할, 제약
- **Skill**: 특정 업무를 수행하는 절차, 도구, 템플릿, 완료 조건
- **Script**: 반복 가능하고 결정론적인 실행 로직
- **Automation**: Skill을 언제 또는 어떤 조건에서 실행할지 정의

```text
Rule → Skill → Script
          ↑
     Automation
```

Rule에는 공통 판단 원칙을, Skill에는 상세 절차를, Script에는 반복 실행 로직을 둡니다. 자세한 구분은 [`docs/rule-vs-skill.md`](docs/rule-vs-skill.md)를 봅니다.

## Source of truth 원칙

중복된 실행본을 양방향으로 수정하지 않습니다.

- 개인 기본 rule: `core/user-rule/`
- 정식 bundle: `bundles/<bundle-name>/`
- 공방 관리 도구: `workshop-kit/`
- 루트 `.cursor/`: `workshop-kit/`에서 내려온 이 repo의 활성 복사본
- 소비 프로젝트의 `.cursor/`: source에서 설치된 실행본

개선은 항상 source에서 먼저 하고 필요한 실행 위치로 내려보냅니다.

```text
source 수정
→ 검증
→ 설치/동기화
→ 소비 프로젝트에서 사용
→ 필요하면 feedback
→ source 개선
```

## 현재 상태

이 저장소는 완성된 범용 framework보다 **개인적으로 실제 사용하면서 계속 다듬는 Cursor toolkit**에 가깝습니다.

- `core/`와 `bundles/`는 반복 사용을 전제로 관리합니다.
- `examples/`와 `workshop/`은 언제든 이동·통합·폐기될 수 있습니다.
- 복잡한 workflow는 필요한 상황에만 opt-in으로 사용합니다.
- 다른 AI coding platform 지원은 실제 필요가 생겼을 때 추가합니다.

핵심 원칙은 단순합니다.

> **AI에게 구현은 적극적으로 맡기되, 중요한 판단과 검증은 사람이 놓치지 않는다.**
