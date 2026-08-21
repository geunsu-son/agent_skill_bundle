# MCP Server Craft — ver0 Example

MCP 서버를 만들 때 Agent가 hello-world나 API 1:1 래핑으로 바로 들어가지 않도록, **판단 기준(Rule)** 과 **구축 작업(Skill)** 을 나눈 예시입니다.

완성된 MCP 프레임워크가 아닙니다. 사내 `purple-context-mcp` README를 참고 경로로 두고, 다음 서버를 같은 기준으로 안내하기 위한 `draft`입니다.

## 해결하려는 문제

MCP 서버 요청은 설계·권한·구현·연결이 섞여 있습니다. 한 번에 처리하면 흔히 다음이 일어납니다.

- Agent 작업과 무관한 도구가 많아진다
- 호출자 신원과 서버가 백엔드를 부르는 신원을 섞는다
- 개인 클라우드 키가 막혀 있는데도 클라이언트에 키를 요구한다
- 시크릿이 설정 파일에 남거나, 연결 확인 없이 끝났다고 한다

이 예시는 다음 질문에 답하는 것을 목표로 합니다.

1. 이 서버는 Agent가 **어떤 작업**을 끝내게 하는가?
2. 개인 자격 증명으로 부족한가, **공유 서버**가 필요한가?
3. 도구·리소스·프롬프트 중 **무엇을 최소로** 여는가?
4. **호출자 신원**과 **워크로드 신원**은 어떻게 나누는가?
5. 로컬 stdio인가, 원격 Streamable HTTP(가능하면 stateless)인가?
6. 클라이언트가 도구를 나열하고 읽기 호출 1건에 성공하는가?

## 상태

`draft` — `purple-context-mcp` README로 참고 경로를 고쳤습니다. 전체 소스·차트는 가져오지 않았습니다.

실제 서버 구현·배포는 이 저장소에 두지 않습니다.

## 참고 서버에서 가져온 것 (README)

사실로 쓰는 것:

- 목적: 팀 공유 검색 백엔드를 전사 MCP로 연다. 도구는 `retrieve` 하나
- 공유 서버인 이유: 개인 IAM은 MFA·IP 제한으로 정적 키가 막히고, 클라우드 계정이 없는 구성원도 있다
- 호출자: 회사 Google Workspace 계정 (ID 토큰 또는 OAuth). 공유 정적 토큰 없음
- 워크로드: 클러스터 역할(IRSA). 클라이언트는 AWS 키를 들지 않음
- 전송: Streamable HTTP `POST /mcp`, **stateless**. GET/DELETE는 세션용이 아니라 405
- 시크릿은 매니저에서 주입. 토큰은 로그에 안 남김

원칙만 옮기고, 계정 ID·클러스터 주소·어드민 API 목록·티켓 번호는 예시에 복사하지 않습니다.

## 구성

```text
Rule
→ 작업 표면, 공유 서버 여부, 두 겹 신원, 전송·품질 원칙

Skill — 오케스트레이션
→ 범위·인증·구현·연결 (mcp-server-craft)

Skill — 구축 작업
→ 작업 표면 (mcp-server-scope)
→ 호출자·워크로드 신원 (mcp-server-auth)
→ 도구 구현 (mcp-tool-implement)
→ 연결·검증 (mcp-server-connect)
```

- [`rules/mcp-server-craft.mdc`](rules/mcp-server-craft.mdc)
- [`skills/mcp-server-craft/SKILL.md`](skills/mcp-server-craft/SKILL.md)
- [`skills/mcp-server-scope/SKILL.md`](skills/mcp-server-scope/SKILL.md)
- [`skills/mcp-server-auth/SKILL.md`](skills/mcp-server-auth/SKILL.md)
- [`skills/mcp-tool-implement/SKILL.md`](skills/mcp-tool-implement/SKILL.md)
- [`skills/mcp-server-connect/SKILL.md`](skills/mcp-server-connect/SKILL.md)

## 권장 흐름

```text
mcp-server-scope
    ↓
mcp-server-auth
    ↓
mcp-tool-implement
    ↓
mcp-server-connect
```

권한만, 도구만, 연결만 요청되면 해당 Skill만 실행합니다.

## ver0에서 일부러 하지 않은 것

- 참고 서버 복제 구현, EKS/차트/Terraform 모듈
- TypeScript/Python SDK 고정
- 어드민 명단 API·감사 스키마를 공통 Skill로 승격
- `.cursor/` 승격
- 시크릿·인프라 식별자를 예시에 보관

같은 서버·같은 도구 표면이 반복될 때만 Script 분리를 검토합니다.

## 아직 코드로 확인하지 않은 것

- SDK 버전, 핸들러 파일 구조
- 로컬 stdio 개발 경로가 운영 HTTP와 어떻게 갈라지는지

## 관찰할 항목

1. 바로 도움이 된 내용
2. 불필요하거나 과도했던 내용
3. 다음 실행에서 바꿀 한 가지

추가로 본다.

- 도구가 작업 단위인가 (참고: `retrieve` 하나)
- 호출자 신원과 워크로드 신원이 섞이지 않는가
- 401/403·부팅 실패 조건이 맞는가
- `tools/list`와 읽기 1건을 확인했는가

## 예시 출력 골격

```md
## 한눈에 보기

- 목적: Agent가 끝낼 작업
- 공유 서버: 필요한 이유 / 로컬만
- 표면: 도구 N / 리소스 N / 프롬프트 N
- 호출자 / 워크로드 신원
- 전송: stdio / Streamable HTTP (stateless 여부)
- 검증: tools/list · 읽기 1건 결과

## 범위

## 자격 증명·권한

## 구현

## 연결

## 한계와 가정
```

> 이 예시는 모든 SaaS를 MCP로 바꾸는 시스템이 아니라, Agent가 MCP 서버를 **더 작고 안전하게** 만들도록 돕는 보조 도구입니다.
