#!/usr/bin/env python3
"""
SE Ranking Data API helper — shared by all three phases of the Source Content Engine.

Self-contained: Python standard library only (no pip install needed).
Reads the API key from the SE_RANKING_API_KEY environment variable.

Two output modes:
  * default  — writes a paired .md + .csv into ./keyword-research/ and prints
               the markdown summary to stdout (Phase 1 deliverable).
  * --json   — prints the raw rows as JSON to stdout and writes NO files
               (used by Phase 2 cluster + Phase 3 brief to chain data).

Commands:
  smoke
  keywords        --seed "<service>" --source au --limit 25 [--method similar|related]
  longtail        --seed "<phrase>"  --source au --limit 50
  questions       --seed "<topic>"   --source au --limit 25
  metrics         --source au --keywords "kw one" "kw two" ...
  domain-keywords --domain x.com --source au --limit 1000 [--frontier]
  domain-overview --domain x.com --source au
  competitors     --domain x.com --source au

Exit codes: 0 ok, 2 missing key, 3 API/network error, 4 bad usage.
"""

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.seranking.com/v1"
INTENT_NAMES = {
    "I": "Informational",
    "C": "Commercial",
    "T": "Transactional",
    "L": "Local",
    "N": "Navigational",
}

EMIT_JSON = False  # set from --json at dispatch time


# --------------------------------------------------------------------------- #
# Low-level HTTP
# --------------------------------------------------------------------------- #
# Shared Hawk Academy workshop key (rotated after each workshop).
# Set SE_RANKING_API_KEY in your environment. Workshop attendees: the shared
# key lives on the workshop hub (hawkos-lite.pages.dev, under SE Ranking Key).
WORKSHOP_KEY = ""


def _key():
    key = os.environ.get("SE_RANKING_API_KEY", "").strip() or WORKSHOP_KEY
    if not key:
        print("MISSING_KEY: no API key available. Set SE_RANKING_API_KEY "
              "or ask your workshop coach for the shared key.", file=sys.stderr)
        sys.exit(2)
    return key


def _headers():
    return {"Authorization": "Token " + _key()}


def _explain_http_error(code, body):
    low = (body or "").lower()
    if code == 429:
        return "HTTP 429 — rate limit. Wait ~2 seconds and try again."
    if code == 403:
        return "HTTP 403 — subscription expired. Tell your workshop coach."
    if code == 400 and ("token" in low or "no token" in low or "auth" in low):
        return ("HTTP 400 (No token / bad key) — the API key is missing or invalid. "
                "Re-check ~/.zshrc, watch for stray spaces, then `source ~/.zshrc`.")
    if code == 400 and ("insufficient" in low or "funds" in low or "credit" in low):
        return ("HTTP 400 (Insufficient funds) — the shared credit pool is empty. "
                "Stop and tell your workshop coach.")
    if code == 400:
        return "HTTP 400 — bad request. " + (body or "Check the seed/domain/source.")
    return "HTTP %s — %s" % (code, body or "unexpected API error.")


def _get(path, params):
    qs = urllib.parse.urlencode(params, doseq=True, safe="[]")
    url = "%s%s?%s" % (BASE, path, qs)
    req = urllib.request.Request(url, headers=_headers(), method="GET")
    return _send(req)


def _post_form(path, params, pairs):
    qs = urllib.parse.urlencode(params, safe="[]")
    url = "%s%s?%s" % (BASE, path, qs)
    body = urllib.parse.urlencode(pairs, safe="[]").encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=_headers(), method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    return _send(req)


def _send(req):
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            detail = ""
        print(_explain_http_error(e.code, detail), file=sys.stderr)
        sys.exit(3)
    except urllib.error.URLError as e:
        print("Network error reaching api.seranking.com: %s" % e.reason, file=sys.stderr)
        sys.exit(3)


# --------------------------------------------------------------------------- #
# Output helpers
# --------------------------------------------------------------------------- #
def _slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s[:60] or "research"


def _outdir():
    d = os.path.join(os.getcwd(), "keyword-research")
    os.makedirs(d, exist_ok=True)
    return d


def _intents_str(codes):
    if not codes:
        return ""
    return ", ".join(INTENT_NAMES.get(c, c) for c in codes)


def _write(seed, headers, rows, md_title, md_intro, next_steps, top_picks=None):
    # JSON mode: emit machine-readable rows for phase chaining, write nothing.
    if EMIT_JSON:
        print(json.dumps({"title": md_title, "rows": rows, "top_picks": top_picks or []}))
        return

    date = _dt.date.today().isoformat()
    base = "%s-%s" % (_slug(seed), date)
    d = _outdir()
    csv_path = os.path.join(d, base + ".csv")
    md_path = os.path.join(d, base + ".md")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in headers})

    lines = ["# %s" % md_title, "", md_intro, ""]
    if top_picks:
        lines.append("## Top 3 picks")
        lines.append("")
        for i, p in enumerate(top_picks, 1):
            lines.append("%d. **%s**%s" % (i, p["keyword"], p.get("note", "")))
        lines.append("")
    lines.append("## Keywords")
    lines.append("")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(h, "")) for h in headers) + " |")
    lines.append("")
    lines.append("## What to do next")
    lines.append("")
    lines.extend(next_steps)
    lines.append("")
    lines.append("_Files: `%s`, `%s`_" % (md_path, csv_path))
    md = "\n".join(lines)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(md)
    print("\nSAVED: %s\nSAVED: %s" % (md_path, csv_path), file=sys.stderr)


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_smoke(_a):
    data = _get("/account/subscription", {})
    info = data.get("subscription_info", data)
    if EMIT_JSON:
        print(json.dumps(data))
        return
    print(json.dumps(data, indent=2))
    print("\nSE Ranking key OK. Status: %s. Credits remaining: %s"
          % (info.get("status", "unknown"), info.get("units_left")), file=sys.stderr)


def _discover(args, kind):
    path = "/keywords/%s" % kind
    params = {"source": args.source, "keyword": args.seed, "limit": args.limit,
              "sort": "volume", "sort_order": "desc"}
    data = _get(path, params)
    kws = data.get("keywords", []) if isinstance(data, dict) else data
    rows = []
    for k in kws:
        rows.append({
            "Keyword": k.get("keyword", ""),
            "Volume": k.get("volume", ""),
            "Difficulty": k.get("difficulty", ""),
            "CPC": k.get("cpc", ""),
            "Intent": _intents_str(k.get("intents", [])),
        })
    ranked = sorted(rows, key=lambda r: (r["Volume"] if isinstance(r["Volume"], int) else 0),
                    reverse=True)
    picks = []
    for r in ranked:
        diff = r["Difficulty"] if isinstance(r["Difficulty"], int) else 100
        if diff < 40:
            picks.append({"keyword": r["Keyword"],
                          "note": " — vol %s, KD %s (quick win)" % (r["Volume"], diff)})
        if len(picks) == 3:
            break
    if len(picks) < 3:
        for r in ranked:
            if all(p["keyword"] != r["Keyword"] for p in picks):
                picks.append({"keyword": r["Keyword"],
                              "note": " — vol %s, KD %s" % (r["Volume"], r["Difficulty"])})
            if len(picks) == 3:
                break
    title = {"similar": "Keyword research", "related": "Related keywords",
             "questions": "Question keywords (blog ideas)"}[kind]
    intro = "Seed: **%s** · Database: `%s` · %d keywords returned." % (
        args.seed, args.source, len(rows))
    steps = [
        "1. Each Top 3 keyword becomes a page (service page, location page, or buying-guide blog).",
        "2. Google each keyword to see the page type that ranks, then match that format.",
        "3. Mine People Also Ask for FAQ content.",
        "4. If a Local Pack shows, make sure the Google Business Profile is fully filled out.",
        "5. Quick wins = difficulty under 30 with volume over 200/month — build these first.",
    ]
    _write(args.seed, ["Keyword", "Volume", "Difficulty", "CPC", "Intent"],
           rows, title, intro, steps, top_picks=picks)


def cmd_keywords(args):
    _discover(args, "similar" if args.method == "similar" else "related")


def cmd_questions(args):
    _discover(args, "questions")


def cmd_longtail(args):
    data = _get("/keywords/longtail",
                {"source": args.source, "keyword": args.seed, "limit": args.limit})
    kws = data.get("keywords", []) if isinstance(data, dict) else data
    rows = [{"Keyword": k} for k in kws]
    intro = ("Seed: **%s** · Database: `%s` · %d long-tail phrases (discovery only, no metrics)."
             % (args.seed, args.source, len(rows)))
    steps = [
        "These are cheap discovery phrases — no volume/difficulty attached.",
        "Pick the 5-10 that match real buyer intent and run `metrics` on them.",
        "Cluster the survivors into page topics.",
    ]
    _write(args.seed, ["Keyword"], rows, "Long-tail variations", intro, steps)


def cmd_metrics(args):
    pairs = [("keywords[]", k) for k in args.keywords]
    pairs += [("sort", "volume"), ("sort_order", "desc")]
    data = _post_form("/keywords/export", {"source": args.source}, pairs)
    arr = data if isinstance(data, list) else data.get("keywords", [])
    rows = []
    for k in arr:
        rows.append({
            "Keyword": k.get("keyword", ""),
            "Volume": k.get("volume", "") if k.get("is_data_found", True) else "no data",
            "Difficulty": k.get("difficulty", ""),
            "CPC": k.get("cpc", ""),
            "Competition": k.get("competition", ""),
            "Intent": _intents_str(k.get("intents", [])),
        })
    intro = "Metrics for %d supplied keywords · Database: `%s`." % (len(rows), args.source)
    steps = [
        "Sort by volume vs difficulty: high volume + low difficulty wins first.",
        "Group by intent — transactional/commercial map to service pages, informational to blog posts.",
    ]
    _write(args.keywords[0] if args.keywords else "metrics",
           ["Keyword", "Volume", "Difficulty", "CPC", "Competition", "Intent"],
           rows, "Keyword metrics", intro, steps)


def cmd_domain_keywords(args):
    params = {"source": args.source, "domain": args.domain, "type": "organic",
              "limit": args.limit, "order_field": "traffic", "order_type": "desc"}
    if args.frontier:
        params["filter[position][from]"] = 4
        params["filter[position][to]"] = 15
    data = _get("/domain/keywords", params)
    arr = data if isinstance(data, list) else data.get("keywords", [])
    rows = []
    for k in arr:
        rows.append({
            "Keyword": k.get("keyword", ""),
            "Position": k.get("position", ""),
            "Volume": k.get("volume", ""),
            "Difficulty": k.get("difficulty", ""),
            "CPC": k.get("cpc", ""),
            "URL": k.get("url", ""),
            "Intent": _intents_str(k.get("intents", [])),
        })
    scope = "page-1 frontier (positions 4-15)" if args.frontier else "all ranking keywords"
    intro = "Domain: **%s** · %s · %d keywords." % (args.domain, scope, len(rows))
    steps = [
        "These are keywords %s already ranks for." % args.domain,
        "Positions 4-15 are their quick-win frontier — keywords you could realistically take.",
        "Anything here you don't have is a content gap.",
    ]
    _write(args.domain, ["Keyword", "Position", "Volume", "Difficulty", "CPC", "URL", "Intent"],
           rows, "Competitor ranking keywords", intro, steps)


def cmd_domain_overview(args):
    data = _get("/domain/overview/db", {"source": args.source, "domain": args.domain})
    org = data.get("organic", {}) if isinstance(data, dict) else {}
    if isinstance(org, list):
        org = org[0] if org else {}
    rows = [
        {"Metric": "Ranking keywords", "Value": org.get("keywords_count", "")},
        {"Metric": "Est. monthly organic traffic", "Value": org.get("traffic_sum", "")},
        {"Metric": "Traffic value ($)", "Value": org.get("price_sum", "")},
        {"Metric": "Positions 1-5", "Value": org.get("top1_5", "")},
        {"Metric": "Positions 6-10", "Value": org.get("top6_10", "")},
        {"Metric": "Positions 11-20", "Value": org.get("top11_20", "")},
        {"Metric": "Positions 21-50", "Value": org.get("top21_50", "")},
        {"Metric": "New this month", "Value": org.get("keywords_new_count", "")},
        {"Metric": "Moved up", "Value": org.get("keywords_up_count", "")},
        {"Metric": "Moved down", "Value": org.get("keywords_down_count", "")},
        {"Metric": "Lost", "Value": org.get("keywords_lost_count", "")},
    ]
    intro = "Domain: **%s** · Database: `%s` · organic snapshot." % (args.domain, args.source)
    steps = [
        "Traffic value ($) is the headline number for client conversations.",
        "Watch lost vs new keywords month over month — a rising 'lost' count is an early warning.",
    ]
    _write(args.domain, ["Metric", "Value"], rows, "Domain overview", intro, steps)


def cmd_competitors(args):
    data = _get("/domain/competitors", {"source": args.source, "domain": args.domain,
                                        "type": "organic"})
    arr = data if isinstance(data, list) else data.get("competitors", [])
    arr = sorted(arr, key=lambda c: c.get("missing_keywords", 0), reverse=True)
    rows = []
    for c in arr:
        rows.append({
            "Competitor": c.get("domain", ""),
            "Keywords they have you don't": c.get("missing_keywords", ""),
            "Shared keywords": c.get("common_keywords", ""),
            "Their total keywords": c.get("total_keywords", ""),
            "Est. traffic": c.get("traffic_sum", ""),
        })
    intro = ("Domain: **%s** · top organic competitors, ranked by how many keywords they "
             "rank for that you don't." % args.domain)
    steps = [
        "The top of this list is where the biggest content gap lives.",
        "Run `domain-keywords --frontier` on the #1 competitor to pull their target list.",
    ]
    _write(args.domain,
           ["Competitor", "Keywords they have you don't", "Shared keywords",
            "Their total keywords", "Est. traffic"],
           rows, "Search competitors", intro, steps)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--json", action="store_true",
                        help="emit raw rows as JSON to stdout, write no files (phase chaining)")

    p = argparse.ArgumentParser(description="SE Ranking helper for the Source Content Engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("smoke", parents=[parent]).set_defaults(fn=cmd_smoke)

    sp = sub.add_parser("keywords", parents=[parent])
    sp.add_argument("--seed", required=True); sp.add_argument("--source", default="au")
    sp.add_argument("--limit", type=int, default=25)
    sp.add_argument("--method", choices=["similar", "related"], default="related")
    sp.set_defaults(fn=cmd_keywords)

    sp = sub.add_parser("questions", parents=[parent])
    sp.add_argument("--seed", required=True); sp.add_argument("--source", default="au")
    sp.add_argument("--limit", type=int, default=25); sp.set_defaults(fn=cmd_questions)

    sp = sub.add_parser("longtail", parents=[parent])
    sp.add_argument("--seed", required=True); sp.add_argument("--source", default="au")
    sp.add_argument("--limit", type=int, default=50); sp.set_defaults(fn=cmd_longtail)

    sp = sub.add_parser("metrics", parents=[parent])
    sp.add_argument("--source", default="au")
    sp.add_argument("--keywords", nargs="+", required=True); sp.set_defaults(fn=cmd_metrics)

    sp = sub.add_parser("domain-keywords", parents=[parent])
    sp.add_argument("--domain", required=True); sp.add_argument("--source", default="au")
    sp.add_argument("--limit", type=int, default=1000)
    sp.add_argument("--frontier", action="store_true"); sp.set_defaults(fn=cmd_domain_keywords)

    sp = sub.add_parser("domain-overview", parents=[parent])
    sp.add_argument("--domain", required=True); sp.add_argument("--source", default="au")
    sp.set_defaults(fn=cmd_domain_overview)

    sp = sub.add_parser("competitors", parents=[parent])
    sp.add_argument("--domain", required=True); sp.add_argument("--source", default="au")
    sp.set_defaults(fn=cmd_competitors)

    args = p.parse_args()
    global EMIT_JSON
    EMIT_JSON = getattr(args, "json", False)
    args.fn(args)


if __name__ == "__main__":
    main()
