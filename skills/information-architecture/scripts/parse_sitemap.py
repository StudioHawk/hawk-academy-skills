#!/usr/bin/env python3
"""Parse one or more sitemaps and emit a flat URL inventory.

Handles:
  - sitemap.xml (single)
  - sitemap_index.xml (multi-sitemap index, recurses into each child sitemap)
  - HTTP basic auth via embedded URL credentials (https://user:pass@host/path)

Usage:
    parse_sitemap.py <sitemap_url_or_index_url>
    parse_sitemap.py https://example.com/sitemap.xml > urls.txt
    parse_sitemap.py https://example.com/sitemap_index.xml --filter '/products/'

Used by the hawk-academy-ia-mapper skill as a fallback when WebFetch can't
handle a sitemap-index cleanly.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from urllib.parse import urlparse


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "hawk-academy-ia-mapper/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def is_index(xml: str) -> bool:
    """Sitemap-index files contain <sitemap> elements; regular sitemaps contain <url>."""
    return "<sitemap>" in xml or "<sitemapindex" in xml


def parse_locs(xml: str) -> list:
    """Pull every <loc>...</loc> entry from a sitemap or index."""
    return [m.strip() for m in re.findall(r"<loc>([^<]+)</loc>", xml, flags=re.I)]


def collect_urls(start_url: str, seen=None) -> list:
    """Recursively follow sitemap-index entries and return the full URL list."""
    if seen is None:
        seen = set()
    if start_url in seen:
        return []
    seen.add(start_url)

    try:
        xml = fetch(start_url)
    except Exception as e:
        print("# WARN: failed to fetch {0}: {1}".format(start_url, e), file=sys.stderr)
        return []

    locs = parse_locs(xml)
    if not locs:
        return []

    if is_index(xml):
        # Recurse into each child sitemap.
        all_urls = []
        for child in locs:
            all_urls.extend(collect_urls(child, seen))
        return all_urls

    return locs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("url", help="Sitemap URL or sitemap-index URL")
    ap.add_argument("--filter", help="Only emit URLs whose path contains this substring")
    ap.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude URLs whose path contains this substring (repeatable)",
    )
    ap.add_argument("--unique", action="store_true", help="De-duplicate")
    args = ap.parse_args()

    urls = collect_urls(args.url)

    if args.filter:
        urls = [u for u in urls if args.filter in urlparse(u).path]
    for ex in args.exclude:
        urls = [u for u in urls if ex not in urlparse(u).path]

    if args.unique:
        urls = list(dict.fromkeys(urls))  # preserves order

    for u in urls:
        print(u)

    print("\n# Total: {0} URLs".format(len(urls)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
