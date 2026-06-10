---
name: source-content-engine
description: End-to-end SEO content engine for the Hawk Academy workshop. Runs one autonomous pipeline — keyword research, then a pillar-and-spoke content cluster built around the main keywords, then a writer-ready content brief for the pillar and each spoke. All keyword data is pulled live from the SE Ranking Data API (SE_RANKING_API_KEY). Use this skill whenever an attendee wants to go from a topic or domain to a full content plan: "run the source content engine", "build content from keyword research", "research keywords and plan content for [domain]", "I want a content cluster and briefs for [topic]", "/source-content-engine", or any request that spans keyword research + clustering + briefs. Also trigger for any one of those three jobs alone — keyword research, a topic cluster, or a content brief — since each is a phase of this engine. Produces a keyword CSV/MD, a cluster .docx, and brief .docx files in the attendee's workspace folder.
---

# Source Content Engine

You run one continuous, autonomous pipeline that takes a Hawk Academy attendee from a topic (or just a domain) all the way to writer-ready content briefs. There are three phases and they always flow in the same direction:

**Keyword research → Content cluster (built around the main keywords) → Content briefs (one per pillar + spoke).**

Each phase hands its output to the next with no stops for approval. The only pause is the one-time business-context setup (Phase 0) when the attendee has never run the engine in this folder before.

This skill merges three former workshop skills (keyword research, topic-cluster builder, content-brief engine) into a single installable unit. All three now share one SE Ranking connection — the Data API key — so there is nothing else to configure.

## Bundled resources

- `scripts/seranking.py` — SE Ranking Data API helper (stdlib only). Powers all keyword data in every phase.
- `scripts/build_cluster_docx.py` — renders the cluster Word document (needs `python-docx`).
- `scripts/brief-template.js` — renders each content brief Word document (needs Node + the `docx` npm package).
- `references/phase0-business-context.md` — one-time context interview + file format.
- `references/phase1-keyword-research.md` — Phase 1 detail.
- `references/phase2-cluster-builder.md` — Phase 2 detail.
- `references/phase3-content-brief.md` — Phase 3 detail.

Run all scripts from this skill's directory using the relative `scripts/...` paths shown in the phase docs.

## Setup checks (do silently, in order, before Phase 0)

1. **API key.** Run `python3 scripts/seranking.py smoke`. The shared workshop key is built in, so this should just work. If the attendee has their own key, they can set `SE_RANKING_API_KEY` in `~/.zshrc` to override. If it prints `HTTP 400 (No token / bad key)`, the key is wrong — have them re-paste it. A healthy smoke test prints subscription info with credits remaining.
2. **Dependencies (install if missing, don't ask):**
   - `pip install python-docx --break-system-packages` (for the cluster .docx)
   - `npm install docx` in the working directory (for the brief .docx files)
   The stdlib helper needs nothing.

## The pipeline

Read each phase's reference doc at the start of that phase, then execute it. Carry the named handoff object from one phase into the next.

### Phase 0 — Business context (one-time pause)
Follow `references/phase0-business-context.md`. If `./business-context.md` exists, read it and continue. If not, run the 10-question interview, write the file, then continue. **This is the only interactive step** — after it, run straight through.

### Phase 1 — Keyword research
Follow `references/phase1-keyword-research.md`. Produces the saved keyword deliverable (`./keyword-research/*.md` + `.csv`) and hands forward `main_keywords` = { pillar_keyword, candidate_spoke_keywords, source }.

### Phase 2 — Content cluster
Follow `references/phase2-cluster-builder.md`. Crawls the site, builds a pillar + 8-10 spokes around `main_keywords`, pulls metrics via `seranking.py metrics --json`, renders `cluster-<pillar-slug>-<date>.docx`, and hands forward `cluster` = { pillar, spokes[] }.

### Phase 3 — Content briefs
Follow `references/phase3-content-brief.md`. Generates one "Visual SEO Content Brief" .docx for the pillar and each spoke (capped at 10 per run), using `./business-context.md` for context and `seranking.py metrics --json` for secondary-keyword volumes.

## Autonomy

After Phase 0, do not stop between phases or ask for confirmation — the attendee chose a fully autonomous run. If something genuinely blocks the pipeline (missing key, SE Ranking error, no sitemap found), surface the specific problem and stop; otherwise keep moving. Make reasonable calls (which spoke is highest priority, which competitor article to cite) without checking in.

## Final summary (after Phase 3)

Give one tight wrap-up (under 150 words) covering:
- Pillar keyword (+ MSV) and how many spokes (new vs refresh).
- Whether a blog section needs building first.
- The full list of deliverables saved to the workspace: the keyword CSV/MD, the cluster .docx, and the brief .docx files (count them).
- One sentence on what to do first (usually: build/refresh the pillar, then the highest-priority spoke).

Don't re-dump the clusters or briefs in chat — point to the files.

## Quality bar (applies to every phase)

- **Never fabricate keyword data or URLs.** Volumes/difficulty/intent come from `seranking.py`; existing URLs come from the real sitemap crawl. Missing data is `0`/`TBC`, never invented.
- **One credit-aware call per metrics pull.** `metrics` is 100 credits flat regardless of list size — batch, never loop.
- **Australian English** for `au`-locale clients throughout.
- **Brief Section Design is the crown jewel** — detailed enough to write from without questions.
- **`[company name]` stays literal** in brief filenames and bodies for the attendee to find-and-replace.
