#!/usr/bin/env python3
"""Count tokens on the SH 51st long-term jeonse notice.

This measures tokenizer input cost, not end-to-end agent billing
(system prompt, tools, cache, and output tokens are excluded).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import tiktoken
from transformers import GPT2TokenizerFast

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
RESULTS = ROOT / "results"

HANGUL_RE = re.compile(r"[\uac00-\ud7a3]")

CALIBRATION = {
    "en": "I refactored the agent loop to cut token usage.",
    "ko": "토큰 사용량을 줄이려고 에이전트 루프를 다시 짰다.",
}


def stats(text: str) -> dict:
    hangul = len(HANGUL_RE.findall(text))
    return {
        "chars": len(text),
        "hangul_syllables": hangul,
        "utf8_bytes": len(text.encode("utf-8")),
        "whitespace_tokens": len(text.split()),
    }


def load_tokenizers() -> dict:
    claude_dir = Path("/tmp/claude-tokenizer")
    return {
        "o200k_base": tiktoken.get_encoding("o200k_base"),
        "cl100k_base": tiktoken.get_encoding("cl100k_base"),
        "claude_xenova": GPT2TokenizerFast.from_pretrained(str(claude_dir)),
    }


def count_tokens(tokenizer, text: str, kind: str) -> int:
    if kind == "tiktoken":
        return len(tokenizer.encode(text))
    ids = tokenizer.encode(text, add_special_tokens=False)
    return len(ids)


def measure_text(tokenizers: dict, text: str) -> dict:
    out = {"text": stats(text), "tokens": {}}
    mapping = {
        "o200k_base": ("tiktoken", "GPT-5.6 family / GPT-4o (tiktoken)"),
        "cl100k_base": ("tiktoken", "GPT-4 / 3.5 (tiktoken)"),
        "claude_xenova": ("hf", "Claude proxy (Xenova/claude-tokenizer, pre-Claude-3 vocab)"),
    }
    for name, (kind, label) in mapping.items():
        n = count_tokens(tokenizers[name], text, kind)
        s = out["text"]
        out["tokens"][name] = {
            "label": label,
            "tokens": n,
            "tokens_per_100_chars": round(n / s["chars"] * 100, 3) if s["chars"] else None,
            "tokens_per_hangul": round(n / s["hangul_syllables"], 3) if s["hangul_syllables"] else None,
            "chars_per_token": round(s["chars"] / n, 3) if n else None,
        }
    o = out["tokens"]["o200k_base"]["tokens"]
    c = out["tokens"]["claude_xenova"]["tokens"]
    old = out["tokens"]["cl100k_base"]["tokens"]
    out["ratios"] = {
        "o200k_over_claude": round(o / c, 3) if c else None,
        "claude_over_o200k": round(c / o, 3) if o else None,
        "cl100k_over_o200k": round(old / o, 3) if o else None,
    }
    return out


def main() -> None:
    tokenizers = load_tokenizers()
    full_ko = (FIXTURES / "sh-51-longterm-lease-ko.txt").read_text(encoding="utf-8")
    pair_ko = (FIXTURES / "pair-ko.txt").read_text(encoding="utf-8")
    pair_en = (FIXTURES / "pair-en.txt").read_text(encoding="utf-8")

    result = {
        "status": "draft",
        "what_this_measures": "input tokens of the same text under public tokenizers",
        "what_this_does_not_measure": [
            "Cursor system prompt / tools / cache",
            "output or reasoning tokens",
            "unpublished Grok 4.6 and Composer 2.5 tokenizers",
        ],
        "assumptions": [
            "GPT-5.6 Luna uses the GPT-5.6 family tokenizer o200k_base (verified publicly for GPT-5.6 Sol; Luna is the same family).",
            "Xenova/claude-tokenizer is the older public Claude vocab, not Claude 4.7+/Fable billing.",
            "Grok 4.6 and Composer 2.5 have no public tokenizer; live agent usage is a separate experiment.",
        ],
        "corpus": {
            "source": "SH 제51차 장기전세주택 입주자 모집공고 PDF, 64 pages, InDesign extract",
            "full_ko": measure_text(tokenizers, full_ko),
            "pair_ko": measure_text(tokenizers, pair_ko),
            "pair_en": measure_text(tokenizers, pair_en),
            "calibration": {
                "en": CALIBRATION["en"],
                "ko": CALIBRATION["ko"],
                "en_counts": measure_text(tokenizers, CALIBRATION["en"]),
                "ko_counts": measure_text(tokenizers, CALIBRATION["ko"]),
            },
        },
    }

    pair_ratios = {}
    for name in ("o200k_base", "cl100k_base", "claude_xenova"):
        ko_n = result["corpus"]["pair_ko"]["tokens"][name]["tokens"]
        en_n = result["corpus"]["pair_en"]["tokens"][name]["tokens"]
        pair_ratios[name] = {
            "ko_tokens": ko_n,
            "en_tokens": en_n,
            "ko_over_en": round(ko_n / en_n, 3) if en_n else None,
        }
    result["meaning_matched_ko_over_en"] = pair_ratios

    cal_ratios = {}
    for name in ("o200k_base", "cl100k_base", "claude_xenova"):
        ko_n = result["corpus"]["calibration"]["ko_counts"]["tokens"][name]["tokens"]
        en_n = result["corpus"]["calibration"]["en_counts"]["tokens"][name]["tokens"]
        cal_ratios[name] = {
            "ko_tokens": ko_n,
            "en_tokens": en_n,
            "ko_over_en": round(ko_n / en_n, 3) if en_n else None,
        }
    result["calibration_ko_over_en"] = cal_ratios

    RESULTS.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS / "tokenizer-counts.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "wrote": str(out_path),
        "full_ko_tokens": {
            name: result["corpus"]["full_ko"]["tokens"][name]["tokens"]
            for name in ("o200k_base", "cl100k_base", "claude_xenova")
        },
        "full_ko_ratios": result["corpus"]["full_ko"]["ratios"],
        "pair_ko_over_en": pair_ratios,
        "calibration_ko_over_en": cal_ratios,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
