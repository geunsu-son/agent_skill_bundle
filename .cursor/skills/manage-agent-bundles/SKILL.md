---
name: manage-agent-bundles
description: 작업 중인 저장소에 Agent Skill Bundle을 연결하고, gate를 통해 번들 설치·업데이트·삭제·보관을 관리하는 절차
---

# Manage Agent Bundles

## 사용 시점

- 작업 중인 저장소에 Agent Skill Bundle을 처음 연결할 때
- gate를 통해 다음 번들을 가져올지 선택할 때
- 설치된 번들을 업데이트·삭제·점검할 때

## 기본값

- **번들 소스**: `https://github.com/geunsu-son/agent_skill_bundle`
- **소스 catalog**: `workshop-kit/catalog.md`
- **로컬 catalog**: `.cursor/agent-bundles/catalog.md`

번들 소스 저장소를 clone하지 않는다. 필요한 파일만 가져온다.

## 절차

### 1. 요청과 범위 확인

다음을 먼저 확인한다.

- 작업: 첫 연결, gate 선택, 업데이트, 삭제, 점검 중 무엇인가
- 현재 저장소가 번들 소스 저장소인지, 다른 프로젝트인지
- 사용자가 이미 선택한 번들 또는 Agent 작업 목적

이미 제공된 정보는 다시 묻지 않는다.

### 2. 저장소 유형 판별

- `workshop-kit/catalog.md`가 있으면 **번들 소스 저장소**다. 원본 편집과 `.cursor/` 동기화를 수행한다.
- 없으면 **소비 프로젝트**다. 번들 소스에서 필요한 파일만 `.cursor/`로 가져온다.

### 3. 첫 연결 (소비 프로젝트)

현재 작업 중인 저장소에 Agent Skill Bundle을 처음 연결할 때는 **Bundle Catalog 번들만** 설치한다.

1. `.cursor/rules/`, `.cursor/skills/`, `.cursor/agent-bundles/` 디렉터리를 준비한다.
2. 번들 소스에서 아래 파일만 가져와 `.cursor/`에 둔다.
   - `workshop-kit/rules/bundle-catalog.mdc` → `.cursor/rules/bundle-catalog.mdc`
   - `workshop-kit/skills/manage-agent-bundles/SKILL.md` → `.cursor/skills/manage-agent-bundles/SKILL.md`
3. `.cursor/agent-bundles/catalog.md`를 만든다.

```md
# Local Agent Bundle Catalog

## Bundle Source

https://github.com/geunsu-son/agent_skill_bundle

## Installed Bundles

| 번들 | 상태 | Rule | Skill | 메모 |
|---|---|---|---|---|
| Bundle Catalog | active | bundle-catalog.mdc | manage-agent-bundles | gate |

## Last Action

- YYYY-MM-DD: Bundle Catalog gate 설치
```

4. 다른 번들은 아직 설치하지 않는다.
5. gate 절차로 넘긴다.

파일 가져오기 예시:

```bash
SOURCE=https://github.com/geunsu-son/agent_skill_bundle
REF=main
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/rules/bundle-catalog.mdc" -o .cursor/rules/bundle-catalog.mdc
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/skills/manage-agent-bundles/SKILL.md" -o .cursor/skills/manage-agent-bundles/SKILL.md
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/catalog.md" -o /tmp/agent-skill-bundle-source-catalog.md
```

### 4. gate: 다음 번들 선택

Bundle Catalog가 활성화된 뒤, 추가 번들은 gate를 통해서만 설치한다.

1. 번들 소스의 `workshop-kit/catalog.md`를 읽는다.
2. 로컬 catalog의 설치 목록과 비교한다.
3. 아직 설치되지 않은 번들 후보를 표로 정리한다.
   - 번들 이름
   - 유형(공방 키트 / 예시)
   - Agent 작업 목적 한 줄
   - 포함 Rule·Skill
4. 사용자에게 어떤 번들이 필요한지 짧게 묻거나, 이미 말한 목적에 맞는 후보를 추천한다.
5. 사용자가 고른 번들만 설치한다. 고르지 않은 번들은 설치하지 않는다.

gate 질문 예시:

```text
지금 저장소에서 어떤 Agent 작업을 맡기려 하나요?
아래 후보 중 필요한 번들만 골라주세요.

1. Agent Skill Workshop — 아이디어를 번들로 구현
2. Session Market Briefing — 세션 경제 브리핑
3. Web Crawler Craft — 웹 크롤러 제작
4. 지금은 gate만 유지
```

### 5. 선택된 번들 설치

사용자가 고른 번들만 번들 소스에서 가져와 `.cursor/`에 둔다.

#### 공방 키트 번들

```text
workshop-kit/rules/<rule>.mdc        → .cursor/rules/<rule>.mdc
workshop-kit/skills/<skill>/SKILL.md → .cursor/skills/<skill>/SKILL.md
```

#### 예시 번들

```text
examples/<bundle-name>/rules/<rule>.mdc        → .cursor/rules/<rule>.mdc
examples/<bundle-name>/skills/<skill>/SKILL.md → .cursor/skills/<skill>/SKILL.md
```

예시 번들 Rule은 기본적으로 `alwaysApply: false`를 유지한다.

설치 후 로컬 catalog에 번들, Rule, Skill, 상태, 설치일을 추가한다.

### 6. 번들 소스 저장소 동기화

번들 소스 저장소 내부에서는 clone 대신 아래 경로를 사용한다.

- 원본: `workshop-kit/`, `examples/`
- 실행본: `.cursor/`
- catalog: `workshop-kit/catalog.md`

공방 키트 번들은 원본과 `.cursor/`를 함께 수정한다. 예시 번들은 기본적으로 `.cursor/`에 설치하지 않는다.

### 7. 업데이트·삭제·점검

- **update**: 로컬 catalog에 active인 번들만 번들 소스에서 다시 가져온다.
- **remove**: `.cursor/`에서 제거하고 로컬 catalog 상태를 `archived`로 바꾼다.
- **audit**: 로컬 catalog, `.cursor/`, 번들 소스 catalog를 비교해 누락·중복·충돌을 찾는다.

### 8. 결과 요약

```md
## 번들 관리 결과

### Gate 상태
- Bundle Catalog: active / not installed

### 활성 번들
- ...

### 이번에 설치·변경한 번들
- ...

### gate 후보 (아직 미설치)
- ...

### 다음 선택
- ...
```

## 완료 조건

- 첫 연결: Bundle Catalog와 로컬 catalog만 준비되어 있다.
- gate 이후: 사용자가 고른 번들만 `.cursor/`에 반영되어 있다.
- 로컬 catalog와 `.cursor/` 상태가 일치한다.
- 다음 gate 후보가 요약되어 있다.

## 기본 요청 예시

첫 연결:

```text
지금 작업 중인 이 저장소에 Agent Skill Bundle을 연결해줘.
번들 소스: https://github.com/geunsu-son/agent_skill_bundle

먼저 Bundle Catalog gate만 .cursor/에 설치하고,
다음에 가져올 번들 후보를 설명한 뒤 내 선택을 받아줘.
```

gate 이후:

```text
Agent Skill Bundle gate를 통해
Agent Skill Workshop 번들만 추가로 설치해줘.
```
