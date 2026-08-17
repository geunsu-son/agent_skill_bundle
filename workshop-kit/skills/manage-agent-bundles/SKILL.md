---
name: manage-agent-bundles
description: 에이전트 번들의 설치·업데이트·삭제·보관을 판단하고, catalog와 .cursor/ 상태를 일치시키는 절차
---

# Manage Agent Bundles

## 사용 시점

다음과 같은 요청에 사용한다.

- 어떤 rule-skill 세트를 설치·삭제·업데이트할지 정리할 때
- `.cursor/`와 `workshop-kit/` 또는 `examples/` 상태를 맞출 때
- 새 번들을 추가한 뒤 카탈로그를 갱신할 때
- 오래된 번들을 보관하거나 대체할 때

## 목표

저장소에 있는 **에이전트 번들** 중 무엇을 활성화하고, 무엇을 제거하고, 무엇을 최신으로 맞출지 판단한 뒤, `workshop-kit/catalog.md`와 `.cursor/`를 일치시킨다.

## 절차

### 1. 요청과 범위 확인

다음을 먼저 확인한다.

- 사용자가 원하는 작업: 설치, 업데이트, 삭제, 전체 점검 중 무엇인가
- 대상 번들 이름 또는 Agent 작업 목적
- 이 저장소를 다루는 공방 작업인지, 특정 업무 예시를 쓰는 것인지

이미 제공된 정보는 다시 묻지 않는다.

### 2. 현재 목록 수집

다음 위치를 확인한다.

- `workshop-kit/catalog.md` — 등록된 번들과 상태
- `workshop-kit/rules/`, `workshop-kit/skills/` — 공방 키트 번들 원본
- `examples/*/` — 예시 번들 원본
- `.cursor/rules/`, `.cursor/skills/` — 현재 활성 번들

각 번들에 대해 Rule, Skill, Script, Automation 경로와 README 상태(`draft`, `testing`, `reusable`, `archived`)를 적는다.

### 3. 중복과 충돌 검사

- 같은 Agent 작업 목적을 가진 활성 번들이 두 개 이상인지 확인한다.
- Rule의 `alwaysApply: true`가 겹치거나 상충하는지 확인한다.
- 예시 번들과 공방 키트 번들의 역할이 섞이지 않았는지 확인한다.

충돌이 있으면 유지할 번들 하나를 정하고, 대체 또는 보관 대상을 명시한다.

### 4. 작업 판단

`bundle-catalog` Rule의 기준에 따라 각 번들에 대해 다음 중 하나를 정한다.

- **install**: `.cursor/`에 복사
- **update**: 원본에서 `.cursor/`로 반영
- **remove**: `.cursor/`에서 제거
- **keep**: 현재 상태 유지
- **archive**: 상태를 `archived`로 바꾸고 `.cursor/`에서 제거

판단 이유를 한 줄씩 남긴다.

### 5. 파일 반영

#### 공방 키트 번들

원본은 `workshop-kit/`에, 실행본은 `.cursor/`에 둔다.

```text
workshop-kit/rules/<rule>.mdc        → .cursor/rules/<rule>.mdc
workshop-kit/skills/<skill>/SKILL.md → .cursor/skills/<skill>/SKILL.md
```

#### 예시 번들

사용자가 명시적으로 요청한 경우에만 설치한다.

```text
examples/<bundle-name>/rules/<rule>.mdc        → .cursor/rules/<rule>.mdc
examples/<bundle-name>/skills/<skill>/SKILL.md → .cursor/skills/<skill>/SKILL.md
```

예시 번들의 Rule은 기본적으로 `alwaysApply: false`를 유지한다.

#### 삭제

- `.cursor/`에서 해당 Rule·Skill 파일 또는 디렉터리를 제거한다.
- 원본은 `archived`가 아니면 삭제하지 않는다.

### 6. 카탈로그 갱신

`workshop-kit/catalog.md`를 다음 기준으로 수정한다.

- 번들 이름, 유형(공방 키트 / 예시), 상태, 원본 경로
- 활성 여부(`.cursor/` 설치 여부)
- 마지막 관리 작업과 한 줄 메모

새 번들을 추가했다면 카탈로그에 등록한다.

### 7. README 연결

필요하면 다음을 갱신한다.

- 루트 `README.md`의 주요 파일 목록
- `workshop-kit/README.md`의 구성 목록
- 해당 번들 README의 상태

### 8. 결과 요약

다음 형식으로 마무리한다.

```md
## 번들 관리 결과

### 활성 번들
- ...

### 변경 사항
- install / update / remove / archive 항목과 이유

### 유지한 번들
- ...

### 다음 검증
- ...
```

## 완료 조건

- 요청한 설치·업데이트·삭제·점검이 반영되었다.
- `workshop-kit/catalog.md`가 실제 `.cursor/` 상태와 일치한다.
- 중복 활성 번들이 없다.
- 변경 이유와 다음 검증 항목이 남아 있다.

## 기본 요청 예시

```text
이 저장소의 에이전트 번들을 점검하고,
bundle-catalog 규칙에 맞춰 설치·업데이트·삭제가 필요한 항목을 정리해줘.
catalog와 .cursor/ 상태를 맞춘 뒤, 무엇을 바꿨는지 요약해줘.
```
