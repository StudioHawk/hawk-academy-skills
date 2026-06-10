# guest-posting — Find, Vet & Pitch Guest Posts (Claude Skill)

Finds guest-post backlink opportunities for a business, vets them, and helps you pitch. Takes a
domain + niche + location, generates targeted Google search footprints, discovers sites that accept
guest contributions (via web search + competitor backlinks), vets each for relevance / real traffic /
dofollow / spam, and outputs a **prioritised prospect tracker CSV** plus ready-to-send outreach emails.

## How to install
- Drop the `guest-posting/` folder into your skills directory (e.g. `~/.claude/skills/`), or upload the
  `.skill` bundle / zip via **Customise → Add Skill**.
- Triggers: *"find guest post opportunities"*, *"where can I guest post"*, *"build backlinks with guest posts"*,
  *"find sites that accept guest posts"*, or `/guest-posting`.

## How to use
Give it your domain, niche, location, and your unique asset (original data / client results / a tool / a
strong take). It finds and vets prospects, builds the tracker, and drafts your first few pitches.

## What's inside
```
guest-posting/
├── README.md
├── SKILL.md
├── references/
│   ├── footprints-and-vetting.md     # search strings + the vetting checklist
│   └── outreach-templates.md         # pitch + follow-up + link-insertion templates
└── scripts/guest_post_finder.py      # generate footprints · build the prospect tracker CSV (stdlib)
```

## Notes
- Tool-agnostic — works off web search; uses SE Ranking for competitor backlinks when available.
- Australian English.
- **Quality over quantity** — only relevant, real, non-spammy sites; never recommends PBN/link-scheme sites.
- **Never invents** sites, contacts or metrics — real search results only; emails only when actually found.
- Pairs with `au-backlinks` (directories/citations), `digital-pr-raids` (earned coverage) and the URC
  framework (the unique asset you pitch).
