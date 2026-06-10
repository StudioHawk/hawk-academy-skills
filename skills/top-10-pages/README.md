# top-10-pages — Audit → Top 10 Pages (Claude Skill)

The bridge between your SEO audit and the content build. Turns audit findings + live keyword research
into a prioritised list of the **10 pages to create or optimise** for your main keyword, and nominates
the **pillar + spokes** to hand straight into URC Elevation and the Content Engine.

## How to install
- Drop `top-10-pages/` into your skills directory, or upload the `.skill` / zip via **Customise → Add Skill**.
- Triggers: *"top 10 pages"*, *"what should I create or optimise"*, *"prioritise my pages"*,
  *"turn my audit into a plan"*, or `/top-10-pages`.

## How to use
Run it **after the audit** (and the IA map, if you built one). Give it your domain, main keyword, and the
audit. It pulls keyword data, maps it to pages, ranks the top 10, and nominates your pillar + spokes.

## What's inside
```
top-10-pages/
├── README.md
├── SKILL.md
└── scripts/build_top10.py    # writes the CSV table + top-10-plan.md handoff
```

## Where it sits in the flow
```
AI Search Audit  +  Information Architecture
        ↓
TOP 10 PAGES → top-10-plan.md (pillar + spokes)
        ↓
URC Elevation → Content Engine → build
```

## Notes
- Australian English; every pick traces back to a real audit finding or keyword metric.
- Reuses the IA map's keyword data when available; otherwise pulls SE Ranking. Never fabricates volumes (`TBC`).
- `top-10-plan.md` is the file URC Elevation and the Content Engine read — that's the handoff.
