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

번들 소스 저장소를 clone하지 않는다. 필요한 파일만 가져온다.

## 절차

### 1. 요청과 범위 확인

- 작업: 연결·점검, gate 보완, 추가 설치, 업데이트, 삭제 중 무엇인가
- 번들 소스 URL
- 사용자가 이미 선택한 번들 또는 Agent 작업 목적

이미 제공된 정보는 다시 묻지 않는다.

### 2. Bundle Catalog gate 보완

gate가 `missing` 또는 `partial`이면 아래 Bundle Catalog 번들 파일을 번들 소스에서 가져와 `.cursor/`에 둔다.

- `workshop-kit/rules/bundle-catalog.mdc` → `.cursor/rules/bundle-catalog.mdc`
- `workshop-kit/skills/audit-installed-bundles/SKILL.md` → `.cursor/skills/audit-installed-bundles/SKILL.md`
- `workshop-kit/skills/manage-agent-bundles/SKILL.md` → `.cursor/skills/manage-agent-bundles/SKILL.md`

로컬 catalog가 없으면 만든다. gate 보완만으로 다른 번들은 아직 설치하지 않는다.

파일 가져오기 예시:

```bash
SOURCE=https://github.com/geunsu-son/agent_skill_bundle
REF=main
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/rules/bundle-catalog.mdc" -o .cursor/rules/bundle-catalog.mdc
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/skills/audit-installed-bundles/SKILL.md" -o .cursor/skills/audit-installed-bundles/SKILL.md
curl -fsSL "$SOURCE/raw/$REF/workshop-kit/skills/manage-agent-bundles/SKILL.md" -o .cursor/skills/manage-agent-bundles/SKILL.md
```

### 3. 설치 상태 조사

`audit-installed-bundles` Skill 절차를 실행한다.

- `.cursor/`와 로컬 catalog, 소스 catalog를 읽는다
- 번들별 `installed` / `partial` / `missing` / `catalog-only` / `files-only` 상태를 만든다
- gate 다음 단계 제안을 받는다

조사 결과를 사용자에게 먼저 보여 준다.

### 4. gate: 설치할 번들 선택

조사 결과를 바탕으로 사용자에게 질문한다.

- 이미 설치된 번들
- 불일치·부분 설치가 있으면 정리 필요 여부
- 아직 설치되지 않은 후보

```text
현재 설치 상태를 확인했습니다.

[설치됨]
- ...

[미설치 후보]
1. Agent Skill Workshop — 아이디어를 번들로 구현
2. Session Market Briefing — 세션 경제 브리핑
3. Web Crawler Craft — 웹 크롤러 제작
4. 지금은 추가 설치하지 않음

어떤 번들을 설치할까요?
```

사용자가 고른 번들만 다음 단계로 넘긴다.

### 5. 선택된 번들 설치

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

설치·삭제·업데이트 후 로컬 catalog를 갱신한다.

### 6. 재조사와 요약

변경이 있었다면 `audit-installed-bundles` Skill을 다시 실행한다.

```md
## 번들 관리 결과

### Gate 상태
- Bundle Catalog: installed | partial | missing

### 조사 결과
- ...

### 이번에 설치·변경한 번들
- ...

### gate 후보 (아직 미설치)
- ...
```

## 번들 소스 저장소 내부

`workshop-kit/catalog.md`가 있는 저장소에서는 원본 편집과 `.cursor/` 동기화를 수행한다. 연결 흐름은 동일하게 **gate 보완 → 조사 → 선택 → 설치**다.

## 완료 조건

- Bundle Catalog gate가 `installed` 상태다.
- `audit-installed-bundles` 결과를 사용자에게 공유했다.
- 사용자가 고른 번들만 `.cursor/`에 반영되었다.
- 재조사 후 로컬 catalog와 `.cursor/` 상태가 일치한다.

## 기본 요청 예시

```text
지금 작업 중인 이 저장소에 Agent Skill Bundle을 연결해줘.
번들 소스: https://github.com/geunsu-son/agent_skill_bundle

1. Bundle Catalog gate를 먼저 설치하거나 보완하고
2. audit-installed-bundles로 현재 설치 상태를 조사한 뒤
3. 어떤 번들을 추가로 설치할지 나에게 물어봐
```
