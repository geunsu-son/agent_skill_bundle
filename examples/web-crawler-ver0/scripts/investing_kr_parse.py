"""Shared parsing helpers for Investing.com KR news (testing)."""

from __future__ import annotations

import json
import re
from html import unescape
from typing import Any

from bs4 import BeautifulSoup

BODY_SELECTORS = [
    "div[class*='article_WYSIWYG']",
    "#article",
    "article",
]

TITLE_SELECTORS = ["h1", "#articleTitle", "title"]


def parse_article_html(html: str, url: str) -> dict[str, Any]:
    if html.strip() in {"403", "Forbidden"} or len(html) < 500:
        return {
            "url": url,
            "fetch_status": "blocked",
            "error": "short_or_blocked_response",
            "body": None,
            "body_char_count": 0,
        }

    soup = BeautifulSoup(html, "lxml")

    title = None
    for sel in TITLE_SELECTORS:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            title = el.get_text(strip=True)
            break

    body = None
    for sel in BODY_SELECTORS:
        el = soup.select_one(sel)
        if not el:
            continue
        paragraphs = [p.get_text(" ", strip=True) for p in el.select("p")]
        if paragraphs:
            body = _normalize_text(" ".join(paragraphs))
        else:
            body = _normalize_text(el.get_text(" ", strip=True))
        if len(body) >= 80:
            break
        body = None

    meta: dict[str, Any] = {}
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text()
        if not raw or "NewsArticle" not in raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("@type") == "NewsArticle":
            meta = {
                "headline": data.get("headline"),
                "description": data.get("description"),
                "date_published": data.get("datePublished"),
                "author": (data.get("editor") or {}).get("name") if isinstance(data.get("editor"), dict) else None,
            }
            break

    if not body:
        return {
            "url": url,
            "fetch_status": "parse_failed",
            "error": "body_not_found",
            "title": title,
            "meta": meta,
            "body": None,
            "body_char_count": 0,
        }

    return {
        "url": url,
        "fetch_status": "ok",
        "title": title or meta.get("headline"),
        "published_at": meta.get("date_published"),
        "author": meta.get("author"),
        "description": meta.get("description"),
        "body": body,
        "body_char_count": len(body),
    }


def article_id_from_url(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


def _normalize_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
