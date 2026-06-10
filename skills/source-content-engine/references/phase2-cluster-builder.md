# Phase 2 — Content Cluster Builder

Goal: take the `main_keywords` from Phase 1 and build a pillar-and-spoke cluster mapped against the site's existing content, then render it as a Word document. Keyword metrics come from the bundled SE Ranking helper (NOT an MCP).

## Steps

### 1. Inputs (already in hand)
- **Pillar topic** = `main_keywords.pillar_keyword` from Phase 1.
- **Domain** = the attendee's domain.
- **Locale** = `main_keywords.source`.

### 2. Crawl the sitemap
Fetch `https://{domain}/sitemap.xml` with WebFetch. If it 404s, try `sitemap_index.xml`, `wp-sitemap.xml`, and `robots.txt` (look for a `Sitemap:` directive). Follow nested sitemaps, cap at ~300 URLs. Filter out `/wp-json/`, `/feed/`, `/?p=`, image sitemaps, admin paths. **Never fabricate URLs you didn't fetch.** If no sitemap is found, note it and proceed with whatever URLs the attendee gave (or an empty existing-content set).

### 3. Detect the content section
Scan URLs for `/blog/`, `/articles/`, `/insights/`, `/news/`, `/resources/`, `/learn/`, `/guides/`, `/journal/`, `/posts/`. Use the most common as the content-section pattern for new spoke slugs. If none exists, default to `/blog/` and make Phase 2's Production Schedule start with "Phase 0 — Build a /blog/ section (required before publishing spokes)."

### 4. Classify existing content against the pillar
From slugs/titles, bucket plausibly-relevant URLs into: **Pillar candidate** (broad hub), **Existing spoke** (narrow — link, don't recreate), **Tangential** (ignore). WebFetch the top ~8-12 candidates to confirm intent and grab the real `<title>`/`<h1>` if unsure.

### 5. Draft the spoke list (8-10)
Start from `main_keywords.candidate_spoke_keywords` (Phase 1's related + question keywords). Each spoke must target one specific long-tail keyword, cover a sub-topic distinct from the pillar, be linkable to the pillar, and map to an existing URL (refresh) or a new recommended URL using the section pattern (e.g. `/blog/invisalign-cost-australia/`). Don't lock the list until metrics come back in step 6.

### 6. Pull keyword metrics via the helper
Collect the pillar keyword + every proposed spoke keyword into one list and call the helper in JSON mode:

```
python3 scripts/seranking.py metrics --json --source <db> --keywords "pillar kw" "spoke kw 1" "spoke kw 2" ...
```

This prints `{"title":..., "rows":[{Keyword, Volume, Difficulty, CPC, Competition, Intent}, ...]}` and writes no files. Map each row back to its keyword by the `Keyword` field. Notes:
- `metrics` (the export endpoint) costs **100 credits flat per call** regardless of list size — send ALL keywords in one call, never loop.
- If a keyword comes back with `Volume: "no data"`, mark its MSV as `0` and flag it so a zero-volume spoke can be dropped or rephrased.
- Map the `Intent` text to the cluster's intent field (informational/commercial/transactional/navigational). If a keyword has multiple intents, use the first/strongest.
- Never fabricate numbers. If the helper errors (e.g. `MISSING_KEY`), stop and surface the message.

### 7. Build the cluster architecture
- **Pillar:** if a strong existing pillar candidate exists, recommend optimising it; otherwise define a new pillar (target keyword, slug, 2000+ word outline, 6-10 H2s).
- **Spoke ordering:** sort by priority weighing MSV, intent fit, and refresh-vs-new (refreshes are faster wins).
- **Internal linking:** every spoke ⇄ pillar; cross-spoke links only where naturally related.
- **Production schedule:** Phase 0 (blog setup) only if step 3 flagged it → Phase 1 pillar → spokes in priority order.

### 8. Render the .docx
Build the JSON cluster definition (schema in the docstring of `scripts/build_cluster_docx.py`) and run:

```
python3 scripts/build_cluster_docx.py cluster.json "<workspace>/cluster-<pillar-slug>-<YYYY-MM-DD>.docx"
```

If python-docx is missing: `pip install python-docx --break-system-packages`. If the script fails, fall back to writing the cluster as a clean `.md` at the same path — don't block the pipeline.

## Handoff to Phase 3

Pass the finalised cluster forward as `cluster`:
- `pillar` — title, target_keyword, msv, intent, recommended_url, is_existing.
- `spokes[]` — for each: title, target_keyword, msv, intent, recommended_url, is_existing.

Phase 3 generates a brief for the pillar and each spoke. Continue without stopping.

## Quality bar
No fabricated URLs or keyword data. Spokes must be distinct sub-topics, not rephrasings of the pillar. Healthy intent mix. AU spelling for `au` sites. Honour blog detection.
