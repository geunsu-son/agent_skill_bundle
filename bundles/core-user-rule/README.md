# Core User Rule

일상적인 Cursor/AI coding 작업의 **기본 행동 원칙**과 **PR 작성 절차**를 프로젝트에 선택 설치하는 정식 번들입니다.

## SSOT (중복 저장 없음)

| 구성요소 | SSOT | 프로젝트 설치본 |
|---|---|---|
| 기본 원칙 전문 | `core/user-rule/user_rule.md` | `.cursor/rules/user-rule.mdc` (설치 시 생성) |
| PR 작성 절차 | `bundles/core-user-rule/cursor/.cursor/skills/pull-request/` | `.cursor/skills/pull-request/` |

`user_rule` 원문은 `core/`에만 두고, 번들 repo 안에 `.mdc` 복사본을 상시 보관하지 않습니다. Bundle Catalog gate가 설치할 때 `core/user-rule/user_rule.md`를 읽어 `.mdc`로 변환해 복사합니다.

전역 Cursor **User Rules**에도 같은 원칙을 쓰려면 `core/user-rule/user_rule.md`를 수동으로 붙여 넣습니다. 프로젝트 Rule과 User Rules를 동시에 켜면 중복 적용될 수 있으므로 한쪽만 쓰는 것을 권장합니다.

## 구성

```text
core-user-rule/
├── README.md
└── cursor/
    ├── README.md
    └── .cursor/
        └── skills/
            └── pull-request/
```

Rule 파일은 `cursor/.cursor/rules/`에 두지 않습니다.

## 설치

Bundle Catalog gate를 통해 **선택 설치**합니다. connect turn에서 "Core User Rule"을 고르면:

1. `pull-request` Skill → `.cursor/skills/pull-request/`
2. `core/user-rule/user_rule.md` → `.cursor/rules/user-rule.mdc` (frontmatter 추가·변환)

자세한 매핑은 [`workshop-kit/catalog.md`](../../workshop-kit/catalog.md)와 `manage-agent-bundles` Skill의 **Core User Rule** 절을 봅니다.

## 기본 적용 모드

- `user-rule.mdc`: `alwaysApply: true` (프로젝트 기본 원칙)
- `pull-request` Skill: PR 생성·수정 요청 시 사용

## 관련 문서

- 배경·변경 관리: [`core/user-rule/README.md`](../../core/user-rule/README.md)
- PR skill SSOT (이 번들 배포본): [`cursor/.cursor/skills/pull-request/SKILL.md`](cursor/.cursor/skills/pull-request/SKILL.md)

## 상태

`draft` — catalog 등록 초안. Bundle Catalog connect에서 선택 설치 가능.
