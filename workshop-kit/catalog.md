# Agent Bundle Catalog

이 파일은 **번들 소스 저장소**에 등록된 **에이전트 번들**의 원본 위치, 상태, `.cursor/` 활성 여부를 기록한다.

다른 저장소에서 Agent Skill Bundle을 쓸 때는 이 파일을 직접 복사하지 않는다. 대신 Bundle Catalog gate를 먼저 설치하고, gate가 이 catalog를 참고해 다음 번들을 선택한다. 소비 프로젝트에는 `.cursor/agent-bundles/catalog.md`를 둔다.

## 용어

| 용어 | 의미 |
|---|---|
| Agent 작업 아이디어 | Agent에게 맡길 작업과 기대 결과에 대한 생각 |
| 에이전트 번들(번들) | 하나의 Agent 작업 아이디어를 Rule·Skill(+ Script·Automation)으로 묶은 단위 |
| 공방 키트 번들 | 공방 운영·총관리용 번들 |
| 예시 번들 | 특정 업무를 시험하는 번들 |
| gate | Bundle Catalog가 다음 번들 설치를 선택하게 하는 관문 |

## gate 설치 순서

소비 프로젝트에 처음 연결할 때 권장 순서:

1. **Bundle Catalog** — gate (필수, 첫 설치)
2. **Agent Skill Workshop** — 아이디어를 번들로 구현할 때
3. **예시 번들** — 해당 업무를 실제로 수행할 때

## 등록 번들

| 번들 | 유형 | 상태 | 원본 | gate | Rule | Skill | Agent 작업 목적 |
|---|---|---|---|---|---|---|---|
| Bundle Catalog | 공방 키트 | `draft` | `workshop-kit/` | 1 — 첫 설치 | `bundle-catalog.mdc` | `manage-agent-bundles` | 번들 설치·업데이트·삭제 관리 |
| Agent Skill Workshop | 공방 키트 | `draft` | `workshop-kit/` | 2 — 선택 | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | Agent 작업 아이디어를 번들로 구현 |
| Session Market Briefing | 예시 | `testing` | `examples/session-market-briefing/` | 3 — 선택 | `market-briefing.mdc` | `session-market-briefing` | 세션 경제 브리핑 |
| Web Crawler Craft | 예시 | `draft` | `examples/web-crawler-ver0/` | 3 — 선택 | `crawler-craft.mdc` | `web-crawler-craft` | 웹 크롤러 제작 |

## 번들 소스 저장소 내부 메모

- **Bundle Catalog**: 다른 저장소에 연결할 때 gate로 먼저 가져간다.
- **Agent Skill Workshop**: 이 저장소에서 아이디어를 구현할 때 gate를 통해 추가 설치한다.
- **예시 번들**: 이 저장소 내부에서는 `examples/`에만 두고, 필요할 때 gate를 통해 `.cursor/`에 설치한다.

## 마지막 관리 기록

- 2026-08-17: gate-first 연결 흐름 반영. 소비 프로젝트용 로컬 catalog는 `.cursor/agent-bundles/catalog.md`.
