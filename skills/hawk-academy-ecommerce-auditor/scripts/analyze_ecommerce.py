#!/usr/bin/env python3
"""
analyze_ecommerce.py

Turns a SiteOne offline HTML export into `findings.json` for the Hawk Academy
eCommerce Auditor skill.

Usage:
    python3 analyze_ecommerce.py \
        --crawl-dir "<work-dir>/crawl" \
        --base-url "https://store.example.com" \
        --out "<work-dir>/findings.json"

Optional:
    --max-products N     cap how many PDPs are deep-checked (default 60)
    --max-blogs N        cap how many blog posts are deep-checked (default 30)
    --quiet              suppress the progress summary on stderr

Standard library only, so it runs on a fresh workshop laptop with no pip
install. `python-docx` is only needed later, by build_ecommerce_docx.py.

WHAT IT PRODUCES
----------------
findings.json is the evidence base for the audit. The skill reads it and
applies judgement; the script never editorialises. Top-level keys:

  meta            run metadata + any limitations worth surfacing
  counts          page counts by classified type
  category_slugs  the category slugs discovered (for coverage judgement)
  categories[]    per category page: product_links, abf_words/abf_present,
                  btf_words/btf_present, links_to_parent, links_to_children
  products[]      per product page: h1_present, intro_present, specs_present,
                  scannable, has_product_schema, merchant_ready,
                  missing_required[], missing_recommended[]
  schema_summary  aggregate Product-schema coverage
  blogs[]         per blog post: tie_back, early_tie_back, commercial_links[]
  key_pages       return / about / seasonal page presence
  robots          robots.txt parse + which Disallow rules block money pages

HEURISTIC THRESHOLDS
--------------------
These are deliberately explicit so the skill can describe them honestly and
tell the attendee to spot-check borderline calls. They are signals, not
verdicts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

# --- Tunable heuristics ------------------------------------------------------

ABF_MIN_WORDS = 40      # paragraph words before the first product link
BTF_MIN_WORDS = 80      # paragraph words after the last product link
INTRO_MIN_WORDS = 25    # a PDP "intro" paragraph must be at least this long
INTRO_WITHIN_WORDS = 500  # ...and must appear within this many words of the top
EARLY_TIE_BACK_WORDS = 150  # a blog tie-back this early counts as "early"

# --- Product schema requirements (Google Merchant listing) -------------------
# Mirrors the required/recommended split documented in SKILL.md so the script
# and the skill text can never disagree.

REQUIRED_FIELDS = [
    "name",
    "image",
    "description",
    "sku/gtin/mpn",
    "brand",
    "offers.price",
    "offers.priceCurrency",
    "offers.availability",
]
RECOMMENDED_FIELDS = ["aggregateRating", "review"]

# --- URL classification vocabulary -------------------------------------------

PRODUCT_SEGS = {"products", "product", "p", "dp", "item", "items", "sku"}
CATEGORY_SEGS = {
    "collections", "collection", "category", "categories", "product-category",
    "shop", "c", "range", "ranges", "departments", "department", "browse",
}
BLOG_SEGS = {
    "blog", "blogs", "news", "article", "articles", "journal", "guides",
    "guide", "learn", "insights", "resources", "advice", "tips", "stories",
}

RETURN_PAT = re.compile(r"(?:^|[-/_])(returns?|refunds?|exchanges?|returns-policy|refund-policy)(?:$|[-/_])", re.I)
ABOUT_PAT = re.compile(r"(?:^|[-/_])(about|about-us|our-story|who-we-are|meet-the-team|our-team)(?:$|[-/_])", re.I)
SEASONAL_PAT = re.compile(
    r"(?:^|[-/_])(black-?friday|cyber-?monday|bfcm|boxing-?day|click-?frenzy|"
    r"eofy|christmas|xmas|sale|sales|clearance|outlet|deals|specials)(?:$|[-/_])",
    re.I,
)

# robots.txt Disallow prefixes that are normal housekeeping, not SEO damage.
BENIGN_ROBOTS_PAT = re.compile(
    r"^/(?:cart|checkout|account|admin|wp-admin|orders|search|apps|"
    r"cdn-cgi|cgi-bin|wp-json|\*\?|\?)", re.I
)

SKIP_TEXT_TAGS = {"script", "style", "noscript", "template", "svg"}
CAPTURE_TAGS = {"title", "h1", "h2", "h3", "p"}


# --- HTML parsing ------------------------------------------------------------

class PageParser(HTMLParser):
    """Single-pass extraction of everything the audit needs from one page.

    Tracks a running word cursor so we can say whether a paragraph appeared
    before or after a given link, which is what the ABF/BTF and blog
    tie-back checks are built on.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.canonical = ""
        self.og_url = ""
        self.og_type = ""
        self.meta_robots = ""
        self.h1s: list[str] = []
        self.h2s: list[str] = []
        self.h3s: list[str] = []
        self.paragraphs: list[tuple[int, str]] = []   # (word_pos, text)
        self.links: list[tuple[int, str]] = []        # (word_pos, href)
        self.jsonld_raw: list[str] = []
        self.counts = {k: 0 for k in ("ul", "ol", "li", "table", "tr", "dl", "dt", "img")}
        self.words = 0

        self._skip_depth = 0
        self._cap: dict | None = None

    # -- helpers
    def _attr(self, attrs, name):
        for k, v in attrs:
            if k and k.lower() == name:
                return v or ""
        return ""

    def _start_capture(self, tag: str) -> None:
        self._cap = {"tag": tag, "buf": [], "start": self.words}

    def _flush_capture(self) -> None:
        if not self._cap:
            return
        text = re.sub(r"\s+", " ", "".join(self._cap["buf"])).strip()
        tag = self._cap["tag"]
        start = self._cap["start"]
        self._cap = None
        if not text:
            return
        if tag == "title" and not self.title:
            self.title = text
        elif tag == "h1":
            self.h1s.append(text)
        elif tag == "h2":
            self.h2s.append(text)
        elif tag == "h3":
            self.h3s.append(text)
        elif tag == "p":
            self.paragraphs.append((start, text))

    # -- HTMLParser interface
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "script":
            script_type = self._attr(attrs, "type").lower()
            self._skip_depth += 1
            if "ld+json" in script_type:
                self._start_capture("jsonld")
            return

        if tag in SKIP_TEXT_TAGS:
            self._skip_depth += 1
            return

        if tag in self.counts:
            self.counts[tag] += 1

        if tag == "a":
            href = self._attr(attrs, "href").strip()
            if href:
                self.links.append((self.words, href))
        elif tag == "link":
            if "canonical" in self._attr(attrs, "rel").lower():
                self.canonical = self._attr(attrs, "href").strip()
        elif tag == "meta":
            prop = (self._attr(attrs, "property") or self._attr(attrs, "name")).lower()
            content = self._attr(attrs, "content").strip()
            if prop == "og:url":
                self.og_url = content
            elif prop == "og:type":
                self.og_type = content
            elif prop == "robots":
                self.meta_robots = content

        if tag in CAPTURE_TAGS and self._cap is None and self._skip_depth == 0:
            self._start_capture(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "script":
            if self._cap and self._cap["tag"] == "jsonld":
                self.jsonld_raw.append("".join(self._cap["buf"]))
                self._cap = None
            self._skip_depth = max(0, self._skip_depth - 1)
            return

        if tag in SKIP_TEXT_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return

        if self._cap and self._cap["tag"] == tag:
            self._flush_capture()

    def handle_data(self, data):
        if self._cap is not None:
            self._cap["buf"].append(data)
        if self._skip_depth == 0:
            self.words += len(data.split())


def parse_page(html: str) -> PageParser:
    p = PageParser()
    try:
        p.feed(html)
        p.close()
    except Exception:
        # Malformed markup should degrade, never abort the run.
        pass
    return p


# --- URL classification ------------------------------------------------------

def path_segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s]


def classify_path(path: str) -> str:
    """Return home | product | category | blog | other for a URL path."""
    segs = [s.lower() for s in path_segments(path)]
    if not segs:
        return "home"

    # Blog before category: Shopify blogs live at /blogs/<handle>/<post>.
    for i, seg in enumerate(segs):
        if seg in BLOG_SEGS:
            return "blog" if i < len(segs) - 1 else "other"

    # Product before category: Shopify PDPs nest under /collections/<c>/products/<p>.
    for i, seg in enumerate(segs):
        if seg in PRODUCT_SEGS:
            # A trailing /products/ with nothing after it is an index, not a PDP.
            return "product" if i < len(segs) - 1 else "category"

    for seg in segs:
        if seg in CATEGORY_SEGS:
            return "category"

    return "other"


def page_flags(path: str, title: str = "") -> dict:
    """Independent trust/seasonal flags. A page can be both category and seasonal."""
    haystack = path if not title else f"{path} {title}"
    return {
        "is_return": bool(RETURN_PAT.search(haystack)),
        "is_about": bool(ABOUT_PAT.search(haystack)),
        "is_seasonal": bool(SEASONAL_PAT.search(haystack)),
    }


def category_slug(path: str) -> str:
    segs = [s.lower() for s in path_segments(path)]
    for i, seg in enumerate(segs):
        if seg in CATEGORY_SEGS and i < len(segs) - 1:
            return segs[i + 1]
    # A bare /collections/ or /shop/ is an index, not a category in its own
    # right, so it contributes no slug to the coverage list.
    if not segs or segs[-1] in CATEGORY_SEGS:
        return ""
    return segs[-1]


# --- JSON-LD product schema --------------------------------------------------

def _iter_nodes(obj):
    """Walk arbitrarily nested JSON-LD, yielding every dict node."""
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _iter_nodes(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_nodes(item)


def _types_of(node: dict) -> set[str]:
    raw = node.get("@type") or node.get("type") or []
    if isinstance(raw, str):
        raw = [raw]
    return {str(t).split("/")[-1].lower() for t in raw if t}


def _has(node: dict, key: str) -> bool:
    value = node.get(key)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _brand_present(node: dict) -> bool:
    brand = node.get("brand")
    if isinstance(brand, str):
        return bool(brand.strip())
    if isinstance(brand, dict):
        return bool(str(brand.get("name", "")).strip())
    if isinstance(brand, list):
        return any(_brand_present({"brand": b}) for b in brand)
    return False


def _identifier_present(node: dict) -> bool:
    for key in ("sku", "gtin", "gtin8", "gtin12", "gtin13", "gtin14", "mpn", "productID"):
        if _has(node, key):
            return True
    return False


def _offer_nodes(node: dict) -> list[dict]:
    offers = node.get("offers")
    if isinstance(offers, dict):
        return [offers]
    if isinstance(offers, list):
        return [o for o in offers if isinstance(o, dict)]
    return []


def _offer_price_present(offers: list[dict]) -> bool:
    for offer in offers:
        if _has(offer, "price"):
            return True
        # AggregateOffer states a range instead of a single price.
        if _has(offer, "lowPrice") or _has(offer, "highPrice"):
            return True
        spec = offer.get("priceSpecification")
        for node in _iter_nodes(spec) if spec else []:
            if _has(node, "price"):
                return True
    return False


def _offer_field_present(offers: list[dict], field: str) -> bool:
    for offer in offers:
        if _has(offer, field):
            return True
        spec = offer.get("priceSpecification")
        for node in _iter_nodes(spec) if spec else []:
            if _has(node, field):
                return True
    return False


def validate_product_node(node: dict) -> tuple[list[str], list[str]]:
    """Return (missing_required, missing_recommended) for one Product node."""
    offers = _offer_nodes(node)
    missing_required = []

    if not _has(node, "name"):
        missing_required.append("name")
    if not _has(node, "image"):
        missing_required.append("image")
    if not _has(node, "description"):
        missing_required.append("description")
    if not _identifier_present(node):
        missing_required.append("sku/gtin/mpn")
    if not _brand_present(node):
        missing_required.append("brand")

    if not offers:
        missing_required += ["offers.price", "offers.priceCurrency", "offers.availability"]
    else:
        if not _offer_price_present(offers):
            missing_required.append("offers.price")
        if not _offer_field_present(offers, "priceCurrency"):
            missing_required.append("offers.priceCurrency")
        if not _offer_field_present(offers, "availability"):
            missing_required.append("offers.availability")

    missing_recommended = [f for f in RECOMMENDED_FIELDS if not _has(node, f)]
    return missing_required, missing_recommended


def extract_product_schema(parser: PageParser) -> dict | None:
    """Find the best Product node on the page and validate it.

    'Best' = the one with the fewest missing required fields, so a page that
    ships both a stub and a complete node is judged on the complete one.
    """
    best = None
    for blob in parser.jsonld_raw:
        blob = blob.strip()
        if not blob:
            continue
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            # Some themes emit trailing commas or concatenated objects.
            try:
                data = json.loads(re.sub(r",\s*([}\]])", r"\1", blob))
            except json.JSONDecodeError:
                continue

        for node in _iter_nodes(data):
            if not isinstance(node, dict):
                continue
            types = _types_of(node)
            if "product" in types or "productgroup" in types:
                missing_required, missing_recommended = validate_product_node(node)
                candidate = {
                    "missing_required": missing_required,
                    "missing_recommended": missing_recommended,
                    "merchant_ready": not missing_required,
                    "schema_type": sorted(types),
                }
                if best is None or len(missing_required) < len(best["missing_required"]):
                    best = candidate
    return best


# --- Crawl discovery ---------------------------------------------------------

def find_offline_root(crawl_dir: Path) -> Path | None:
    """Locate the directory holding the mirrored site."""
    for candidate in ("offline", "offline-export", "export"):
        sub = crawl_dir / candidate
        if sub.is_dir():
            return sub
    if any(crawl_dir.rglob("*.html")):
        return crawl_dir
    return None


def html_files(root: Path) -> list[Path]:
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in (".html", ".htm")]
    return sorted(files)


# The crawler writes a tiny meta-refresh stub next to each real page unless
# --offline-export-no-auto-redirect-html is passed. Counting those would double
# every total, so they are skipped no matter how the crawl was run.
REDIRECT_STUB_PAT = re.compile(r"http-equiv\s*=\s*[\"']?refresh", re.I)


def is_redirect_stub(html: str) -> bool:
    return (
        len(html) < 2000
        and bool(REDIRECT_STUB_PAT.search(html))
        and "<body" not in html.lower()
    )


def load_inventory(crawl_dir: Path, offline_root: Path) -> list[tuple[str, Path]] | None:
    """Map exported files to their real URLs using the crawler's JSON inventory.

    This beats reconstructing URLs from file paths: it gives the exact URL the
    crawler requested, and its status codes let us drop 404s and redirects so
    error pages never get audited as though they were real pages.
    """
    inventory_file = None
    for name in ("crawl.json", "output.json", "report.json"):
        candidate = crawl_dir / name
        if candidate.is_file():
            inventory_file = candidate
            break
    if inventory_file is None:
        return None

    try:
        data = json.loads(inventory_file.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return None

    results = data.get("results")
    if not isinstance(results, list):
        return None

    pages: list[tuple[str, Path]] = []
    for entry in results:
        if not isinstance(entry, dict):
            continue
        url = entry.get("url")
        offline = entry.get("offlineFilePath")
        if not url or not offline:
            continue
        status = str(entry.get("status", "")).strip()
        if status and not status.startswith("2"):
            continue
        candidate_file = offline_root / offline
        if candidate_file.is_file() and candidate_file.suffix.lower() in (".html", ".htm"):
            pages.append((url, candidate_file))

    return pages or None


def url_for_file(path: Path, root: Path, base_url: str) -> str:
    """Reconstruct the live URL a mirrored file corresponds to."""
    rel = path.relative_to(root)
    parts = list(rel.parts)

    base_host = urlparse(base_url).netloc.lower()
    # Offline exports usually nest under a <host>/ directory; drop it if present.
    if parts and parts[0].lower().replace("www.", "") == base_host.replace("www.", ""):
        parts = parts[1:]

    if parts and parts[-1].lower() in ("index.html", "index.htm"):
        parts = parts[:-1]
        tail = "/".join(parts)
        return urljoin(base_url, "/" + tail + ("/" if tail else ""))

    if parts:
        parts[-1] = re.sub(r"\.html?$", "", parts[-1], flags=re.I)
    return urljoin(base_url, "/" + "/".join(parts))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# --- robots.txt --------------------------------------------------------------

def find_robots(crawl_dir: Path) -> tuple[str, str] | tuple[None, None]:
    for candidate in sorted(crawl_dir.rglob("robots.txt")):
        if candidate.is_file():
            text = read_text(candidate)
            if text.strip():
                return text, str(candidate)
    return None, None


def analyse_robots(crawl_dir: Path, live_paths: dict[str, list[str]]) -> dict:
    """Parse robots.txt and work out which Disallow rules hit money pages."""
    text, source = find_robots(crawl_dir)
    if text is None:
        return {
            "found": False,
            "source": None,
            "note": "robots.txt not found in the crawl. Fetch it with web_fetch and "
                    "save it to <crawl-dir>/robots.txt, then re-run.",
            "blanket_disallow": False,
            "rules": [],
            "blocking": [],
            "benign": [],
            "sitemaps": [],
        }

    groups: list[dict] = []
    current: dict | None = None
    sitemaps: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field = field.strip().lower()
        value = value.strip()

        if field == "user-agent":
            if current is None or current.get("_closed"):
                current = {"user_agents": [], "disallow": [], "allow": [], "_closed": False}
                groups.append(current)
            current["user_agents"].append(value)
        elif field == "disallow" and current is not None:
            current["_closed"] = True
            current["disallow"].append(value)
        elif field == "allow" and current is not None:
            current["_closed"] = True
            current["allow"].append(value)
        elif field == "sitemap":
            sitemaps.append(value)

    for g in groups:
        g.pop("_closed", None)

    blanket = False
    rules: list[dict] = []
    blocking: list[dict] = []
    benign: list[dict] = []

    for group in groups:
        agents = ", ".join(group["user_agents"]) or "*"
        for rule in group["disallow"]:
            if not rule:
                continue  # "Disallow:" with no value allows everything
            entry = {"user_agent": agents, "path": rule}

            if rule.strip() == "/":
                blanket = True
                entry.update(severity="critical", reason="Blanket Disallow: / blocks the entire site")
                blocking.append(entry)
                rules.append(entry)
                continue

            prefix = rule.split("*")[0].rstrip("$")
            hit_types = []
            for page_type in ("category", "product", "blog"):
                for p in live_paths.get(page_type, []):
                    if prefix and p.startswith(prefix):
                        hit_types.append(page_type)
                        break

            if hit_types:
                entry.update(
                    severity="high",
                    reason=f"Blocks crawled {', '.join(sorted(set(hit_types)))} pages",
                    blocks=sorted(set(hit_types)),
                )
                blocking.append(entry)
            elif BENIGN_ROBOTS_PAT.match(rule) or "?" in rule or "=" in rule:
                entry.update(severity="benign", reason="Faceted, parameter or utility path")
                benign.append(entry)
            else:
                entry.update(severity="review", reason="No crawled page matched this prefix")
                benign.append(entry)

            rules.append(entry)

    return {
        "found": True,
        "source": source,
        "blanket_disallow": blanket,
        "groups": groups,
        "rules": rules,
        "blocking": blocking,
        "benign": benign,
        "sitemaps": sitemaps,
    }


# --- Per-page analysis -------------------------------------------------------

def resolve_links(parser: PageParser, page_url: str, base_host: str) -> list[tuple[int, str, str]]:
    """Return (word_pos, absolute_url, path) for same-host links only."""
    out = []
    for pos, href in parser.links:
        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        absolute = urljoin(page_url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc and parsed.netloc.lower().replace("www.", "") != base_host:
            continue
        out.append((pos, absolute.split("#")[0], parsed.path))
    return out


def analyse_category(parser: PageParser, url: str, links: list) -> dict:
    product_positions = [pos for pos, _, path in links if classify_path(path) == "product"]
    path = urlparse(url).path

    if product_positions:
        first, last = min(product_positions), max(product_positions)
        abf_words = sum(len(t.split()) for pos, t in parser.paragraphs if pos < first)
        btf_words = sum(len(t.split()) for pos, t in parser.paragraphs if pos > last)
    else:
        # No product links found: cannot split above/below the grid.
        abf_words = btf_words = 0

    own_segs = path_segments(path)
    links_to_parent = False
    links_to_children = 0
    for _, _, link_path in links:
        if classify_path(link_path) != "category":
            continue
        link_segs = path_segments(link_path)
        if link_segs == own_segs:
            continue
        if len(link_segs) < len(own_segs) and own_segs[:len(link_segs)] == link_segs:
            links_to_parent = True
        elif len(link_segs) > len(own_segs) and link_segs[:len(own_segs)] == own_segs:
            links_to_children += 1

    return {
        "url": url,
        "path": path,
        "slug": category_slug(path),
        "title": parser.title,
        "h1": parser.h1s[0] if parser.h1s else "",
        "product_links": len(product_positions),
        "abf_words": abf_words,
        "abf_present": abf_words >= ABF_MIN_WORDS,
        "btf_words": btf_words,
        "btf_present": btf_words >= BTF_MIN_WORDS,
        "links_to_parent": links_to_parent,
        "links_to_children": links_to_children,
        "assessable": bool(product_positions),
    }


def analyse_product(parser: PageParser, url: str) -> dict:
    intro_words = 0
    for pos, text in parser.paragraphs:
        if pos <= INTRO_WITHIN_WORDS:
            intro_words = max(intro_words, len(text.split()))

    c = parser.counts
    specs_present = (
        (c["table"] >= 1 and c["tr"] >= 3)
        or (c["dl"] >= 1 and c["dt"] >= 3)
        or (c["ul"] >= 1 and c["li"] >= 4)
    )
    scannable_signals = [
        (len(parser.h2s) + len(parser.h3s)) >= 2,
        (c["ul"] + c["ol"] + c["dl"]) >= 1,
        c["table"] >= 1,
    ]

    schema = extract_product_schema(parser)
    result = {
        "url": url,
        "title": parser.title,
        "h1_present": bool(parser.h1s),
        "h1": parser.h1s[0] if parser.h1s else "",
        "intro_present": intro_words >= INTRO_MIN_WORDS,
        "intro_words": intro_words,
        "specs_present": specs_present,
        "scannable": sum(scannable_signals) >= 2,
        "word_count": parser.words,
    }

    if schema:
        result.update(
            has_product_schema=True,
            merchant_ready=schema["merchant_ready"],
            missing_required=schema["missing_required"],
            missing_recommended=schema["missing_recommended"],
            schema_type=schema["schema_type"],
        )
    else:
        result.update(
            has_product_schema=False,
            merchant_ready=False,
            missing_required=list(REQUIRED_FIELDS),
            missing_recommended=list(RECOMMENDED_FIELDS),
            schema_type=[],
        )
    return result


def analyse_blog(parser: PageParser, url: str, links: list) -> dict:
    commercial = [
        (pos, absolute) for pos, absolute, path in links
        if classify_path(path) in ("product", "category")
    ]
    first_pos = min((pos for pos, _ in commercial), default=None)
    threshold = min(EARLY_TIE_BACK_WORDS, max(50, int(parser.words * 0.25))) if parser.words else EARLY_TIE_BACK_WORDS

    return {
        "url": url,
        "title": parser.title,
        "word_count": parser.words,
        "tie_back": bool(commercial),
        "early_tie_back": first_pos is not None and first_pos <= threshold,
        "first_tie_back_word": first_pos,
        "commercial_links": sorted({absolute for _, absolute in commercial})[:10],
        "commercial_link_count": len(commercial),
    }


# --- Main --------------------------------------------------------------------

def build_findings(crawl_dir: Path, base_url: str, max_products: int, max_blogs: int) -> dict:
    notes: list[str] = []
    root = find_offline_root(crawl_dir)
    if root is None:
        return {
            "meta": {
                "base_url": base_url,
                "crawl_dir": str(crawl_dir),
                "generated": date.today().isoformat(),
                "pages_analysed": 0,
                "notes": [
                    "No offline HTML export found. Re-run scripts/run_crawl.sh, or point "
                    "--crawl-dir at the directory containing the mirrored site."
                ],
            },
            "counts": {},
            "category_slugs": [],
            "categories": [],
            "products": [],
            "schema_summary": {},
            "blogs": [],
            "key_pages": {},
            "robots": analyse_robots(crawl_dir, {}),
        }

    base_host = urlparse(base_url).netloc.lower().replace("www.", "")

    inventory = load_inventory(crawl_dir, root)
    if inventory:
        candidates: list[tuple[str | None, Path]] = list(inventory)
    else:
        candidates = [(None, f) for f in html_files(root)]
        notes.append(
            "No JSON inventory found, so URLs were reconstructed from file paths. "
            "Any error pages saved by the crawler may be counted as real pages."
        )
    if not candidates:
        notes.append("Offline export directory exists but contains no HTML files.")

    pages: list[dict] = []
    for url_hint, path in candidates:
        html = read_text(path)
        if not html.strip() or is_redirect_stub(html):
            continue
        parser = parse_page(html)

        # The inventory URL is what the crawler actually requested, so it wins.
        url = url_hint or parser.canonical or parser.og_url or url_for_file(path, root, base_url)
        if not urlparse(url).netloc:
            url = url_for_file(path, root, base_url)
        url_path = urlparse(url).path or "/"

        page_type = classify_path(url_path)
        # og:type is a strong product signal when the URL pattern is unusual.
        if page_type != "product" and parser.og_type.lower() in ("product", "og:product"):
            page_type = "product"

        pages.append({
            "file": path,
            "parser": parser,
            "url": url,
            "path": url_path,
            "type": page_type,
            "flags": page_flags(url_path, parser.title),
        })

    counts: dict[str, int] = {}
    for page in pages:
        counts[page["type"]] = counts.get(page["type"], 0) + 1

    live_paths: dict[str, list[str]] = {}
    for page in pages:
        live_paths.setdefault(page["type"], []).append(page["path"])

    categories, products, blogs = [], [], []
    for page in pages:
        parser = page["parser"]
        links = resolve_links(parser, page["url"], base_host)
        if page["type"] == "category":
            categories.append(analyse_category(parser, page["url"], links))
        elif page["type"] == "product":
            products.append(analyse_product(parser, page["url"]))
        elif page["type"] == "blog":
            blogs.append(analyse_blog(parser, page["url"], links))

    if len(products) > max_products:
        notes.append(f"Sampled {max_products} of {len(products)} product pages found (use --max-products to raise).")
        products = products[:max_products]
    if len(blogs) > max_blogs:
        notes.append(f"Sampled {max_blogs} of {len(blogs)} blog posts found (use --max-blogs to raise).")
        blogs = blogs[:max_blogs]

    if not products:
        notes.append("No product pages were classified. The store may use unusual URL patterns; "
                     "check the crawl before concluding anything about Product schema.")
    if not categories:
        notes.append("No category pages were classified. Check the crawl depth and URL patterns.")

    missing_counts: dict[str, int] = {}
    for product in products:
        for field in product["missing_required"]:
            missing_counts[field] = missing_counts.get(field, 0) + 1

    schema_summary = {
        "product_pages": len(products),
        "with_schema": sum(1 for p in products if p["has_product_schema"]),
        "no_schema": sum(1 for p in products if not p["has_product_schema"]),
        "merchant_ready": sum(1 for p in products if p["merchant_ready"]),
        "missing_required_counts": dict(sorted(missing_counts.items(), key=lambda kv: -kv[1])),
        "required_fields": list(REQUIRED_FIELDS),
        "recommended_fields": list(RECOMMENDED_FIELDS),
    }

    key_pages = {}
    for flag, label in (("is_return", "return"), ("is_about", "about"), ("is_seasonal", "seasonal")):
        urls = [p["url"] for p in pages if p["flags"][flag]]
        key_pages[label] = {"found": bool(urls), "count": len(urls), "urls": sorted(urls)[:10]}

    category_slugs = sorted({c["slug"] for c in categories if c["slug"]})

    return {
        "meta": {
            "base_url": base_url,
            "crawl_dir": str(crawl_dir),
            "offline_export_root": str(root),
            "generated": date.today().isoformat(),
            "pages_analysed": len(pages),
            "thresholds": {
                "abf_min_words": ABF_MIN_WORDS,
                "btf_min_words": BTF_MIN_WORDS,
                "intro_min_words": INTRO_MIN_WORDS,
                "early_tie_back_words": EARLY_TIE_BACK_WORDS,
            },
            "notes": notes,
        },
        "counts": counts,
        "category_slugs": category_slugs,
        "categories": categories,
        "products": products,
        "schema_summary": schema_summary,
        "blogs": blogs,
        "key_pages": key_pages,
        "robots": analyse_robots(crawl_dir, live_paths),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyse a SiteOne crawl of an online store.")
    ap.add_argument("--crawl-dir", required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-products", type=int, default=60)
    ap.add_argument("--max-blogs", type=int, default=30)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    crawl_dir = Path(args.crawl_dir)
    if not crawl_dir.is_dir():
        sys.stderr.write(f"ERROR: crawl directory not found: {crawl_dir}\n")
        return 1

    findings = build_findings(crawl_dir, args.base_url.rstrip("/"), args.max_products, args.max_blogs)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")

    if not args.quiet:
        counts = findings["counts"]
        schema = findings["schema_summary"]
        sys.stderr.write(
            f"Analysed {findings['meta']['pages_analysed']} pages "
            f"(category {counts.get('category', 0)}, product {counts.get('product', 0)}, "
            f"blog {counts.get('blog', 0)}).\n"
            f"Product schema: {schema.get('merchant_ready', 0)} of "
            f"{schema.get('product_pages', 0)} PDPs Merchant-ready.\n"
        )
        for note in findings["meta"]["notes"]:
            sys.stderr.write(f"NOTE: {note}\n")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
