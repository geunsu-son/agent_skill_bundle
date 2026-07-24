# Workshop Kit

이 디렉터리는 Agent Skill Bundle 공방을 운영하기 위한 **관리·배포용 원본**을 보관합니다.

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
├── rules/
│   └── agent-skill-workshop.mdc
└── skills/
    └── idea-to-agent-artifact/
        └── SKILL.md
```

- `agent-skill-workshop.mdc`: 공방에서 Agent가 작업할 때 지켜야 할 운영 원칙
- `idea-to-agent-artifact/SKILL.md`: 아이디어를 최소 구현 예시로 바꾸는 절차

## 사용 예시

```text
이 아이디어를 공방 규칙에 맞춰 정리하고,
Rule·Skill·Script·Automation으로 필요한 만큼만 분해해서
실제로 시험할 수 있는 최소 예시를 만들어줘.
```

## 현재 상태

`draft`

실제 아이디어를 여러 번 구현해본 뒤 다음을 검토합니다.

- Rule이 지나치게 강하거나 장황하지 않은가
- Skill의 단계가 실제 작업 흐름과 맞는가
- `.cursor/`와 원본의 중복 관리 비용이 큰가
- Script 또는 동기화 도구가 필요한가
