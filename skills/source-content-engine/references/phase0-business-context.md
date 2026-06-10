# Phase 0 — Business Context (one-time setup)

The engine reads `./business-context.md` for locale, services, audience, voice, and competitors. Every phase depends on it. This is the ONLY point where the engine pauses for input — once the context exists, Phases 1-3 run autonomously.

## Check first
Look for `./business-context.md` in the current working directory.
- **If it exists:** read it, confirm the business name + locale back in one line, and proceed straight to Phase 1. Don't re-interview.
- **If it doesn't exist:** run the short interview below, write the file, then proceed.

## Interview (ask conversationally; group 2-3 per message)
1. **Business name** — trading name.
2. **What you do** — one or two sentences.
3. **Where you serve** — city/region/country or "online/national". Sets the keyword database locale.
4. **Services or products** — the main 5-10 things to be found for. (The first one seeds Phase 1.)
5. **Ideal customer** — who buys (B2B/B2C, homeowner/trade, budget/premium).
6. **Top customer questions** — what prospects ask before buying (4-10).
7. **Competitors** — 2-5 rival domains (actual URLs — they feed competitor research).
8. **What makes you different** — the real point of difference.
9. **SEO goal** — e.g. local leads, e-commerce sales, authority.
10. **Brand voice** — how they want to sound.

If the attendee already gave some of this in their opening message, confirm rather than re-ask.

## Locale mapping (derive, don't ask)
From "where you serve", set a two-letter SE Ranking `Locale source` code: Australia `au`, US `us`, UK `uk`, NZ `nz`, Canada `ca`. Default `au` if Australian or unclear.

## Write `./business-context.md`
Use this exact structure so every phase can parse it:

```markdown
# Business Context

- **Business name:** ...
- **What we do:** ...
- **Where we serve:** ...
- **Locale source (SE Ranking db code):** au
- **SEO goal:** ...
- **Ideal customer:** ...
- **Brand voice:** ...

## Services / products
- ...

## Top customer questions
- ...

## Competitors
- example-rival.com.au

## What makes us different
...
```

Never invent competitor domains — if unknown, write "TBC — attendee to add". AU businesses get Australian English.
