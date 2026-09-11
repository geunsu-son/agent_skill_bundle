# Agent Bundle Catalog

이 파일은 **번들 소스 저장소**에 등록된 에이전트 번들의 원본 위치, 상태, 설치 구성요소를 기록한다.

**현재 공식 target은 Cursor다.** Bundle Catalog gate와 이 catalog가 정의하는 설치 artifact는 소비 프로젝트의 `.cursor/` 구조를 기준으로 한다. 공통 `docs/`는 플랫폼 중립적인 원칙 문서로 유지할 수 있지만, 다른 AI coding platform용 실행 artifact는 현재 관리하지 않는다.

다른 저장소에서 Agent Skill Bundle을 쓸 때는 이 파일을 직접 복사하지 않는다. Bundle Catalog gate를 먼저 설치하고, `audit-installed-bundles` Skill로 설치 상태를 조사한 뒤 gate가 이 catalog를 참고해 필요한 번들을 선택한다.

## Bundle 유형

- **공방 키트**: 번들 자체를 만들고 관리하기 위한 meta bundle. 원본은 `workshop-kit/`.
- **정식 번들**: 반복 사용과 배포를 전제로 승격된 stable source. 원본은 `bundles/<bundle-name>/`.
- **예시 번들**: 특정 Agent 작업을 실제로 시험하는 draft/testing source. 원본은 `examples/<bundle-name>/`.

`core/`는 번들 catalog 대상이 아니다. 개인 기본 규칙처럼 번들보다 상위에서 항상 가까이 두는 최소 원칙을 보관한다.

## Bundle Catalog gate 구성

**Bundle Catalog는 하나의 번들**입니다. `bundle-catalog` Rule 아래 하위 Skill 세 개로 나뉩니다. Issue 피드백은 별도 번들이 아닙니다.

| 계층 | 이름 | 역할 |
|---|---|---|
| Rule | `bundle-catalog.mdc` | 총관리·gate·피드백 원칙 |
| 하위 Skill | `audit-installed-bundles` | 설치 상태 조사 |
| 하위 Skill | `manage-agent-bundles` | gate 설치, 번들 선택·변경, 피드백 참여 설정 |
| 하위 Skill | `report-bundle-feedback` | 사용 기록 Issue 초안·2차 gate·전송 |

## gate 흐름

```text
총괄 rule(Bundle Catalog gate) 선설치
→ audit-installed-bundles로 .cursor/ 설치 상태 조사
→ gate가 연결/add turn에서만 설치할 번들 질문
→ manage-agent-bundles로 선택한 번들만 설치
→ connect turn에서 피드백 참여(enabled/disabled) 설정
→ (enabled) 작업 완료·Skill 사용 PR 시 report-bundle-feedback
```

## 피드백 Issue (선택)

`enabled`일 때만 **작업 완료** 또는 **Skill 사용 PR 작성** 시 1차 gate → 초안 공개 → 2차 전송 승인 → Issue 생성. 본문 기본은 사용 기록이다.

## 등록 번들

| 번들 | 유형 | 상태 | 원본 | gate | Rule | Skill | Agent / 기타 | Agent 작업 목적 |
|---|---|---|---|---|---|---|---|---|
| Bundle Catalog | 공방 키트 | `draft` | `workshop-kit/` | 1 — 선설치 | `bundle-catalog.mdc` | `audit-installed-bundles`, `manage-agent-bundles`, `report-bundle-feedback` | — | gate — 조사·선택·사용 기록 Issue |
| Agent Skill Workshop | 공방 키트 | `draft` | `workshop-kit/` | 2 — 선택 | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | — | Agent 작업 아이디어를 번들로 구현 |
| **Agent Thinking Guidelines** | **정식 번들** | `stable` | `bundles/agent-thinking-guidelines/` | 3 — 선택 | `core-principles.mdc`, `worker-conduct.mdc`, `analysis-protocol.mdc`, `design-protocol.mdc` | `agent-thinking-guidelines`, `analysis-protocol`, `design-protocol` | `orchestrator`, `reviewer`, `docs/`, memory/state templates | 대규모·장기·다단계·고위험 작업의 사고·검증·review/orchestration |
| **Core User Rule** | **정식 번들** | `draft` | `bundles/core-user-rule/` | 3 — 선택 | `user-rule.mdc` (설치 시 `core/user-rule/user_rule.md`에서 생성) | `pull-request` | — | 일상 작업 기본 원칙 + PR 작성 절차 |
| Session Market Briefing | 예시 | `testing` | `examples/session-market-briefing/` | 3 — 선택 | `market-briefing.mdc` | `session-market-briefing` | — | 세션 경제 브리핑 |
| Web Crawler Craft | 예시 | `draft` | `examples/web-crawler-ver0/` | 3 — 선택 | `crawler-craft.mdc` | `web-crawler-craft` | — | 웹 크롤러 제작 |
| Domain Data Analysis | 예시 | `testing` | `examples/domain-data-analysis/` | 3 — 선택 | `domain-data-analysis.mdc` | `domain-data-analysis` | — | 도메인 기반 데이터 분석 설계·보고 |
| MCP Server Craft | 예시 | `testing` | `examples/mcp-server-craft-ver0/` | 3 — 선택 | `mcp-server-craft.mdc` | `mcp-server-craft`, `mcp-server-scope`, `mcp-server-auth`, `mcp-tool-implement`, `mcp-server-connect` | — | MCP 서버 설계·권한·구현·연결 |
| Blog Style Writing | 예시 | `draft` | `examples/blog-style-writing-ver0/` | 3 — 선택 | `blog-style-writing.mdc` | `blog-style-writing`, `collect-blog-corpus`, `build-style-context`, `write-blog-manuscript` | — | 기존 블로그 문체 팩 구축·초고·첨삭. 수집은 Web Crawler Craft에 의존 |
| Career Management | 예시 | `draft` | `examples/career-management-ver0/` | 3 — 선택 | `career-management.mdc` | `career-management-session`, `career-market-research`, `resume-strength-discovery`, `portfolio-hosting-choice`, `portfolio-design-research`, `portfolio-site-build`, `job-posting-fit`, `interview-story-crafting`, `profile-optimization`, `learning-path-planning`, `networking-outreach`, `compensation-research` | — | 커리어 상담·이력 강점 발굴·포트폴리오·지원/성장 지원 |

## Cursor 정식 번들 설치 규칙

`bundles/<bundle-name>/`는 bundle 전체 원본이다. Cursor 소비 프로젝트에는 해당 bundle의 `cursor/.cursor/`와 필요한 공통 docs만 설치한다.

예: Agent Thinking Guidelines

```text
bundles/agent-thinking-guidelines/cursor/.cursor/rules/*
  → .cursor/rules/*

bundles/agent-thinking-guidelines/cursor/.cursor/skills/*
  → .cursor/skills/*

bundles/agent-thinking-guidelines/cursor/.cursor/agents/*
  → .cursor/agents/*

bundles/agent-thinking-guidelines/cursor/.cursor/memory/*
  → .cursor/memory/*

bundles/agent-thinking-guidelines/cursor/.cursor/state/*
  → .cursor/state/*

bundles/agent-thinking-guidelines/docs/*
  → docs/*
```

프로젝트 전용 memory, runtime state, 같은 이름의 커스텀 파일은 무조건 덮어쓰지 않는다. 차이를 확인한 뒤 사용자가 선택한다.

### Core User Rule (정식 번들, SSOT 분리)

`user_rule` 원문은 `core/user-rule/user_rule.md`에만 둔다. 번들 repo 안에 `.mdc` 복사본을 상시 보관하지 않는다.

```text
bundles/core-user-rule/cursor/.cursor/skills/pull-request/
  → .cursor/skills/pull-request/

core/user-rule/user_rule.md
  → .cursor/rules/user-rule.mdc   (설치·업데이트 시 변환 생성)
```

`user_rule.md` → `user-rule.mdc` 변환:

- frontmatter 추가: `description`, `globs: "**/*"`, `alwaysApply: true`
- body: `user_rule.md` 본문 유지 (제목·섹션 번호 포함)
- §9는 `pull-request` skill 참조

업데이트 시 `core/user-rule/user_rule.md`와 기존 `.cursor/rules/user-rule.mdc`를 diff하고 사용자 확인 후 갱신한다.

다른 platform용 구현 경로를 추정하거나 자동 생성하지 않는다. 실제 지원 필요가 생기면 `docs/`를 기준으로 별도 target을 명시적으로 추가한다.

## 마지막 관리 기록

- 2026-09-08: Core User Rule 정식 번들 초안 등록 (`bundles/core-user-rule/`). `user_rule` SSOT는 `core/` 유지, Rule은 설치 시 `.mdc` 생성, `pull-request` skill만 cursor 배포본에 포함.
- 2026-09-08: 공식 target을 Cursor로 정리. Agent Thinking Guidelines의 Claude Code 배포본을 제거하고 Cursor 구현만 유지. 루트 README에 bundle 상태 목록을 노출하고 Career Management를 `draft`로 catalog에 등록.
- 2026-09-08: `my_cursor_user_rule`을 `core/user-rule/`, `agent-thinking-guidelines`를 `bundles/agent-thinking-guidelines/`로 통합. Agent Skill Bundle을 단일 SSOT로 정리하고 Agent Thinking Guidelines를 첫 정식 번들로 등록.
- 2026-08-27: #11. `report-bundle-feedback` 초안을 사용 기록 중심으로 바꿈. 소비 특수 규칙은 다른 예시 Skill에 넣지 않음.
- 2026-08-27: Blog Style Writing 예시 번들 등록. 실제 실험은 `blog_agnet`에서 하고 공방에는 관찰만 되돌림.
- 2026-08-27: `report-bundle-feedback` Skill 추가. connect 시 참여 설정, 2차 gate Issue 전송.
- 2026-08-26: MCP Server Craft 상태를 `testing`으로 두고 이 저장소 구현을 마감. 실제 제작 테스트는 추후. `.cursor/` 미승격.
- 2026-08-21: MCP Server Craft 인증 Skill을 `mcp-server-auth`로 바꿈. 참고 README 기준으로 호출자(GWS)·워크로드(IRSA) 분리. `.cursor/` 미승격.
- 2026-08-21: MCP Server Craft 예시 번들 등록. GWS/GCP 경로를 1순위로 둔 draft. `.cursor/` 미승격.
- 2026-08-17: Domain Data Analysis 예시 번들 등록. 케이스별 testing 파일은 예시에 두지 않음.
- 2026-08-17: `audit-installed-bundles` Skill 추가. gate 흐름을 선설치 → 조사 → 질문 → 설치로 정리.
