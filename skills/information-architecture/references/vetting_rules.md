# Keyword Vetting Rules

This file is the auto-vetting ruleset for Step 6 of the Hawk Academy IA Mapper. It is what makes the deliverable client-ready instead of a bulk dump of SE Ranking data.

## Why we vet

SE Ranking (like Semrush) surfaces semantically-related keywords. Semantic similarity is not the same as intent or audience match. A page about commercial trench drainage will return keywords like "shower drain channel" because they share the word "drain" — but those queries come from homeowners, not civil contractors, and the page won't satisfy them.

Bulk-dumping the SE Ranking export into the deliverable means:

- Vol / KD numbers look great on paper but the keywords don't match the page's audience.
- The client gets a list that includes their competitors' branded terms.
- Writers waste hours optimising for queries the page can't convert.

So every keyword gets a **KEEP** or **REMOVED** decision plus a one-line **reason**. The reason is the audit trail — it is what we tell the client when they ask "why didn't you target X?".

## How auto-vetting works in this skill

In the workshop version, you (Claude) walk every keyword and apply the rules below to assign a decision yourself. **Only pause and ask the attendee** when a keyword is genuinely borderline — usually because audience, intent, or geo could plausibly go either way. Batch ambiguous keywords (cap at ~6 per pause) and ask with `AskUserQuestion` using `multiSelect: true` so the attendee can KEEP or REMOVE several in one click.

When the attendee answers, **apply the same answer to identical patterns** for the rest of the set. If they REMOVED `trench drain bunnings` because it's residential, every other Bunnings keyword should be auto-REMOVED with reason `Residential intent — same pattern as attendee-vetted example`.

## KEEP rules

Keep a keyword if **all** of these are true:

1. **Audience match** — the searcher would be the page's target audience (e.g. B2B civil contractor, not residential homeowner; specifier, not job-seeker).
2. **Intent match** — the page satisfies the query type (commercial / informational / transactional / navigational).
3. **Topic match** — the keyword is genuinely about what the page covers, not just a semantic neighbour.

Specifically keep:

- **Branded competitor terms** — "humes box culvert" on a Cubis culvert page lets us rank for "competitor + product" queries. High commercial intent, often easier than the unbranded term.
- **Long-tail spec queries** even at zero volume — "p6 telstra pit dimensions", "class d 600x600 pit lid". SE Ranking "0" usually means 0–10 monthly. Niche B2B spec queries are typically 0-vol but high-intent.
- **Geographic + product combos** if the client has presence — "concrete pit brisbane", "stormwater pit melbourne". Don't keep these for cities the client doesn't service.
- **Spec dimensions** — sizes (600x600, 900x900), load classes (Class A through G), approval bodies (Telstra, NBN, AS 3996, MRTS91). These signal contractor intent.
- **Question-based queries** if the page answers them — "what is a stormwater pit" on a stormwater-pit category page that has an FAQ section. If the page is a pure category page with no FAQ, REMOVE and flag for a `/blog/` or `/resources/` spoke.

## REMOVED rules

Remove a keyword if **any** of these is true:

1. **Different audience.** Common on B2B civil / industrial pages:
   - Residential homeowner queries on a B2B page (e.g. "stormwater pit in backyard" on a commercial drainage page).
   - DIY / Bunnings / Reece queries on a contractor-spec page.
   - Job-seeker queries (e.g. "civil engineer jobs") on a product page.
2. **Different intent.** A category page targets commercial intent. Informational / how-to queries don't belong there (they go to `/blog/` or `/resources/`).
3. **Brand confusion.** A competitor brand name combined with the product (e.g. "civilmart pit" on a Cubis page) — unless we're explicitly going after competitor takedowns. Default: REMOVE.
4. **Off-topic semantic neighbour.** SE Ranking has a habit of surfacing these:
   - "shower drain" / "kitchen drain" on B2B trench / channel drain pages.
   - "fire pit" / "barbecue pit" on civil / stormwater pit pages.
   - "minecraft pit" / "bottomless pit" on anything (yes, it happens).
5. **Product mismatch.** The keyword is about a product the client doesn't sell. E.g. "septic tank installation" on a stormwater-pits page when they don't sell septic tanks.
6. **Geo mismatch.** Cities the client doesn't service.
7. **Attendee-flagged noise.** Words the attendee listed in Step 1 ("bunnings", "diy", their competitor's brand, etc.). Auto-REMOVE with reason `Attendee-flagged noise`.

## Standard reason codes

For the Vetting Log, use these phrases so the audit trail is consistent across pages:

| Reason text | When to use |
|---|---|
| `B2B match — keep` | Default KEEP for on-topic commercial queries |
| `Spec / size match — keep` | KEEP for dimension or class-based queries |
| `Branded competitor term — keep` | KEEP for "competitor + product" queries we want to rank for |
| `Geo match — keep` | KEEP for city / region queries where the client has presence |
| `0-vol but on-topic — keep` | KEEP for niche zero-vol queries that match audience + intent |
| `Question intent — fold to /blog/` | REMOVE from category page; flag for blog or glossary instead |
| `Residential intent — different audience` | REMOVE Bunnings / DIY / homeowner queries on B2B pages |
| `Off-topic semantic neighbour` | REMOVE SE Ranking noise (fire pit on stormwater, shower drain on trench) |
| `Brand confusion — competitor` | REMOVE branded queries for competitor products |
| `Product mismatch — not sold` | REMOVE queries for products the client doesn't sell |
| `Geo mismatch — out of service area` | REMOVE city queries where the client has no presence |
| `Attendee-flagged noise` | REMOVE because the attendee listed this term in Step 1 |
| `Attendee call — KEEP` / `Attendee call — REMOVED` | Use for any decision the attendee made themselves via the ambiguity prompt |

## Healthy retention rates

When you've finished a topic, sanity-check the KEEP rate:

- A B2B civil / industrial topic with mixed Bunnings noise → ~30–50% retention.
- A pure brand-product topic (e.g. "STAKKAbox") → ~70–90% retention.
- A high-noise topic ("drain grate" — residential + commercial mix) → ~20–40% retention.

If you're keeping > 80% you're probably under-vetting. If < 20% the seed was too broad — surface this to the attendee and offer to narrow the seed before pulling SE Ranking again.

## Worked example — `/product-categories/trench/` (Cubis case study)

Seed: "trench drainage". Raw SE Ranking export had ~150 keywords. Vetted:

| Keyword | MSV | Decision | Reason |
|---|---|---|---|
| trench drainage | 320 | KEEP | B2B match — keep (primary) |
| concrete trench drain | 140 | KEEP | B2B match — keep |
| trench and channel drain | 320 | KEEP | B2B match — keep |
| commercial trench drainage | 90 | KEEP | B2B match — keep |
| trench drain bunnings | 90 | REMOVED | Residential intent — different audience |
| diy trench drain | 70 | REMOVED | Residential intent — different audience |
| shower trench drain | 320 | REMOVED | Off-topic semantic neighbour |
| concrete channel drain | 210 | KEEP | B2B match — fold under same page |
| mufle linear drainage | 20 | KEEP | Branded sister-product (Burdens range) |
| trench drainage brisbane | 0 | KEEP | 0-vol but on-topic — keep (geo match) |
| how to install a trench drain | 70 | REMOVED | Question intent — fold to /blog/ |

Final: ~40 of 150 KEEP. The KEEP set is what populates the page's primary + supporting keywords on the IA Map sheet.
