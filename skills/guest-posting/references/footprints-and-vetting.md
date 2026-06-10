# Finding & vetting guest-post opportunities

## Search footprints (swap in the niche / city)
```
{niche} "write for us"
{niche} "guest post" OR "guest article"
{niche} "contribute" inurl:write-for-us
{niche} intitle:"write for us"
{niche} "become a contributor"
{niche} "submit a guest post"
{niche} "guest post guidelines"
{niche} "accepting guest posts"
{niche} blog "this is a guest post by"
{city} {niche} blog "write for us"
```
Generate these automatically with `scripts/guest_post_finder.py footprints --niche "..." --location "..."`.

## Other discovery angles
- **Competitor backlinks** — find where rivals already guest-posted (SE Ranking → backlinks / referring domains) and pitch the same sites. If they published a rival, they'll consider you.
- **Be the expert quote (AU)** — SourceBottle and Qwoted connect journalists to sources daily; a quote often earns a link without writing a full post.
- **Reuse the RAIDS media list** — the journalists you pitch for digital PR are also a guest-post network.
- **Local angles** — local news, council/community sites, industry associations, chambers of commerce.

## Vetting — only pitch a site if it passes ALL of these
1. **Relevant** — the audience overlaps with the business's customers. A link from an unrelated blog does little.
2. **Real** — the site is indexed (search `site:domain.com`), has genuine traffic, and recent posts. Skip abandoned or content-farm blogs.
3. **Links out (dofollow likely)** — check an existing post; if all external links are `nofollow` or sponsored, the SEO value is low (still fine for referral/brand).
4. **Not a link scheme** — avoid "guest post network" sites that publish anything for a fee, foreign-language link farms, or sites with hundreds of low-quality guest posts. These can *hurt* rankings.
5. **Editorial standard** — would a real person actually read it? Quality of existing posts is the tell.

Mark each prospect **Relevance** (High/Medium/Low) and **Dofollow** (Likely/Unknown/Nofollow). Prioritise High + Likely first.

## What to pitch (the angle)
Lead with something only this business has — the **URC** unique asset: original data, a client-results story, a strong contrarian take, or a free tool. A generic "10 tips" post gets ignored; a data point or first-hand story gets accepted.
