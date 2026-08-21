# MCP Server Craft — ver0 Example

MCP 서버를 만들 때 Agent가 hello-world나 API 1:1 래핑으로 바로 들어가지 않도록, **판단 기준(Rule)** 과 **구축 작업(Skill)** 을 나눈 예시입니다.

완성된 MCP 프레임워크가 아닙니다. 사내 GWS/GCP 컨텍스트 서버(`purple-context-mcp`)를 참고 경로로 두고, 다음 서버를 같은 기준으로 안내하기 위한 `draft`입니다.

## 해결하려는 문제

MCP 서버 요청은 설계·권한·구현·연결이 섞여 있습니다. 한 번에 처리하면 흔히 다음이 일어납니다.

- Agent 작업과 무관한 도구가 많아진다
- GCP/GWS 자격 증명과 최소 권한이 나중에 붙는다
- 시크릿이 설정 파일에 남거나, 연결 확인 없이 끝났다고 한다

이 예시는 다음 질문에 답하는 것을 목표로 합니다.

1. 이 서버는 Agent가 **어떤 작업**을 끝내게 하는가?
2. 도구·리소스·프롬프트 중 **무엇을 최소로** 여는가?
3. GWS/GCP라면 **어떤 자격 증명·스코프**가 그 표면에 맞는가?
4. 로컬 stdio인가, GCP에서 열어 Streamable HTTP로 붙이는가?
5. 클라이언트가 도구를 나열하고 읽기 호출 1건에 성공하는가?

## 상태

`draft` — Rule·Skill 초안. 이 환경에서는 `purple-context-mcp` 코드를 열 수 없어, 사용자 설명(GWS + GCP 권한·자격 증명으로 서버를 염)과 MCP/Cursor 공개 문서에 기반합니다.

실제 서버 구현·배포는 이 저장소에 두지 않습니다. 다음 MCP 요청에서 Skill만으로 수행되는지 관찰합니다.

## 구성

```text
Rule
→ MCP 서버를 설계·구현할 때 계속 지킬 역할·권한·품질 원칙

Skill — 오케스트레이션
→ 요청을 범위·인증·구현·연결 순으로 묶음 (mcp-server-craft)

Skill — 구축 작업
→ 작업 표면 정의 (mcp-server-scope)
→ GWS/GCP 권한·자격 증명 (mcp-gcp-workspace-auth)
→ 도구·리소스 구현 (mcp-tool-implement)
→ 실행·클라이언트 연결·검증 (mcp-server-connect)
```

- [`rules/mcp-server-craft.mdc`](rules/mcp-server-craft.mdc)
- [`skills/mcp-server-craft/SKILL.md`](skills/mcp-server-craft/SKILL.md)
- [`skills/mcp-server-scope/SKILL.md`](skills/mcp-server-scope/SKILL.md)
- [`skills/mcp-gcp-workspace-auth/SKILL.md`](skills/mcp-gcp-workspace-auth/SKILL.md)
- [`skills/mcp-tool-implement/SKILL.md`](skills/mcp-tool-implement/SKILL.md)
- [`skills/mcp-server-connect/SKILL.md`](skills/mcp-server-connect/SKILL.md)

## 권장 흐름

```text
mcp-server-scope
    ↓
mcp-gcp-workspace-auth   (GWS/GCP 대상일 때)
    ↓
mcp-tool-implement
    ↓
mcp-server-connect
```

전체 제작은 `mcp-server-craft`가 위 순서를 묶습니다. 권한만, 도구만, 연결만 요청되면 해당 Skill만 실행합니다.

## ver0에서 일부러 하지 않은 것

- TypeScript/Python SDK를 하나로 고정
- 공통 MCP 런타임·보일러플레이트 저장소
- `purple-context-mcp` 복제 구현
- Cloud Run/IAP Terraform 모듈
- `.cursor/` 공통 Rule·Skill 승격
- 자격 증명 파일·실제 스코프 목록을 예시에 보관

같은 서버·같은 도구 표면이 반복될 때만 Script 분리를 검토합니다.

## 가정 (코드로 확인하지 못한 것)

- 사내 1순위 경로는 GWS 컨텍스트 + GCP 자격 증명이다.
- 로컬은 stdio, 팀 공유·GCP 호스팅은 Streamable HTTP다.
- 컨텍스트 서버의 기본 권한은 읽기다.

`purple-context-mcp`의 transport, 배포 형태, OAuth vs 서비스 계정, 실제 도구 목록은 다음 실험에서 대조한다.

## 관찰할 항목

1. 바로 도움이 된 내용
2. 불필요하거나 과도했던 내용
3. 다음 실행에서 바꿀 한 가지

추가로 본다.

- 도구가 Agent 작업 단위인가, API 메서드 나열인가?
- 스코프가 도구보다 넓지 않은가?
- 시크릿이 git·로그에 없는가?
- `tools/list`와 읽기 1건을 확인했는가?

## 예시 출력 골격

Skill 출력과 동일합니다.

```md
## 한눈에 보기

- 목적: Agent가 끝낼 작업
- 표면: 도구 N / 리소스 N / 프롬프트 N
- 권한: 읽기 기본, 쓰기 여부
- 전송: stdio / Streamable HTTP
- 검증: tools/list · 읽기 1건 결과

## 범위

## 자격 증명·권한 (해당 시)

## 구현

## 연결

## 한계와 가정
```

> 이 예시는 모든 SaaS를 MCP로 바꾸는 시스템이 아니라, Agent가 MCP 서버를 **더 작고 안전하게** 만들도록 돕는 보조 도구입니다.
