#!/usr/bin/env python3
"""Format SE Ranking API JSON into workshop-friendly markdown + CSV.

Stdlib only — no pip install needed.

Usage:
  python3 format_results.py --json <path> --mode <mode> --seed <seed> [--out-dir <dir>]

Modes:
  keywords         — for /keywords/related, /similar, /questions, /export
  longtail         — for /keywords/longtail (phrases only, no metrics)
  domain-keywords  — for /domain/keywords (per-keyword ranking data)
  domain-overview  — for /domain/overview/db (summary stats)
  gap              — for /domain/keywords/comparison (competitor gap)

Output:
  <out-dir>/<seed-slug>-<YYYY-MM-DD>.md   (markdown table + recommendations)
  <out-dir>/<seed-slug>-<YYYY-MM-DD>.csv  (spreadsheet, opens in Excel/Numbers/Sheets)

Defaults <out-dir> to ./keyword-research/ (workspace-relative).
"""
import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path


INTENT_NAMES = {
    "I": "Informational",
    "C": "Commercial",
    "T": "Transactional",
    "L": "Local",
    "N": "Navigational",
}

SERP_FEATURE_NAMES = {
    "local_pack": "Local Pack (map)",
    "reviews": "Reviews",
    "video": "Video carousel",
    "people_also_ask": "People Also Ask",
    "images": "Image carousel",
    "related_searches": "Related searches",
    "featured_snippets": "Featured snippet",
    "sge": "Google AI Overview",
    "ai_overview": "Google AI Overview",
    "knowledge_panel": "Knowledge panel",
    "shopping": "Shopping results",
    "twitter": "X/Twitter results",
    "news": "Top stories",
    "site_links": "Sitelinks",
    "answer_box": "Answer box",
    "ads_top": "Ads (top)",
    "ads_bottom": "Ads (bottom)",
    "tads": "Ads (top)",
    "bads": "Ads (bottom)",
    "thumbnail": "Thumbnails",
    "hotels_pack": "Hotels pack",
    "flights_pack": "Flights pack",
    "jobs": "Jobs results",
    "tweets": "Tweets",
    "directions": "Directions",
    "discussions_and_forums": "Discussions & forums",
    "gmb": "Google Business Profile",
    "google_business_profile": "Google Business Profile",
    "map": "Map",
    "events": "Events",
    "recipes": "Recipes",
    "podcasts": "Podcasts",
}


def translate_intents(intents):
    if not intents:
        return ""
    return " + ".join(INTENT_NAMES.get(i.upper(), i) for i in intents)


def translate_serp_features(features):
    if not features:
        return ""
    return ", ".join(SERP_FEATURE_NAMES.get(f, f) for f in features)


def slugify(s):
    s = re.sub(r"^https?://", "", s.lower())
    s = re.sub(r"^www\.", "", s)
    # Keep dots and slashes as separators rather than dropping them entirely
    s = re.sub(r"[/.]+", "-", s)
    s = re.sub(r"[^\w\s-]", "", s).strip()
    return re.sub(r"[\s_-]+", "-", s)[:60]


def fmt_int(n):
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return "—"


def fmt_money(v):
    try:
        return f"${float(v):.2f}"
    except (TypeError, ValueError):
        return "—"


def score(k):
    """Workshop ranking: prefers relevant matches over generic high-volume.

    relevance is squared so low-relevance keywords drop hard even if volume
    is huge — workshop attendees want on-topic matches for their business,
    not generic head terms.
    """
    vol = float(k.get("volume") or 0)
    kd = float(k.get("difficulty") or 50)
    rel = float(k.get("relevance") or 50)
    intents = [i.upper() for i in (k.get("intents") or [])]
    bonus = 1.3 if ("C" in intents or "T" in intents) else 1.1 if "I" in intents else 1.0
    penalty = max(0.0, (kd - 60) * 50) if kd > 60 else 0.0
    rel_factor = (rel / 50.0) ** 2
    return (vol * bonus * rel_factor) - penalty


def format_keywords(data, seed, out_dir):
    rows = data.get("keywords", [])

    if rows and isinstance(rows[0], str):
        return format_longtail(data, seed, out_dir)

    rows_sorted = sorted(rows, key=score, reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(seed)
    md_path = out_dir / f"{slug}-{today}.md"
    csv_path = out_dir / f"{slug}-{today}.csv"

    headers = [
        "Keyword",
        "Searches/month",
        "Difficulty (0-100)",
        "Top intent",
        "On-topic %",
        "Value per click",
        "SERP features",
    ]

    md = [
        f"# Keyword research — {seed}",
        "",
        f"Generated {today}. {data.get('total', len(rows))} total candidates in SE Ranking, {len(rows)} returned.",
        "Sorted by on-topic relevance, then monthly searches (workshop default).",
        "",
        "## Top picks to target first",
        "",
        "_Criteria: on-topic ≥30% AND difficulty ≤60 — keywords you can realistically rank for and that actually match your business._",
        "",
    ]

    picks = [k for k in rows_sorted if (k.get("relevance") or 0) >= 30 and (k.get("difficulty") or 100) <= 60][:3]

    if not picks:
        md.append("_No strong picks in this batch (nothing met the on-topic ≥30% + difficulty ≤60 criteria)._")
        md.append("")
        md.append("Try a different seed phrase (more specific to your business — add your location or service type), or run `/keywords/longtail` to see narrower phrases.")
    else:
        for i, p in enumerate(picks, 1):
            intent = translate_intents(p.get("intents", []))
            md.append(
                f"{i}. **{p.get('keyword', '?')}** — "
                f"{fmt_int(p.get('volume'))} searches/mo, "
                f"difficulty {p.get('difficulty', '?')}/100, "
                f"on-topic {p.get('relevance', '?')}%, "
                f"intent: {intent or '—'}, "
                f"value/click {fmt_money(p.get('cpc'))}"
            )
        if len(picks) < 3:
            md.append("")
            md.append(f"_Only {len(picks)} strong pick(s) in this batch. Run a wider `limit=` or try a different seed to surface more._")

    # High commercial value callout — keywords with CPC >= $10
    high_cpc = [k for k in rows_sorted if (k.get("cpc") or 0) >= 10][:5]
    if high_cpc:
        md += [
            "",
            "## High commercial value (CPC $10+)",
            "",
            "_These are what businesses pay top dollar for in Google Ads. Every organic click you steal is worth what's in the CPC column. Big CPC × big volume = big prize._",
            "",
        ]
        for k in high_cpc:
            cpc_val = float(k.get("cpc") or 0)
            vol_val = float(k.get("volume") or 0)
            monthly_value = cpc_val * vol_val
            md.append(
                f"- **{k.get('keyword', '?')}** — {fmt_money(cpc_val)}/click × {fmt_int(vol_val)} searches/mo "
                f"= **{fmt_money(monthly_value)}** in equivalent ad spend per month"
            )

    md += ["", "## All keywords", "", "| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for k in rows_sorted:
        md.append(
            "| " + " | ".join([
                str(k.get("keyword", "")),
                fmt_int(k.get("volume")),
                str(k.get("difficulty", "—")),
                translate_intents(k.get("intents", [])) or "—",
                str(k.get("relevance", "—")),
                fmt_money(k.get("cpc")),
                translate_serp_features(k.get("serp_features", [])) or "—",
            ]) + " |"
        )

    md += [
        "",
        "## What to do next",
        "",
        "1. Pick the **Top 3** above. Each becomes a page on your site — usually a service page, location page, or buying-guide blog post.",
        "2. For each chosen keyword, check Google to see what type of pages already rank. Match that format on your own site.",
        "3. If **People Also Ask** appears in SERP features, scroll those questions on Google and mine them for FAQ content on your page.",
        "4. If **Local Pack (map)** appears, your Google Business Profile matters as much as the page itself. Make sure your GBP is fully filled out for this service + location.",
        "5. Difficulty (KD) under 30 with reasonable volume (>200/mo) = a quick win. Build these first.",
        "6. **Watch the Value per click column.** Anything $10+ is a high-commercial-intent keyword — businesses pay that much per click in Google Ads. Ranking organically = recurring savings. The bigger the CPC × volume, the bigger the prize.",
        "7. Anything with **on-topic %** under 30 is the API saying \"this is a stretch from your seed.\" Skip unless you have a specific reason.",
        "",
    ]

    md_path.write_text("\n".join(md))

    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(headers)
        for k in rows_sorted:
            w.writerow([
                k.get("keyword", ""),
                k.get("volume", ""),
                k.get("difficulty", ""),
                translate_intents(k.get("intents", [])),
                k.get("relevance", ""),
                k.get("cpc", ""),
                translate_serp_features(k.get("serp_features", [])),
            ])

    return md_path, csv_path


def format_longtail(data, seed, out_dir):
    rows = data.get("keywords", [])
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(seed)
    md_path = out_dir / f"{slug}-longtail-{today}.md"
    csv_path = out_dir / f"{slug}-longtail-{today}.csv"

    md = [
        f"# Longtail phrases — {seed}",
        "",
        f"Generated {today}. {data.get('total', len(rows))} total candidates, {len(rows)} shown.",
        "Longtail returns phrases only — no search volume yet.",
        "",
        "## Phrases",
        "",
    ]
    md.extend(f"- {phrase}" for phrase in rows)
    md += [
        "",
        "## What to do next",
        "",
        "1. Read through the phrases. Mark the 10–20 that match real questions or products your business answers.",
        "2. Ask Claude: \"Get search volume and difficulty for these keywords: [paste your list].\" Claude will use the `/keywords/export` endpoint (100 credits flat) to pull metrics for the whole batch.",
        "3. From the metrics, pick the 3–5 strongest and build pages/blog posts around them.",
        "",
    ]
    md_path.write_text("\n".join(md))

    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Phrase"])
        for phrase in rows:
            w.writerow([phrase])

    return md_path, csv_path


def format_domain_keywords(data, domain, out_dir):
    # /domain/keywords returns a top-level list of keyword rows.
    # Some other shapes wrap them in {keywords: [...]} or {data: [...]}.
    if isinstance(data, list):
        rows = data
    else:
        rows = data.get("keywords") or data.get("data") or []
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(domain)
    md_path = out_dir / f"{slug}-rankings-{today}.md"
    csv_path = out_dir / f"{slug}-rankings-{today}.csv"

    headers = ["Keyword", "Position", "URL", "Searches/mo", "Difficulty", "Traffic estimate"]

    total = (data.get("total") if isinstance(data, dict) else None) or len(rows)
    md = [
        f"# Organic rankings — {domain}",
        "",
        f"Generated {today}. {total} ranking keywords found, {len(rows)} shown.",
        "",
        "## Quick wins (positions 4–15 — the page-1 frontier)",
        "",
    ]

    frontier = [r for r in rows if 4 <= (r.get("position") or 0) <= 15]
    frontier.sort(key=lambda r: -(r.get("volume") or 0))
    for r in frontier[:10]:
        md.append(
            f"- **{r.get('keyword', '?')}** — position {r.get('position', '?')}, "
            f"{fmt_int(r.get('volume'))} searches/mo, "
            f"URL: {r.get('url', '?')}"
        )
    if not frontier:
        md.append("_(none found in positions 4–15)_")

    md += ["", "## All ranking keywords", "", "| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        md.append("| " + " | ".join([
            str(r.get("keyword", "")),
            str(r.get("position", "—")),
            str(r.get("url", "")),
            fmt_int(r.get("volume")),
            str(r.get("difficulty", "—")),
            fmt_int(r.get("traffic")),
        ]) + " |")

    md += [
        "",
        "## What to do next",
        "",
        "1. Focus on the **Quick wins** list above. These are keywords where you already rank on page 2 — small improvements get you to page 1.",
        "2. For each quick win, open the page that's currently ranking. Look at what's missing vs the page-1 results: word count, headings, internal links, images.",
        "3. Add the missing content. Re-publish. Wait 2–4 weeks. Check rank again.",
        "4. Keywords ranking 1–3: protect these. Don't let the pages go stale.",
        "5. Keywords ranking 16+: deprioritise unless they're high commercial value — too far back to move easily.",
        "",
    ]
    md_path.write_text("\n".join(md))

    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(headers)
        for r in rows:
            w.writerow([
                r.get("keyword", ""),
                r.get("position", ""),
                r.get("url", ""),
                r.get("volume", ""),
                r.get("difficulty", ""),
                r.get("traffic", ""),
            ])

    return md_path, csv_path


def format_domain_overview(data, domain, out_dir):
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(domain)
    md_path = out_dir / f"{slug}-overview-{today}.md"
    csv_path = out_dir / f"{slug}-overview-{today}.csv"

    # SE Ranking wraps the stats in an "organic" object
    s = data.get("organic") or data.get("summary") or data
    if isinstance(s, list) and s:
        s = s[0]

    def pick(*names):
        for n in names:
            if n in s and s[n] not in (None, ""):
                return s[n]
        return None

    metrics = [
        ("Total ranking keywords", pick("keywords_count", "total_keywords")),
        ("Estimated monthly traffic", pick("traffic_sum", "total_traffic", "traffic")),
        ("Traffic value (Google Ads equivalent, monthly)", pick("price_sum", "total_traffic_cost", "traffic_cost")),
        ("Keywords in top 1–5", pick("top1_5", "top_3_keywords_count")),
        ("Keywords in top 6–10", pick("top6_10")),
        ("Keywords in positions 11–20 (page-2 frontier)", pick("top11_20", "top_11_20_keywords_count")),
        ("Keywords in positions 21–50", pick("top21_50")),
        ("Keywords in positions 51–100", pick("top51_100")),
    ]
    movement = [
        ("Keywords moving up", pick("keywords_up_count")),
        ("Keywords moving down", pick("keywords_down_count")),
        ("Keywords stable", pick("keywords_equal_count")),
        ("New keywords this period", pick("keywords_new_count")),
        ("Lost keywords this period", pick("keywords_lost_count")),
    ]

    period_year = pick("year")
    period_month = pick("month")
    period_str = f"{period_year}-{period_month:02d}" if period_year and period_month else "current period"

    md = [
        f"# Domain overview — {domain}",
        "",
        f"Generated {today}. Source: SE Ranking `/v1/domain/overview/db` (AU database). Stats for {period_str}.",
        "",
        "## Headline numbers",
        "",
    ]
    for label, value in metrics:
        if value is not None:
            if "Traffic value" in label:
                md.append(f"- **{label}:** {fmt_money(value)}")
            else:
                md.append(f"- **{label}:** {fmt_int(value)}")

    md += ["", "## Movement this period", ""]
    for label, value in movement:
        if value is not None:
            md.append(f"- **{label}:** {fmt_int(value)}")

    # Quick read of current state for the recommendation
    total_kw = pick("keywords_count", "total_keywords") or 0
    top10 = (pick("top1_5") or 0) + (pick("top6_10") or 0)
    page2 = pick("top11_20") or 0
    traffic = pick("traffic_sum") or 0
    up = pick("keywords_up_count") or 0
    down = pick("keywords_down_count") or 0

    md += ["", "## What to do next", ""]
    if total_kw < 20:
        md.append("1. You have **almost no organic presence yet** (under 20 ranking keywords). The priority is publishing your first 5–10 service or location pages. Use `keyword-research` to find what to target.")
    elif total_kw < 100:
        md.append(f"1. You have **{total_kw} ranking keywords** — small footprint. Focus on adding ~10 more well-targeted pages over the next quarter. Use `keyword-research` for ideas.")
    else:
        md.append(f"1. You have **{total_kw} ranking keywords** — solid footprint. Focus on quality over quantity from here.")

    if top10 < 5 and page2 >= 3:
        md.append(f"2. You have **{page2} keywords on page 2 (positions 11–20)** but only **{top10} in the top 10**. These page-2 keywords are your fastest wins — small on-page improvements (better title tag, more content, internal links) can push them into the top 10. Use `/domain/keywords` to see exactly which ones.")
    elif top10 >= 5:
        md.append(f"2. You have **{top10} keywords in the top 10** — protect these pages. Don't let them go stale. Run a fresh `/domain/keywords` query monthly to spot drops early.")

    if traffic < 100:
        md.append(f"3. Traffic estimate is **{fmt_int(traffic)}/mo** — very low. Rankings without clicks usually means you're ranking on terms that don't drive volume, or you're sitting just below page 1. Quick wins (item 2) are the lever.")

    if up > down:
        md.append(f"4. Good momentum: **{up} keywords moved up** vs **{down} down**. Keep doing what's working.")
    elif down > up:
        md.append(f"4. Caution: **{down} keywords moved down** vs **{up} up**. Look at what changed on your site recently — content edits, redirects, site speed. Run a tech audit if you haven't.")

    md.append("5. The **Traffic value** number is what the same clicks would cost you in Google Ads — that's the dollar value of your organic work each month.")
    md.append("")

    md_path.write_text("\n".join(md))

    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Metric", "Value"])
        for label, value in metrics + movement:
            if value is not None:
                w.writerow([label, value])

    return md_path, csv_path


def format_gap(data, target, out_dir):
    """Consumes /v1/domain/competitors output — a top-level list of competitor
    summaries with common_keywords, total_keywords, missing_keywords, traffic, value.

    Note: SE Ranking's /v1/domain/keywords/comparison endpoint exists but its
    param shape is currently unclear (returns "Bad request" for the obvious
    forms). The /competitors endpoint gives workshop attendees better data
    anyway: it tells them WHO they're competing with, plus the size of each
    gap, in a single 100-cr call.
    """
    rows = data if isinstance(data, list) else (data.get("competitors") or data.get("data") or [])
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(target)
    md_path = out_dir / f"{slug}-competitors-{today}.md"
    csv_path = out_dir / f"{slug}-competitors-{today}.csv"

    headers = [
        "Competitor",
        "Their total keywords",
        "Keywords you both rank for",
        "Keywords they have, you don't",
        "Their monthly traffic",
        "Their traffic value ($)",
        "Relevance to you",
    ]

    # Sort by missing_keywords desc — biggest gap = biggest opportunity
    rows_sorted = sorted(rows, key=lambda r: -(r.get("missing_keywords") or 0))

    md = [
        f"# Competitor analysis — {target}",
        "",
        f"Generated {today}. {len(rows)} competitors found by SE Ranking based on shared rankings.",
        "Sorted by **keywords they have that you don't** — biggest opportunities first.",
        "",
        "## Top 5 competitors to study",
        "",
    ]

    for i, r in enumerate(rows_sorted[:5], 1):
        gap = r.get("missing_keywords") or 0
        common = r.get("common_keywords") or 0
        total = r.get("total_keywords") or 0
        rel = r.get("domain_relevance") or 0
        md.append(
            f"{i}. **{r.get('domain', '?')}** — "
            f"{fmt_int(gap)} keywords they have that you don't, "
            f"{fmt_int(common)} overlap, "
            f"{fmt_int(total)} total. "
            f"Relevance to your business: {rel}/100."
        )

    md += [
        "",
        "## All competitors",
        "",
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for r in rows_sorted:
        md.append("| " + " | ".join([
            str(r.get("domain", "")),
            fmt_int(r.get("total_keywords")),
            fmt_int(r.get("common_keywords")),
            fmt_int(r.get("missing_keywords")),
            fmt_int(r.get("traffic_sum")),
            fmt_money(r.get("price_sum")),
            str(r.get("domain_relevance", "—")),
        ]) + " |")

    md += [
        "",
        "## What to do next",
        "",
        "1. **Focus on the top 2–3 competitors with high relevance** (Relevance to you > 30). Low-relevance entries are weak matches — SE Ranking is reaching.",
        "2. For each chosen competitor, visit their site. What pages are doing the heavy lifting? Service pages? Location pages? Blog posts? That tells you the shape of content Google rewards in your niche.",
        "3. To see the actual keywords they rank for that you don't, ask Claude: \"Show me the top keywords [competitor.com.au] ranks for.\" That runs `/domain/keywords` (100 cr flat) on the competitor.",
        "4. Pick 3 missing keywords per quarter and build pages targeting them. Don't try to fill the whole gap at once.",
        "5. Their **traffic value** is the dollar-equivalent of their organic clicks each month — useful context for how big the competitor really is online.",
        "",
    ]
    md_path.write_text("\n".join(md))

    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(headers)
        for r in rows_sorted:
            w.writerow([
                r.get("domain", ""),
                r.get("total_keywords", ""),
                r.get("common_keywords", ""),
                r.get("missing_keywords", ""),
                r.get("traffic_sum", ""),
                r.get("price_sum", ""),
                r.get("domain_relevance", ""),
            ])

    return md_path, csv_path


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", required=True, help="Path to saved JSON response")
    ap.add_argument("--mode", required=True,
                    choices=["keywords", "longtail", "domain-keywords", "domain-overview", "gap"])
    ap.add_argument("--seed", required=True, help="Seed keyword or domain — used for filename + title")
    ap.add_argument("--out-dir", default="./keyword-research", help="Output directory (default: ./keyword-research)")
    args = ap.parse_args(argv)

    data = json.loads(Path(args.json).read_text())
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    handlers = {
        "keywords": format_keywords,
        "longtail": format_longtail,
        "domain-keywords": format_domain_keywords,
        "domain-overview": format_domain_overview,
        "gap": format_gap,
    }
    md_path, csv_path = handlers[args.mode](data, args.seed, out_dir)

    print(f"📄 Markdown summary: {md_path}")
    print(f"📊 Spreadsheet:      {csv_path}")


if __name__ == "__main__":
    main(sys.argv[1:])
