# Agent Skill Bundle

Agent Rule, Skill, Script, Automation을 떠오르는 **Agent 작업 아이디어**부터 실제 구현까지 천천히 다듬어가는 작은 공방입니다.

이 저장소에서 말하는 아이디어는 제품 아이디어 전반이 아니라, **Agent에게 어떤 작업을 맡길지, 그 작업을 어떤 기준과 절차로 수행하게 할지에 대한 아이디어**를 의미합니다.

이 저장소는 완성된 프레임워크를 선언하기보다 다음 과정을 기록하는 데 목적이 있습니다.

```text
Agent 작업 아이디어
→ 짧은 인터뷰와 작업 정의
→ Rule / Skill / Script / Automation 분리
→ 작은 예시 구현
→ 실제 사용
→ 관찰과 수정
```

## 현재 상태

**ver0 — 공간 만들기와 첫 아이디어 배치**

아직 구조와 규칙을 확정하지 않습니다. 문서와 예시는 언제든 이동·통합·폐기될 수 있습니다. 실제 업무에서 반복 사용해보고 유용한 패턴만 남깁니다.

## 시작하기

**작업 중인 저장소**에 Agent Skill Bundle을 연결할 때 Agent에게 아래 프롬프트를 입력합니다. 번들 소스 저장소를 clone하지 않고, 현재 저장소의 `.cursor/`만 다룹니다.

번들 소스: https://github.com/geunsu-son/agent_skill_bundle

```text
지금 작업 중인 이 저장소에 Agent Skill Bundle을 연결해줘.
번들 소스: https://github.com/geunsu-son/agent_skill_bundle

1. Bundle Catalog gate(총괄 rule)를 먼저 .cursor/에 설치하거나 보완한다
   - bundle-catalog.mdc
   - audit-installed-bundles Skill
   - manage-agent-bundles Skill
2. audit-installed-bundles Skill로 .cursor/와 catalog를 조사해
   어떤 번들이 이미 설치되어 있는지 확인한다
3. **이번 연결 turn 안에서만** 조사 결과를 보여 준 뒤, 추가로 설치할 번들이 무엇인지 나에게 물어본다
4. 내가 고른 번들만 .cursor/에 설치한다 (추가하지 않음을 선택해도 됨)
5. .cursor/agent-bundles/catalog.md를 갱신하고 최종 상태를 요약한다
6. 연결이 끝난 뒤에는 내가 다시 요청하기 전까지 추가 번들 설치를 묻지 않는다
```

### gate 흐름

```text
작업 중인 저장소
→ Bundle Catalog gate 선설치 (총괄 rule)
→ audit-installed-bundles로 설치 상태 조사
→ gate가 **연결 turn 안에서만** 설치할 번들 질문
→ 선택한 번들만 .cursor/에 설치
→ 이후에는 사용자가 요청할 때만 추가 설치
```

이미 gate가 있거나 일부 번들이 설치되어 있어도 같은 흐름으로 점검합니다. 적용 여부를 추정하지 않고 먼저 조사합니다. **연결이 끝난 뒤에는 번들 추가를 다시 묻지 않습니다.**

설치 상태만 조사할 때:

```text
audit-installed-bundles Skill로
이 저장소에 설치된 Agent Skill Bundle 상태를 조사해줘.
```

추가 번들만 설치할 때:

```text
Agent Skill Bundle gate를 통해
Agent Skill Workshop 번들만 추가로 설치해줘.
```

## 용어: 에이전트 번들

이 저장소에서 아이디어를 구현한 rule-skill 세트의 공식 단위는 **에이전트 번들(Agent Bundle, 줄여서 번들)** 입니다.

| 용어 | 의미 |
|---|---|
| Agent 작업 아이디어 | Agent에게 맡길 작업과 기대 결과에 대한 생각 |
| **에이전트 번들(번들)** | 하나의 Agent 작업 아이디어를 Rule·Skill(+ Script·Automation)으로 묶은 단위 |
| 구성 요소 | 번들 안의 Rule, Skill, Script, Automation |
| 공방 키트 번들 | 공방 운영·총관리용 번들. 원본은 `workshop-kit/` |
| 예시 번들 | 특정 업무를 시험하는 번들. 원본은 `examples/<bundle-name>/` |
| 활성 번들 | `.cursor/`에 설치되어 Cursor가 읽는 번들 |

```text
Agent 작업 아이디어
→ 에이전트 번들 (Rule + Skill [+ Script] [+ Automation])
→ 필요 시 .cursor/에 설치해 활성화
```

예시 번들은 `examples/`에 두고, 실제로 쓸 때 gate를 통해 `.cursor/`에 설치합니다. 가져올 수 있는 번들 목록은 [`workshop-kit/catalog.md`](workshop-kit/catalog.md), 설치된 번들 목록은 소비 프로젝트의 `.cursor/agent-bundles/catalog.md`에서 관리합니다.

## 기본 관점

- **Rule**: Agent가 지속적으로 지켜야 할 판단 기준, 역할, 제약
- **Skill**: 특정 업무를 수행하는 절차, 도구, 템플릿, 완료 조건
- **Script**: 반복 가능하고 결정론적인 실행 로직
- **Automation**: Skill을 언제 또는 어떤 조건에서 실행할지 정의

권장 흐름은 다음과 같습니다.

```text
Rule → Skill → Script
          ↑
     Automation
```

Rule에는 공통 원칙을, Skill에는 상세 절차를, Script에는 반복 실행 로직을 둡니다. 이렇게 분리하면 긴 코드와 절차를 항상 컨텍스트에 넣지 않아도 되고, Agent는 판단과 예외 처리에 더 집중할 수 있습니다.

## 왜 공방 운영용 Agent Rule과 Skill을 두는가

이 저장소에는 개별 업무를 수행하는 Rule과 Skill뿐 아니라, **Agent 작업 아이디어를 구체화하고 구현하는 Agent 자체를 위한 메타 Rule과 Skill**도 둡니다.

개별 업무용 Agent만 있으면 매번 다음을 사람이 다시 판단해야 합니다.

- 이 아이디어가 정확히 어떤 작업인지
- 누구의 어떤 문제를 해결하려는지
- 어떤 결과물이 나와야 하는지
- 이 아이디어를 어디에 기록할지
- Rule, Skill, Script, Automation 중 무엇으로 만들지
- 어느 수준까지 구현할지
- 언제 재사용 가능한 산출물로 승격할지
- 변경 후 무엇을 기록할지

공방 운영용 Agent는 이 판단 과정을 일정하게 만드는 역할을 합니다.

```text
공방 운영용 Agent
→ 작업 아이디어를 인터뷰하고 필요한 산출물로 분해

개별 업무용 Agent
→ 세션 브리핑, 데이터 검증 등 실제 업무 수행
```

### 공방 운영용 Rule

`.cursor/rules/agent-skill-workshop.mdc`

공방에서 Agent가 작업할 때 지켜야 할 기준을 정의합니다.

- 처음부터 범용 프레임워크를 만들지 않기
- 작업 목적과 결과가 불명확하면 구현 전에 짧게 인터뷰하기
- 사용자가 이미 제공한 정보는 다시 묻지 않기
- 구현에 가장 큰 영향을 주는 질문부터 확인하기
- 인터뷰가 목적이 되지 않도록 구현 가능한 상태에서 질문을 끝내기
- 아이디어와 검증된 구현을 구분하기
- Rule은 짧게 유지하기
- 상세 절차는 Skill로 분리하기
- 반복 로직은 Script로 분리하기
- 과도한 리팩터링을 피하기
- 변경 후 미완성과 다음 실험을 기록하기

### 공방 운영용 Skill

`.cursor/skills/idea-to-agent-artifact/SKILL.md`

떠오른 Agent 작업 아이디어를 짧게 인터뷰하고 실제로 시험할 수 있는 최소 산출물로 바꾸는 절차를 정의합니다.

```text
제공된 정보 확인
→ 필요한 경우 짧은 인터뷰
→ 작업 아이디어 정의
→ 기존 자료 확인
→ Rule / Skill / Script / Automation 분해
→ 현재 상태 결정
→ 최소 예시 구현
→ 검증 방법 작성
→ README와 관찰 기록 연결
```

기본 호출 예시는 다음과 같습니다.

```text
이 Agent 작업 아이디어를 공방 규칙에 맞춰 구체화해줘.
이미 설명한 내용은 다시 묻지 말고, 구현에 꼭 필요한 정보만 짧게 확인한 뒤
Rule·Skill·Script·Automation으로 필요한 만큼만 분해해서
실제로 시험할 수 있는 최소 예시를 만들어줘.
```

### 번들 총관리 Rule과 Skill

번들이 늘어날수록 어떤 세트를 가져오고·업데이트하고·삭제할지 판단하는 **gate 번들**입니다.

- Rule: [`workshop-kit/rules/bundle-catalog.mdc`](workshop-kit/rules/bundle-catalog.mdc)
- Skill — 설치 조사: [`workshop-kit/skills/audit-installed-bundles/SKILL.md`](workshop-kit/skills/audit-installed-bundles/SKILL.md)
- Skill — 설치·변경: [`workshop-kit/skills/manage-agent-bundles/SKILL.md`](workshop-kit/skills/manage-agent-bundles/SKILL.md)
- 소스 catalog: [`workshop-kit/catalog.md`](workshop-kit/catalog.md)

연결 흐름은 [시작하기](#시작하기)와 같습니다. 총괄 rule 선설치 → `audit-installed-bundles`로 조사 → gate가 설치할 번들 질문 → 선택분만 설치. 소비 프로젝트의 설치 기록은 `.cursor/agent-bundles/catalog.md`에 둡니다.

## 작업 아이디어 인터뷰

Agent가 요청을 받자마자 파일부터 만드는 것을 막기 위해, 핵심 정보가 부족한 경우 짧은 인터뷰를 먼저 수행합니다.

최소한 다음 세 가지가 명확해야 `draft` 구현을 시작합니다.

1. Agent에게 맡길 작업
2. 기대하는 최종 결과물
3. 현재 방식에서 해결하려는 가장 큰 문제

작업 성격에 따라 다음 내용을 추가로 확인할 수 있습니다.

| 상황 | 확인할 내용 |
|---|---|
| 반복 업무 | 실행 시점과 주기 |
| 판단 업무 | 사용하는 정보와 판단 기준 |
| 자동화 업무 | 시작·중단 조건 |
| 권한 또는 위험이 있는 작업 | 제약과 금지사항 |
| 결과물 생성 | 대상 독자, 형식, 저장 위치 |
| 품질 검증 필요 | 완료와 실패 조건 |

모든 질문을 한 번에 묻지는 않습니다. 이미 제공된 정보는 재질문하지 않고, 구현 범위에 가장 큰 영향을 주는 질문부터 하나씩 확인합니다. 사소한 공백은 가정으로 명시하고 진행합니다.

다음 상태가 되면 인터뷰를 종료합니다.

- 작업 목적을 한두 문장으로 설명할 수 있음
- Agent의 최종 출력 또는 행동이 구체적임
- 최소 구현 범위를 정할 수 있음
- 남은 불확실성을 가정이나 실험 항목으로 기록할 수 있음

인터뷰 결과는 필요에 따라 다음 형태로 정리합니다.

```text
작업 이름
해결하려는 문제
Agent가 수행할 작업
기대 결과물
현재 방식과 불편한 점
실행 시점 또는 조건
판단 기준과 제약
완료 조건
가정과 아직 결정하지 못한 점
```

## `.cursor/`와 `workshop-kit/`을 함께 두는 이유

메타 Rule과 Skill은 두 위치에 둡니다.

```text
workshop-kit/   관리·배포용 원본
      ↓
.cursor/        현재 저장소에서 Cursor가 사용하는 실행본
```

### `.cursor/`

Cursor가 이 저장소에서 바로 읽고 적용하는 실행 위치입니다.

### `workshop-kit/`

Rule과 Skill을 저장소의 독립적인 결과물로 관리하는 원본 위치입니다.

- 다른 프로젝트로 복사하기 쉬움
- `.cursor` 설정과 별개로 내용을 검토하기 쉬움
- 이후 패키지나 설치 스크립트로 발전시키기 쉬움
- 이 저장소 자체를 위한 설정과 배포 가능한 산출물을 구분할 수 있음

ver0에서는 자동 동기화 도구를 만들지 않습니다. 구조가 안정되기 전부터 자동화를 추가하면 관리 방식 자체가 실험 대상인데도 구현이 먼저 굳어질 수 있기 때문입니다. 당분간 두 위치를 함께 수정하며 중복 비용과 사용성을 관찰합니다.

## 디렉터리

```text
.cursor/                  현재 저장소에서 사용하는 Agent 설정
├── rules/
└── skills/

docs/                     개념과 설계 기록
examples/                 아직 검증되지 않은 예시 번들
workshop/                 다음에 다듬을 아이디어와 관찰 메모
workshop-kit/             공방 키트 번들의 관리 원본
├── catalog.md            등록된 에이전트 번들 목록
├── rules/
└── skills/
```

현재 주요 파일:

- [Rule과 Skill의 차이](docs/rule-vs-skill.md)
- [Workshop Kit](workshop-kit/README.md)
- [에이전트 번들 카탈로그](workshop-kit/catalog.md)
- [공방 운영용 Rule](workshop-kit/rules/agent-skill-workshop.mdc)
- [아이디어 구현 Skill](workshop-kit/skills/idea-to-agent-artifact/SKILL.md)
- [번들 총관리 Rule](workshop-kit/rules/bundle-catalog.mdc)
- [번들 설치 조사 Skill](workshop-kit/skills/audit-installed-bundles/SKILL.md)
- [번들 관리 Skill](workshop-kit/skills/manage-agent-bundles/SKILL.md)
- [세션 경제 브리핑 예시](examples/session-market-briefing/README.md)
- [커리어 매니지먼트 예시](examples/career-management-ver0/README.md)
- [웹 크롤러 제작 예시](examples/web-crawler-ver0/README.md)
- [작업대 메모](workshop/README.md)

## 첫 예시: 세션 경제 브리핑

첫 예시는 직장인을 위한 **세션 경제 브리핑**입니다.

단순히 뉴스와 경제 일정을 나열하지 않고 다음 질문에 답하는 것을 목표로 합니다.

- 상승·하락·횡보 중 현재 무엇이 가장 유력한가
- 그 판단의 핵심 근거는 무엇인가
- 어떤 조건에서 판단이 바뀌는가
- 다음 확인 시점까지 무엇만 보면 되는가

이 예시는 다음 구분을 시험합니다.

```text
Rule
→ 시장 판단과 표현에서 지켜야 할 원칙

Skill
→ 조사, 비교, 방향 판정, 출력 절차

Automation
→ 평일 07:30·20:30 실행 시점

Script 후보
→ 경제 일정과 시장 데이터의 반복 수집·정규화
```

아직 정답이나 완성품이 아니라 실제 브리핑 결과를 보며 수정할 첫 번째 실험입니다.

## 이 공방에서 일하는 방식

### 1. Agent 작업 아이디어를 먼저 남긴다

분류가 확실하지 않아도 `workshop/`에 맡기려는 작업, 해결하려는 문제, 기대 결과, 아직 모르는 점을 적습니다.

### 2. 필요한 경우 짧게 인터뷰한다

작업 목적과 결과물이 불명확하면 구현에 필요한 최소 질문만 확인합니다. 질문을 위한 질문은 하지 않습니다.

### 3. 작업 아이디어를 정의한다

인터뷰 결과와 이미 제공된 내용을 바탕으로 어떤 작업을 왜 만드는지 한눈에 볼 수 있게 정리합니다.

### 4. 시험할 가치가 있으면 최소 예시를 만든다

`examples/` 아래에 필요한 Rule, Skill, Automation만 배치합니다. 코드가 아직 필요하지 않다면 빈 Script 구조를 만들지 않습니다.

### 5. 실제 사용 결과를 기록한다

기본 관찰 항목은 세 가지입니다.

1. 바로 도움이 된 내용
2. 불필요하거나 과도했던 내용
3. 다음 실행에서 바꿀 한 가지

### 6. 반복해서 유효한 것만 승격한다

한두 번의 아이디어를 공통 원칙으로 만들지 않습니다. 여러 사례에서 반복해서 유효했던 기준만 재사용 Rule이나 Skill로 다듬습니다.

### 7. 같은 코드가 반복되면 Script로 분리한다

Agent가 같은 쿼리나 코드를 계속 생성하기 시작하면, 테스트 가능한 Script로 옮기고 Skill에는 실행 순서와 완료 조건만 남깁니다.

## 산출물 상태

각 아이디어와 예시는 다음 상태를 사용할 수 있습니다.

| 상태 | 의미 |
|---|---|
| `idea` | 생각만 기록된 상태 |
| `draft` | 최소 구조가 작성된 상태 |
| `testing` | 실제 사용하며 검증 중인 상태 |
| `reusable` | 반복 사용으로 재사용 가치가 확인된 상태 |
| `archived` | 현재 사용하지 않지만 기록은 보존하는 상태 |

ver0에서 새로 만드는 예시는 기본적으로 `draft` 또는 `testing` 상태로 둡니다.

## 운영 원칙

1. 처음부터 완성도를 요구하지 않는다.
2. 사용자가 해결하려는 실제 문제부터 정의한다.
3. 목적과 기대 결과가 불명확하면 구현 전에 짧게 인터뷰한다.
4. 이미 제공된 정보는 다시 묻지 않는다.
5. 인터뷰가 구현보다 커지지 않게 한다.
6. 아이디어와 검증된 구현을 구분한다.
7. 예시는 정답이 아니라 검증 대상이다.
8. Rule은 짧게, 상세 절차는 Skill로, 반복 코드는 Script로 분리한다.
9. 필요한 구성 요소만 만들고 빈 구조를 억지로 늘리지 않는다.
10. 실제 사용 후 관찰한 문제를 다음 버전에 반영한다.
11. 구조보다 사용 경험을 먼저 축적한다.

## 다음에 해볼 것

- 새 인터뷰 절차로 두 번째 Agent 작업 아이디어 구체화
- 인터뷰 질문이 과하거나 부족하지 않은지 관찰
- 세션 경제 브리핑을 실제 출력과 비교해 Rule·Skill 수정
- `observations.md` 형식 추가
- 방향 판단 기준과 유력도 표현 방식 실험
- 뉴스·경제 일정 수집 중 반복 가능한 부분을 Script 후보로 분리
- `.cursor/`와 `workshop-kit/` 이중 관리가 실제로 유용한지 검토

> 이 저장소의 목표는 좋은 지침을 한 번에 만드는 것이 아니라, 반복해서 더 나은 작업 방식을 발견하는 것입니다.