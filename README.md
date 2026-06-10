# Hawk Academy Skills

The 16 Claude skills taught at StudioHawk's Hawk Academy Workshop. Each skill turns a common SEO task into a guided, repeatable workflow that ends in a writer-ready or client-ready deliverable. They run inside your Claude (Claude Code or the desktop app), pull live keyword data from SE Ranking where relevant, and produce branded `.docx` / `.xlsx` / `.md` outputs.

Workshop attendees: the workshop hub at [hawkos-lite.pages.dev](https://hawkos-lite.pages.dev) has install steps, the shared SE Ranking key, useful links and an example output for every skill.

## Install

In Claude: **Customize → Plugins → Personal plugins → + → Add marketplace**, then paste:

```
StudioHawk/hawk-academy-skills
```

Or in Claude Code:

```
/plugin marketplace add StudioHawk/hawk-academy-skills
/plugin install hawk-academy-skills@hawkos-lite
```

## Skills (in workshop order)

| # | Skill | What it does | Output |
|---|-------|--------------|--------|
| 1 | `business-context` | First-run skill: ~10 questions about your business, written to `business-context.md`. Every other skill reads it, so you never re-state your business. | `.md` |
| 2 | `site-crawler` | Bundles the free SiteOne crawler (Mac + Windows binaries included), runs the crawl and explains pages, broken links, redirects and missing titles/metas/H1s. | Crawl report |
| 3 | `ai-search-audit` | Baseline SEO / GEO / AEO audit of a website. The foundation of the workshop. | `.docx` + PDF |
| 4 | `information-architecture` | Turns a sitemap/domain into a keyword-mapped IA with live SE Ranking data and KEEP/REMOVED vetting. | `.xlsx` + CSV |
| 5 | `top-10-pages` | Reads the audit + IA, confirms intent, ranks the 10 highest-value pages to create or optimise, nominates one pillar + spokes. | `.md` |
| 6 | `urc-elevation` | Runs each priority page through Uniqueness / Relevance / Credibility, starting with a search-intent gate. | `.md` per page |
| 7 | `source-content-engine` | End-to-end engine: keyword research, pillar-and-spoke cluster, then writer-ready briefs in one run. | `.docx` + CSV |
| 8 | `keyword-research` | Live keyword research via the SE Ranking Data API: volumes, CPC, intent, difficulty, clustered and vetted. | CSV + `.md` |
| 9 | `hawk-academy-ecommerce-auditor` | Crawls an online store and audits it like a StudioHawk eComm SEO: categories, product schema, product pages, blog tie-back. | `.docx` |
| 10 | `hawk-academy-local-seo-checker` | GBP completeness scorecard, NAP consistency, review analysis, 3-pack report and a prioritised local action plan. | `.docx` |
| 11 | `au-backlinks` | Audits an AU business's free backlink and citation opportunities and writes a personalised tracker. | Tracker |
| 12 | `guest-posting` | Finds, vets and helps pitch guest-post opportunities, with a prospect tracker and outreach emails. | CSV + emails |
| 13 | `digital-pr-raids` | Data-led digital PR through RAIDS: ideation sheet, dataset, media list, pitch + press release, coverage tracker. | `.docx` + `.xlsx` |
| 14 | `ux-insights` | Installs Microsoft Clarity, then diagnoses UX problems from pasted analytics data into a prioritised fix list. | `.docx` |
| 15 | `ga4-gtm-setup` | Five-stage GA4 + GTM setup with the Hawk Academy starter container and Looker Studio dashboard. | Tracking setup |
| 16 | `recap-roadmap` | Day 1 debrief, then a phased 6-month roadmap built from every deliverable in your workspace. | `.md` + `.docx` |

## SE Ranking API key

Skills that pull live keyword data read the `SE_RANKING_API_KEY` environment variable (or use the key configured as a connector). The key is **not** stored in this repository. Workshop attendees can copy the shared workshop key from the hub: [hawkos-lite.pages.dev](https://hawkos-lite.pages.dev) → **SE Ranking Key**.

## Repository structure

```
.claude-plugin/
  marketplace.json   ← marketplace "hawkos-lite"
  plugin.json        ← plugin "hawk-academy-skills"
skills/
  <one folder per skill, each with SKILL.md at its root>
```
