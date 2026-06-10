# ux-insights — Clarity Setup + UX Diagnosis (Claude Skill)

A two-in-one Claude skill that gets behavioural analytics running and then uses Claude to turn that
data into prioritised UX fixes.

- **SETUP mode** — installs and verifies **Microsoft Clarity** (free heatmaps, session recordings,
  friction signals) on any platform: Google Tag Manager, WordPress, Shopify, Squarespace, Wix,
  Webflow, or manual `<head>` install.
- **DIAGNOSE mode** — tool-agnostic. The user pastes or exports data from whatever they use
  (Microsoft Clarity, Hotjar, GA4, PostHog, FullStory, Mouseflow); Claude reads the signals
  (rage clicks, dead clicks, quick-backs, scroll depth, exit rates, funnel drop-off), infers the
  likely cause, and produces a prioritised UX report.

## How to install
- Drop the `ux-insights/` folder into your skills directory (e.g. `~/.claude/skills/`), or share the
  `ux-insights.skill` bundle for one-click install.
- Auto-triggers on: *"install Microsoft Clarity"*, *"set up Clarity"*, *"diagnose UX issues"*,
  *"why are users dropping off"*, *"analyse my heatmaps / Clarity / Hotjar data"*, *"improve conversion"*,
  or `/ux-insights`.

## How to use
- **Setup:** "Help me install Microsoft Clarity on my [platform] site."
- **Diagnose:** "Here's my Clarity/Hotjar/GA4 data — find my UX problems." Paste the metrics or attach an
  export; Claude returns a prioritised findings table and a UX Diagnosis Report `.docx`.

## What's inside
```
ux-insights/
├── README.md
├── SKILL.md                          # routing + both modes
├── references/
│   ├── clarity-setup.md              # per-platform install + verification + first-run config
│   └── ux-signals.md                 # signal → cause → fix dictionary + diagnosis framework
└── scripts/build_ux_report.py        # renders the prioritised UX Diagnosis Report (.docx)
```
Requires `python-docx` (the skill installs it automatically if missing).

## Notes
- Australian English for AU clients.
- Behavioural data shows *what* users do, not always *why* — the skill labels findings Confirmed vs
  Hypothesis and tells you how to validate before a big rebuild.
- Tool-agnostic and portable: it never assumes a live API connection — it works off pasted/exported data.
- Privacy: when installing Clarity/Hotjar, mask sensitive fields and reflect tracking in your
  cookie-consent + privacy policy.
