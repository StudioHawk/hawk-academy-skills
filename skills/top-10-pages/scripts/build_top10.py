#!/usr/bin/env python3
"""
build_top10.py — Render the Top 10 Pages deliverable + the handoff file the next steps read.

Usage:
    python3 build_top10.py top10.json /path/to/output_dir/

Writes:
    top-10-pages-<domain>.csv   — the prioritised table (paste into Sheets)
    top-10-plan.md              — human-readable plan + the nominated pillar + spokes
                                  (URC Elevation and the Content Engine read this file)

Stdlib only.

JSON schema (only "domain" required):
{
  "domain": "example.com.au",
  "business": "Example Pty Ltd",
  "main_keyword": "personal trainer near me",
  "date": "2026-06-11",
  "pages": [
    {
      "rank": 1,
      "page": "/personal-training",
      "action": "Optimise",            // Optimise | Create
      "keyword": "personal trainer near me",
      "msv": 4400, "kd": 67, "intent": "commercial",
      "why": "Money page; blank meta + thin (audit)",
      "effort": "Low", "impact": "High"
    }
  ],
  "pillar":  { "title": "Personal Training hub", "target_keyword": "personal trainer near me", "url": "/personal-training" },
  "spokes":  [ { "title": "Mums & Bubs", "target_keyword": "mums and bubs", "url": "/mums-bubs-classes" } ],
  "consolidate": ["/local-group-fitness-1 -> 301 to /local-group-fitness"]
}
"""
import json, sys, os, csv

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: build_top10.py top10.json output_dir\n"); sys.exit(1)
    c = json.load(open(sys.argv[1], encoding="utf-8"))
    outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    dom = c.get("domain", "site"); slug = dom.split(".")[0]
    pages = sorted(c.get("pages", []), key=lambda p: p.get("rank", 99))

    # CSV
    csv_path = os.path.join(outdir, "top-10-pages-%s.csv" % slug)
    cols = ["Rank", "Page", "Action", "Target keyword", "MSV", "KD", "Intent", "Why now", "Effort", "Impact"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cols)
        for p in pages:
            w.writerow([p.get("rank", ""), p.get("page", ""), p.get("action", ""),
                        p.get("keyword", ""), p.get("msv", "TBC"), p.get("kd", "TBC"),
                        p.get("intent", ""), p.get("why", ""), p.get("effort", ""), p.get("impact", "")])

    # handoff markdown
    md_path = os.path.join(outdir, "top-10-plan.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Top 10 Pages — %s\n\n" % c.get("business", dom))
        f.write("**Domain:** %s  ·  **Main keyword:** %s  ·  **Date:** %s\n\n"
                % (dom, c.get("main_keyword", "—"), c.get("date", "")))
        f.write("| # | Page | Create/Optimise | Target keyword | MSV | KD | Intent | Why now | Effort | Impact |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for p in pages:
            f.write("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
                p.get("rank", ""), p.get("page", ""), p.get("action", ""), p.get("keyword", ""),
                p.get("msv", "TBC"), p.get("kd", "TBC"), p.get("intent", ""), p.get("why", ""),
                p.get("effort", ""), p.get("impact", "")))
        if c.get("consolidate"):
            f.write("\n## Consolidate / 301 first\n")
            for x in c["consolidate"]: f.write("- %s\n" % x)
        # the handoff the engine + URC read
        f.write("\n## Nominated cluster (hand to URC Elevation → Content Engine)\n\n")
        pil = c.get("pillar", {})
        f.write("**Pillar:** %s — `%s` (%s)\n\n" % (pil.get("title", "—"), pil.get("target_keyword", "—"), pil.get("url", "")))
        f.write("**Spokes:**\n")
        for s in c.get("spokes", []):
            f.write("- %s — `%s` (%s)\n" % (s.get("title", ""), s.get("target_keyword", ""), s.get("url", "")))

    print("Wrote", csv_path)
    print("Wrote", md_path, "(handoff for URC + Content Engine)")
    print("Pages: %d | Pillar: %s | Spokes: %d" % (
        len(pages), c.get("pillar", {}).get("target_keyword", "—"), len(c.get("spokes", []))))


if __name__ == "__main__":
    main()
