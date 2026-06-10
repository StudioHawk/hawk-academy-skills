# The URC Framework — full detail

URC is the quality lens that turns a competent brief into a page worth citing. It asks three questions
of every page, in order. A page that nails all three is something an LLM can't generate on its own —
because it carries the business's own data, the real answer, and verifiable trust.

---

## U — Uniqueness — "Why you, not them?"
The information-gain layer. If a model could write it from everyone else's content, it adds nothing.

**What good looks like**
- Original data, surveys, or internal research no one else has.
- First-hand experience the LLMs can't synthesise from elsewhere.
- A point of view — your stance, your bets, your why.
- Unique formats: tools, calculators, original imagery, templates.

**Owner-facing question**
> "What do you have on this topic that no competitor does — real numbers from your business, a customer story, a strong opinion/stance, or a tool or calculator we could build?"

**Turn answers into items like**
- "Add the '66% of members never use their membership' stat from your intake data."
- "Build a simple cost-per-visit calculator and embed it."
- "Lead with your contrarian take: lock-in contracts don't drive attendance."

---

## R — Relevance — "Does this answer the question they actually asked?"
The gate. If the content doesn't address the real query, nothing else helps. Run it in two parts —
**intent first, then depth.**

### R1 — Intent match (do this first)
You can't elevate a page that's the wrong *type*. Don't guess the intent — let the SERP show you.

**Owner-facing prompt**
> "Quick check — Google `[target keyword]` and tell me what kind of pages rank on page 1 (or paste me the top result): guides/how-tos (**informational**), 'best'/comparisons (**commercial**), product·service·booking pages (**transactional**), or a map pack + 'near me' listings (**local**)?"

**The rule: match the SERP, don't fight it.** Map what they see to the page type:
- Guides/how-tos → informational → a guide/article
- "Best"/comparisons/reviews → commercial → a comparison or "best X" page
- Product/service/booking pages → transactional → a service/product page
- Map pack + "near me" → local → a local/suburb page (+ Google Business Profile)

Then confirm the page being **created or optimised is that same type**. If it's a mismatch (a hard
sales page for an informational query, or a thin service page for a "how much does it cost" search),
**flag it and recommend the right page type before doing anything else.** Record the confirmed intent
and page type in the elevation block.

### R2 — Depth & coverage
**What good looks like**
- Topical depth: the page covers the whole question, not just the keyword.
- Entity coverage: the right concepts, in the right order, named clearly.
- Internal links that reinforce relevance to the rest of the site.

**Owner-facing question**
> "What's the exact question someone is really asking when they land on this page — and is anything they'd need to make a decision missing from the current plan?"

**Turn answers into items like**
- "Add a 'how much does it cost' section — it's the first thing they ask."
- "Answer 'is it beginner-friendly?' explicitly near the top."
- "Internally link to the Hyrox coaching page and the pricing FAQ."

---

## C — Credibility — "Why should Google, an LLM or a customer trust this?"
The trust layer. Determines whether you get cited and whether the visitor believes you.

**What good looks like**
- Named author with real credentials and a public footprint.
- Citations to primary sources, not other content marketers.
- Reviews, testimonials, case studies — third-party signals.
- Schema for Author, Organisation, and Review where relevant.

**Owner-facing question**
> "Who's the credible human behind this, and what proof can we show — results, reviews, qualifications, or primary sources we can cite?"

**Turn answers into items like**
- "Attribute to Laura Healy (Ironman triathlete, 8 yrs coaching) with an author bio + Person schema."
- "Embed 3 named client results from /clientresults."
- "Cite the ABS / Finder source directly, not a blog that quoted it."

---

## The elevation block (what each page ends with)
Append to the page's brief:

```
## URC Elevation
**Search intent:** <informational | commercial | transactional | local>  ·  **Page type:** <guide | comparison | service/product | local page>
**Uniqueness:** <specific items>
**Relevance:** <specific items>
**Credibility:** <specific items>
**To gather:** <stats / quotes / testimonials the owner still needs to collect>
```

This is the spec the writing step builds from — so the unique data, the real answer, and the trust
signals are decided up front, not improvised during drafting.
