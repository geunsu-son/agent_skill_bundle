# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **관리·배포용 원본**을 보관합니다.

여기 있는 Rule·Skill 묶음은 **공방 키트 번들**이라 부릅니다. 업무별 시험 구현은 `examples/`의 **예시 번들**에 둡니다.

## 왜 `.cursor/`와 분리하는가

`.cursor/`는 Cursor가 현재 저장소에서 직접 읽는 실행 위치입니다. 반면 `workshop-kit/`은 Rule과 Skill을 하나의 결과물로 관리하고, 다른 프로젝트로 복사하거나 수정 이력을 검토하기 쉬운 원본 위치입니다.

```text
workshop-kit/   관리·배포용 원본
      ↓
.cursor/        현재 저장소에서 사용하는 실행본
```

ver0에서는 자동 동기화 도구를 만들지 않습니다. 구조가 안정되기 전에는 두 위치를 명시적으로 함께 수정하며 어떤 방식이 실제로 편한지 관찰합니다.

## 구성

```text
workshop-kit/
├── catalog.md                              등록된 에이전트 번들 목록
├── rules/
│   ├── agent-skill-workshop.mdc            공방 운영 원칙
│   └── bundle-catalog.mdc                  번들 설치·업데이트·삭제 판단 원칙
└── skills/
    ├── idea-to-agent-artifact/
    │   └── SKILL.md                        아이디어 → 최소 번들 구현
    └── manage-agent-bundles/
        └── SKILL.md                        catalog와 .cursor/ 정리 절차
```

| 번들 | Rule | Skill | 역할 |
|---|---|---|---|
| Agent Skill Workshop | `agent-skill-workshop.mdc` | `idea-to-agent-artifact` | 아이디어를 번들로 구현 |
| Bundle Catalog | `bundle-catalog.mdc` | `manage-agent-bundles` | 번들 설치·업데이트·삭제 관리 |

등록 상태와 활성 여부는 [`catalog.md`](catalog.md)를 기준으로 합니다.

## 사용 예시

아이디어를 새 번들로 만들 때:

```text
이 아이디어를 공방 규칙에 맞춰 정리하고,
Rule·Skill·Script·Automation으로 필요한 만큼만 분해해서
실제로 시험할 수 있는 최소 예시를 만들어줘.
```

저장소를 Cursor에 처음 적용할 때는 루트 [README의 시작하기](../README.md#시작하기) 프롬프트를 사용합니다.

## 현재 상태

`draft`

실제 아이디어를 여러 번 구현해본 뒤 다음을 검토합니다.

- Rule이 지나치게 강하거나 장황하지 않은가
- Skill의 단계가 실제 작업 흐름과 맞는가
- `.cursor/`와 원본의 중복 관리 비용이 큰가
- catalog만으로 번들 관리가 충분한가
- Script 또는 동기화 도구가 필요한가
