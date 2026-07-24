# Changelog

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
