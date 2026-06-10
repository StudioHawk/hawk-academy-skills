---
name: digital-pr-raids
description: >
  Guides a user step-by-step through a complete digital PR campaign using the RAIDS protocol
  (Recon, Analyze, Infiltrate, Deploy, Score) and generates every deliverable along the way:
  an ideation sheet, a supporting dataset, a targeted media list, a pitch email + press release,
  and a coverage tracker. Built to earn high-authority backlinks and brand mentions that improve
  both traditional SEO and AI-search visibility (ChatGPT, Perplexity, Google AI Overviews). Use
  whenever a user wants to run a digital PR campaign, do data-led PR, build a press release or
  media list, pitch journalists, earn editorial backlinks, get press coverage, or invokes
  /digital-pr-raids or mentions "RAIDS". Auto-researches angles, data and journalists where tools allow.
---

# Digital PR — the RAIDS Protocol

You run a workshop attendee through one full digital PR campaign, phase by phase, and generate
the real deliverables as you go. RAIDS = **R**econ → **A**nalyze → **I**nfiltrate → **D**eploy → **S**core.

This skill is **guide + generate + auto-research**: coach the attendee through each phase, do the
research you can with your own tools (web search, trends, data lookup, journalist discovery), and
produce the files. Read `references/raids-protocol.md` at the start, and `references/kadi-example.md`
for a worked example to model quality on.

## Bundled resources
- `references/raids-protocol.md` — full per-phase detail, headline formulas, pitch structure.
- `references/kadi-example.md` — a complete worked campaign (Kadi Luggage hidden airline fees).
- `scripts/build_pr_docs.py` — generates all five deliverables from one JSON config (python-docx + openpyxl).

## Setup (silent)
Install deps if missing, don't ask: `pip install python-docx openpyxl --break-system-packages`.
If `./business-context.md` exists, read it for client name, niche, audience and voice.

## How to run it
Work through the five phases **in order**. Each phase: state the goal, do the research, fill the
relevant part of a running JSON config in working memory, and confirm before moving on. The attendee
may already have an idea — if so, confirm and skip ahead, don't force the full interview.

### Phase R — Recon (Ideation)
Goal: a story idea people actually care about.
- Ask for the client, URL, audience and any angle they already have.
- **Auto-research:** scan Google News / Trends / Reddit / relevant blogs (via your search tools) for timely, data-led angles tied to the brand. Look for an AU-first or regional hook.
- Draft a main data-led idea + 3–5 headlines using the formulas in the reference, plus 2–3 smaller/reactive ideas.
- Fill the ideation fields (title, done-before, data collection, limitations, hooks, dream publications, outlets, why-care, markets).

### Phase A — Analyze (Data & Story)
Goal: back the idea with real facts.
- Identify concrete data sources (gov reports, public listings, surveys, Trends). **Auto-research** real stats where you can; never fabricate figures — if you can't verify, mark it as "to be collected" and tell the attendee what to pull.
- Shape findings into ONE headline + 3–5 bullet key findings + a ranked table. Populate `dataset_columns` / `dataset_rows`.

### Phase I — Infiltrate (Media List)
Goal: the right 20–30 reporters.
- **Auto-research** outlets and named journalists who've covered this topic in the last ~12 months (via web search). For each, capture outlet, journalist, a relevant recent article URL, and a one-line note. Leave email blank with a note to verify via Hunter.io — don't invent addresses.
- Keep it tight and relevant; relevance beats volume.

### Phase D — Deploy (Pitch & Outreach)
Goal: a story that's easy to publish.
- Write 2–3 subject-line options (lead with the number).
- Write the short pitch: 2-sentence intro + 3 bullet findings + dataset link.
- Write the full press release (headline, findings, data table, named quote, methodology, about, editor's-note credit request) and a follow-up email for day 5–7.

### Phase S — Score (Tracking)
Goal: capture proof.
- Generate the coverage tracker so the attendee logs each placement (type, date, link-vs-mention, DR, anchor text). Explain how to report total links/mentions/avg DR per campaign.

## Generate the deliverables
Once the JSON config is filled (as much as known — the script renders whatever it's given), write it
to `./pr-campaign.json` and run:
```
python3 scripts/build_pr_docs.py ./pr-campaign.json "<workspace>"
```
This writes five files: `<Client> - Ideation Sheet.docx`, `<Client> - Dataset.xlsx`,
`<Client> - Media List.xlsx`, `<Client> - Pitch & Press Release.docx`, `<Client> - Coverage Tracker.xlsx`.
You can generate the ideation sheet after Phase R and regenerate the full set at the end — just re-run with the updated JSON.

## Final summary (under 150 words)
- The campaign idea + headline, and the data angle.
- The deliverables saved (name and count them) and where.
- The single next action: verify journalist emails (Hunter.io), then send the pitch and set a 5–7 day follow-up reminder.
- Reminder that RAIDS is quarterly — one campaign every 3 months compounds.

## Rules
- **Australian English** throughout for AU clients (optimise, colour, programme).
- **Never fabricate data or journalist emails.** Real stats from real sources; leave emails to verify.
- **Every idea must be genuinely newsworthy** — data-led, fresh angle, regionally hookable, and tied naturally back to the brand (like Kadi → pack light → avoid baggage fees).
- **Always request a linked credit** in the editor's notes — the backlink is the point.
- **Keep pitches short.** Subject + intro + 3 bullets + link. One follow-up only.
