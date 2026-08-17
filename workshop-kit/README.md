# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **관리·배포용 원본**을 보관합니다.

## 다른 저장소에 연결할 때

작업 중인 저장소에 Agent Skill Bundle을 쓸 때는 이 저장소를 clone하지 않습니다.

```text
Bundle Catalog gate 선설치
→ audit-installed-bundles로 설치 상태 조사
→ gate가 설치할 번들 질문
→ manage-agent-bundles로 선택분만 설치
```

설치 기록은 소비 프로젝트의 `.cursor/agent-bundles/catalog.md`에 둡니다.

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
    └── manage-agent-bundles/
```

| 번들 | Rule | Skill | 역할 |
|---|---|---|---|
| Agent Skill Workshop | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | 아이디어를 번들로 구현 |
| Bundle Catalog | `bundle-catalog.mdc` | `audit-installed-bundles`, `manage-agent-bundles` | gate — 조사·선택·설치 |

## 사용 예시

작업 중인 다른 저장소에 연결할 때는 루트 [README의 시작하기](../README.md#시작하기) 프롬프트를 사용합니다.

## 현재 상태

`draft`
