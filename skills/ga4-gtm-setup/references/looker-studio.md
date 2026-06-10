# Looker Studio dashboard walkthrough

For Stage 4 of `ga4-gtm-setup`. ~10 min. Gives attendees a one-click clone of the Hawk Academy SEO dashboard, connected to their own GA4 property.

## Why a pre-built dashboard

Most SMBs never build their own dashboard. They check GA4 once, get overwhelmed, never come back. A pre-built dashboard:

- Shows them the 5-7 numbers that actually matter for SEO
- One bookmark, weekly habit
- Looks more polished than raw GA4 reports
- Pre-tuned for service vs ecom emphasis

## The Hawk Academy template

**Template URL:** https://datastudio.google.com/reporting/83f2f965-9d54-4480-b770-1de0a1baea95

The template should include:

### Page 1 — Headline numbers (top section)

- Organic sessions (last 30 days) + WoW % change
- Organic users (last 30 days) + WoW
- Avg engagement time
- Total goals / conversions OR revenue (service vs ecom)

### Page 1 — Top performers (middle section)

- Top 10 organic landing pages (URL + sessions + conversions)
- Top 10 organic search queries (pulled from Google Search Console — set up later if not yet linked to GA4)
- Top 10 source/mediums

### Page 1 — Splits (bottom section)

- Mobile vs desktop traffic
- New vs returning visitors
- Top 10 countries (or AU vs ROW for AU-focused businesses)

### Page 2 — Service-mode extras (auto-hidden in ecom mode via filter)

- Phone click events (total + by page)
- Form submission events
- File download events
- Outbound link clicks

### Page 2 — Ecom-mode extras (auto-hidden in service mode)

- Add-to-cart funnel: view_item → add_to_cart → begin_checkout → purchase (conversion rate at each step)
- Revenue by product
- Revenue by landing page
- Revenue by source

---

## Step-by-step (cloning the template)

1. Open the template URL (see Template URL above)
2. Click **Use template** in the top-right
3. **Data source selection panel** opens:
   - The template uses placeholder data sources. Click each placeholder.
   - Select **Google Analytics**.
   - Authorise Looker Studio to access your GA4 account (one-time).
   - Pick the **GA4 property** you created in Stage 2.
4. Click **Copy Report**
5. The new report opens. Top-left: rename it to *"[Business Name] — Hawk Academy SEO Dashboard"*
6. **Bookmark the URL** in their browser
7. Share access if they want — they can add team members under File → Add people

---

## What if the GSC data is missing?

The "Top 10 organic search queries" widget requires Google Search Console linked to GA4.

If GSC isn't linked:
- The widget shows "No data"
- Their GSC may not be connected yet (set up in Skool Month 2 via the `gsc-audit-7` skill)
- OR they don't have GSC at all (also Skool Month 2 territory)

For Day 1, the widget being empty is fine. Note it in the chat: *"GSC data will fill in once we connect Search Console next month."*

---

## Customisation suggestions (for attendees who want to extend)

After Day 1, attendees can:

- **Add scorecards for their specific KPIs** — like "calls from Google" or "average order value"
- **Filter by date range** — last 7 days, last 30 days, this month vs last month
- **Add comparison columns** — show YoY (this month vs same month last year)
- **Create custom segments** — e.g. "visitors from Sydney" or "visitors who hit the contact page"

Looker Studio has a steep learning curve but generous free tier. Encourage them to spend 30 min in Month 2 watching a Looker Studio basics tutorial — covered in the Skool community.

---

## Common gotchas

| Symptom | Fix |
|---|---|
| "Use template" button is greyed out | Looker Studio access not granted — they need to sign in with the same Google account as their GA4 property |
| Data source can't find their GA4 property | Refresh the data source list (sometimes takes 1-2 min after property creation to propagate). Worst case: log out + back in. |
| "No data" everywhere on the dashboard | GA4 property is too new — needs at least 24-48 hours of data to populate. Fine for Day 1 (they just set it up). Have them re-check next day. |
| GSC widget shows error | GSC not linked to GA4. Day 1 = expected, skip. Skool Month 2 covers linking. |
| Mobile vs desktop split shows 0 mobile | Could be real (their site doesn't get mobile traffic), or could be tracking issue. Cross-check with their phone visiting the site → should appear as mobile within an hour. |

---

## Output

After Stage 4:
- Looker Studio URL bookmarked in attendee's browser
- They've named the report after their business
- They know how to come back to it (URL in their bookmark bar)

If `./ga4-setup/<domain>-<date>.md` is being saved (per the SKILL.md option), include:
- The Looker Studio dashboard URL
- Notes if any pages of the template needed troubleshooting

---

## Future improvements (Skool roadmap)

- Month 2: Connect GSC → fill in the missing widget
- Month 3: Add GBP-driven traffic dashboard
- Month 4: Conversion attribution model
- Month 6: Multi-month YoY view
