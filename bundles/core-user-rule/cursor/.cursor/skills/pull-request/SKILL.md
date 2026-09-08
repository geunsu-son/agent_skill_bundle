---
name: pull-request
description: Pull Request 제목·본문 작성 및 생성. PR을 만들거나, PR 본문을 고쳐 달라고 하거나, create pull request / open PR 요청을 받으면 반드시 사용한다.
---

# Pull Request 작성

## 사용 시점

- PR 생성·업데이트를 요청받았을 때
- 작업 완료 후 PR을 열어야 할 때
- PR 제목·본문을 다시 작성해 달라고 할 때

Core User Rule 번들이 설치된 프로젝트에서는 `.cursor/rules/user-rule.mdc` §9의 선언적 원칙을 지키고, 이 Skill은 실행 순서·형식·검증을 담당한다.

## 절차

PR을 생성·업데이트하기 전에 다음 순서로 확인한다.

1. 현재 브랜치를 확인한다.
2. 변경된 파일과 커밋 내역을 확인한다.
3. 이미 동일 브랜치로 생성된 PR이 있는지 확인한다.
4. 저장소에 PR Template이 있는지 확인한다.
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `.github/PULL_REQUEST_TEMPLATE/*.md`
   - 저장소 루트 `PULL_REQUEST_TEMPLATE.md`
5. base branch와 비교하여 전체 변경사항(diff)을 확인한다.
6. 변경사항을 기반으로 PR 제목과 본문을 작성한다.
7. 필요한 경우 remote에 push한다.
8. PR을 생성하거나 기존 PR을 업데이트한다.
9. PR 생성·업데이트 후 CI / 테스트 결과를 확인한다.

## PR 제목

가능하면 Conventional Commit 형식을 사용한다.

형식:

```
<type>: <description>
```

예시:

- feat: add user authentication
- fix: handle API timeout
- refactor: simplify data processing
- docs: update README

scope가 명확한 경우:

```
<type>(<scope>): <description>
```

예시:

- feat(auth): add Google login
- fix(api): handle timeout errors

PR 제목은 변경사항 전체를 대표할 수 있도록 짧고 명확하게 작성한다.

## PR 본문

저장소에 PR Template이 있으면 **반드시** 해당 Template을 우선해서 사용한다.

PR Template이 없는 경우 다음 형식을 기본으로 사용한다.

```markdown
## Summary

이번 PR에서 무엇을 변경했는지와 변경한 이유를 1~2문장으로 요약한다.

## Changes

주요 변경사항을 bullet 형태로 작성한다.

- 변경사항 1
- 변경사항 2
- 변경사항 3

## Files Changed

필요한 경우 주요 변경 파일을 정리한다.

- Added: 새로 추가된 파일
- Modified: 수정된 파일
- Deleted: 삭제된 파일

단순한 PR이라면 이 섹션은 생략할 수 있다.

## Testing

변경사항을 어떻게 검증했는지 작성한다.

예시:

- [x] Unit tests passed
- [x] Manual verification completed
- [x] Lint passed

실제로 수행하지 않은 테스트는 수행했다고 작성하지 않는다.
CI가 없으면 "자동 CI 없음"과 실제로 수행한 수동 확인 항목만 적는다.

## Related Issues

관련 Issue가 있다면 연결한다.

예시:

Closes #123

관련 Issue가 없다면 해당 섹션은 생략한다.
```

## 작성 원칙

- PR 내용은 작업 요청(prompt)이 아니라 **실제 diff**를 기준으로 작성한다.
- 변경하지 않은 내용을 PR 본문에 포함하지 않는다.
- 변경사항을 과장하지 않는다.
- 구현 세부사항을 불필요하게 길게 설명하지 않는다.
- 리뷰어가 "무엇이 바뀌었고 왜 바뀌었는지" 빠르게 이해할 수 있도록 작성한다.
- UI 변경이 있는 경우 필요한 경우 스크린샷을 포함한다.
- 서로 관련 없는 변경사항이 하나의 PR에 섞여 있다면 PR을 분리하는 것을 고려한다.
- 변경 파일이 지나치게 많거나 PR의 목적이 여러 개인 경우 PR 분리를 제안한다.

## 실행 메모

- **Cloud Agent**: `ManagePullRequest` 도구로 생성·업데이트한다. `gh` CLI로 PR을 만들지 않는다.
- **로컬 Agent**: `gh pr create` / `gh pr edit` 또는 GitHub API를 사용할 수 있다. `gh`가 없으면 설치하거나 API로 생성한다.
- 인증은 사용자 자격증명/`GH_TOKEN`을 쓰되, 토큰·비밀번호를 출력·커밋하지 않는다.
- base branch는 저장소 기본 branch(보통 `main`)를 따른다.

## 완료 조건

- PR 제목이 Conventional Commits 형식을 따른다.
- PR 본문이 Template(또는 기본 형식)을 채우고, diff와 일치한다.
- 수행하지 않은 검증을 완료했다고 표시하지 않았다.
- 동일 브랜치에 중복 PR이 없거나, 기존 PR이 올바르게 업데이트되었다.
