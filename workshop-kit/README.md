# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **관리·배포용 원본**을 보관합니다.

## 다른 저장소에 연결할 때

```text
Bundle Catalog gate 선설치
→ audit-installed-bundles
→ (connect turn) 번들 선택·피드백 참여 설정
→ (enabled) 작업 완료·Skill PR 시 report-bundle-feedback
```

## 구성

```text
workshop-kit/
├── catalog.md
├── rules/
│   ├── agent-skill-workshop.mdc
│   └── bundle-catalog.mdc
└── skills/
    ├── audit-installed-bundles/
    ├── idea-to-agent-artifact/
    ├── manage-agent-bundles/
    └── report-bundle-feedback/
```

| 번들 | Rule | Skill | 역할 |
|---|---|---|---|
| Agent Skill Workshop | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | 아이디어를 번들로 구현 |
| Bundle Catalog | `bundle-catalog.mdc` | `audit-installed-bundles`, `manage-agent-bundles`, `report-bundle-feedback` | gate — 조사·선택·피드백 Issue |

## 사용 예시

작업 중인 다른 저장소에 연결할 때는 루트 [README의 시작하기](../README.md#시작하기) 프롬프트를 사용합니다.

## 현재 상태

`draft`
