# PR 작성 규칙

## 문제

PR을 요청할 때 형식을 명시하지 않으면 Agent가 제목 한 줄·빈 본문으로 PR을 열고, 형식을 주면 Summary / Changes / Testing 등이 채워진 결과가 나온다. 같은 작업인데 요청 방식에 따라 결과물 품질이 달라진다.

## 가설

- **Rule** (`core/user-rule/user_rule.md` §9): PR 요청 시 항상 적용할 선언적 원칙
- **Skill** (`.cursor/skills/pull-request/SKILL.md`): 절차·Template·실행 메모

## 작은 실험

- `user_rule.md`에 §9 추가
- `pull-request` Skill 초안 추가
- 다음 PR부터 형식 없이 "PR 만들어줘"만 요청해 본문이 채워지는지 관찰

## 관찰

(아직 없음)

## 다음 작업

- 2~3회 사용 후 Template·섹션 생략 기준이 맞는지 확인
- 필요하면 `workshop-kit/` 또는 소비 프로젝트용 설치 경로 정리
