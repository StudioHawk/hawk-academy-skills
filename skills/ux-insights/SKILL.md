---
name: ux-insights
description: >
  Two-in-one UX skill. SETUP mode installs and verifies Microsoft Clarity (free heatmaps, session
  recordings and friction signals) on any site — GTM, WordPress, Shopify, Squarespace, Wix, Webflow
  or manual — and points the user at the right dashboards. DIAGNOSE mode uses Claude to find and fix
  user-experience problems from whatever behavioural data the user has: Microsoft Clarity, Hotjar,
  GA4, PostHog, FullStory or Mouseflow (pasted or exported). It reads the signals (rage clicks, dead
  clicks, quick-backs, scroll depth, exit rates, funnel drop-off), infers the likely cause, and gives
  prioritised fixes as a polished report. Use whenever someone says "install Microsoft Clarity",
  "set up Clarity", "diagnose UX issues", "why are users dropping off / not converting", "analyse my
  heatmaps / session recordings / Clarity / Hotjar data", "improve conversion", or /ux-insights.
---

# UX Insights — Clarity Setup + UX Diagnosis

This skill has two modes. Figure out which the user needs (ask if unclear) and run it.

- **SETUP** — they don't have behavioural analytics yet, or want Microsoft Clarity installed → `references/clarity-setup.md`.
- **DIAGNOSE** — they have data (Clarity/Hotjar/GA4/etc.) and want UX problems found and fixed → `references/ux-signals.md`.

A natural flow is Setup → wait a few days for data → Diagnose. Many attendees will already have a tool
running and jump straight to Diagnose.

## Bundled resources
- `references/clarity-setup.md` — step-by-step Clarity install per platform + verification + first-run config.
- `references/ux-signals.md` — the signal dictionary (signal → cause → fix) and diagnosis framework, tool-agnostic.
- `scripts/build_ux_report.py` — renders a prioritised **UX Diagnosis Report** .docx from a findings JSON (needs python-docx).

## SETUP mode
Follow `references/clarity-setup.md`:
1. Create the Clarity project (clarity.microsoft.com) and grab the tracking code.
2. Confirm the user's platform and give the exact install path (GTM is the universal default; Squarespace/Wix/WordPress/Shopify/Webflow each have a specific spot).
3. Verify tracking is live (recordings appear; `clarity.ms` fires).
4. First-run config: masking/privacy + cookie-consent note, optional GA4 link, set up a funnel for the key conversion path.
5. Tell them what to watch and to give it a few days before diagnosing.
Note any other tools they run (Hotjar, GA4…) so Diagnose mode can use them.

## DIAGNOSE mode
Tool-agnostic — this skill does NOT assume a live connection. The user **pastes or exports** their data
(Clarity dashboard numbers or a CSV, Hotjar heatmap/recording notes, a GA4 funnel/exit report, etc.).
Then follow `references/ux-signals.md`:
1. Confirm the **goal** of each page being reviewed (what should the user do there?).
2. Read the signals; map each to a likely cause using the dictionary.
3. **Corroborate across sources** — agreement between two tools = strong signal; one alone = hypothesis.
4. Ask the user to check a **recording** where a signal is ambiguous (recordings reveal the *why*).
5. Produce a prioritised findings list (Area · Signal+evidence · Likely cause · Fix · Severity · Effort · Impact), a short summary, and a "fix these 3 first" quick-win list.
6. Render the report:
   ```
   python3 scripts/build_ux_report.py ./ux-findings.json "<workspace>/UX Diagnosis - <client>.docx"
   ```
   (install python-docx first if missing: `pip install python-docx --break-system-packages`)

### What to ask the user to paste/export (give them this menu)
- **Clarity:** dashboard metrics (rage clicks, dead clicks, quick-backs, excessive scrolling, JS errors, scroll depth) + any recording observations, per top page.
- **Hotjar:** click + scroll heatmap notes, recording highlights, survey themes.
- **GA4:** exit rate by page, engagement rate / avg time, funnel step drop-off, mobile vs desktop split.
- **Anything else** (PostHog, FullStory, Mouseflow): the equivalent friction signals.
They don't need all of it — even one tool's data is enough to start.

## Final summary
- The 1–3 biggest UX problems found and the single highest-leverage fix.
- The report file saved (path).
- For [Hypothesis] findings, the exact way to confirm them (recording, survey, or A/B test) before a big rebuild.

## Rules
- **Australian English** for AU clients (optimise, behaviour, colour, analyse).
- **Data shows what, not why.** Label findings Confirmed vs Hypothesis; never state a cause as fact from numbers alone.
- **Prioritise ruthlessly** — quick wins (high impact, low effort) before rebuilds.
- **Privacy:** when advising on Clarity/Hotjar install, remind the user to mask sensitive fields and reflect it in their cookie-consent + privacy policy.
- **Don't invent metrics.** Diagnose only from data the user actually provides; if a key signal is missing, say what to pull.
