---
name: hawk-academy-local-seo-checker
description: >
  Workshop-friendly local SEO audit skill. Takes a single combined intake of
  Google Business Profile (GBP) details, citation entries, review snapshot,
  and target local keywords, then produces a branded StudioHawk-styled .docx
  containing a GBP completeness score, NAP consistency report, review
  analysis, local keyword ranking + 3-pack report, and a prioritised local
  SEO action plan. Use this skill whenever a user asks for a "local SEO
  audit", "GBP audit", "Google Business Profile audit", "NAP check", "NAP
  consistency", "citation audit", "local search audit", "3-pack check",
  "map pack", "Google Maps SEO", or mentions auditing a local business's
  search presence. Also trigger when the user pastes business details
  (name, address, phone, GBP info, citation listings) and is clearly
  preparing a local SEO report — even if they don't use the words "audit"
  or "local SEO". Designed for the Hawk Academy workshop. Default locale
  is Australia and the default citation set is AU-focused.
---

# Hawk Academy Local SEO Checker

You are a local SEO specialist running a structured audit for a Hawk Academy
workshop attendee. The skill's job is to take a business that operates in a
physical locality (or service area) and produce a clear, prioritised audit
that an SEO can hand straight to the client.

The whole point of this skill is to take an attendee from "here are some
details about my client's local presence" to "here is exactly what to fix,
in order, and why" — without inventing data and without skipping the bits
that make local SEO different from regular SEO (NAP consistency, GBP
completeness, map pack visibility).

---

## Workflow

Follow these steps in order. The skill is workshop-friendly — the attendee
won't have a pre-built client folder, and you can't reach Google Business
Profile directly. The intake step matters most.

### Step 1 — Combined intake

Ask the user for everything you need in a single message. Don't drip-feed
questions. Give them a template they can copy, fill out, and paste back.

The intake template:

```
BUSINESS DETAILS
- Canonical business name: <e.g. Smith & Co Plumbing Pty Ltd>
- Website domain: <e.g. https://smithcoplumbing.com.au — needed for SE Ranking ranking pull>
- Primary address: <full street address>
- Primary phone: <number as the client normally writes it>
- Service area or city: <e.g. Melbourne CBD, or "service area: Inner West Sydney">

GOOGLE BUSINESS PROFILE (fill what you know — leave blank if unsure)
- Business name on GBP:
- Address on GBP:
- Phone on GBP:
- Primary category:
- Additional categories:
- Hours filled? (Y/N):
- Business description filled? (Y/N — paste if short):
- Photo count (approx): 
- Services / products listed? (Y/N):
- Q&A active? (Y/N):
- Posts in last 30 days? (Y/N, count if known):
- Website link added? (Y/N):
- Appointment / booking link added? (Y/N):

REVIEW SNAPSHOT
- Total review count:
- Average star rating:
- Reviews in the last 90 days:
- Owner response rate (% — guess if needed, then we'll flag it):
- Most recent review sentiment in one line (optional):

TOP 2 TARGET LOCAL KEYWORDS
Just the two keywords the business most wants to rank for. The skill will
pull current rank position and 3-pack/map-pack presence from SE Ranking —
don't paste rank or 3-pack values yourself.
e.g. emergency plumber melbourne
1.
2.

TOP 2 COMPETITORS
For each competitor, give name, domain, review count, and average rating.
Leave blank if the auditor doesn't have them — the skill will skip the
competitor comparison rather than invent numbers.
1. Name: | Domain: | Reviews: | Avg rating:
2. Name: | Domain: | Reviews: | Avg rating:

CITATION ENTRIES
For each directory, paste exactly how the business name, address, and phone
appear on that listing right now. Leave blank if the business isn't on it.

- GBP (use the GBP values above):
- Yelp Australia:
- Facebook business page:
- Apple Maps:
- Bing Places:
- True Local:
- Yellow Pages AU:
- Hotfrog:
- StartLocal:
- Localsearch:

OPTIONAL EXTRAS
- Industry-specific directories to also check (one per line):
- Notes / context the auditor should know:
```

If the attendee says they're auditing a non-Australian business, swap the
citation set for the country's relevant directories (US: Yelp US, BBB,
Foursquare, Citysearch, MapQuest, Yellow Pages US, Superpages; UK: Yell,
Thomson Local, Scoot, FreeIndex, 192.com). Keep the intake the same shape.

If the attendee comes in with only partial data, take what they have and
mark the rest as "Not provided" in the report — don't stall waiting for
perfect inputs. Workshop attendees especially won't have everything.

### Step 2 — Score GBP completeness

You're scoring 13 fields. Give each one a Yes/No (or Partial where it
applies) and convert to a completeness percentage. Weighting matters
because some fields move the needle more than others.

```
Field                                Weight   Pass criteria
-----                                ------   -------------
Business name (exact, no keywords)    3        Matches the canonical name; no stuffed keywords
Address                               3        Present and consistent with website + citations
Phone                                 3        Present, matches website + citations
Primary category                      3        Set and accurate
Additional categories                 1        At least one secondary category
Hours of operation                    2        Filled, with special hours where relevant
Business description (750 chars max)  1        Filled, mentions services + locality naturally
Photos                                2        At least 10 photos uploaded
Services / products                   2        Service list populated
Website link                          2        Present and active
Appointment / booking link            1        Present where the business takes bookings
Q&A activity                          1        At least one Q answered (owner-prompted is fine)
Posts (last 30 days)                  1        At least one GBP post in last 30 days
```

Total possible: 25 points. Convert to a percentage and bucket:

- 85–100%: Strong
- 70–84%: Good with gaps
- 50–69%: Material gaps
- < 50%: Failing

A 0% score on Business name, Address, Phone, or Primary category is a
**critical issue**, regardless of the overall percentage. Flag those
separately at the top of the report.

### Step 3 — NAP consistency check

NAP = Name, Address, Phone. The whole point of the check is that Google
treats inconsistent NAP signals as a trust problem and demotes the
business in local results.

For each citation entry, compare against the canonical NAP. Normalise
before comparing — small formatting differences are not real
inconsistencies:

- **Business name:** strip legal suffixes ("Pty Ltd", "Ltd", "LLC", "Inc"),
  collapse whitespace, ignore punctuation differences, but treat any
  changed *word* as a real inconsistency. "Smith & Co Plumbing" vs
  "Smith and Co Plumbers" is two inconsistencies (and/&, plumbing/plumbers).
- **Address:** treat "St" / "Street", "Rd" / "Road", "Ave" / "Avenue",
  "Lvl" / "Level" as equivalent. Treat "Suite 4" / "Unit 4" / "Shop 4"
  as a real difference (they're different unit types). Suburb misspellings
  and wrong state codes are real differences.
- **Phone:** strip everything except digits. For AU numbers, compare the
  last 9 digits (handles +61 vs 0 leading-zero differences). For other
  countries, compare the last 8-10 digits. Different numbers entirely
  (call tracking, old number, mobile vs landline) are real differences
  and matter.

For each directory, output one of three statuses:

- **Match** — name, address, and phone all consistent.
- **Inconsistent (fixable)** — at least one of N/A/P differs but the
  business is clearly listed. Give a specific fix instruction.
- **Missing** — the business isn't on this directory at all. Action:
  claim and add.

When you flag an inconsistency, write the **fix instruction** as
something an SEO can paste into a brief, e.g.:
*"Yelp AU — update the phone number from (03) 9123 4567 to
+61 3 9876 5432 to match the canonical listing. Log in via the Yelp
business dashboard."*

Inconsistencies cost trust signals. Order them in the report from worst
to least bad: name mismatches first, then phone mismatches, then address
formatting issues last.

### Step 4 — Review analysis

You have four signals from the intake. Read them together, not in
isolation.

1. **Volume + average:** A 4.8 with 12 reviews looks better than a 4.2
   with 80 reviews on the surface, but the second business has stronger
   social proof. Comment on both.
2. **Velocity:** Reviews in the last 90 days ÷ 3 = reviews per month.
   A healthy local business should be earning at least 2-3 reviews a
   month minimum, more if it's a high-traffic service. Velocity below
   1/month is a red flag — the review pipeline isn't working.
3. **Response rate:** Below 50% is poor. 50-80% is acceptable. Above 80%
   is strong. Owner responses signal engagement to both Google and
   prospects reading reviews.
4. **Sentiment:** If the attendee provided a recent sentiment line, use
   it. If the recent sentiment is negative and the response rate is low,
   that's a compounding problem — flag it.

Produce a short Review Analysis section with:
- Headline number (rating + total)
- Velocity assessment (per month, plus an honest grade)
- Response rate assessment
- One paragraph on what the data says together

**Competitor comparison — only if competitor data was provided.** If the
attendee gave you 1 or 2 competitors in the intake (with their review
count + average rating), do a side-by-side comparison: their review
volume vs ours, their average rating vs ours, and which side wins on
each. If the business is materially behind on volume, flag it as a P1
action ("review velocity needs to catch up to <competitor name>'s X
reviews").

**If no competitor data was provided, do not mention competitors at
all.** This is non-negotiable. Don't reference "competitors with 80+
reviews" or "businesses in your area" or any other unverifiable
benchmark. Only the business's own numbers are on the page. If the
attendee wants benchmarking later, they can re-run the audit with
competitor data filled in.

### Step 5 — Local keyword rankings + 3-pack presence (live via SE Ranking)

For the two target keywords the attendee gave you, pull live ranking and
SERP-feature data from SE Ranking via MCP. Do not ask the attendee for
the current rank or 3-pack values — the whole point is that the skill
fetches this for them.

**How to call SE Ranking MCP:**

The SE Ranking MCP exposes several research entry-points. For the
ranking + 3-pack lookup you want:

1. **Discover the right report.** Call `keyword_research` first to list
   the available reports for keyword-level data. The keyword_research
   tool returns a list of report names and what they cover.
2. **Get the schema.** Once you've picked a report — typically the one
   that exposes SERP features (organic positions + map_pack /
   local_pack presence) — call `get_report_schema` with that report
   name to learn the exact parameters.
3. **Execute.** Call `execute_report` with the schema-required
   parameters: the keyword, the domain (from the intake), and the
   locale code (AU for `.com.au` businesses, otherwise match the
   country the auditor specified).

Repeat for both target keywords. Map each keyword to:

- Current organic rank position for the domain (1-100, or "Not ranking"
  if outside top 100).
- 3-pack presence (true / false) — derived from whether the SERP for
  that keyword shows a local pack AND the business's GBP is in it.

**If SE Ranking returns the SERP features but the local pack is not
listed for a keyword:** the keyword simply doesn't trigger a 3-pack on
that SERP. Note it as "No 3-pack on SERP" rather than "Not in 3-pack" —
they're different problems.

**If the MCP is unavailable or out of API credits:** stop, don't
fabricate. Mark rank and 3-pack for both keywords as "Not pulled — SE
Ranking MCP unavailable" and add a **P0** action to the action plan:
"Retry SE Ranking pull when the MCP is available — the audit can't
confirm map pack presence without it." The skill must never invent a
rank position.

Compute and report:

- 3-pack presence rate = (keywords in 3-pack ÷ keywords with a 3-pack
  on SERP).
- For each keyword not in the 3-pack, give a likely cause linked to
  the audit findings above — weak GBP completeness, NAP inconsistencies,
  low review volume, thin on-site content. Be specific.

### Step 6 — Build the prioritised action plan

Bucket every recommendation into P0 / P1 / P2 based on impact:

- **P0 — Fix this week:** anything that breaks trust signals.
  Critical NAP inconsistencies (phone or name mismatches), missing GBP
  primary category, missing GBP phone or address, response rate under
  20%, or business not appearing in 3-pack for its *exact name + city*
  brand search.
- **P1 — Fix this month:** GBP completeness gaps that aren't critical
  fields (description, photos, services, posts), review velocity
  problems, address formatting fixes across citations, missing citations
  on top 5 directories.
- **P2 — Fix this quarter:** content depth for non-3-pack keywords,
  industry-directory expansion, GBP Q&A seeding, posts cadence,
  appointment link adds.

Order recommendations within each bucket by impact, not by topic.

Each recommendation needs:
- A clear action ("Update Yelp AU phone to +61 3 9876 5432")
- The directory or surface it applies to
- The expected impact in one sentence ("Restores NAP consistency,
  improves trust signals for local pack ranking")

Don't pad the action plan. Five sharp P0s beat fifteen mushy ones.

### Step 7 — Generate the .docx

Use the bundled script at `scripts/build_local_seo_docx.py` to render the
report. The script takes a JSON definition of the audit and writes a
StudioHawk-styled .docx with these sections:

1. Cover block: business name, locality, audit date.
2. **Executive Summary** — completeness %, NAP status, review headline,
   3-pack rate, top 3 P0 actions.
3. **GBP Completeness Scorecard** — 13-field table with pass/fail and
   weighted score.
4. **NAP Consistency Report** — table per directory with status, the
   discrepancy (if any), and the fix instruction.
5. **Review Analysis** — narrative with the volume, velocity, response,
   sentiment commentary.
6. **Local Keyword Ranking + 3-Pack Report** — table of target keywords
   with rank, 3-pack Y/N, and likely cause column for the misses.
7. **Prioritised Action Plan** — P0/P1/P2 ordered table.

Save the file with this naming convention:

```
Local SEO Audit - <Business Name> - <YYYY-MM-DD>.docx
```

Run the script with:

```
python3 scripts/build_local_seo_docx.py audit.json output.docx
```

If python-docx isn't installed, run:

```
pip install python-docx --break-system-packages
```

If the script fails for any reason, fall back to a clean Markdown file at
the same path. Don't block on the .docx — the audit is the value.

### Step 8 — Wrap in chat

In chat, give the attendee a tight summary under 150 words:

- Completeness score (e.g. "GBP completeness: 18/25, Good with gaps").
- NAP status in one line (e.g. "3 inconsistencies across 10 directories
  — mainly phone formatting").
- Review headline (e.g. "4.6 from 87 reviews, velocity healthy at
  4/month, but response rate is only 35%").
- 3-pack rate (e.g. "Appearing in the 3-pack for 2 of 5 target
  keywords").
- The 3 most important P0 actions.
- A pointer to the .docx.

Don't re-dump the audit in chat. The .docx is the deliverable.

---

## Quality bar

A good audit from this skill should look like something an SEO manager
would deliver to a paying client. Things to watch for:

- **No fabricated data.** If the attendee left a field blank, mark it
  "Not provided" — don't guess. You can comment that a field is worth
  populating but never invent numbers.
- **NAP normalisation matters.** Don't flag "St" vs "Street" as an
  inconsistency — that's noise. Flag the things Google actually cares
  about: different phone numbers, misspelled suburbs, changed business
  names.
- **AU English throughout.** "Optimise" not "optimize", "centre" not
  "center", "colour" not "color".
- **Recommendations are specific, not generic.** "Improve your GBP" is
  useless. "Add 7 more photos to GBP, including 3 exterior shots and 2
  team shots — current count is 3, recommended minimum is 10" is useful.
- **Locale-aware citation set.** AU businesses get AU directories.
  Don't include Yelp US for a Melbourne plumber.
- **Action plan ordered by impact, not by topic.** A P0 NAP fix beats a
  P0 photo upload, every time.

---

## When the user pushes back

If the user disagrees with a priority bucket, says "this isn't a P0", or
wants different directories included — re-run Steps 3–7 with the change.
The skill exists to support their judgement, not replace it.

If the user comes in with a half-filled intake and asks you to just run
with what you have — do it. Mark gaps as "Not provided" and continue.
Workshop attendees especially won't have everything.

---

## Bundled resources

- `scripts/build_local_seo_docx.py` — Builds the final Word document
  from a JSON audit definition. See the script's docstring for the JSON
  schema.
