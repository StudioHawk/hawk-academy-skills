---
name: top-10-pages
description: >
  The bridge step between the SEO audit and the content engine. Turns audit findings + live keyword
  research into a prioritised list of the TOP 10 pages to create or optimise, and nominates ONE pillar +
  its spokes to hand straight into the URC elevation and content engine. Reads the audit and Information
  Architecture map already in the workspace, pulls real keyword data (SE Ranking), maps each high-value
  keyword to an existing page (optimise) or a new page (create), and outputs a prioritised CSV + a
  top-10-plan.md handoff file. Use when a user says "what 10 pages should I build", "top 10 pages",
  "prioritise my pages", "what should I create or optimise", "turn my audit into a plan", or /top-10-pages.
---

# Top 10 Pages

You bridge the audit and the content build: decide the **10 highest-leverage pages** to create or
optimise for the main keyword, and nominate the **pillar + spokes** the next steps will build. This is a
decision step — the output is a signed-off priority list, not content.

## Step 1 — Gather inputs
- **Domain** + **business + location**
- **Main keyword / money topic**
- **The audit** — read the audit report in the workspace (or ask the user to paste/attach it)
- **The IA map** — if `information-architecture` already ran, read its `.xlsx`/CSV: it has the URL list + keyword volumes, so you don't re-pull from scratch.
Read `./business-context.md` if present.

## Step 2 — Read the audit
Pull out: pages that already exist, pages flagged thin / missing H1 / missing meta / wrong schema,
duplicate or cannibalising URLs, and standout strengths. **If a page already exists it's an *optimise*,
not a *create*.**

## Step 3 — Keyword research (don't fabricate)
Use the IA map's keyword data where available; otherwise pull the main keyword + related + question
keywords from **SE Ranking** (and the site's organic competitors). Record real **MSV, KD, intent** for
every candidate. Flag quick wins (KD < 30, vol > 100). Mark anything unmeasured `TBC` — never invent volumes.

## Step 4 — Map keywords to pages
For each high-value keyword decide: does an existing page target it (**Optimise** — faster win) or is a
new page needed (**Create**)? Prefer optimising existing equity. Note duplicate URLs to consolidate/301 first.

**Confirm intent from the SERP.** For each page, the search intent (informational / commercial /
transactional / local) is whatever already ranks for that keyword — let that decide the **page type**
(guide vs comparison vs service/product vs local page), which in turn shapes create-vs-optimise. Record
the intent in the table; URC Elevation and the Content Engine inherit it.

## Step 5 — Output the Top 10
Rank by `(commercial value × winnability × audit-leverage)`. Present the table:

| # | Page | Create/Optimise | Target keyword | MSV | KD | Intent | Why now (tie to audit) | Effort | Impact |

Then give a **3-phase sequence** (reclaim equity → high-value rebuilds → net-new) and the **consolidate-first** list.

## Step 6 — Nominate the pillar + spokes
From the 10, nominate ONE **pillar** (the broad hub targeting the main keyword) and the rest as **spokes**
(each a distinct sub-topic linkable to the pillar). This is the handoff the next steps expect.

## Step 7 — Write the deliverable
Assemble the JSON (schema in `scripts/build_top10.py`) and run:
```
python3 scripts/build_top10.py ./top10.json "<workspace>"
```
This writes `top-10-pages-<domain>.csv` (the table) and **`top-10-plan.md`** — the handoff file that
**URC Elevation** and the **SOURCE Content Engine** read.

## Step 8 — Hand off
Tell the user the next step: **run URC Elevation** on these 10 pages to capture the unique angle, then the
**Content Engine** to build the briefs. Confirm the pillar + spokes are saved in `top-10-plan.md`.

## Rules
- **Australian English.** Every recommendation references something real — an audit finding or a pulled metric.
- **Be specific** — name the URL, quote the title/meta gap. No generic advice.
- **Optimise > Create** where a relevant page already exists. Never recommend creating something that exists.
- **Never fabricate keyword data** — SE Ranking or `TBC`.
