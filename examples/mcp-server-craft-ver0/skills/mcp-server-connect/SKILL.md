# MCP Server Connect

## 상태

`ver0` draft. Cursor `mcp.json`과 MCP Inspector를 1순위 검증 수단으로 둡니다. 배포 인프라는 고정하지 않습니다.

## 목적

구현한 MCP 서버를 클라이언트에 연결하고, **도구 목록과 읽기 호출 1건**으로 동작과 권한을 확인합니다.

## 사용 시점

- 서버 코드가 있거나 기존 서버 URL/명령이 있을 때
- GCP에서 연 원격 서버를 Cursor에 붙일 때
- `mcp-server-craft` 마지막 단계

## 입력

- transport (stdio / Streamable HTTP)
- 실행 명령 또는 URL
- 환경 변수 **이름** (값 아님)
- 클라이언트 (기본: Cursor)
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
    "purple-context": {
      "command": "node",
      "args": ["${workspaceFolder}/dist/index.js"],
      "env": {
        "GOOGLE_IMPERSONATE_SUBJECT": "${env:GOOGLE_IMPERSONATE_SUBJECT}"
      }
    }
  }
}
```

**Streamable HTTP**

- 서버가 GCP 등에서 리슨. Cursor는 `url`로 붙음
- `headers`에 토큰을 넣을 때 `${env:NAME}`만. 평문 시크릿 금지
- 신규는 SSE URL을 기본으로 두지 않음. 기존 SSE면 그 사실을 적음

```json
{
  "mcpServers": {
    "purple-context": {
      "url": "https://example.internal/mcp",
      "headers": {
        "Authorization": "Bearer ${env:MCP_TOKEN}"
      }
    }
  }
}
```

공개 HTTP 엔드포인트에 인증 없이 올리지 않습니다. GCP라면 IAP, 클라우드 Run 인증, 또는 MCP OAuth 중 실제로 쓰는 것을 한 줄로 적습니다. 추측으로 모듈을 생성하지 않습니다.

### 2. 클라이언트 연결

- `mcp.json`을 쓰거나, Cursor Customize에서 서버 추가를 안내
- 시크릿이 커밋되지 않게 `mcp.json`의 값을 검사
- 연결 후 Settings / MCP 로그에서 프로세스 기동·프로토콜 오류를 확인

이 환경에서 Cursor UI를 조작할 수 없으면 Inspector 또는 SDK 클라이언트로 `tools/list`를 대신합니다. 못 하면 미실행으로 적고 사용자가 확인할 항목만 남깁니다.

### 3. 스모크

순서대로:

1. 서버가 연결됨 (에러 없이 기동)
2. `tools/list`가 범위와 같은 이름을 반환
3. 읽기 도구 1건 — 최소 인자, 소량 결과
4. (선택) 잘못된 인자 → 설명적 오류
5. (선택) 권한 없는 동작 → 인증/스코프 오류. 쓰기 도구가 없으면 생략

실패 시 구현을 완료로 바꾸지 않고, 인증 / 네트워크 / 스키마 / 백엔드 중 어디인지 적습니다.

### 4. 운영 메모

짧게만 적습니다.

- 재시작 방법
- 로그 위치 (Cursor MCP Logs, Cloud Logging)
- 스코프를 늘릴 때 콘솔 위임과 도구를 같이 바꾸는 것

## 출력 형식

```md
## 연결 요약

- 전송:
- 설정 파일:
- 검증: 연결 / tools/list / 읽기 1건 — 통과·실패·미실행

## 클라이언트 설정

시크릿 없는 mcp.json 골격.

## 스모크 결과

호출한 도구, 성공 여부, 권한 오류 여부.

## 사람이 확인할 것

이 환경에서 못 한 UI·콘솔 항목.

## 한계
```

## 완료 조건

- transport에 맞는 설정이 있음
- 시크릿이 설정 파일에 평문으로 없음
- `tools/list` 또는 동등 확인을 했거나 미실행 사유가 있음
- 읽기 1건을 했거나, 권한/환경 때문에 못 한 이유가 있음
- 공개 무인증 원격 배포를 권하지 않음

## 실패 조건

- 연결 없이 구현 완료로 보고
- 예시에 실제 토큰·키 경로 포함
- 팀 공유 서버를 인증 없는 HTTP로 열기
