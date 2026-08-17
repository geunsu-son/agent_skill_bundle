#!/usr/bin/env python3
"""Fetch Velog or Tistory blog posts via RSS (and optional Velog GraphQL body).

Testing artifact for blog platform migration / comparison (velog vs tistory).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any

from blog_platform_parse import parse_rss_item, parse_velog_graphql_post

USER_AGENT = "AgentSkillWorkshop/1.0 (rss-reader; blog-platform-testing)"
DEFAULT_DELAY_SEC = 1.0
VELOG_GRAPHQL = "https://v2.velog.io/graphql"


def fetch_url(url: str, timeout: float = 60.0, method: str = "GET", body: bytes | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def velog_rss_url(username: str) -> str:
    username = username.lstrip("@")
    return f"https://api.velog.io/rss/@{username}"


def tistory_rss_url(blog: str) -> str:
    blog = blog.strip().rstrip("/")
    if blog.startswith("http://") or blog.startswith("https://"):
        if blog.endswith("rss") or blog.endswith("rss.xml"):
            return blog
        return f"{blog}/rss"
    if "/" in blog:
        return f"https://{blog}"
    if blog.endswith(".tistory.com"):
        return f"https://{blog}/rss"
    if "." in blog:
        return f"https://{blog}/rss.xml"
    return f"https://{blog}.tistory.com/rss"


def parse_feed(xml_text: str, platform: str, source_feed: str, limit: int) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel element not found")

    items: list[dict[str, Any]] = []
    for item in channel.findall("item"):
        parsed = parse_rss_item(item, platform, source_feed)
        if not parsed.get("url"):
            continue
        items.append(parsed)
        if len(items) >= limit:
            break
    return items


def velog_username_from_feed(feed_url: str) -> str | None:
    match = re.search(r"@([^/]+)", feed_url)
    if match:
        return match.group(1)
    match = re.search(r"/rss/([^/]+)", feed_url)
    return match.group(1) if match else None


def fetch_velog_graphql_body(username: str, url_slug: str) -> dict[str, Any]:
    query = (
        "query($username: String!, $url_slug: String!) {"
        " post(username: $username, url_slug: $url_slug) {"
        " id title body released_at tags url_slug } }"
    )
    payload = json.dumps(
        {"query": query, "variables": {"username": username, "url_slug": url_slug}}
    ).encode("utf-8")
    raw = fetch_url(VELOG_GRAPHQL, method="POST", body=payload)
    data = json.loads(raw)
    if data.get("errors"):
        raise RuntimeError(data["errors"][0].get("message", "graphql error"))
    return parse_velog_graphql_post(data.get("data", {}), username)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Velog/Tistory blog via RSS")
    parser.add_argument("--platform", choices=["velog", "tistory"], required=True)
    parser.add_argument(
        "--target",
        required=True,
        help="Velog: username (@velopert). Tistory: blog id or full RSS URL",
    )
    parser.add_argument("--feed", help="Override RSS feed URL")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument(
        "--velog-graphql-body",
        action="store_true",
        help="For Velog: fetch first post body as markdown via GraphQL",
    )
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SEC)
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()

    if args.feed:
        feed_url = args.feed
    elif args.platform == "velog":
        feed_url = velog_rss_url(args.target)
    else:
        feed_url = tistory_rss_url(args.target)

    try:
        xml_text = fetch_url(feed_url)
        items = parse_feed(xml_text, args.platform, feed_url, args.limit)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.delay > 0:
        time.sleep(args.delay)

    graphql_sample: dict[str, Any] | None = None
    if args.platform == "velog" and args.velog_graphql_body and items:
        username = velog_username_from_feed(feed_url) or args.target.lstrip("@")
        slug = items[0]["id"].split("/", 1)[-1] if "/" in items[0]["id"] else items[0]["id"]
        try:
            time.sleep(args.delay)
            graphql_sample = fetch_velog_graphql_body(username, slug)
        except Exception as exc:  # noqa: BLE001
            graphql_sample = {"error": str(exc)}

    fetched_at = datetime.now(timezone.utc).isoformat()
    with_body = sum(1 for row in items if row.get("body_char_count", 0) > 0)

    if args.output == "text":
        for row in items:
            print(
                f"{row.get('published_at')}\t{row['title']}\t"
                f"{row['body_char_count']} chars\t{row['url']}"
            )
        if graphql_sample and graphql_sample.get("body_char_count"):
            print(
                f"graphql\t{graphql_sample['title']}\t"
                f"{graphql_sample['body_char_count']} chars\t{graphql_sample['url']}"
            )
        return 0 if with_body > 0 else 2

    print(
        json.dumps(
            {
                "fetched_at": fetched_at,
                "platform": args.platform,
                "feed_url": feed_url,
                "count": len(items),
                "with_body_count": with_body,
                "items": items,
                "velog_graphql_sample": graphql_sample,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if with_body > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
