---
name: guest-posting
description: >
  Finds, vets and helps you pitch guest-post backlink opportunities. Takes a domain + niche + location,
  generates targeted Google search footprints, discovers sites that accept guest contributions (via web
  search and competitor-backlink analysis), vets each for relevance / real traffic / dofollow / spam, and
  outputs a prioritised prospect tracker CSV plus ready-to-send outreach emails. Use whenever a user asks
  to "find guest post opportunities", "where can I guest post", "build backlinks with guest posts", "find
  sites that accept guest posts", "guest posting for [business]", or /guest-posting. Tool-agnostic — works
  off web search; competitor backlinks via SE Ranking when available.
---

# Guest Posting — Find, Vet & Pitch

You help a business build authority by landing guest posts on relevant, trustworthy sites. The deliverable
is a prioritised prospect tracker the user can work through, plus personalised outreach emails. Read
`references/footprints-and-vetting.md` and `references/outreach-templates.md` before you start.

## Step 1 — Gather inputs (one message)
1. **Domain** (`example.com.au`)
2. **Niche / topic** the business is credible in
3. **Location** (for local angles) — optional
4. **Their unique asset** — the URC thing they can pitch (original data, client results, a tool, a strong POV). If they don't have one, flag it: a generic post is much harder to place.
If `./business-context.md` exists, read it and confirm rather than re-ask.

## Step 2 — Generate footprints
```
python3 scripts/guest_post_finder.py footprints --niche "<niche>" --location "<city>"
```
This prints the Google search strings to run.

## Step 3 — Discover prospects
Using your web search tools, run the footprints and collect candidate sites. Also:
- **Competitor backlinks** — if SE Ranking is available, find where rivals have guest-posted (referring domains / "guest" anchor patterns) and add those sites; they already accept outside contributors in this niche.
- **Local + association angles** — local news, industry bodies, chambers, niche communities.
For each candidate capture: site, the write-for-us / contact URL, a contact email if visible, and (if you can tell) DR/traffic.

## Step 4 — Vet every candidate
Apply the checklist in `references/footprints-and-vetting.md`. Keep only sites that are **relevant + real + likely-dofollow + not a link scheme + editorially decent**. Mark each:
- **Relevance**: High / Medium / Low
- **Dofollow**: Likely / Unknown / Nofollow
Drop or flag spammy "guest post network" sites — those can hurt rankings. Be honest; don't pad the list.

## Step 5 — Build the tracker
Assemble the vetted prospects into JSON (schema in the script's docstring) and run:
```
python3 scripts/guest_post_finder.py build prospects.json "<workspace>"
```
This writes `guest-post-prospects-<brand>.csv`, sorted by relevance → dofollow → DR, with a suggested angle and a Status column (To pitch / Pitched / Won / Declined).

## Step 6 — Draft the outreach
For the top prospects, write personalised pitches from `references/outreach-templates.md`:
- Lead with a real detail from one of *their* articles.
- Pitch the business's unique asset as the angle (a specific headline).
- One site, one ask, one follow-up (day 5–7).
Offer to draft the first 3–5 emails ready to send.

## Step 7 — Wrap
Summarise: how many vetted prospects, how many High-relevance, the top 5 to pitch this week, and the single best angle. Point to the tracker CSV.

## Rules
- **Australian English** for AU clients.
- **Quality over quantity.** A handful of relevant, real sites beats 50 low-quality ones. Never recommend link-scheme/PBN sites.
- **Don't invent sites, contacts, or metrics.** Sites come from real search results; emails only if actually found (else note "find on contact page"); DR/traffic from a real tool or left blank.
- **Lead with the unique asset.** Placement rates collapse without something only this business has — push the user for it (ties to the URC framework).
- **Vet for dofollow honestly** — mark Unknown rather than guessing.
