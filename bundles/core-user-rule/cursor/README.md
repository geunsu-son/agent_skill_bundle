# Core User Rule — Cursor 배포본

이 디렉터리는 소비 프로젝트 `.cursor/`에 설치할 Cursor artifact만 담습니다.

## 설치 매핑

```text
bundles/core-user-rule/cursor/.cursor/skills/pull-request/
  → .cursor/skills/pull-request/

core/user-rule/user_rule.md   (번들 source의 core/, 설치 시 읽기)
  → .cursor/rules/user-rule.mdc
```

Rule은 이 폴더에 복사본을 두지 않습니다. `manage-agent-bundles`가 설치 시 SSOT에서 생성합니다.

## 설치 후 확인

- `.cursor/skills/pull-request/SKILL.md` 존재
- `.cursor/rules/user-rule.mdc` 존재, §9가 `pull-request` skill을 참조
- 로컬 catalog에 Core User Rule이 `active`로 기록됨
