# GTM setup walkthrough

For Stage 3 of `ga4-gtm-setup`. ~20 min total. Split into:

- 3a. Get a GTM container (5 min)
- 3b. Install GTM on their site (5-10 min — most variance)
- 3c. Import the Hawk Academy starter container (3 min)
- 3d. Add the event tags they need (mode-dependent — see bottom of doc)

## Prerequisites

- A Google account (same one as their GA4)
- GA4 Measurement ID from Stage 2 (looks like `G-XXXXXXXXXX`)
- Admin access to their website (WordPress admin, Shopify admin, etc.)

---

## 3a. Create a GTM container (5 min)

### If they DON'T have GTM yet

1. Open `https://tagmanager.google.com/` in a new tab
2. Sign in with the same Google account as their GA4
3. Click **Create Account**
   - **Account name:** their business name
   - **Country:** Australia (or wherever they operate)
4. **Container name:** their primary domain (without `https://`, e.g. `obplumbingpros.com.au`)
5. **Target platform:** **Web** (NOT iOS/Android/AMP/Server)
6. Click **Create** → Accept Terms of Service
7. They land on the container homepage. The top bar shows their **Container ID** (`GTM-XXXXXXX`). Copy this.

### If they DO have GTM already

Ask for the Container ID. Have them log in and skip to 3c (import the starter container into their existing setup).

---

## 3b. Install GTM on their website

This is the most platform-specific step. GTM gives them two code snippets:
1. A `<script>` for the `<head>` of every page
2. A `<noscript>` for the start of `<body>` on every page

How to install depends on their platform:

### WordPress + SEO plugin (Yoast / Rank Math / All-in-One SEO)

Most modern SEO plugins have a "Google Tag Manager" field in Settings → Integrations:
- **Yoast:** Yoast SEO → Integrations → No GTM field in free; need Yoast SEO Premium OR use a separate plugin
- **Rank Math:** Rank Math → General Settings → Analytics → Google Tag Manager ID
- **All-in-One SEO:** AIOSEO → General Settings → Webmaster Tools → Google Tag Manager

Paste `GTM-XXXXXXX`. Save. Done.

### WordPress + GTM4WP plugin (recommended for ecom)

1. WordPress admin → Plugins → Add New → search "GTM4WP" → Install + Activate
2. Settings → Google Tag Manager → paste `GTM-XXXXXXX`
3. **For ecom:** in GTM4WP settings, enable "WooCommerce integration" → choose which events to track (view_item, add_to_cart, purchase, etc.)
4. Save

GTM4WP is specifically built for the dataLayer pattern GTM expects. **Strongly recommended for ecom attendees** because manual dataLayer setup is painful.

### WordPress without a helper plugin (manual)

In their theme's `header.php`:
- Paste the `<script>` snippet immediately after `<head>`
- Paste the `<noscript>` snippet immediately after `<body>`

> **Coach warning:** editing theme files directly will be overwritten on theme update. Use a child theme OR use a helper plugin. Flag in Skool follow-up.

### Squarespace

Settings → Advanced → Code Injection
- **Header:** paste `<script>` snippet
- **Footer:** paste `<noscript>` snippet (Squarespace doesn't expose `<body>` directly — footer is the closest, GTM tolerates this)

### Wix

Wix admin → Marketing & SEO → Marketing Integrations → Custom Code
- Click **Add Custom Code**
- Paste the GTM snippet, set "Add Code to Pages: All Pages", "Place Code in: Head" → Apply
- Repeat for the body snippet, place in "Body — start"

### Webflow

Project Settings → Custom Code
- **Head Code:** paste `<script>` snippet
- **Footer Code:** paste `<noscript>` snippet (Webflow doesn't expose body-start)
- Publish to all pages

### Shopify (ecom)

**Recommended path:** install the **Google & YouTube channel** app from the Shopify App Store. It auto-installs GA4 + Conversion API without GTM — simpler for non-technical attendees.

**If they want GTM specifically:**
1. Shopify admin → Online Store → Themes → Customize → Edit code
2. Open `theme.liquid`
3. Paste `<script>` snippet immediately after `<head>`
4. Paste `<noscript>` snippet immediately after `<body>`
5. Save

> **Coach note:** Shopify has its own quirks with GA4 ecommerce events. Even with GTM, ecom event coverage may be partial without a helper app. Flag for Skool follow-up.

---

## 3c. Import the Hawk Academy starter container (3 min)

Run the customise script to swap the placeholder Measurement ID for the attendee's actual one:

```bash
python3 <skill-dir>/scripts/customise_gtm.py \
  --template <skill-dir>/templates/gtm-starter.json \
  --measurement-id G-XXXXXXXXXX \
  --out ~/Downloads/hawk-academy-gtm.json
```

Then in GTM:

1. **Admin** (top-right) → **Import Container**
2. Click **Choose container file** → select `~/Downloads/hawk-academy-gtm.json`
3. **Workspace:** New → name it *"Hawk Academy Setup"*
4. **Import option:** **Merge** (preserves any existing tags they have)
5. Click **Confirm**
6. Review the imported tags + variables + triggers — walk attendee through what each one does (see "What's in the starter" below)
7. Top-right: **Submit** → Version name *"Hawk Academy initial setup"* → **Publish**

After Publish, the tags are LIVE on their website. Stage 5 verifies.

### What's in the starter container

The starter ships these:

| Item | Type | What it does |
|---|---|---|
| `GA4 - Configuration` | Tag (Google Tag) | Sends a page_view to GA4 on every page load + enables Enhanced Measurement (free clicks, scrolls, file downloads) |
| `All Pages` | Trigger (Page View) | Fires the GA4 tag on every page |
| `Page URL` | Built-in variable | Available for custom triggers/tags later |
| `Page Hostname` | Built-in variable | — |
| `Page Path` | Built-in variable | — |
| `Click URL` | Built-in variable | Available for click-based tracking (phone, email, outbound) |
| `Click Element` | Built-in variable | — |
| `Form Element` | Built-in variable | Available for form submission tracking |

After Publish, attendees have GA4 firing on every page. The other 6 event tags (clicks, forms, scrolls, ecom) are added manually in 3d below.

---

## 3d. Add the event tags they need

The starter only handles page views. Most attendees want more — at minimum, phone clicks (service) or ecommerce events (ecom). Walk them through adding the tags they need.

### Universal event tags (both service + ecom)

**Phone click tracking** — fires when someone clicks a `tel:` link:

1. GTM → Tags → New
2. **Tag Configuration:** Google Analytics: GA4 Event
3. **Measurement ID:** select GA4 Configuration tag from dropdown (NOT paste the ID — link to the existing tag)
4. **Event Name:** `phone_click`
5. **Event Parameters:** add `link_url` = `{{Click URL}}`
6. **Triggering:** New trigger → Just Links → Some Link Clicks → "Click URL starts with `tel:`"
7. Save. Name the tag *"GA4 - Phone Click"*.

**Email click tracking** — same as phone click, but trigger is "Click URL starts with `mailto:`":
- Event name: `email_click`

**Outbound link click** — fires when someone clicks a link to another domain:
1. Tag: GA4 Event, event name `outbound_click`, parameter `link_url` = `{{Click URL}}`
2. Trigger: Just Links → Some Link Clicks → "Click URL does not contain {{Page Hostname}}"

**Form submission tracking** — fires when any form is submitted:
1. Tag: GA4 Event, event name `form_submit`, parameter `form_id` = `{{Form ID}}` (enable Form ID built-in variable first under Variables → Built-In Variables → Configure)
2. Trigger: Form Submission → All Forms (or "Some Forms" with conditions if they have spammy newsletter forms etc.)

**Scroll depth** — fires at 50%, 75%, 90%:
1. Tag: GA4 Event, event name `scroll`, parameter `percent_scrolled` = `{{Scroll Depth Threshold}}`
2. Trigger: Scroll Depth → Vertical Scroll Depths: 50, 75, 90 (Percentages) → On all pages

### Service-mode extras

- **File download tracking** (PDF, DOC, ZIP — common for capability statements, brochures):
  - Tag: GA4 Event, event name `file_download`
  - Trigger: Just Links → URL ends with `.pdf` OR `.doc` OR `.docx` OR `.zip`

- **"Get a quote" CTA click** — if they have specific quote-form buttons:
  - Tag: GA4 Event, event name `quote_request`
  - Trigger: Click → specific button class or ID

### Ecom-mode extras

**Critical prerequisite:** their ecom platform must populate the dataLayer with ecommerce events. WordPress + WooCommerce + GTM4WP does this. Shopify with Google & YouTube channel does this. Custom builds usually don't — flag as homework.

If their dataLayer is populated, add these tags:

- **view_item** — fires on product page view
  - Tag: GA4 Event, event name `view_item`, send Ecommerce data = True
  - Trigger: Custom Event → `view_item`

- **add_to_cart** — same pattern, custom event `add_to_cart`
- **begin_checkout** — custom event `begin_checkout`
- **purchase** — custom event `purchase` (this is THE money one — verify it fires after a test purchase)
- **view_item_list** — custom event `view_item_list` (category page view)
- **select_item** — custom event `select_item` (product card click)

For each, enable **Send Ecommerce data** in the tag configuration and set **Data source** to **Data Layer**.

---

## After all tags are added

1. GTM top-right: **Submit**
2. Version name: *"Hawk Academy event tags added"*
3. Description: brief note of what was added
4. **Publish**

Tags are live. Proceed to Stage 4 (Looker Studio) then Stage 5 (verify).

---

## Common gotchas

| Symptom | Fix |
|---|---|
| Imported container says "0 tags imported" | The starter JSON file is malformed OR has wrong account/container IDs. Re-run `customise_gtm.py`, check Measurement ID format. |
| Realtime in GA4 still empty after Publish | GTM container not actually live on the site — use Tag Assistant Chrome extension to verify on the live URL. Common cause: WordPress caching plugin needs clear. |
| "Some forms" trigger fires too often | Trigger conditions need narrowing. Filter by Form ID or Form URL. |
| Ecommerce events don't fire | dataLayer isn't populated by their ecom platform. Need helper plugin (GTM4WP for WooCommerce, Google & YouTube channel for Shopify). |
| Tag Assistant says "No requests sent" | GTM container ID wrong on the site OR adblocker active. Try Incognito + check container ID. |
