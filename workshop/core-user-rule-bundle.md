# Core User Rule 번들

## 문제

`user_rule`과 `pull-request` skill이 번들 catalog 밖에 있어 connect 시 선택 설치되지 않음. SSOT를 `core/`와 `bundles/`에 중복 두고 싶지 않음.

## 가설

- `core/user-rule/user_rule.md`만 SSOT
- `bundles/core-user-rule/`에는 `pull-request` skill 배포본만
- Rule은 설치 시 `core/`에서 읽어 `.cursor/rules/user-rule.mdc` 생성
- catalog + `manage-agent-bundles`에 예외 경로 명시

## 초안

- `bundles/core-user-rule/` README·cursor README·pull-request skill
- `workshop-kit/catalog.md` 등록 (`draft`)
- `manage-agent-bundles` Core User Rule 절

## 다음 작업

- connect turn에서 실제 설치·변환 동작 관찰
- `audit-installed-bundles`가 `user-rule.mdc` (생성본) 인식하는지 확인
- 안정화 후 catalog 상태 `stable` 승격 검토
