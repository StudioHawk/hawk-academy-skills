# Phase 1 — Keyword Research

Goal: turn the attendee's domain + topic + business context into (a) a saved keyword research deliverable and (b) the **main keyword set** that Phase 2 will build a cluster around.

All SE Ranking calls go through the bundled helper. From the skill directory:

```
python3 scripts/seranking.py <command> [args] --source <db>
```

`<db>` is the `Locale source` two-letter code from `./business-context.md` (default `au`).

## Steps

1. **Pick the seed.** Use the pillar topic the attendee gave. If they only gave a domain, derive the seed from the dominant service in `./business-context.md` (the first item under "Services / products"). One seed drives the cluster; note any secondary services for later runs.

2. **Pull the core keyword set (saves the deliverable).**
   ```
   python3 scripts/seranking.py keywords --seed "<seed>" --source <db> --limit 25
   ```
   This writes `./keyword-research/<seed>-<date>.md` + `.csv` and prints a table with a Top 3. Keep these files — they are the Phase 1 deliverable.

3. **Pull question keywords (spoke fuel for Phase 2).**
   ```
   python3 scripts/seranking.py questions --seed "<seed>" --source <db> --limit 25
   ```

4. **(Optional, cheap context) Competitor frontier.** If `./business-context.md` lists a competitor, you may pull their page-1 frontier to surface gap keywords:
   ```
   python3 scripts/seranking.py domain-keywords --domain <competitor> --source <db> --limit 100 --frontier
   ```
   Skip if no competitor is listed — don't burn credits guessing domains.

## Handoff to Phase 2

Assemble a `main_keywords` object in working memory and pass it forward:

- **pillar_keyword** — the single best high-volume, on-topic term from step 2 (usually the #1 Top pick). This becomes the Phase 2 pillar topic.
- **candidate_spoke_keywords** — a deduped list of ~15-20 keywords drawn from steps 2 and 3 (and step 4 if run), each a distinct sub-topic or question. Phase 2 narrows these to 8-10 spokes.
- **source** — the locale code.

Do not stop for confirmation — the engine runs autonomously. Carry the main keyword set straight into Phase 2.

## Rules

- Never fabricate volume/difficulty/intent. Everything comes from the helper. If a call prints `no data`, leave it.
- `--limit 25` is plenty; discovery endpoints cost ~10 credits per returned keyword.
- Australian spelling in any chat summary if `source = au`.
