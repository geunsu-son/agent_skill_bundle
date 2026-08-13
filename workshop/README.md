# Workshop

아직 정리되지 않은 아이디어와 다음 실험 재료를 잠시 올려두는 작업대입니다.

완성된 문서는 `docs/`, 실제 형태를 갖춘 예시는 `examples/`로 이동합니다. 여기의 메모는 결론이 아니라 질문이어도 됩니다.

## 메모 형식

```md
## 아이디어 이름

### 문제
무엇이 반복해서 불편한가?

### 가설
Rule, Skill, Script, Automation 중 무엇으로 해결할 수 있을까?

### 작은 실험
가장 적은 구현으로 무엇을 확인할까?

### 관찰
실제 사용했을 때 무엇이 달랐나?

### 다음 작업
유지, 수정, 분리, 폐기 중 무엇을 할까?
```

## 현재 작업대

### 세션 경제 브리핑

- 방향을 단정하지 않되 결론을 회피하지 않는 기준이 필요함
- 상승·하락·횡보 중 가장 유력한 시나리오와 유력도를 제시
- 주 시나리오의 무효화 조건을 함께 제공
- 뉴스 목록보다 직장인이 바로 확인할 변수와 다음 판단 시점을 우선
- 경제 캘린더와 시장 데이터 수집을 Script로 분리할 수 있는지 검토
- 실제 브리핑 결과를 저장하고 판단 일관성을 비교하는 방법 필요

### 웹 크롤러 제작 Rule·Skill

- Agent가 크롤 요청마다 API 확인·robots·스키마 설계를 건너뛰는 패턴이 반복됨
- Rule: 수집 경로 우선순위, 법·예의, 데이터·구현 품질, 금지 패턴
- Skill: 요청 정리 → 경로 검토 → 사전 조사 → 스키마 → 구현 → 검증 → 한계 기록
- ver0 예시: [`examples/web-crawler-ver0/`](../../examples/web-crawler-ver0/README.md)
- SPA·내부 API 직접 호출 검토 단계와 참고 문서 추가
- **testing:** kr.investing.com — RSS 경로 채택, HTML 403, 관찰 기록 [`testing/investing-kr-news/`](../../examples/web-crawler-ver0/testing/investing-kr-news/README.md)
- 아직 확인 필요: 대상 사이트 유형(뉴스, 쇼핑, 공공데이터 등)에 따라 Skill 단계를 쪼갤지
- Script 후보: robots·sitemap 스캔, JSON-LD 추출, 스키마 검증

### 다음 후보

- 데이터 검증 Skill
- 주간 리포트 Skill
- 분석 결과 검토 Rule
- 배포 전 검증 Skill
