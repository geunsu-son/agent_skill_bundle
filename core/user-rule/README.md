# My Cursor User Rule

> 기존 `my_cursor_user_rule` 저장소에서 이관된 문서입니다. 현재 SSOT는 `agent_skill_bundle/core/user-rule/`입니다.

Cursor와 AI coding agent를 사용할 때의 개인적인 작업 원칙을 정리해 둔 저장소입니다.

이 rule의 목적은 AI에게 최대한 많은 코드를 작성하게 만드는 것이 아니라, **AI에게 구현은 적극적으로 맡기되 사람이 판단해야 할 지점은 놓치지 않는 작업 방식**을 만드는 것입니다.

## Why this rule exists

AI coding agent는 빠르게 많은 코드를 작성하고, 여러 파일을 수정하고, 테스트와 리팩토링까지 수행할 수 있습니다. 하지만 실제로 사용하다 보면 몇 가지 반복적인 문제가 생깁니다.

- 요구하지 않은 범위까지 확장하거나 과하게 리팩토링함
- 단순한 작업에도 불필요하게 복잡한 구조나 추상화를 추가함
- 불확실한 API나 프로젝트 동작을 추측해서 구현함
- 작은 수정에도 긴 계획과 여러 단계의 agent workflow를 사용함
- 데이터 작업에서 최종 코드만 완성하고 중간 데이터의 이상을 충분히 확인하지 못함
- notebook과 script의 역할을 구분하지 않고 한쪽으로만 작업함

이 저장소의 `user_rule.md`는 이런 문제를 줄이기 위해 만들었습니다.

## Core principles

### Think before coding

모호한 부분을 임의로 가정하지 않고, 필요한 경우에만 질문합니다. 여러 선택지가 실제로 중요한 차이를 만든다면 하나의 추천안을 먼저 제시하고 대안을 짧게 비교합니다.

반대로 명확한 작업까지 지나치게 확인하면서 흐름을 끊지 않도록 합니다.

### Simplicity first

요청한 문제를 해결하는 최소한의 코드를 우선합니다.

한 번만 쓰는 로직을 미리 추상화하거나, 필요하지 않은 설정·확장성·예외 처리를 추가하지 않습니다. 코드가 더 단순하게 해결될 수 있다면 단순한 쪽을 선택합니다.

### Surgical changes

기존 코드를 수정할 때는 요청과 직접 관련된 부분만 변경합니다.

주변 코드의 스타일을 임의로 정리하거나, 관계없는 dead code를 삭제하거나, 필요하지 않은 리팩토링을 함께 수행하지 않습니다.

### Goal-driven execution

작업은 가능한 한 검증 가능한 목표로 바꿉니다.

버그 수정이라면 재현 후 수정하고, validation 추가라면 잘못된 입력에 대한 테스트를 만들고, refactor라면 전후 동작이 동일한지 확인합니다.

다만 typo나 one-line fix처럼 작은 작업에는 별도의 긴 계획이나 checkpoint를 만들지 않습니다.

## Notebook → Verify → Promote to Script

이 rule에서 가장 중요하게 생각한 부분 중 하나는 **Jupyter Notebook과 Python script의 역할을 분리하는 것**입니다.

AI coding이 보편화될수록 `.py` 기반 코드베이스는 agent가 읽고 수정하고 테스트하기에 유리합니다. 반면 데이터 분석에서는 사람이 중간 결과를 확인하고, 가설을 바꾸고, 데이터가 예상대로 변하는지 직접 보는 과정이 여전히 중요합니다.

그래서 다음과 같이 역할을 나눕니다.

```text
.ipynb
= exploration + validation + human review

.py
= reusable + automated + production logic
```

데이터 탐색, join, aggregation, schema 확인, integrity validation처럼 중간 과정을 사람이 확인해야 하는 작업은 notebook을 우선합니다.

notebook에서는 row count, null rate, key uniqueness, join fan-out 같은 중간 상태를 확인하고, 가능하면 역검증도 수행합니다.

그 후 로직이 충분히 안정화되고 재사용할 가치가 생기면 `.py` 모듈이나 script로 옮깁니다.

```text
Explore in notebook
        ↓
Verify intermediate results
        ↓
Stabilize the logic
        ↓
Promote reusable logic to .py
        ↓
Keep notebook for exploration / audit / interpretation
```

즉 notebook을 단순한 임시 분석 파일이 아니라, **사람이 AI가 만든 분석 과정을 검토하는 인터페이스**로 활용하는 것이 목표입니다.

## Keep heavy agent workflows opt-in

Multi-agent review, orchestrator, reviewer loop 같은 방식은 큰 작업에서는 유용하지만 모든 코딩 작업에 필요한 것은 아닙니다.

일상적인 수정에서는 단일 agent가 빠르게 처리하도록 하고, 새로운 설계나 irreversible data change, 중요한 수치 보고처럼 실제로 검증 비용이 필요한 경우에만 무거운 workflow를 사용합니다.

## Repository contents

- [`user_rule.md`](./user_rule.md) — Cursor / coding agent에 적용하는 실제 user rule
- PR 작성 절차 Skill: 이 저장소의 [`.cursor/skills/pull-request/SKILL.md`](../../.cursor/skills/pull-request/SKILL.md) (`user_rule.md` §9에서 참조)

## Updating this rule

이 rule은 자주 바뀌는 설정이 아니라, 실제 사용 중 반복되는 문제나 더 나은 작업 방식이 발견됐을 때만 수정합니다.

변경 이력 관리는 **Pull Request만 사용**합니다. 별도의 Issue나 CHANGELOG는 기본적으로 만들지 않습니다. 수정 빈도가 낮은 개인 rule repository이므로, PR 하나에 변경 이유와 실제 diff를 함께 남기는 것으로 충분하다고 봅니다.

### Workflow

```text
main
  ↓
create branch
  ↓
edit user_rule.md (and related docs if needed)
  ↓
open PR
  ↓
review the diff and intent
  ↓
merge to main
```

`main`은 항상 현재 사용 중인 최신 rule을 유지합니다. rule 변경은 가능하면 별도 branch에서 진행하고 PR을 통해 merge합니다.

### PR as change history

PR은 단순한 merge 절차가 아니라 **왜 rule을 바꿨는지 기록하는 변경 이력**으로 사용합니다.

PR 본문에는 가능하면 다음 세 가지를 남깁니다.

```markdown
## Why

기존 rule에서 어떤 문제가 있었는지, 왜 수정이 필요한지 기록합니다.

## Changes

- 변경한 규칙
- 추가하거나 제거한 동작
- 기존 동작과 달라진 점

## Expected behavior

이 변경 이후 agent가 어떻게 행동하기를 기대하는지 기록합니다.
```

모든 문구 수정에 긴 설명이 필요한 것은 아닙니다. 오타나 표현 정리처럼 agent의 실제 행동을 바꾸지 않는 변경은 짧은 PR 설명으로 충분합니다.

반대로 다음과 같이 **agent의 판단이나 작업 흐름을 바꾸는 수정**은 이유와 기대 동작을 명확히 기록합니다.

- notebook / script 선택 기준 변경
- 질문하거나 확인하는 조건 변경
- 검증 방식 추가 또는 변경
- refactoring / scope 제한 기준 변경
- heavy agent workflow 사용 조건 변경

이렇게 하면 `README.md`는 현재의 철학과 운영 방식을 설명하고, `user_rule.md`는 현재 rule을 담으며, **과거 변경의 이유와 diff는 Pull Requests가 담당**합니다.

## Philosophy

이 rule을 한 문장으로 정리하면 다음과 같습니다.

> **AI에게 구현은 많이 맡기되, 중요한 판단과 검증은 사람이 놓치지 않는다.**

AI가 코드를 작성하는 비중이 커질수록 사람이 모든 코드를 직접 입력하는 능력보다, 문제를 올바르게 정의하고 중간 결과를 검증하고 필요 이상의 복잡성을 막는 능력이 더 중요해진다고 생각합니다.

이 저장소는 그 작업 방식을 지속적으로 다듬고 보관하기 위한 개인 rule repository입니다.
