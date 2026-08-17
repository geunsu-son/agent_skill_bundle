# Agent Bundle Catalog

이 파일은 저장소에 등록된 **에이전트 번들**의 원본 위치, 상태, `.cursor/` 활성 여부를 기록한다.

번들을 설치·업데이트·삭제할 때 `manage-agent-bundles` Skill과 함께 갱신한다.

## 용어

| 용어 | 의미 |
|---|---|
| Agent 작업 아이디어 | Agent에게 맡길 작업과 기대 결과에 대한 생각 |
| 에이전트 번들(번들) | 하나의 Agent 작업 아이디어를 Rule·Skill(+ Script·Automation)으로 묶은 단위 |
| 공방 키트 번들 | 공방 운영·총관리용 번들 (`workshop-kit/`) |
| 예시 번들 | 특정 업무를 시험하는 번들 (`examples/<bundle-name>/`) |

## 등록 번들

| 번들 | 유형 | 상태 | 원본 | 활성(`.cursor/`) | Rule | Skill |
|---|---|---|---|---|---|---|
| Agent Skill Workshop | 공방 키트 | `draft` | `workshop-kit/` | yes | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` |
| Bundle Catalog | 공방 키트 | `draft` | `workshop-kit/` | yes | `bundle-catalog.mdc` | `manage-agent-bundles` |
| Session Market Briefing | 예시 | `testing` | `examples/session-market-briefing/` | no | `market-briefing.mdc` | `session-market-briefing` |
| Web Crawler Craft | 예시 | `draft` | `examples/web-crawler-ver0/` | no | `crawler-craft.mdc` | `web-crawler-craft` |

## 활성 번들 메모

- **Agent Skill Workshop**: 공방에서 아이디어를 구현할 때 기본으로 유지한다.
- **Bundle Catalog**: 번들 설치·삭제·업데이트 요청 시 `bundle-catalog` Rule과 `manage-agent-bundles` Skill을 함께 설치한다.

## 마지막 관리 기록

- 2026-08-17: Bundle Catalog 번들과 catalog 초안 추가. Bundle Catalog를 `.cursor/`에 설치.
