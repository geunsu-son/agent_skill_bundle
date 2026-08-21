# MCP Server Connect

## 상태

`ver0` draft. Cursor `mcp.json`과 MCP Inspector를 1순위 검증 수단으로 둡니다. 참고 서버의 운영 배포(클러스터·차트)는 복제하지 않습니다.

## 목적

구현한 MCP 서버를 클라이언트에 연결하고, **도구 목록과 읽기 호출 1건**으로 동작과 권한을 확인합니다.

## 사용 시점

- 서버 코드가 있거나 기존 서버 URL/명령이 있을 때
- 원격 Streamable HTTP 서버를 Cursor·Claude Code에 붙일 때
- `mcp-server-craft` 마지막 단계

## 입력

- transport (stdio / Streamable HTTP)
- 실행 명령 또는 URL
- 호출자 토큰을 넣는 방법 (환경 변수 **이름**, OAuth)
- 클라이언트
- 스모크에 쓸 읽기 도구와 무해한 인자

## 절차

### 1. 실행 방식

**stdio**

- Cursor가 `command` + `args`로 프로세스를 띄움
- `env`에는 이름만. 값은 `${env:VAR}` 또는 `envFile` (stdio만)
- 프로젝트: `.cursor/mcp.json` / 개인 전역: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "example-context": {
      "command": "node",
      "args": ["${workspaceFolder}/dist/index.js"]
    }
  }
}
```

**Streamable HTTP**

- 클라이언트는 `url`로 붙음. 인증은 `Authorization: Bearer <호출자 신원 토큰>`
- 공유 정적 토큰을 기본 예시에 두지 않음. `${env:NAME}`만
- 신규는 SSE URL을 기본으로 두지 않음
- 참고 서버는 `POST /mcp`만. 세션용 GET/DELETE는 405

```json
{
  "mcpServers": {
    "example-context": {
      "url": "https://mcp.example.internal/mcp",
      "headers": {
        "Authorization": "Bearer ${env:CALLER_ID_TOKEN}"
      }
    }
  }
}
```

공개 HTTP에 인증 없이 올리지 않습니다. 운영에서 쓰는 것(호출자 ID 토큰, MCP OAuth, 내부망)만 한 줄로 적습니다. 추측으로 인프라 모듈을 만들지 않습니다.

Google OAuth 자동 플로우가 필요하면, Google이 동적 클라이언트 등록을 지원하지 않을 수 있음을 `mcp-server-auth`와 같이 적습니다. 실패 시 ID 토큰 헤더 경로가 대안입니다.

### 2. 클라이언트 연결

- `mcp.json` 또는 클라이언트 UI에서 서버 추가
- 시크릿·토큰이 커밋되지 않게 검사
- 연결 후 MCP 로그에서 기동·프로토콜 오류를 확인. 401과 403을 구분

이 환경에서 UI를 조작할 수 없으면 Inspector 또는 `GET /health` + `POST /mcp`로 대신합니다. 못 하면 미실행으로 적습니다.

### 3. 스모크

순서대로:

1. 서버가 연결됨 (`/health` 또는 프로세스 기동)
2. 인증 없이 호출하면 401. 힌트에 토큰 값이 없음
3. `tools/list`가 범위와 같은 이름을 반환
4. 읽기 도구 1건 — 최소 인자, 소량 결과
5. (선택) 명단 없는 계정 → 403, OAuth 루프가 아님
6. (선택) 빈 질의 → 백엔드 호출 없이 거절

실패 시 구현을 완료로 바꾸지 않고, 인증 / 허용 / 네트워크 / 스키마 / 백엔드 중 어디인지 적습니다.

### 4. 운영 메모

짧게만 적습니다.

- 토큰 만료 시 다시 받는 방법 (값은 적지 않음)
- 로그 위치. 호출자 이메일은 남아도 토큰은 없음
- 관리자 경로는 공용 URL이 아님

## 출력 형식

```md
## 연결 요약

- 전송:
- 설정 파일:
- 검증: 연결 / 401 / tools/list / 읽기 1건 — 통과·실패·미실행

## 클라이언트 설정

시크릿 없는 mcp.json 골격.

## 스모크 결과

호출한 도구, 401/403 구분, 성공 여부.

## 사람이 확인할 것

## 한계
```

## 완료 조건

- transport에 맞는 설정이 있음
- 호출자 토큰이 설정 파일에 평문으로 없음
- 공유 정적 토큰을 안내하지 않음 (감사가 필요한 서버)
- `tools/list` 또는 동등 확인을 했거나 미실행 사유가 있음
- 읽기 1건을 했거나, 권한/환경 때문에 못 한 이유가 있음
- 공개 무인증 원격 배포를 권하지 않음

## 실패 조건

- 연결 없이 구현 완료로 보고
- 예시에 실제 토큰 포함
- 팀 공유 서버를 인증 없는 HTTP로 열기
- 403인데 401을 재로그인으로 안내하기
