# MCP Server Craft

## 상태

`ver0` draft. 사내 GWS/GCP 컨텍스트 서버를 참고 경로로 두고, 범위→권한→구현→연결 순서를 검증할 예정입니다.

## 목적

MCP 서버 제작 요청을 manager rule에 맞춰 한 흐름으로 수행합니다. 상세 절차는 아래 Skill에 맡기고, 여기서는 순서·생략 조건·최종 보고만 책임집니다.

## 사용 시점

- “MCP 서버 만들어줘”, “GWS 컨텍스트를 Agent에 열어줘”
- 기존 MCP에 도구·권한·배포를 추가할 때
- 범위만 / 권한만 / 연결만 요청된 경우가 아닌 **전체 제작**

## 관련 Rule·Skill

- Rule: [`rules/mcp-server-craft.mdc`](../../rules/mcp-server-craft.mdc)
- [`mcp-server-scope`](../../skills/mcp-server-scope/SKILL.md)
- [`mcp-gcp-workspace-auth`](../../skills/mcp-gcp-workspace-auth/SKILL.md)
- [`mcp-tool-implement`](../../skills/mcp-tool-implement/SKILL.md)
- [`mcp-server-connect`](../../skills/mcp-server-connect/SKILL.md)

## 입력

- Agent가 끝낼 작업 (가능하면)
- 백엔드 (GWS/GCP, 그 외 API, 로컬 데이터)
- 클라이언트 (Cursor 등)와 사용자 범위 (개인 / 팀)
- 읽기만인지, 쓰기·관리가 필요한지
- 이미 있는 MCP·GCP 프로젝트·자격 증명 경로 (있으면)

이미 제공된 정보는 다시 묻지 않습니다.

## 절차

### 1. 기존 서버 확인

공식 서버, 마켓플레이스, 사내 서버(`purple-context-mcp` 등)가 같은 작업을 이미 열면 새로 만들지 않고 연결 방법만 안내합니다.

### 2. 범위

`mcp-server-scope`를 따릅니다. 목적, 도구/리소스/프롬프트, transport가 정해지기 전에 코드를 쓰지 않습니다.

불명확하면 가정을 한 줄로 적고 진행합니다. 구현을 막는 질문만 짧게 확인합니다.

### 3. 권한

GWS 또는 GCP 자격 증명이 필요하면 `mcp-gcp-workspace-auth`를 따릅니다.

그 외 백엔드는 해당 시스템의 최소 권한 토큰·시크릿 이름만 기록합니다. 값은 받지 않고, 저장 위치만 정합니다.

### 4. 구현

`mcp-tool-implement`를 따릅니다. 언어/SDK는 저장소가 있으면 맞추고, 없으면 TypeScript 공식 SDK 또는 Python 중 요청·기존 스택에 맞는 쪽을 고릅니다. 고른 이유를 한 줄로 적습니다.

### 5. 연결·검증

`mcp-server-connect`를 따릅니다. `tools/list`와 읽기 호출 1건이 성공하기 전에 완료라고 하지 않습니다.

권한만 요청되면 2·4·5를 생략하고 인증 Skill만 실행합니다. 연결만 요청되면 기존 서버 기준으로 5만 실행합니다.

### 6. 보고

아래 형식으로 요약합니다. 시크릿·키 파일·토큰 값을 넣지 않습니다.

## 출력 형식

```md
## 한눈에 보기

- 목적:
- 표면: 도구 N / 리소스 N / 프롬프트 N
- 권한: 읽기 기본 / 쓰기 여부, 스코프 요약(이름만)
- 전송: stdio / Streamable HTTP
- 검증: tools/list · 읽기 1건 — 통과/실패/미실행

## 범위

목적, 포함·제외 도구, 기존 서버 재사용 여부.

## 자격 증명·권한

사용한 경로(사용자 OAuth / 서비스 계정+위임 / ADC). 키 값은 쓰지 않는다.

## 구현

SDK, 도구 목록, 오류·페이지 처리.

## 연결

클라이언트 설정 위치, 실행 방법. env 이름만.

## 한계와 가정

하지 않은 범위, 확인하지 못한 인프라, 다음 검증.
```

## 완료 조건

- Rule의 금지 패턴을 어기지 않음
- 기존 서버로 충분하면 신규 구현을 하지 않음
- 범위가 도구 목록으로 떨어짐
- GWS/GCP면 스코프가 도구와 맞음
- 연결 검증 또는 왜 못 했는지가 기록됨
- 시크릿이 출력·커밋에 없음

## 향후 Script 후보

- 도구 스키마·이름 중복 검사
- 스코프 목록과 도구 권한 대조
- MCP Inspector로 `tools/list` 스모크

현재 ver0에서는 서버와 SDK를 고정하지 않습니다.
