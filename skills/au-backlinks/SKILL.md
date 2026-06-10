---
name: au-backlinks
description: >
  Audits a business's free Australian backlink and citation opportunities and shows
  which links they already have versus which are missing. Works from a curated, tiered
  list of high-authority free AU link sources — .gov.au supplier registries, council
  procurement panels, the non-negotiables (Google Business Profile, Bing Places, Apple
  Business Connect, LinkedIn), core AU directories, global high-DA profiles,
  industry-specific platforms, review sites, and data aggregators. Use whenever a user
  asks "what backlinks do I have", "what free backlinks can I get", "build my citations",
  "link building checklist", "where should I list my business", "audit my backlinks",
  or invokes /au-backlinks. Produces a personalised, prioritised tracker CSV and live-checks
  the highest-value listings to mark Have / Missing.
---

# AU Backlinks — Free Citation & Link Opportunity Audit

You help an Australian business find the free, high-authority backlinks and citations it
should have, see which it already has, and get a prioritised plan to claim the rest.

This is a workshop activity. Keep it concrete, fast, and encouraging. The deliverable is a
personalised tracker the attendee can work through.

## Bundled resources
- `assets/free-australian-backlinks.csv` — the curated, tiered source list (do not edit; it's the data).
- `scripts/backlink_audit.py` — filters the list to one business, prioritises it, and writes the tracker. Stdlib only.

## Step 1 — Gather the business (don't guess)
Collect these four. If a `./business-context.md` exists in the working directory, read it and
confirm rather than re-ask.
1. **Domain** (e.g. `example.com.au`)
2. **Business name** (exact trading name — used for verification searches)
3. **Industry / vertical** (e.g. fitness, plumber, dentist, café, law firm, SaaS agency)
4. **State** (NSW, VIC, QLD, SA, WA, TAS, NT, ACT)

## Step 2 — Generate the personalised plan
Run the script from the skill directory:
```
python3 scripts/backlink_audit.py --domain <domain> --business "<name>" --industry <industry> --state <STATE> --out "<workspace>/backlink-tracker-<brand>.csv"
```
It filters the list (the attendee's state .gov + Federal/National, councils, all universal
tiers, and only the industry-specific platforms that match their vertical), prioritises by
tier, writes the tracker CSV, and prints a tiered checklist. Each row gets a one-click Google
verification query (`site:listing.com "Business Name"`).

## Step 3 — Live-check the high-value listings (best-effort)
The script does not hit the network. YOU now do a best-effort presence check so the attendee
sees what they already have. Using your web search / fetch tools, check whether the business
already appears on the highest-leverage listings — at minimum:
- **All Tier 2 non-negotiables** (Google Business Profile, Bing Places, Apple Business Connect, LinkedIn)
- **The top 5–8 Tier 3 directories by authority** (True Local, Yellow Pages, White Pages, Yelp AU, Localsearch)
- **Any Tier 4 / Tier 5 that's obviously relevant** to their vertical

For each, run the `site:` query (or fetch the listing's search) and mark the tracker row
`Have`, `Missing`, or `Unknown` (if you can't tell). Be honest about confidence — a directory
listing can exist without being in a backlink index. Update the CSV via:
```
python3 scripts/backlink_audit.py --tracker "<tracker.csv>" --done "<Platform name>"
```
(or edit the Status column directly). Don't burn time checking all 38 — the key ones only.

## Step 4 — Report and recommend
Give a tight summary:
- **What they likely already have** (Have count) and **the biggest gaps** (Missing, highest tier first).
- **The next 5 to claim this week**, in priority order, each with the URL and the one-line "why it matters" from the data. Favour Tier 2 first, then any missing Tier 1 .gov / Tier 1b council links (rare, high-authority), then core directories.
- Point to the tracker CSV as the working file.

## Step 5 — Offer next steps
Offer to: re-run after they've claimed some, write their NAP (Name/Address/Phone) block so
every listing is consistent, draft the business description they'll paste into each profile,
or check a specific listing they're unsure about.

## Rules
- **Australian English.** This is an AU-specific list — don't suggest US/UK equivalents.
- **NAP consistency is the whole game** — if you draft their listing details, keep Name, Address and Phone identical to their Google Business Profile every time.
- **Be honest about verification limits.** Mark `Unknown` rather than guessing `Have`.
- **Tier 1 .gov.au and Tier 1b council links usually require an ABN** and a few minutes per form — flag that they're higher-effort but exceptional authority.
- **Don't recommend paid or spammy link schemes.** This list is free, legitimate sources only.
