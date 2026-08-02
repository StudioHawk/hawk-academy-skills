# Changelog

## 2.1.1 — 2026-08-02 (bug fix)

### `hawk-academy-ecommerce-auditor`
- **Shipped the three scripts the skill has always referenced but never included.** `SKILL.md` instructed Claude to run `scripts/run_crawl.sh`, `scripts/analyze_ecommerce.py` and `scripts/build_ecommerce_docx.py`, but no `scripts/` directory was ever committed, so the skill failed partway through every run. All three now exist.
- `analyze_ecommerce.py` uses the Python standard library only, so it runs on a fresh workshop laptop. It validates Product schema against the same Merchant listing required/recommended split documented in `SKILL.md`, and reads the crawler's `crawl.json` so 404s and redirect stubs are never audited as real pages.
- `build_ecommerce_docx.py` renders the branded report in the current StudioHawk blue and black palette. Every section is optional and section numbers are assigned as sections render, so a thin crawl still produces a clean document.
- **Removed the Homebrew-only crawler install.** Homebrew is macOS-only and most workshop attendees are on locked corporate Windows laptops. The wrapper now detects the platform and resolves the crawler via `$SITEONE_CRAWLER`, `PATH`, an existing install, the binary bundled with the sibling `site-crawler` skill, and only then an official download. No admin rights needed.
- Added `scripts/run_crawl.ps1` for Windows attendees who do not have Git Bash.
- Fixed a stale reference to a `siteone-technical-audit` skill, which does not exist in this package. The crawler skill is `site-crawler`.

## 2.1.0 — 2026-07-24 (post-workshop update)

Keeps the toolkit current with how AI search moved in the six weeks after the June workshop.

### `ai-search-audit`
- **Explicit AI-crawler `robots.txt` check.** The Technical GEO section now audits each AI user-agent by name (`GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `ClaudeBot`, `Google-Extended`) and separates **training** bots from **retrieval** bots, because blocking a retrieval bot silently removes you from AI citations. Any blocked retrieval bot is flagged P0.
- **`llms.txt` presence check** added as a quick-win signal.
- **AI Overviews vs AI Mode** are now treated as two distinct Google surfaces, matching Google's June 2026 Search Console reporting split.
- Points clients to the **Search Console Generative AI performance report** (launched June 2026) as the real AI-visibility scoreboard.
- Fixed a stale example filename date and a `sameAs` typo.

### `recap-roadmap`
- The 6-month roadmap now bakes in an **AI-visibility measurement loop**: a GSC generative-AI baseline plus a recurring monthly citation check across ChatGPT, Perplexity and Google AI Mode, laddering to the north-star goal.

## 2.0.0 — 2026-06-10

Replaced the four legacy skills with the 16 Hawk Academy Workshop skills.
