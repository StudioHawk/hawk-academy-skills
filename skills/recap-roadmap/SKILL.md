---
name: recap-roadmap
description: >
  One skill for the workshop's end-of-day debriefs and the final 6-month roadmap. Three modes that chain:
  (1) Day 1 Summary — reviews the day's work and gives Day 2 recommendations; (2) Day 2 Summary — reads
  Day 1, reviews Day 2, shows where things stand; (3) 6-Month Roadmap — reads both summaries + every
  deliverable in the workspace and builds a phased plan (Months 0-2 / 3-4 / 5-6) as a Word doc. The skill
  auto-detects which mode to run from what the user says and which summary files already exist. Use when a
  user says "summarise my day", "day one/two summary", "end of day recap", "what did we do today", "build
  my roadmap", "6 month plan", "/recap-roadmap", or similar. Daily summaries print in chat and save a
  handoff .md; the roadmap renders a .docx.
---

# Recap & Roadmap

This skill runs the workshop's three reflection steps. They chain through two small handoff files
(`day-1-summary.md`, `day-2-summary.md`) so the final roadmap pulls everything through.

```
End of Day 1 → Day 1 Summary  → chat + saves day-1-summary.md
End of Day 2 → Day 2 Summary  → reads day-1-summary.md → chat + saves day-2-summary.md
The finale   → 6-Month Roadmap → reads day-1-summary.md + scans all deliverables → roadmap .docx
```

Day 2 normally **heads straight into the roadmap** — the roadmap *is* the Day 2 wrap. The separate Day 2
Summary (Mode 2) is **optional**: only run it if the user explicitly asks for an end-of-Day-2 recap.

## Step 0 — Pick the mode (auto-detect, don't pepper the user)
- Wording like "day one", "end of day 1", "recap today" → **Day 1 Summary**.
- "day two summary", "recap day two", "end-of-day-2 recap" → **Day 2 Summary** (optional).
- "roadmap", "6 month plan", "build my roadmap", "the plan I leave with" → **6-Month Roadmap**.
- If ambiguous, infer from files: no `day-1-summary.md` → Day 1; otherwise default to **Roadmap** (don't force a Day 2 summary). Confirm in one line, then go.
Always read `./business-context.md` if present for the business name + domain.

---

## Mode 1 — Day 1 Summary
Review everything done today in the workspace (files created/edited, changes, decisions, parked items).
Produce a **Day 1 Debrief** in chat:
1. **What we set out to do** (one line)
2. **✅ Done / shipped** — naming the actual deliverables/files
3. **🔧 Implemented & live** — changes now on the site
4. **🧭 Decisions** — each + the one-line reason
5. **✂️ Cut / dropped** — and why
6. **🅿️ Parked for later** — why + rough when (feeds the roadmap)
7. **❓ Open questions / blockers**
8. **➡️ Recommendations for Day 2** — 3–5 highest-leverage, prioritised

Then **save it to `day-1-summary.md`** and confirm.

---

## Mode 2 — Day 2 Summary *(optional — usually skipped)*
Day 2 normally goes **straight to the roadmap**; only run this if the user explicitly asks for an
end-of-Day-2 recap. First **read `day-1-summary.md`**. Then review today's work. Produce a **Day 2 Debrief** (same structure as
Day 1) plus:
- **🔗 Picked up from Day 1** — which parked/recommended items were actioned vs still parked
- **📍 Where things stand after two days** — live / queued / parked snapshot
End with **➡️ Recommendations going into the roadmap**. Then **save to `day-2-summary.md`** and confirm.

---

## Mode 3 — 6-Month Roadmap *(the Day 2 wrap)*
Read **`day-1-summary.md`** and **scan every deliverable in the workspace** — audit, IA, cluster, briefs,
backlink tracker, PR campaign, UX report, etc. (this is where all of Day 2's work gets picked up, so a
separate Day 2 summary isn't needed). If a `day-2-summary.md` happens to exist, read it too.

**Gate — first:** confirm a concrete, measurable **north-star goal** (e.g. "double organic enquiries in 6
months"). If it's missing or vague, STOP and ask for one before building — never invent it.

Then build a phased plan:
- **Phase 1 — Foundations & Quick Wins (Months 0–2)**
- **Phase 2 — Build (Months 3–4)**
- **Phase 3 — Scale & Authority (Months 5–6)**

For each phase: **Objective · Actions** (pulled from the parked items, briefs, trackers and recommendations
— name the real pages/links/campaigns) **· Owner · KPIs** (laddering to the north-star) **· Dependencies**.
Open with a **"Where you are now"** baseline (from the audit) and a **"First 2 weeks"** kickstart; close with
the **one thing to protect time for each month**.

Render the doc: assemble the JSON (schema in `scripts/build_roadmap_docx.py`) and run:
```
python3 scripts/build_roadmap_docx.py ./roadmap.json "<workspace>"
```
(install python-docx first if missing: `pip install python-docx --break-system-packages`). Give the file path.

## Rules
- **Australian English.** Specific — everything traces back to real work from the two days; no generic filler.
- **Daily summaries are honest** — name what's incomplete, cut and parked.
- **The roadmap is built backwards from the north-star goal** — don't proceed without one.
- Realistic for a solo owner / small team; prioritise ruthlessly.
