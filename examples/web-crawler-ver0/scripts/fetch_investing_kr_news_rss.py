#!/usr/bin/env python3
"""Fetch latest items from kr.investing.com news RSS (testing artifact).

RSS is the preferred collection path for this site when HTML pages
return 403 from automated clients. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

DEFAULT_FEED = "https://kr.investing.com/rss/news.rss"
USER_AGENT = "AgentSkillWorkshop/1.0 (rss-reader; research)"


def fetch_rss(url: str, timeout: float = 30.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_items(xml_text: str, limit: int) -> list[dict]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel element not found")

    items: list[dict] = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        author = (item.findtext("author") or "").strip()

        enclosure = item.find("enclosure")
        image_url = enclosure.get("url") if enclosure is not None else None

        if not link:
            continue

        items.append(
            {
                "id": link.rsplit("/", 1)[-1],
                "title": title,
                "url": link,
                "published_at": pub_date or None,
                "author": author or None,
                "image_url": image_url,
                "source_feed": DEFAULT_FEED,
            }
        )
        if len(items) >= limit:
            break

    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch kr.investing.com news via RSS")
    parser.add_argument("--feed", default=DEFAULT_FEED, help="RSS feed URL")
    parser.add_argument("--limit", type=int, default=10, help="Max items to return")
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="json",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        xml_text = fetch_rss(args.feed)
        items = parse_items(xml_text, args.limit)
    except Exception as exc:  # noqa: BLE001 — CLI tool surfaces all failures
        print(f"error: {exc}", file=sys.stderr)
        return 1

    fetched_at = datetime.now(timezone.utc).isoformat()

    if args.output == "text":
        for row in items:
            print(f"{row['published_at']}\t{row['title']}\t{row['url']}")
        return 0

    print(json.dumps({"fetched_at": fetched_at, "items": items}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
