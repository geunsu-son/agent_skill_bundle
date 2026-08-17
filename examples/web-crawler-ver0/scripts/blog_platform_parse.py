"""Parse Velog / Tistory blog RSS items (testing artifact)."""

from __future__ import annotations

import re
from html import unescape
from typing import Any

from bs4 import BeautifulSoup

CONTENT_NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def article_id_from_url(url: str, platform: str) -> str:
    if platform == "velog":
        match = re.search(r"velog\.io/@([^/]+)/([^/?#]+)", url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
    if platform == "tistory":
        match = re.search(r"tistory\.com/(\d+)", url)
        if match:
            return match.group(1)
        match = re.search(r"/entry/([^/?#]+)", url)
        if match:
            return match.group(1)
    return url.rstrip("/").rsplit("/", 1)[-1]


def parse_rss_item(item: Any, platform: str, source_feed: str) -> dict[str, Any]:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    published_at = (item.findtext("pubDate") or item.findtext("published") or "").strip() or None
    author = (item.findtext("author") or item.findtext("dc:creator") or "").strip() or None
    description = (item.findtext("description") or "").strip() or None

    content_el = item.find("content:encoded", CONTENT_NS)
    content_html = content_el.text if content_el is not None and content_el.text else None
    body_html = content_html or description
    body = html_to_text(body_html) if body_html else None
    body_source = None
    if content_html:
        body_source = "rss_content_encoded"
    elif description and body:
        body_source = "rss_description"

    categories = [
        (cat.text or "").strip()
        for cat in item.findall("category")
        if (cat.text or "").strip()
    ]

    return {
        "id": article_id_from_url(link, platform),
        "platform": platform,
        "title": title,
        "url": link,
        "published_at": published_at,
        "author": author,
        "description": description,
        "categories": categories,
        "body": body,
        "body_char_count": len(body) if body else 0,
        "body_source": body_source,
        "source_feed": source_feed,
    }


def parse_velog_graphql_post(data: dict[str, Any], username: str) -> dict[str, Any]:
    post = data.get("post") or {}
    url_slug = post.get("url_slug") or ""
    url = f"https://velog.io/@{username}/{url_slug}" if url_slug else None
    body = post.get("body")
    tags = post.get("tags") or []

    return {
        "id": f"{username}/{url_slug}" if url_slug else post.get("id"),
        "platform": "velog",
        "title": post.get("title"),
        "url": url,
        "published_at": post.get("released_at"),
        "author": username,
        "description": None,
        "categories": tags if isinstance(tags, list) else [],
        "body": body,
        "body_char_count": len(body) if body else 0,
        "body_source": "graphql_markdown" if body else None,
        "source_feed": "https://v2.velog.io/graphql",
        "velog_post_id": post.get("id"),
    }
