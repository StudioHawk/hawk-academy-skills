---
name: site-crawler
description: >
  Installs and runs the free SiteOne Crawler (a Screaming Frog alternative) and reads the results.
  All-in-one: detects the attendee's computer (Mac Apple Silicon / Mac Intel / Windows / Linux),
  installs the bundled binary with no licence or signup, crawls any website with a live progress
  view, then summarises what the crawl found — pages, titles, broken links, redirects, slow pages,
  missing metadata — and exports reports the other workshop skills can use. Use whenever a user
  says "crawl my site", "run the site crawler", "install the crawler", "scan my website like
  Screaming Frog", "find broken links", or /site-crawler.
---

# Site Crawler — install, crawl, read the results

You install SiteOne Crawler for the attendee, run a crawl of their site, and translate the output
into plain English. No licence, no signup — the binaries are bundled right here.

## Step 1 — Install (once)
Check if it's already available: `siteone-crawler --version` (or `~/siteone-crawler/siteone-crawler --version`).

If not installed:
- **Mac / Linux:** run the bundled installer from this skill's directory:
  ```
  bash install.sh
  ```
  It auto-detects Apple Silicon vs Intel and installs from `binaries/` (no internet needed on Mac).
- **Windows:** extract `binaries/siteone-crawler-v2.3.0-win-x64.zip` to a folder (e.g. `C:\siteone-crawler`)
  and run `siteone-crawler.exe` from there. Offer to do this for the user if running in a shell.

## Step 2 — Crawl
Confirm the domain (read `./business-context.md` if present), then run:
```
siteone-crawler --url=https://theirdomain.com.au/
```
Useful flags:
- `--output-html-report=report` — the full interactive HTML report
- `--offline-export-dir=offline` — an offline copy of the site
- `--markdown-export-dir=md` — pages as markdown (great input for other skills)
- `--max-visited-urls=1000` — cap for very large sites (default is fine for most SMBs)

Let it run; it shows live progress. Big sites take a few minutes.

## Step 3 — Read the results for them
Open the output (the console summary and/or HTML report directory) and summarise in plain English:
- **Size & shape:** total pages, sections, depth.
- **Problems:** broken links (404s), redirect chains, slow pages, oversized images,
  missing/duplicate titles and meta descriptions, missing H1s.
- **Quick wins:** the 5 most impactful fixes, named with the actual URLs.
Keep it tight — this feeds the AI Search Audit and Information Architecture steps, so point the
attendee there next: the audit gives the scored baseline; the IA maps keywords to every page found.

## Rules
- **Australian English.** Plain language — the attendee may never have crawled a site before.
- **Never crawl a site the user doesn't own/manage** without flagging that polite crawling etiquette
  applies (the crawler respects robots.txt by default — leave that on).
- If the crawl fails (firewall, bot protection), say so honestly and fall back to the sitemap
  (`/sitemap.xml`) so the workshop can continue.
