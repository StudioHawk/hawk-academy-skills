#!/usr/bin/env python3
"""
write_elevation.py — Write a URC Elevation block per page from a small JSON.

Usage:
  python3 write_elevation.py urc-findings.json /path/to/output_dir

Writes one `urc-elevation-<slug>.md` per page. Standard library only.

JSON schema:
{
  "pages": [
    {
      "slug": "personal-training",
      "title": "Personal Training in Upper Ferntree Gully",
      "target_keyword": "personal trainer near me",
      "intent": "local",                 // informational | commercial | transactional | local (confirmed from the SERP)
      "page_type": "service page",       // guide | comparison | service/product | local page
      "uniqueness":  ["Add the '66% never use it' stat from intake data", "Build a cost-per-visit calculator"],
      "relevance":   ["Add a 'how much does it cost' section", "Internally link to the Hyrox page"],
      "credibility": ["Quote Laura (Ironman, 8 yrs coaching)", "Embed 3 named client results", "Add Author + Review schema"],
      "to_gather":   ["Exact session price", "2 client testimonials with names"]
    }
  ]
}
"""
import json, os, sys


def block(items):
    return "\n".join("- %s" % i for i in (items or [])) or "- (none yet — to gather)"


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: write_elevation.py urc-findings.json output_dir\n"); sys.exit(1)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    pages = data.get("pages", [])
    if not pages:
        sys.stderr.write("No 'pages' in JSON.\n"); sys.exit(1)
    written = []
    for p in pages:
        slug = p.get("slug") or (p.get("title", "page").lower().replace(" ", "-"))
        md = []
        md.append("# URC Elevation — %s" % p.get("title", slug))
        if p.get("target_keyword"):
            md.append("**Target keyword:** %s" % p["target_keyword"])
        if p.get("intent") or p.get("page_type"):
            md.append("**Search intent:** %s  ·  **Page type:** %s"
                      % (p.get("intent", "TBC"), p.get("page_type", "TBC")))
        md.append("")
        md.append("## Uniqueness — why you, not them?")
        md.append(block(p.get("uniqueness")))
        md.append("\n## Relevance — does this answer what they asked?")
        md.append(block(p.get("relevance")))
        md.append("\n## Credibility — why should anyone trust this?")
        md.append(block(p.get("credibility")))
        if p.get("to_gather"):
            md.append("\n## To gather (before writing)")
            md.append(block(p.get("to_gather")))
        path = os.path.join(outdir, "urc-elevation-%s.md" % slug)
        open(path, "w", encoding="utf-8").write("\n".join(md) + "\n")
        written.append(path)
        print("Wrote", path)
    print("\n%d URC elevation block(s) written to %s" % (len(written), outdir))


if __name__ == "__main__":
    main()
