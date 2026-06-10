# digital-pr-raids — Digital PR Campaign Engine (Claude Skill)

A Claude skill that guides a user through a complete digital PR campaign using the **RAIDS
protocol** and generates every deliverable along the way. Digital PR earns the high-authority
backlinks and brand mentions that lift both traditional SEO and AI-search visibility (ChatGPT,
Perplexity, Google AI Overviews).

**RAIDS = Recon → Analyze → Infiltrate → Deploy → Score.**

## What it does
Coaches the user phase by phase, auto-researches angles/data/journalists where tools allow, and
produces five ready-to-use files:
1. **Ideation Sheet** (Recon) — the story idea, headlines, hooks, target outlets.
2. **Dataset** (Analyze) — the ranked, citable data table.
3. **Media List** (Infiltrate) — 20–30 targeted journalists (Outlet / Journalist / Email / Article / Notes).
4. **Pitch & Press Release** (Deploy) — subject lines, short pitch, full release, follow-up.
5. **Coverage Tracker** (Score) — log placements by link type, DR and anchor text.

## How to install
- **Claude Code / desktop:** drop the `digital-pr-raids/` folder into your skills directory
  (e.g. `~/.claude/skills/`), or share the `digital-pr-raids.skill` bundle for one-click install.
- Auto-triggers on requests like *"run a digital PR campaign"*, *"build a press release"*,
  *"data-led PR"*, *"pitch journalists"*, or `/digital-pr-raids`.

## How to use
Ask Claude: **"Run a digital PR campaign for [brand]"** (or *"let's do RAIDS"*). Work through the
five phases — Claude researches, drafts, and generates the files into your working folder. You can
generate the ideation sheet after Phase R and regenerate the full set at the end.

## What's inside
```
digital-pr-raids/
├── SKILL.md                          # the phase-by-phase instructions Claude follows
├── references/
│   ├── raids-protocol.md             # full per-phase detail, headline formulas, pitch structure
│   └── kadi-example.md               # a complete worked campaign (Kadi Luggage hidden airline fees)
└── scripts/build_pr_docs.py          # generates all 5 deliverables from one JSON config
```
Requires `python-docx` and `openpyxl` (the skill installs them automatically if missing).

## Notes
- Australian English for AU clients.
- **Never fabricates data or journalist emails** — unverifiable stats are flagged "to be collected"
  and emails are left blank to verify (e.g. via Hunter.io).
- Every press release requests a **linked credit** — the backlink is the goal.
- RAIDS is built to repeat: run one campaign per quarter and the mentions compound.
