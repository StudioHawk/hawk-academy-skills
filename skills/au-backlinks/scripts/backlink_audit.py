#!/usr/bin/env python3
"""
backlink_audit.py — Personalised AU backlink opportunity audit.

Loads the curated free-Australian-backlinks list, filters it to ONE business
(by state + industry), prioritises it, and writes a personal tracker CSV plus a
clickable Google verification query for every listing so the attendee can confirm
in one click whether they already have the link.

Standard library only.

Usage:
  python3 backlink_audit.py \
      --domain example.com.au \
      --business "Example Pty Ltd" \
      --industry fitness \
      --state VIC \
      [--out /path/to/backlink-tracker-example.csv]

  # mark one as done in an existing tracker:
  python3 backlink_audit.py --tracker /path/tracker.csv --done "True Local"

The script prints a tiered, prioritised plan to stdout and writes the tracker CSV.
It does NOT hit any network — live presence checks on the high-value listings are
performed by the assistant using its own search/fetch tools (see SKILL.md).
"""
import argparse, csv, os, sys, urllib.parse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "assets", "free-australian-backlinks.csv")

# Tier-5 (industry-specific) category -> keywords that map a business to it.
INDUSTRY_MAP = {
    "Trades": ["trade", "tradie", "builder", "construction", "plumb", "electric",
               "carpenter", "landscap", "renovation", "handyman", "roofing", "hvac"],
    "Health": ["health", "medical", "doctor", "gp", "dental", "dentist", "physio",
               "chiro", "psycholog", "clinic", "allied health", "nurse", "podiat"],
    "Tourism": ["tourism", "travel", "tour", "accommodation", "hotel", "resort",
                "experience", "attraction"],
    "Hospitality": ["restaurant", "cafe", "hospitality", "food", "venue", "bar",
                    "catering", "winery", "brewery", "eatery"],
    "Legal": ["legal", "law", "lawyer", "solicitor", "barrister", "conveyanc"],
}
# Verticals that benefit most from the global high-DA profile tier (Tier 4).
GLOBAL_PROFILE_VERTICALS = ["agency", "saas", "software", "startup", "tech",
                            "consult", "marketing", "design", "developer", "b2b"]

STATES = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]


def host(url):
    try:
        return urllib.parse.urlparse(url).netloc.replace("www.", "")
    except Exception:
        return url


def verify_query(listing_url, business, domain):
    h = host(listing_url)
    q = 'site:%s "%s"' % (h, business)
    return "https://www.google.com/search?q=" + urllib.parse.quote(q)


def industry_categories(industry):
    industry = (industry or "").lower()
    cats = set()
    for cat, kws in INDUSTRY_MAP.items():
        if any(k in industry for k in kws):
            cats.add(cat)
    return cats


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def relevant(row, ind_cats, state, wants_global):
    tier = row["Tier"].strip()
    cat = (row.get("Category") or "").strip()
    # Tier 1: state .gov registries — keep the attendee's state + Federal + National.
    if tier == "1":
        if cat in STATES:
            return cat == state
        return True  # Federal / National
    # Tier 1b councils — keep all (multi-state platforms).
    if tier == "1b":
        return True
    # Tier 5 industry-specific — keep only matching vertical categories.
    if tier == "5":
        return cat in ind_cats
    # Tier 4 global profiles — always useful, flag as priority for digital verticals.
    # Tiers 2,3,6,7 — universal, always keep.
    return True


def priority(row, wants_global):
    tier = row["Tier"].strip()
    base = {"2": 1, "1": 2, "1b": 3, "3": 4, "4": 5, "6": 6, "5": 7, "7": 8}.get(tier, 9)
    if tier == "4" and wants_global:
        base = 4  # bump global profiles for agencies/saas/startups
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain")
    ap.add_argument("--business")
    ap.add_argument("--industry", default="")
    ap.add_argument("--state", default="", choices=[""] + STATES)
    ap.add_argument("--out")
    ap.add_argument("--tracker", help="existing tracker CSV to update")
    ap.add_argument("--done", help="listing Platform name to mark Done in --tracker")
    args = ap.parse_args()

    # --- update mode ---
    if args.tracker and args.done:
        rows = list(csv.DictReader(open(args.tracker, newline="", encoding="utf-8")))
        hit = False
        for r in rows:
            if r.get("Platform", "").strip().lower() == args.done.strip().lower():
                r["Status"] = "Have"
                hit = True
        if rows:
            with open(args.tracker, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
        print(("Marked '%s' as Have." % args.done) if hit else ("No listing named '%s' found." % args.done))
        return

    if not args.business or not args.domain:
        ap.error("--business and --domain are required (or use --tracker with --done)")

    ind_cats = industry_categories(args.industry)
    wants_global = any(v in (args.industry or "").lower() for v in GLOBAL_PROFILE_VERTICALS)
    rows = [r for r in load_rows() if relevant(r, ind_cats, args.state, wants_global)]
    rows.sort(key=lambda r: (priority(r, wants_global), r["Tier"], r["Platform"]))

    out = args.out or os.path.join(
        os.getcwd(), "backlink-tracker-%s.csv" % host(args.domain).split(".")[0])
    fieldnames = ["Priority", "Tier", "Tier Name", "Category", "Platform", "URL",
                  "Why it matters", "Status", "Verify (Google)"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({
                "Priority": priority(r, wants_global),
                "Tier": r["Tier"], "Tier Name": r["Tier Name"], "Category": r.get("Category", ""),
                "Platform": r["Platform"], "URL": r["URL"], "Why it matters": r["Why it matters"],
                "Status": "Unknown",
                "Verify (Google)": verify_query(r["URL"], args.business, args.domain),
            })

    # --- console summary ---
    print("# Backlink opportunity plan — %s (%s)" % (args.business, args.domain))
    print("Industry: %s   State: %s   Listings matched: %d" %
          (args.industry or "n/a", args.state or "n/a", len(rows)))
    print("Tracker written: %s\n" % out)
    cur = None
    for r in rows:
        label = "%s — %s" % (r["Tier"], r["Tier Name"])
        if label != cur:
            cur = label
            print("\n## Tier %s" % label)
        print("  [ ] %-34s %s" % (r["Platform"][:34], r["URL"]))
    print("\nNext: the assistant will live-check the Tier 2 non-negotiables + top "
          "high-DA listings and mark Have/Missing, then recommend the next 5 to claim.")


if __name__ == "__main__":
    main()
