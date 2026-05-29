# Hawk Academy Skills

A collection of Claude skills built for the StudioHawk Hawk Academy workshops. Each skill turns a common SEO task into a guided, repeatable workflow that ends in a writer-ready or client-ready deliverable. They are workshop-friendly versions of StudioHawk's internal tooling: they pull live keyword data via the SE Ranking MCP, run short interviews when context is missing, and produce branded `.docx` / `.xlsx` outputs.

## Skills

### `hawk-academy-content-brief-engine`
Generates a branded "Visual SEO Content Brief" `.docx` for any client. Single-phase workflow: gathers context, pulls keyword data live from SE Ranking, and produces the final brief in one run. Runs a quick 4-question interview (industry, audience, voice, competitors) when no client profile exists. Supports batching up to 10 briefs at a time.

### `hawk-academy-ia-mapper`
Keyword-mapped Information Architecture builder. Takes a sitemap, domain, or URL list, classifies every URL into a section, pulls live keyword data, auto-vets each keyword (KEEP/REMOVED with a one-line reason), and outputs a hierarchically-sorted `.xlsx` + `.csv` with one row per page plus a Vetting Log sheet. Includes a thin-site fallback that proposes an IA from scratch.

### `hawk-academy-local-seo-checker`
Local SEO audit skill. Takes a single combined intake of Google Business Profile details, citation entries, a review snapshot, and target local keywords, then produces a branded `.docx` with a GBP completeness score, NAP consistency report, review analysis, local keyword + 3-pack ranking report, and a prioritised action plan. Defaults to an Australian locale and AU citation set.

### `hawk-academy-topic-cluster-builder`
Builds a complete topic cluster (pillar page + 8-10 spokes) mapped against a site's existing content, with gap analysis, recommended URL structures, and an internal linking plan, delivered as a `.docx`. Keyword data (MSV, CPC, intent) is pulled live from SE Ranking. Triggered by `/cluster-builder` or any natural-language equivalent.

## Repository structure

```
skills/
  hawk-academy-content-brief-engine/
    SKILL.md
    scripts/
  hawk-academy-ia-mapper/
    SKILL.md
    references/
    scripts/
  hawk-academy-local-seo-checker/
    SKILL.md
    scripts/
  hawk-academy-topic-cluster-builder/
    SKILL.md
    scripts/
```

Each skill follows the standard skill layout: a `SKILL.md` with YAML frontmatter (`name` + `description`) and the workflow instructions, plus supporting `scripts/` and `references/` where relevant.

## Requirements

These skills are designed to run inside a Claude environment (Claude Code or Cowork) with:

- The SE Ranking MCP connected, for live keyword data.
- Python 3 with `python-docx` and `openpyxl` available for the `.docx` / `.xlsx` builders.

## Usage

Install or reference the skills in your Claude skills directory, then invoke them by describing the task in natural language (for example, "build a content brief for [client]" or "do an IA for example.com.au"). Each skill's `SKILL.md` documents its full workflow and triggers.

## Notes

Built for the StudioHawk Hawk Academy workshop. Outputs follow StudioHawk brand and writing conventions: Australian English, no em dashes, plain confident tone.
