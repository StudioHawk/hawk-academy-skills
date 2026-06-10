# Site Crawler — all-in-one bundle (SiteOne Crawler v2.3.0)

Crawl any website like Screaming Frog — free, no licence, no signup. This bundle includes the
crawler binaries for **Mac (Apple Silicon + Intel)** and **Windows**, a one-command installer, and a
Claude skill so you can just ask Claude to do the whole thing.

## Easiest way — let Claude do it
Add this folder as a skill (drag the zip into Claude → Install, or Customise → Add Skill), then say:
> **"Crawl my site"**

Claude installs the crawler, runs the crawl, and explains the results in plain English.

## Manual install (2 minutes)

**Mac:** double-click won't work for terminal tools — open Terminal in this folder and run:
```
bash install.sh
```
It detects your chip, installs from the bundled files (no internet needed), and sets up the
`siteone-crawler` command.

**Windows:** unzip `binaries/siteone-crawler-v2.3.0-win-x64.zip` to a folder
(e.g. `C:\siteone-crawler`), then in that folder run:
```
siteone-crawler.exe --url=https://yourdomain.com.au/
```

**Linux:** `bash install.sh` (downloads the right Linux build automatically).

## Run a crawl
```
siteone-crawler --url=https://yourdomain.com.au/
```
Handy extras:
```
--output-html-report=report     # full interactive HTML report
--markdown-export-dir=md        # pages as markdown (feeds other skills)
--offline-export-dir=offline    # offline copy of your site
```

## What you get
Pages, titles, meta descriptions, H1s, broken links, redirects, slow pages, image sizes — the raw
material your AI Search Audit and Information Architecture steps build on.

Source & docs: https://github.com/janreges/siteone-crawler (open source, MIT-style licence — see
LICENSE inside each binary package). Bundled version: **v2.3.0** (March 2026).
