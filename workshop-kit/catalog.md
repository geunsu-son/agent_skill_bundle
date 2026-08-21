# Agent Bundle Catalog

이 파일은 **번들 소스 저장소**에 등록된 **에이전트 번들**의 원본 위치, 상태, `.cursor/` 활성 여부를 기록한다.

다른 저장소에서 Agent Skill Bundle을 쓸 때는 이 파일을 직접 복사하지 않는다. Bundle Catalog gate를 먼저 설치하고, `audit-installed-bundles` Skill로 설치 상태를 조사한 뒤 gate가 이 catalog를 참고해 다음 번들을 선택한다.

## Bundle Catalog gate 구성

| 구성 요소 | 파일 |
|---|---|
| Rule | `bundle-catalog.mdc` |
| Skill — 설치 조사 | `audit-installed-bundles` |
| Skill — 설치·변경 | `manage-agent-bundles` |

## gate 흐름

```text
총괄 rule(Bundle Catalog gate) 선설치
→ audit-installed-bundles로 설치 상태 조사
→ gate가 **연결 turn 안에서만** 설치할 번들 질문
→ manage-agent-bundles로 선택한 번들만 설치
→ 이후에는 사용자가 요청할 때만 추가 설치
```

## 등록 번들

| 번들 | 유형 | 상태 | 원본 | gate | Rule | Skill | Agent 작업 목적 |
|---|---|---|---|---|---|---|---|
| Bundle Catalog | 공방 키트 | `draft` | `workshop-kit/` | 1 — 선설치 | `bundle-catalog.mdc` | `audit-installed-bundles`, `manage-agent-bundles` | gate — 조사·선택·설치 관리 |
| Agent Skill Workshop | 공방 키트 | `draft` | `workshop-kit/` | 2 — 선택 | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | Agent 작업 아이디어를 번들로 구현 |
| Session Market Briefing | 예시 | `testing` | `examples/session-market-briefing/` | 3 — 선택 | `market-briefing.mdc` | `session-market-briefing` | 세션 경제 브리핑 |
| Web Crawler Craft | 예시 | `draft` | `examples/web-crawler-ver0/` | 3 — 선택 | `crawler-craft.mdc` | `web-crawler-craft` | 웹 크롤러 제작 |
| Domain Data Analysis | 예시 | `testing` | `examples/domain-data-analysis/` | 3 — 선택 | `domain-data-analysis.mdc` | `domain-data-analysis` | 도메인 기반 데이터 분석 설계·보고 |
| MCP Server Craft | 예시 | `draft` | `examples/mcp-server-craft-ver0/` | 3 — 선택 | `mcp-server-craft.mdc` | `mcp-server-craft`, `mcp-server-scope`, `mcp-server-auth`, `mcp-tool-implement`, `mcp-server-connect` | MCP 서버 설계·권한·구현·연결 |

## 마지막 관리 기록

- 2026-08-21: MCP Server Craft 인증 Skill을 `mcp-server-auth`로 바꿈. 참고 README 기준으로 호출자(GWS)·워크로드(IRSA) 분리. `.cursor/` 미승격.
- 2026-08-21: MCP Server Craft 예시 번들 등록. GWS/GCP 경로를 1순위로 둔 draft. `.cursor/` 미승격.
- 2026-08-17: Domain Data Analysis 예시 번들 등록. 케이스별 testing 파일은 예시에 두지 않음.
- 2026-08-17: `audit-installed-bundles` Skill 추가. gate 흐름을 선설치 → 조사 → 질문 → 설치로 정리.
