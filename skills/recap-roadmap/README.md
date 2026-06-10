# recap-roadmap — Daily Recaps + 6-Month Roadmap (Claude Skill)

One skill for the workshop's three reflection steps, merged into a single trigger:
1. **Day 1 Summary** — reviews the day, gives Day 2 recommendations → saves `day-1-summary.md`
2. **Day 2 Summary** — reads Day 1, reviews Day 2, shows where things stand → saves `day-2-summary.md`
3. **6-Month Roadmap** — reads both summaries + every deliverable → a phased plan (.docx)

The skill auto-detects which mode to run from what you say and which summary files already exist.

## How to install
- Drop `recap-roadmap/` into your skills directory, or upload the `.skill` / zip via **Customise → Add Skill**.
- Triggers: *"summarise my day"*, *"day one summary"*, *"day two summary"*, *"end of day recap"*,
  *"build my roadmap"*, *"6 month plan"*, or `/recap-roadmap`.

## How to use
- **End of Day 1:** "recap today" → debrief in chat + `day-1-summary.md`.
- **End of Day 2:** "day two summary" → reads Day 1 + debrief + `day-2-summary.md`.
- **The finale:** "build my 6-month roadmap" → set your north-star goal → renders `6-Month-Roadmap-*.docx`.

## What's inside
```
recap-roadmap/
├── README.md
├── SKILL.md
└── scripts/build_roadmap_docx.py    # renders the 3-phase roadmap .docx from JSON
```
`python-docx` is auto-installed for the roadmap doc.

## Notes
- Australian English; every output traces back to real work from the two days.
- The roadmap is built backwards from a concrete north-star goal — the skill won't proceed without one.
- Replaces the three separate prompts (Day 1 / Day 2 / Roadmap) with one trigger.
