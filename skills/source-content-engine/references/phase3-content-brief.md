# Phase 3 — Content Brief Engine

Goal: turn the `cluster` from Phase 2 into writer-ready "Visual SEO Content Brief" .docx files — one for the pillar and one per spoke. Context comes from `./business-context.md`; keyword volumes come from the bundled SE Ranking helper.

## Which briefs to build
Generate a brief for the **pillar** and **each spoke**, in cluster priority order, **capped at 10 briefs per run**. If the cluster has more than 10 items, do the pillar + top 9 spokes and tell the attendee the rest can be run again.

## Context (no interview needed)
Read `./business-context.md` once. It already supplies everything the old 4-question interview asked for:
- **Industry / niche** ← "What we do" + "Services / products"
- **Target audience** ← "Ideal customer"
- **Brand voice** ← "Brand voice"
- **Competitors** ← "Competitors"

Use this context for the Brand and Context, Target Audience, and Competitors sections of every brief. Customise each brief to its specific topic — don't paste identical context across all of them.

## Per-brief steps

For each pillar/spoke item:

### 1. Keywords
- **Primary keyword** = the item's `target_keyword` (with `msv` already carried from Phase 2).
- **Secondary keywords** = 5-8 supporting terms. Derive candidates from the cluster's related/question keywords for this topic, then pull their volumes in one call:
  ```
  python3 scripts/seranking.py metrics --json --source <db> --keywords "secondary 1" "secondary 2" ...
  ```
  Map volumes back by the `Keyword` field. `metrics` is 100 credits flat per call — batch all secondaries for one brief into a single call. Keep 0-volume keywords if strategically useful; note "0". Never fabricate volumes — if the helper errors, stop and surface it.

### 2. Competitor article URLs
Use web search to find 2-3 real articles currently ranking for the primary keyword. Put the actual URLs in the Competitors section. Don't invent URLs.

### 3. Build the brief content
1. **Details** — client name (use the business name from context), topic/category.
2. **Brand and Context** — objective, angle, voice/style (from context, customised to this topic).
3. **Target Audience** — who + what they're searching for.
4. **Competitors** — content requirements to outrank + the real competitor URLs.
5. **Internal Linking** — links out / links in. Use the cluster's internal-linking map: each spoke links to the pillar; the pillar links to its spokes. Reference real site URLs from the Phase 2 sitemap crawl where possible; otherwise leave a clear placeholder.
6. **Keywords** — primary + secondary with MSV.
7. **Page Metadata** — URL slug (use the cluster's `recommended_url`), title tag, meta description, word count.
8. **Section Design** — the most important part. A detailed H1/H2/H3 outline with section-by-section direction, word-count guidance, and visual notes, detailed enough that a copywriter can write the whole article without follow-up questions.

### 4. Render the .docx
Create a small temporary Node script that requires the bundled template and calls `buildBrief`:

```javascript
const docx = require('docx');
const { buildBrief, p, bl, linkP } = require('<skill-dir>/scripts/brief-template')(docx);
buildBrief({
  filename: '<workspace>/<Topic Title> - Blog Brief [company name].docx',
  clientName: '<Business name from context>',
  topic: '<Topic/Category>',
  objective: [p('...')], angle: [p('...')], voiceAndStyle: [p('...'), bl('...')],
  audience: [p('...'), bl('...')], searchIntent: [p('...'), bl('...')],
  contentReqs: [p('...'), bl('...')],
  competitorUrls: [linkP('Competitor 1','https://...'), linkP('Competitor 2','https://...')],
  linksOut: [bl('...')], linksIn: [bl('...')],
  primaryKw: { keyword: '...', volume: '...' },
  secondaryKws: [ { keyword: '...', volume: '...' } ],
  url: '/...', titleTag: '... | [company name]', metaDesc: '...', wordCount: '1,500-2,000 words',
  sections: [ { designNotes: [p('H1'), p('...')], contentDirection: [p('...'), bl('...')] } ],
});
```

- The `docx` npm package is required. If `node_modules/docx` isn't present in the working directory: `npm install docx`.
- There is no `logoPath` parameter — the workshop template renders no logo.
- Filename convention: `<Topic Title> - Blog Brief [company name].docx`. Keep the literal `[company name]` placeholder in the filename and inside the brief — the attendee find-and-replaces it after the workshop.

## Rules
- Never estimate or fabricate search volumes — pull from the helper.
- Australian English throughout (`colour`, `optimise`, `analyse`).
- Section Design quality matters most — be concrete for every section.
- Each brief must feel tailored to its topic and the client's context, not generic.
