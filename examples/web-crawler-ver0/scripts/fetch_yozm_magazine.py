#!/usr/bin/env python3
"""Fetch yozm.wishket.com magazine articles via official RSS (testing artifact).

RSS feed includes content:encoded with full article HTML — preferred path per
crawler-craft Rule (no Playwright required for body).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from yozm_parse import parse_rss_item

DEFAULT_FEED = "https://yozm.wishket.com/magazine/feed/"
USER_AGENT = "AgentSkillWorkshop/1.0 (rss-reader; yozm-testing)"
DEFAULT_DELAY_SEC = 5.0  # robots.txt Crawl-delay: 5


def fetch_rss(url: str, timeout: float = 60.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_feed(xml_text: str, limit: int) -> list[dict]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel element not found")

    items: list[dict] = []
    for item in channel.findall("item"):
        parsed = parse_rss_item(item)
        if not parsed.get("url"):
            continue
        items.append(parsed)
        if len(items) >= limit:
            break
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch yozm.wishket.com magazine via RSS")
    parser.add_argument("--feed", default=DEFAULT_FEED)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY_SEC,
        help="Pause after fetch (robots Crawl-delay: 5)",
    )
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()

    try:
        xml_text = fetch_rss(args.feed)
        items = parse_feed(xml_text, args.limit)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.delay > 0:
        time.sleep(args.delay)

    fetched_at = datetime.now(timezone.utc).isoformat()
    with_body = sum(1 for row in items if row.get("body_char_count", 0) > 0)

    if args.output == "text":
        for row in items:
            print(f"{row.get('published_at')}\t{row['title']}\t{row['body_char_count']} chars\t{row['url']}")
        return 0 if with_body > 0 else 2

    print(
        json.dumps(
            {
                "fetched_at": fetched_at,
                "feed": args.feed,
                "items": items,
                "summary": {
                    "total": len(items),
                    "with_body": with_body,
                    "without_body": len(items) - with_body,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if with_body > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
