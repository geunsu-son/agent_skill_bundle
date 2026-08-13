#!/usr/bin/env python3
"""Fetch kr.investing.com news with article body (testing artifact).

Pipeline:
1. List items from official RSS feed
2. Fetch each article HTML (Playwright browser fallback)
3. Parse body from HTML (SSR content in article_WYSIWYG container)

Note: kr.investing.com blocks many automated clients (403). From datacenter IPs,
Playwright headless often fails. Use --samples-dir with browser-saved HTML for
testing, or run from a residential/local network.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from investing_kr_parse import article_id_from_url, parse_article_html

DEFAULT_FEED = "https://kr.investing.com/rss/news.rss"
USER_AGENT = "AgentSkillWorkshop/1.0 (rss-reader; research)"
DEFAULT_DELAY_SEC = 2.0


def fetch_rss(url: str, timeout: float = 30.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_rss_items(xml_text: str, limit: int) -> list[dict]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel element not found")

    items: list[dict] = []
    for item in channel.findall("item"):
        link = (item.findtext("link") or "").strip()
        if not link:
            continue
        items.append(
            {
                "id": article_id_from_url(link),
                "title": (item.findtext("title") or "").strip(),
                "url": link,
                "published_at": (item.findtext("pubDate") or "").strip() or None,
                "author": (item.findtext("author") or "").strip() or None,
                "source_feed": DEFAULT_FEED,
            }
        )
        if len(items) >= limit:
            break
    return items


def fetch_html_playwright(url: str, timeout_ms: int = 60000) -> tuple[str | None, str | None]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, "playwright_not_installed"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                locale="ko-KR",
                timezone_id="Asia/Seoul",
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            response = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_timeout(2000)
            status = response.status if response else None
            html = page.content()
            browser.close()
            if status == 403 or html.strip() == "403" or len(html) < 500:
                return None, f"blocked_http_{status}"
            return html, None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def load_sample_html(samples_dir: Path, article_id: str) -> str | None:
    path = samples_dir / f"{article_id}.html"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def enrich_item(
    item: dict,
    *,
    use_playwright: bool,
    samples_dir: Path | None,
    delay_sec: float,
) -> dict:
    url = item["url"]
    article_id = item["id"]
    html: str | None = None
    fetch_errors: list[str] = []

    if use_playwright:
        html, err = fetch_html_playwright(url)
        if err:
            fetch_errors.append(f"playwright:{err}")
        time.sleep(delay_sec)

    if html is None and samples_dir is not None:
        html = load_sample_html(samples_dir, article_id)
        if html is None:
            fetch_errors.append("sample:not_found")
        else:
            fetch_errors.append("sample:used")

    if html is None:
        item.update(
            {
                "body": None,
                "body_char_count": 0,
                "body_fetch_status": "failed",
                "body_fetch_errors": fetch_errors,
            }
        )
        return item

    parsed = parse_article_html(html, url)
    item.update(
        {
            "body": parsed.get("body"),
            "body_char_count": parsed.get("body_char_count", 0),
            "body_fetch_status": parsed.get("fetch_status"),
            "description": parsed.get("description"),
            "body_fetch_errors": fetch_errors,
        }
    )
    if parsed.get("title") and not item.get("title"):
        item["title"] = parsed["title"]
    if parsed.get("published_at"):
        item["published_at"] = parsed["published_at"]
    return item


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch kr.investing.com news with body")
    parser.add_argument("--feed", default=DEFAULT_FEED)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SEC, help="Delay after each article fetch")
    parser.add_argument("--no-playwright", action="store_true", help="Skip live HTML fetch")
    parser.add_argument(
        "--samples-dir",
        type=Path,
        default=None,
        help="Fallback directory with {article_id}.html files from browser saves",
    )
    parser.add_argument(
        "--urls",
        nargs="*",
        default=None,
        help="Explicit article URLs (skips RSS when provided)",
    )
    args = parser.parse_args()

    try:
        if args.urls:
            items = [
                {
                    "id": article_id_from_url(url),
                    "title": None,
                    "url": url,
                    "published_at": None,
                    "author": None,
                    "source_feed": None,
                }
                for url in args.urls
            ]
        else:
            xml_text = fetch_rss(args.feed)
            items = parse_rss_items(xml_text, args.limit)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    enriched = []
    for item in items:
        enriched.append(
            enrich_item(
                item,
                use_playwright=not args.no_playwright,
                samples_dir=args.samples_dir,
                delay_sec=args.delay,
            )
        )

    ok_bodies = sum(1 for row in enriched if row.get("body_char_count", 0) > 0)
    fetched_at = datetime.now(timezone.utc).isoformat()

    print(
        json.dumps(
            {
                "fetched_at": fetched_at,
                "feed": args.feed,
                "items": enriched,
                "summary": {
                    "total": len(enriched),
                    "with_body": ok_bodies,
                    "without_body": len(enriched) - ok_bodies,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0 if ok_bodies > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
