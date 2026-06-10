# GA4 setup walkthrough

For Stage 2 of `ga4-gtm-setup`. Skip if the attendee already has a working GA4 property — just capture their Measurement ID.

## Prerequisites

- A Google account the attendee owns (Gmail or Google Workspace — both work)
- 10 minutes
- Their website URL

## Step-by-step (fresh property creation)

### 1. Open Google Analytics

Open `https://analytics.google.com/` in a new tab. Sign in with the email they want to own this GA4 property.

> **Coach tip:** push them to use an email they'll keep access to. NOT a temporary email or a former employee's account.

### 2. If they've never used GA4 before

They'll see a "Welcome to Google Analytics" screen. Click **Start measuring**.

If they have a GA account already (perhaps an old Universal Analytics one), they'll go straight to the Admin panel — skip to step 4.

### 3. Create an Analytics account

Enter:
- **Account name:** their business name (e.g. *"OB Plumbing Pros"*)
- Leave the default data sharing settings unless they have a specific compliance reason to change
- Click **Next**

### 4. Create a property

- **Property name:** their business name + " — Web" (e.g. *"OB Plumbing Pros — Web"*)
- **Reporting time zone:** Australia → Melbourne (or wherever they operate)
- **Currency:** Australian Dollar (AUD) — or their primary currency
- Click **Next**

### 5. Business details

- **Industry category:** pick the closest match. Doesn't drive ranking, drives the example benchmarks GA shows.
- **Business size:** small / medium per their headcount
- Click **Next**

### 6. Business objectives

Pick:
- **Service business:** *"Generate leads"* (turns on lead-focused report templates)
- **Ecom business:** *"Drive online sales"* (turns on ecommerce report templates)
- Both checkboxes are OK for hybrids

Click **Create** → accept Terms of Service.

### 7. Set up a data stream

GA4 asks where data is coming from. Click **Web**.

- **Website URL:** their primary domain (e.g. `https://www.obplumbingpros.com.au`)
- **Stream name:** *"Main website"* (or whatever they want)
- **Enhanced measurement:** leave ON — gives them free outbound clicks, scrolls, file downloads, video engagement
- Click **Create stream**

### 8. Capture the Measurement ID

After the stream is created, they see a panel showing:
- **Stream name**, **Stream URL**, **Stream ID**
- **MEASUREMENT ID** — in the top-right of the panel, looks like `G-XXXXXXXXXX`

Copy this. Paste it into the chat with Claude. The skill needs it for Stage 3 (GTM setup).

> **Coach tip:** the Measurement ID is what binds GTM to this specific GA4 property. If they have multiple sites, they'll have multiple Measurement IDs. Today we're setting up the one for the site they're working on.

### 9. DO NOT install the tracking code directly

GA4 will show a "Tag installation" panel suggesting they paste a snippet into their site. **Skip this** — GTM (Stage 3) handles installation more cleanly and gives them control over all their tags.

If they accidentally installed it directly: that's fine, won't break anything, but they should ALSO use GTM going forward. Two snippets isn't a disaster but creates double-counting issues — fix in Skool follow-up if it happens.

---

## Existing property — just verify

If the attendee already has GA4:

1. Ask for the Measurement ID (`G-XXXXXXXXXX`)
2. Open `https://analytics.google.com/` → Reports → Realtime
3. Have them visit their own site in a new tab
4. After 30 sec, Realtime should show 1 active user

If it doesn't show a user: their tracking isn't installed correctly OR an adblocker is preventing it. We'll re-verify properly in Stage 5 after GTM is set up.

---

## Common gotchas

| Problem | Fix |
|---|---|
| "Account creation rejected" | Their Google account needs 2FA / phone verification. Have them check email/phone for prompts. |
| Two-step verification prompts loop | Use Incognito tab. Some browsers cache stale credentials. |
| "Time zone doesn't match" | Doesn't matter for cohort 1 — pick Australia/Melbourne, can change later. |
| GDPR / cookie banner concerns | Out of scope for Day 1. Flag as a Skool topic if attendee is in a regulated industry. |
| They have Universal Analytics (old GA) | UA is sunset. Don't worry about it. Create GA4 fresh. |
| They don't know if they have GA already | Search their Gmail for "analytics.google.com" — they'll see verification emails if a property exists. |
