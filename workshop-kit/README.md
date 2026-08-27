# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **관리·배포용 원본**을 보관합니다.

## Bundle Catalog gate (하나의 번들)

총관리 **Rule 하나 + 하위 Skill 세 개**. Issue 피드백(`report-bundle-feedback`)은 **별도 번들이 아닙니다.**

```text
bundle-catalog.mdc (Rule)
├── audit-installed-bundles
├── manage-agent-bundles
└── report-bundle-feedback
```

## 다른 저장소에 연결할 때

```text
Bundle Catalog gate 선설치 (Rule + 하위 Skill 3개)
→ audit-installed-bundles
→ (connect turn) 번들 선택·피드백 참여 설정
→ (enabled) 작업 완료·Skill PR 시 report-bundle-feedback
```

## 등록 번들 (catalog.md)

| 번들 | Rule | 하위 Skill |
|---|---|---|
| Agent Skill Workshop | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` |
| Bundle Catalog | `bundle-catalog.mdc` | `audit-installed-bundles`, `manage-agent-bundles`, `report-bundle-feedback` |

## 사용 예시

작업 중인 다른 저장소에 연결할 때는 루트 [README의 시작하기](../README.md#시작하기) 프롬프트를 사용합니다.

## 현재 상태

`draft`
