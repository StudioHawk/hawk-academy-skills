---
name: hawk-academy-content-brief-engine
description: >
  Workshop-friendly version of the SEO content brief engine. Generates a
  branded "Visual SEO Content Brief" .docx for any client, using SE Ranking
  to pull keyword data live (no manual copy/paste loop). Designed for Hawk
  Academy workshop attendees who do not have a pre-built client folder. If
  no brief-format.md exists, the skill runs a quick 4-question interview to
  capture industry, audience, voice, and competitors. Use this skill whenever
  a user asks to create a content brief, blog brief, SEO brief, page brief,
  article brief, or writing brief for any client, or mentions
  "brief for [client]", "write a brief", or asks to produce content direction
  for a copywriter. Supports batching up to 10 briefs at a time.
---

# Workshop Content Brief Engine

This skill generates branded "Visual SEO Content Brief" .docx files for any
client. It is a single-phase workflow: it gathers context, pulls keyword data
live from SE Ranking, and produces the final .docx in one continuous run.

Designed for Hawk Academy workshops, but works for any production use too.

---

## WORKFLOW OVERVIEW

The skill runs in three stages, all in one session:

1. **Context capture** — read the client's brief-format.md if it exists, or
   run a quick 4-question interview if it doesn't.
2. **Keyword research + live MSV pull** — research keywords for each topic
   and pull monthly search volume directly from SE Ranking via MCP.
3. **Brief generation** — render the final .docx using
   `scripts/brief-template.js`.

**Batch limit: maximum 10 briefs per run.** If more are requested, split into
batches and process sequentially.

---

## STAGE 1: CONTEXT CAPTURE

The brief needs enough context about the client to feel tailored rather than
generic. There are two paths to get it.

### Path A — Read the client's brief-format.md (preferred)

If the user has a client folder, look for it at this path pattern:

```
<mounted-folder>/Clients/<ClientName>/content-brief-template/brief-format.md
```

Read this file in full. It contains:

- Brand voice and style
- Target audience
- Competitor landscape
- Internal linking strategy
- Content outline templates
- Quality checklist

### Path B — Quick interview (workshop fallback)

If no brief-format.md exists for the client, run a short interview before
anything else. Ask these four questions using the AskUserQuestion tool (one
batch, four questions):

1. **Industry / niche** — e.g. legal, healthcare, e-commerce, SaaS, trades.
2. **Target audience** — who is this content for? Job title, life stage,
   problem they're trying to solve.
3. **Brand voice in one line** — e.g. "warm and plain-spoken", "technical and
   precise", "playful but credible".
4. **Top 2 competitors** — domains or names of the businesses they're trying
   to outrank.

Treat the answers as a lightweight brief-format.md for this run. They feed
directly into the Brand and Context, Target Audience, and Competitors
sections of the brief.

Do not skip the interview. A brief without this context comes out generic
and the workshop attendee won't get the "aha" moment.

---

## STAGE 2: KEYWORD RESEARCH + LIVE MSV PULL

SE Ranking is available via MCP, so you can pull keyword data directly
without leaving the chat — no manual copy/paste loop needed.

### Step 1: Research keywords for each topic

For each topic the user provides, build a candidate list of **8–10 keywords**
using your knowledge of SEO and the client's industry:

- **1 primary keyword** — the main search term the page should rank for
- **5–8 secondary keywords** — supporting terms, long-tail variants, question
  queries, and related intent variations

Consider:

- The client's industry and audience (from Stage 1)
- Search intent alignment (informational, commercial, transactional,
  navigational)
- Natural language variations people actually search
- Question-based queries (how, what, why, where, best, vs)
- Long-tail specificity (location, specification, use-case modifiers)
- Competitor keyword gaps (from the Stage 1 competitor info)

### Step 2: Pull MSV from SE Ranking via MCP

Use the SE Ranking MCP tools to pull monthly search volume for the full
candidate keyword list. The relevant tools are:

- `keyword_research` — pull MSV, difficulty, CPC, intent for a list of
  keywords in a given database (country).
- `overview_research` — keyword overview report.
- `get_report_schema` — call this first if you're unsure of the parameter
  schema for the report you want.

Default to the AU database unless the client is clearly in another market.
If the user gave you a country or region for the client, use that.

Pass the candidate keyword list to `keyword_research` in one call where
possible to keep things fast. Map the returned volumes back to each keyword.

If SE Ranking returns 0 volume for some keywords, keep them — they may still
be strategically valuable in niche B2B markets. Note "0" in the volume cell
rather than dropping them.

**Do not fabricate or estimate search volumes.** If SE Ranking can't be
reached, stop and tell the user so they can either fix the MCP connection or
provide the data manually.

### Step 3: Confirm the keyword list with the user (optional)

Before generating the brief, show a compact summary of the chosen keywords
+ MSV per brief and ask the user if they want to swap anything out. Skip
this confirmation step only if the user asked for a fully autonomous run.

---

## STAGE 3: BRIEF GENERATION

For each brief, build:

1. **Details** — Client name, topic/category.
2. **Brand and Context** — Objective, angle, voice/style (drawn from Stage 1
   but customised to this specific topic).
3. **Target Audience** — Who + what they're searching for (customised to
   topic).
4. **Competitors** — Content requirements to outrank + competitor article
   URLs. Use web search to find real competitor articles ranking for the
   primary keyword.
5. **Internal Linking** — Links out and links in. Reference the client's
   site structure from Stage 1 if available; otherwise leave placeholders
   the attendee can fill in.
6. **Keywords** — Primary keyword + secondary keywords with MSV from SE
   Ranking.
7. **Page Metadata** — URL slug, title tag, meta description, word count.
8. **Section Design** — Detailed content outline with section-by-section
   direction for the copywriter, including H1/H2/H3 structure, content
   direction for each section, word count guidance, and any visual notes.

The Section Design is the most important part of the brief. It should be
detailed enough that a copywriter can write the entire article from it
without needing to ask questions.

### Render the .docx

Use the bundled `scripts/brief-template.js` to generate the final file.

The script requires Node.js and the `docx` npm package. Run it like this:

```javascript
// generate-brief.js (create this as a temporary script)
const docx = require('docx');
const { buildBrief, p, bl, linkP } = require('<skill-path>/scripts/brief-template')(docx);

buildBrief({
  filename: '<output-path>/<Topic> - Blog Brief [company name].docx',
  clientName: '<Client Name>',
  topic: '<Topic/Category>',

  // Brand and Context
  objective: [p('...')],
  angle: [p('...')],
  voiceAndStyle: [p('...'), bl('...'), bl('...')],

  // Target Audience
  audience: [p('...'), bl('...'), bl('...')],
  searchIntent: [p('...'), bl('...')],

  // Competitors
  contentReqs: [p('...'), bl('...'), bl('...')],
  competitorUrls: [linkP('Competitor 1', 'https://...'), linkP('Competitor 2', 'https://...')],

  // Internal Linking
  linksOut: [bl('...'), bl('...')],
  linksIn: [bl('...'), bl('...')],

  // Keywords
  primaryKw: { keyword: '...', volume: '...' },
  secondaryKws: [
    { keyword: '...', volume: '...' },
    // ...
  ],

  // Page Metadata
  url: '/...',
  titleTag: '... | [company name]',
  metaDesc: '...',
  wordCount: '1,500-2,000 words',

  // Section Design
  sections: [
    {
      designNotes: [p('H1'), p('...')],
      contentDirection: [p('...'), bl('...'), bl('...')],
    },
    // ... more sections
  ],
});
```

Note: there is no `logoPath` parameter — the workshop version of the
template does not render a logo.

**docx npm module location:** if `node_modules/docx` is not already present
in the working directory, install with `npm install docx`.

### Deliver

Save the generated .docx file(s) to the outputs folder and provide download
links. Name the files using this convention:

```
<Topic Title> - Blog Brief [company name].docx
```

The literal string `[company name]` stays in the filename and inside the
brief. The attendee can find-and-replace it with their actual company name
after the workshop.

---

## IMPORTANT NOTES

- **Never estimate or fabricate search volumes.** Always pull from SE Ranking
  via MCP. If the MCP is down, stop and tell the user.
- **Australian English throughout.** Use "colour" not "color", "optimise"
  not "optimize", "analyse" not "analyze".
- **Section Design quality matters most.** This is what the copywriter
  actually uses. Make it detailed, specific, and actionable. Don't be vague
  — give concrete direction for every section.
- **Respect the client's context.** Whether you got it from a brief-format.md
  or from the 4-question interview, the brief must feel tailored to that
  specific client, not generic.
- **Batch limit is 10 briefs per run.**
- **Use `[company name]` as a literal placeholder** anywhere the original
  template referenced a specific agency name. The attendee will find-and-
  replace after the workshop.
- **No logo.** The workshop template does not render a logo above the title.
