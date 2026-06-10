# information-architecture — Keyword-Mapped IA Builder (Claude Skill)

Takes a sitemap or domain and builds a **keyword-mapped Information Architecture**: it classifies every
URL into a section (Home, Categories/Services, Products, Locations, Blog, etc.), pulls live keyword data
from SE Ranking, auto-vets each keyword **KEEP/REMOVED** with a one-line reason (pausing only on genuinely
ambiguous calls), and outputs a hierarchically-sorted **`.xlsx`** (IA Map + Vetting Log) plus mirrored CSVs
— one row per page. Has a **thin-site fallback** that proposes an IA from scratch when a site has almost no pages.

*(Renamed from `hawk-academy-ia-mapper`.)*

## How to install
- Drop the `information-architecture/` folder into your skills directory (e.g. `~/.claude/skills/`), or
  upload the `.skill` bundle / zip via **Customise → Add Skill**.
- Triggers: *"build a keyword-mapped IA"*, *"build my information architecture"*, *"map keywords to my site"*,
  *"do an IA for [domain]"*, *"what should each page rank for"*, or `/information-architecture`.

## How to use
Give it your domain or sitemap URL, your locale (AU default), and any brand/competitor noise to filter.
It crawls, classifies, pulls keyword data, vets, and hands back the spreadsheet.

## What's inside
```
information-architecture/
├── README.md
├── SKILL.md
├── references/vetting_rules.md          # the KEEP/REMOVED ruleset
├── scripts/parse_sitemap.py             # sitemap → URL list (handles index recursion)
├── scripts/build_ia_csv.py              # vetted data → .xlsx + .csv deliverable
└── examples/                            # two finished worked examples
    ├── eCommerce — Koala Living (xlsx + csvs)
    └── Service — StudioHawk (xlsx + csvs)
```
Needs Claude + the **SE Ranking MCP** (or it outputs with keyword columns marked `TBC`). `openpyxl` is
auto-installed for the `.xlsx`.

## Notes
- Australian English for AU clients.
- **Never fabricates URLs or keyword data** — URLs come from the real sitemap, numbers from SE Ranking or marked `TBC`.
- Every keyword carries a vetting decision + reason (the audit trail clients ask for).
- See `examples/README.md` for the eCommerce vs Service worked examples.
