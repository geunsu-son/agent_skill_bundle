# Rule·Skill reusable 판단 (testing 2사이트 후)

`web-crawler-ver0` Rule·Skill을 두 사이트에 적용한 뒤의 **판단 메모**입니다.  
결론이 아니라, 승격 전 확인할 체크리스트입니다.

## testing 대상

| 사이트 | 기록 | 목록 | 본문 | 무인 E2E |
|---|---|---|---|---|
| [kr.investing.com](investing-kr-news/README.md) | RSS + HTML fallback | ✅ RSS | ⚠️ GUI/로컬 | ❌ 클라우드 403 |
| [yozm.wishket.com](yozm-wishket/README.md) | RSS full content | ✅ RSS | ✅ RSS | ✅ 클라우드 |

## reusable 승격 기준 (공방 정의)

| 기준 | 현재 |
|---|---|
| 실제 작업 2건 이상 testing | ✅ 2사이트 |
| 관찰 기록 (도움/과함/다음 수정) | ✅ 각 testing README |
| 반복 사용으로 가치 확인 | ❌ 아직 1회성 testing |
| Rule·Skill 책임 분리 유지 | ✅ |
| Script는 반복 로직만 | ✅ 사이트별 fetch+parse |

## 지금 reusable라고 말할 수 있는 것

- **절차 패턴**은 두 사이트에서 재사용됨:
  1. 요청 정리
  2. RSS/API/피드 우선
  3. 충분하면 SPA·HTML·Playwright 생략
  4. 스키마·robots·한계 기록
- **사이트별 Script** 분리가 맞음 (통합 크롤러 프레임워크 X)

## 아직 reusable가 아닌 것

- `.cursor/` 공통 Rule·Skill 승격 — **2사이트만**으로는 부족 (공방 원칙: 반복 사용 검증)
- Investing 본문 경로 — 환경 의존(403) 해결 패턴이 Skill에 **한 줄 원칙**으로만 반영됨
- Skill 9단계 — 짧은 작업에 **경로 확정 후 생략** 규칙은 yozm에서 검증, 문서화는 draft

## 권장 다음 단계 (reusable 전)

1. **제3 사이트** testing (정적 HTML만 / 로그인 필요 등 다른 유형 1건)
2. 같은 Rule·Skill로 **사용자 실제 작업 1건** (Agent가 Skill만 읽고 수행)
3. 관찰 3회 누적 후:
   - Skill 단계 **축약판** (RSS 충분 / HTML만 / 강한 차단)
   - `reusable` 표시 + `.cursor/` 승격 여부 결정

## 한 줄 결론

> **yozm testing으로 「절차가 사이트마다 다르게 적용된다」는 것을 확인했으므로, reusable 논의는 가능해졌다.  
> 하지만 「지금 reusable로 승격」은 아니고, `testing` → (1~2건 더) → `reusable` 순서가 맞다.**
