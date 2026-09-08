# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **Cursor 관리·배포용 원본**을 보관합니다.

현재 Agent Skill Bundle의 공식 target은 **Cursor**입니다. 이 디렉터리의 Rule·Skill은 소비 프로젝트의 `.cursor/`를 조사하고 필요한 bundle을 설치·업데이트·제거하는 것을 기준으로 합니다.

## Bundle Catalog gate (하나의 번들)

총관리 **Rule 하나 + 하위 Skill 세 개**. Issue 피드백(`report-bundle-feedback`)은 **별도 번들이 아닙니다.**

```text
bundle-catalog.mdc (Rule)
├── audit-installed-bundles
├── manage-agent-bundles
└── report-bundle-feedback
```

## 다른 Cursor 저장소에 연결할 때

```text
Bundle Catalog gate 선설치 (Rule + 하위 Skill 3개)
→ audit-installed-bundles로 .cursor/ 조사
→ (connect turn) 번들 선택·피드백 참여 설정
→ 선택한 bundle의 Cursor artifact만 설치
→ (enabled) 작업 완료·Skill PR 시 report-bundle-feedback
```

## 등록 번들

등록 상태와 원본 경로는 [`catalog.md`](catalog.md)가 SSOT입니다.

- 공방 키트: Bundle Catalog, Agent Skill Workshop
- 정식 번들: Agent Thinking Guidelines
- 예시 번들: Session Market Briefing, Web Crawler Craft, Domain Data Analysis, MCP Server Craft, Blog Style Writing, Career Management

## 사용 예시

작업 중인 다른 저장소에 연결할 때는 루트 [README의 Bundle Catalog 연결 안내](../README.md#bundle-catalog로-cursor-프로젝트에-연결)를 사용합니다.

## 현재 상태

`draft` — 공방 관리 도구 자체는 계속 보정합니다.
