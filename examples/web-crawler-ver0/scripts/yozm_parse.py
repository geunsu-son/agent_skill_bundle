"""Parse yozm.wishket.com magazine RSS and article HTML (testing)."""

from __future__ import annotations

import json
import re
from html import unescape
from typing import Any

from bs4 import BeautifulSoup

CONTENT_NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def article_id_from_url(url: str) -> str:
    match = re.search(r"/magazine/detail/(\d+)", url)
    return match.group(1) if match else url.rstrip("/").rsplit("/", 1)[-1]


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def parse_rss_item(item: Any) -> dict[str, Any]:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    published_at = (item.findtext("pubDate") or item.findtext("published") or "").strip() or None
    author = (item.findtext("author") or "").strip() or None
    description = (item.findtext("description") or "").strip() or None

    content_el = item.find("content:encoded", CONTENT_NS)
    content_html = content_el.text if content_el is not None and content_el.text else None
    body = html_to_text(content_html) if content_html else None

    return {
        "id": article_id_from_url(link),
        "title": title,
        "url": link,
        "published_at": published_at,
        "author": author,
        "description": description,
        "body": body,
        "body_char_count": len(body) if body else 0,
        "body_source": "rss_content_encoded" if body else None,
        "source_feed": "https://yozm.wishket.com/magazine/feed/",
    }


def parse_article_html(html: str, url: str) -> dict[str, Any]:
    if len(html) < 500:
        return {"url": url, "fetch_status": "blocked", "body": None, "body_char_count": 0}

    soup = BeautifulSoup(html, "lxml")

    title = None
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"].strip()
    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    body = None
    for sel in ["article", "main", "[class*='article']", "[class*='content']"]:
        el = soup.select_one(sel)
        if el:
            candidate = html_to_text(str(el))
            if len(candidate) >= 200:
                body = candidate
                break

    if not body:
        body = html_to_text(html)
        if len(body) < 200:
            body = None

    return {
        "url": url,
        "fetch_status": "ok" if body else "parse_failed",
        "title": title,
        "body": body,
        "body_char_count": len(body) if body else 0,
        "body_source": "html" if body else None,
    }
