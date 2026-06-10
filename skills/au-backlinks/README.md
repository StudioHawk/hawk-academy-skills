# au-backlinks — Free AU Backlink & Citation Audit (Claude Skill)

A Claude skill that shows an Australian business which free, high-authority backlinks and
citations it should have, which it already has, and what to claim next. Built from a curated,
tiered list of free AU link sources (.gov.au supplier registries, council panels, Google
Business Profile / Bing / Apple / LinkedIn, core AU directories, global high-DA profiles,
industry platforms, review sites, and data aggregators).

## What it does
1. Takes a business's **domain, name, industry and state**.
2. Filters and prioritises the list to *that* business (their state .gov links, matching
   industry platforms, all universal tiers).
3. Writes a personalised **tracker CSV** with a one-click Google verification query for every listing.
4. Live-checks the highest-value listings and marks each **Have / Missing / Unknown**.
5. Recommends the next 5 links to claim this week.

## How to install
- **Claude Code / desktop:** drop the `au-backlinks/` folder into your skills directory
  (e.g. `~/.claude/skills/`), or share the `au-backlinks.skill` bundle for one-click install.
- The skill auto-triggers on requests like *"what backlinks do I have"*, *"free backlinks"*,
  *"build my citations"*, or `/au-backlinks`.

## How to use
Just ask Claude: **"Audit my backlinks for [domain]"** and answer the four questions
(domain, business name, industry, state). You'll get a prioritised plan and a tracker CSV.

## What's inside
```
au-backlinks/
├── SKILL.md                              # instructions Claude follows
├── assets/free-australian-backlinks.csv  # the curated source list (the data)
└── scripts/backlink_audit.py             # filters/prioritises the list, writes the tracker (stdlib only)
```

## Notes
- Australian English; AU-specific sources only.
- Tier 1 .gov.au and council links usually need an ABN — higher effort, exceptional authority.
- The presence check is best-effort `site:` verification (not a backlink-index lookup), so the
  skill marks `Unknown` rather than guessing. Free, legitimate sources only — no paid link schemes.
