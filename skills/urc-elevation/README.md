# urc-elevation — URC Page Elevation (Claude Skill)

The content-quality step between the content engine and writing. It takes each page a content plan
suggested (to create or optimise) and runs it through the **URC framework — Uniqueness, Relevance,
Credibility** — using simple, plain-English questions to pull out what only the business owner knows,
so each page is elevated above generic LLM output *before* a word is written.

```
Content plan (cluster + briefs)
        ↓
URC ELEVATION — simple questions per page → U/R/C elevation block added to each brief
        ↓
Write / publish the pages
```

## The three pillars
| Pillar | The real question | Owner-facing question |
|---|---|---|
| **U** Uniqueness | "Why you, not them?" | What do you have that competitors don't? |
| **R** Relevance | "Does this answer the question they asked?" | What's the real question — and what's missing? |
| **C** Credibility | "Why should anyone trust this page?" | Who's the expert, and what's the proof? |

## How to install
- Drop the `urc-elevation/` folder into your skills directory (e.g. `~/.claude/skills/`), or share the
  `urc-elevation.skill` bundle for one-click install.
- Triggers: "elevate this page", "URC", "run URC on my pages", "make this page unique",
  "add information gain", "what can only I add to this", or `/urc-elevation`.

## How to use
Run it **after the content engine / briefs**: "Run URC on my pages." Claude works through each page one
at a time, asks the three simple questions, and turns your answers into a concrete U/R/C elevation block
saved as `urc-elevation-<slug>.md` (and/or appended to the brief). The writing step then builds from that.

## What's inside
```
urc-elevation/
├── README.md
├── SKILL.md                       # the per-page URC process Claude follows
├── references/urc-framework.md    # full framework detail + example items
└── scripts/write_elevation.py     # writes a urc-elevation-<slug>.md per page (stdlib only)
```

## Notes
- Plain-English questions — built for business owners, not SEOs.
- Pushes for specifics (a number, a name, a story); parks anything you don't have yet as a "to gather" item.
- Never fabricates data, credentials or reviews. Australian English for AU clients.
