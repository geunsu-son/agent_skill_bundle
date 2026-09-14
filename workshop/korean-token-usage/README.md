# 한국어 공고문 토큰 측정 (draft)

SH 제51차 장기전세주택 입주자 모집공고로 입력 토큰만 잰 기록이다. 예시는 정답이 아니라 검증 대상이다.

정의·관찰: [`../korean-token-usage.md`](../korean-token-usage.md)

## 재실행

```bash
python3 workshop/korean-token-usage/measure.py
```

필요 패키지: `tiktoken`, `transformers`, `pymupdf`(PDF를 다시 추출할 때). Claude 근사 어휘는 Hugging Face `Xenova/claude-tokenizer`를 `/tmp/claude-tokenizer`에 받는다.

## 파일

- `fixtures/sh-51-longterm-lease-ko.txt` — PDF 텍스트 추출본
- `fixtures/pair-ko.txt` / `pair-en.txt` — 의미 대응 서문
- `fixtures/live-input-ko.txt` — 서브에이전트에 넣은 12,000자 발췌
- `measure.py` — 토큰 집계
- `results/tokenizer-counts.json` — 공개 토크나이저 결과
- `results/live-runs.json` — 서브에이전트 실행 기록 (usage 없음)
