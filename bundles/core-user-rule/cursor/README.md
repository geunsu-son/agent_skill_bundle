# Core User Rule — Cursor 배포본

이 디렉터리는 소비 프로젝트 `.cursor/`에 설치할 Cursor artifact만 담습니다.

## 설치 매핑

```text
bundles/core-user-rule/cursor/.cursor/skills/pull-request/
  → .cursor/skills/pull-request/

core/user-rule/user_rule.md   (번들 source의 core/, 설치 시 읽기)
  → .cursor/rules/user-rule.mdc
```

일반 작업용 원칙은 [Ponytail](https://github.com/DietrichGebert/ponytail)의
최소 구현 기준과 [i-have-adhd](https://github.com/ayghri/i-have-adhd)의
실행 가능한 응답 형식에서 영감을 받았습니다. 이를 이 번들의 기존 user rule과
연결된 선택형 Skill로 재구성했습니다.

Rule은 이 폴더에 복사본을 두지 않습니다. `manage-agent-bundles`가 설치 시 SSOT에서 생성합니다.

## 설치 후 확인

- `.cursor/skills/pull-request/SKILL.md` 존재
- `.cursor/skills/minimal-implementation/SKILL.md` 존재
- `.cursor/skills/actionable-response/SKILL.md` 존재
- `.cursor/rules/user-rule.mdc` 존재, §9가 `pull-request` skill을 참조
- 로컬 catalog에 Core User Rule이 `active`로 기록됨
