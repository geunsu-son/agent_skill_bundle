---
name: manage-agent-bundles
description: Bundle Catalog gate 설치, 번들 선택, 설치·업데이트·삭제·보관을 수행하는 절차
---

# Manage Agent Bundles

## 사용 시점

- 작업 중인 저장소에 Agent Skill Bundle을 연결·점검할 때
- gate를 통해 추가 번들을 설치할 때
- 설치된 번들을 업데이트·삭제할 때

설치 상태 조사는 `audit-installed-bundles` Skill에 맡긴다. 이 Skill은 조사 결과를 받은 뒤 설치·변경을 수행한다.

## 기본값

- **번들 소스**: `https://github.com/geunsu-son/agent_skill_bundle`
- **소스 catalog**: `workshop-kit/catalog.md`
- **로컬 catalog**: `.cursor/agent-bundles/catalog.md`

번들 소스 저장소를 소비 프로젝트 안에 clone하지 않는다. 필요한 파일만 가져온다.

## 절차

### 1. 요청과 범위 확인

- **요청 유형**: `connect`, `add`, `audit`, `update`, `remove` 중 무엇인가
- 번들 소스 URL
- 사용자가 이미 선택한 번들 또는 Agent 작업 목적

이미 제공된 정보는 다시 묻지 않는다.

`connect`가 아닌 일반 작업 turn에서는 번들 추가 설치를 묻지 않는다.

### 2. Bundle Catalog gate 보완

gate가 `missing` 또는 `partial`이면 아래 Bundle Catalog 번들 파일을 번들 소스에서 가져와 `.cursor/`에 둔다.

- `workshop-kit/rules/bundle-catalog.mdc` → `.cursor/rules/bundle-catalog.mdc`
- `workshop-kit/skills/audit-installed-bundles/SKILL.md` → `.cursor/skills/audit-installed-bundles/SKILL.md`
- `workshop-kit/skills/manage-agent-bundles/SKILL.md` → `.cursor/skills/manage-agent-bundles/SKILL.md`
- `workshop-kit/skills/report-bundle-feedback/SKILL.md` → `.cursor/skills/report-bundle-feedback/SKILL.md`

로컬 catalog가 없으면 아래 템플릿으로 만든다. gate 보완만으로 다른 번들은 아직 설치하지 않는다.

```md
# Local Agent Bundle Catalog

## Bundle Source

https://github.com/geunsu-son/agent_skill_bundle

## Feedback Participation

| 항목 | 값 |
|---|---|
| status | pending |
| set_at | — |

`connect` turn 끝에 `enabled` 또는 `disabled`로 기록한다.

## Installed Bundles

| 번들 | 상태 | Rule | Skill / Agent | 메모 |
|---|---|---|---|---|
| Bundle Catalog | active | bundle-catalog.mdc | audit-installed-bundles, manage-agent-bundles, report-bundle-feedback | gate |

## Feedback Log

| date | action | note |
|---|---|---|
```

### 3. 설치 상태 조사

`audit-installed-bundles` Skill 절차를 실행한다.

- `.cursor/`, 필요한 `docs/`, 로컬 catalog, 소스 catalog를 읽는다
- 번들별 `installed` / `partial` / `missing` / `catalog-only` / `files-only` 상태를 만든다
- gate 다음 단계 제안을 받는다

조사 결과를 사용자에게 보여 준다. `audit` 요청이면 여기서 종료한다.

### 4. gate: 설치할 번들 선택

**`connect` 또는 `add` 요청일 때만** 실행한다.

- `connect`: 조사 결과를 보여 준 뒤, 이번 turn 안에서 한 번만 추가 설치할 번들을 묻는다.
- `add`: 요청에 번들이 지정되어 있으면 바로 해당 번들 설치 절차로 가고, 없을 때만 짧게 확인한다.
- 사용자가 “추가하지 않음”, “gate만 유지”, “여기까지” 등으로 끝내면 설치하지 않고 종료한다.

질문에는 이미 설치된 번들, 부분 설치·불일치, 아직 설치되지 않은 후보를 짧게 포함한다.

사용자가 고른 번들만 다음 단계로 넘긴다.

### 5. 선택된 번들 설치

설치 전에 소스 catalog에서 해당 번들의 **유형과 원본 경로**를 확인한다.

#### 공방 키트 번들

```text
workshop-kit/rules/<rule>.mdc
  → .cursor/rules/<rule>.mdc

workshop-kit/skills/<skill>/SKILL.md
  → .cursor/skills/<skill>/SKILL.md
```

#### 정식 번들 (`bundles/`)

정식 번들은 bundle 내부의 Cursor 배포본을 기준으로 설치한다.

```text
bundles/<bundle>/cursor/.cursor/rules/*
  → .cursor/rules/*

bundles/<bundle>/cursor/.cursor/skills/*
  → .cursor/skills/*

bundles/<bundle>/cursor/.cursor/agents/*
  → .cursor/agents/*

bundles/<bundle>/cursor/.cursor/memory/*
  → .cursor/memory/*

bundles/<bundle>/cursor/.cursor/state/*
  → .cursor/state/*
```

bundle에 공통 `docs/`가 있고 실행 시 필요하면:

```text
bundles/<bundle>/docs/*
  → docs/*
```

**정식 번들 설치 보존 규칙**

- 같은 이름의 Rule·Skill·Agent가 이미 있으면 무조건 덮어쓰지 않는다. diff/차이를 요약하고 확인 후 처리한다.
- `.cursor/memory/`에서 source에 없는 프로젝트 전용 교훈 파일은 유지한다.
- `.cursor/state/loop-status.md` 같은 runtime state는 유지한다.
- source의 README/example/template은 필요한 경우만 갱신한다.
- bundle의 `README.md`, `LICENSE`, `.gitignore`, `.gitattributes` 같은 source metadata는 소비 프로젝트 루트로 설치하지 않는다.
- source에서 `alwaysApply: false`인 opt-in Rule은 사용자가 별도로 요청하지 않는 한 그대로 유지한다.

**Agent Thinking Guidelines**의 경우 `docs/agent-thinking-guidelines.md`가 호출 SSOT이므로 `docs/`도 함께 확인·설치한다.

**Core User Rule**은 Rule 복사본을 bundle repo에 두지 않는다. Skill은 일반 정식 번들 매핑을 따르고, Rule은 설치·업데이트 시 `core/user-rule/user_rule.md`를 읽어 `.cursor/rules/user-rule.mdc`로 변환 생성한다.

```text
bundles/core-user-rule/cursor/.cursor/skills/pull-request/
  → .cursor/skills/pull-request/

core/user-rule/user_rule.md
  → .cursor/rules/user-rule.mdc
```

변환 규칙:

- frontmatter: `description` (일상 Cursor/agent 작업 원칙), `globs: "**/*"`, `alwaysApply: true`
- body: `user_rule.md` 본문 전체 유지
- 기존 `.cursor/rules/user-rule.mdc`가 있으면 diff 후 사용자 확인 후 갱신

#### 예시 번들

```text
examples/<bundle-name>/rules/<rule>.mdc
  → .cursor/rules/<rule>.mdc

examples/<bundle-name>/skills/<skill>/SKILL.md
  → .cursor/skills/<skill>/SKILL.md
```

예시 번들 Rule은 기본적으로 `alwaysApply: false`를 유지한다.

설치·삭제·업데이트 후 로컬 catalog를 갱신한다.

### 6. 업데이트

업데이트는 설치와 동일한 원본 매핑을 사용하되, source와 local을 먼저 비교한다.

- source에 있는 관리 대상 파일만 갱신 후보로 본다.
- 소비 프로젝트 전용 파일은 보존한다.
- 같은 이름 파일이 local에서 수정됐으면 변경 내용을 보여주고 확인한다.
- 정식 번들의 memory/state runtime 파일은 덮어쓰지 않는다.
- 업데이트 후 `audit-installed-bundles`로 다시 확인한다.

### 7. 피드백 참여 설정 (`connect`만)

`Feedback Participation`이 `pending`이거나 없을 때 한 번 묻는다.

```text
Agent Skill Bundle 개선에 참여하시겠습니까?

작업을 마치거나 Skill을 사용한 PR을 작성했을 때,
Rule·Skill에 추가·개선하면 좋겠다는 제안이 있으면 Issue로 보낼지 물어볼 수 있습니다.
보내기 전에는 Issue 초안을 보여 드리고, 정말 보낼지 다시 확인합니다.

- 예 → enabled
- 아니오 → disabled (이후 피드백 전송을 묻지 않음)
```

선택 결과를 `.cursor/agent-bundles/catalog.md`에 기록한다. 이미 `enabled`/`disabled`이면 다시 묻지 않는다.

### 8. 재조사와 요약

변경이 있었다면 `audit-installed-bundles` Skill을 다시 실행한다.

```md
## 번들 관리 결과

### Gate 상태
- Bundle Catalog: installed | partial | missing

### 조사 결과
- ...

### 이번에 설치·변경한 번들
- ...

### 추가 설치
- 사용자가 다시 요청할 때만 gate를 통해 진행
```

연결 turn을 마칠 때 미설치 후보 목록을 반복해 설치를 재촉하지 않는다.

## 번들 소스 저장소 내부

`workshop-kit/catalog.md`가 있는 저장소에서는 다음 위치를 구분한다.

- `workshop-kit/` — 관리 도구 SSOT
- `bundles/` — 정식 bundle SSOT
- `examples/` — 실험 bundle source
- 루트 `.cursor/` — 이 monorepo에서 활성화된 관리 도구 복사본

`workshop-kit/`의 관리 Rule·Skill을 수정했다면 루트 `.cursor/`의 해당 활성 복사본도 동기화한다.

`bundles/<bundle>/cursor/.cursor/`를 루트 `.cursor/`와 자동으로 합치지 않는다. 전자는 소비 프로젝트 배포 source다.

## 완료 조건

- Bundle Catalog gate가 `installed` 상태다.
- 요청 유형 범위를 벗어나지 않았다.
- `connect`/`add` turn에서만 설치 질문을 했다.
- 정식 번들의 Rule·Skill·Agent·필수 docs가 필요한 범위에서 모두 확인되었다.
- 프로젝트 전용 memory/state/custom 파일을 무단 덮어쓰지 않았다.
- `connect` turn에서 피드백 참여 상태가 기록되었다.
- 재조사 후 로컬 catalog와 실제 파일 상태가 일치한다.

피드백 전송은 `report-bundle-feedback` Skill을 따른다.

## 기본 요청 예시

```text
지금 작업 중인 이 저장소에 Agent Skill Bundle을 연결해줘.
번들 소스: https://github.com/geunsu-son/agent_skill_bundle

1. Bundle Catalog gate를 먼저 설치하거나 보완하고
2. audit-installed-bundles로 현재 설치 상태를 조사한 뒤
3. 어떤 번들을 추가로 설치할지 나에게 물어봐
```
