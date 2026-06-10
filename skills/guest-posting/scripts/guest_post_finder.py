#!/usr/bin/env python3
"""
guest_post_finder.py — Generate guest-post search footprints for a niche, and/or
build a prioritised prospect tracker CSV from a JSON of vetted prospects.

Standard library only.

Two modes:

  # 1) Print ready-to-run Google search footprints for a niche/location:
  python3 guest_post_finder.py footprints --niche "personal training" --location "Melbourne"

  # 2) Build a prospect tracker CSV from a JSON the assistant assembled:
  python3 guest_post_finder.py build prospects.json /path/to/output_dir/

prospects.json schema:
{
  "domain": "example.com.au",
  "niche": "personal training",
  "prospects": [
    {
      "site": "example-blog.com.au",
      "url": "https://example-blog.com.au/write-for-us/",
      "contact": "editor@example-blog.com.au",   // or contact-page URL, or ""
      "dr": 42,                                    // domain rating if known, else null
      "relevance": "High",                         // High / Medium / Low
      "dofollow": "Likely",                        // Likely / Unknown / Nofollow
      "angle": "Pitch the 2026 client-results data piece",
      "notes": "Accepts 1 guest post/month",
      "status": "To pitch"                         // To pitch / Pitched / Won / Declined
    }
  ]
}
"""
import argparse, csv, json, os, sys

FOOTPRINTS = [
    '{niche} "write for us"',
    '{niche} "guest post" OR "guest article"',
    '{niche} "contribute" inurl:write-for-us',
    '{niche} intitle:"write for us"',
    '{niche} "become a contributor"',
    '{niche} "submit a guest post"',
    '{niche} "guest post guidelines"',
    '{niche} "accepting guest posts"',
    '{niche} blog "this is a guest post by"',
    '{loc}{niche} blog "write for us"',
]


def cmd_footprints(args):
    niche = args.niche.strip()
    loc = (args.location.strip() + " ") if args.location else ""
    print("# Guest-post search footprints — %s%s" % (loc, niche))
    print("# Paste each into Google (or hand to Claude's web search), then vet the results.\n")
    for fp in FOOTPRINTS:
        print(fp.format(niche=niche, loc=loc))
    print("\n# Also worth doing:")
    print('#  - Competitor backlinks: find where rivals guest-posted (SE Ranking → backlinks) and pitch the same sites.')
    print('#  - Expert sources (AU): SourceBottle, Qwoted — get quoted instead of writing a full post.')
    print('#  - Reuse your RAIDS media list — those journalists are your guest-post network.')


def cmd_build(args):
    cfg = json.load(open(args.json, encoding="utf-8"))
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    dom = cfg.get("domain", "site").replace("/", "-")
    rel_rank = {"High": 0, "Medium": 1, "Low": 2}
    df_rank = {"Likely": 0, "Unknown": 1, "Nofollow": 2}
    prospects = sorted(
        cfg.get("prospects", []),
        key=lambda p: (rel_rank.get(p.get("relevance", "Medium"), 1),
                       df_rank.get(p.get("dofollow", "Unknown"), 1),
                       -(p.get("dr") or 0)),
    )
    fields = ["Priority", "Site", "URL", "Contact", "DR", "Relevance",
              "Dofollow", "Suggested angle", "Status", "Notes"]
    out = os.path.join(outdir, "guest-post-prospects-%s.csv" % dom.split(".")[0])
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, p in enumerate(prospects, 1):
            w.writerow({
                "Priority": i,
                "Site": p.get("site", ""),
                "URL": p.get("url", ""),
                "Contact": p.get("contact", ""),
                "DR": p.get("dr", ""),
                "Relevance": p.get("relevance", ""),
                "Dofollow": p.get("dofollow", ""),
                "Suggested angle": p.get("angle", ""),
                "Status": p.get("status", "To pitch"),
                "Notes": p.get("notes", ""),
            })
    print("Wrote", out, "(%d prospects)" % len(prospects))
    highs = [p for p in prospects if p.get("relevance") == "High"]
    print("High-relevance prospects: %d" % len(highs))
    for p in highs[:5]:
        print("  -", p.get("site", ""), "->", p.get("url", ""))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    fp = sub.add_parser("footprints"); fp.add_argument("--niche", required=True); fp.add_argument("--location", default="")
    bd = sub.add_parser("build"); bd.add_argument("json"); bd.add_argument("outdir")
    args = ap.parse_args()
    {"footprints": cmd_footprints, "build": cmd_build}[args.cmd](args)


if __name__ == "__main__":
    main()
