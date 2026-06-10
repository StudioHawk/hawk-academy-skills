---
name: ga4-gtm-setup
description: >
  Workshop analytics-foundation skill — verifies the attendee's GA4 property,
  installs a Google Tag Manager container tailored to their business type
  (service or ecom), and clones a Looker Studio dashboard template so they
  can see their SEO numbers from Day 1. Reads ./business-context.md for the
  business type. No API keys or OAuth needed — runs through the standard
  GA4 + GTM web admin UIs. Use when attendee says "set up GA4", "GA4 GTM
  setup", "tracking setup", or any other workshop skill discovers GA4
  isn't configured yet.
---

# GA4 + GTM Setup (Hawk Academy Day 1 Module 5)

50-minute hands-on module. By end of it, every attendee has:

1. **GA4 verified** working on their site (or a fresh property created)
2. **GTM container imported** with tags tailored to their business type (service or ecom)
3. **Looker Studio dashboard** cloned + bookmarked
4. **Verification passed** — real-time report shows them as an active user

## When to use this skill

Trigger when the attendee says:
- *"Set up my GA4"*, *"GA4 GTM setup"*, *"tracking setup"*, *"install analytics"*
- *"How do I measure if SEO is working?"*
- Auto-route from Day 1 Module 5 in the workshop schedule
- Auto-route from any other skill that detects GA4 isn't configured (e.g. `keyword-research` could nudge during Skool follow-up)

## Module structure (50 min)

The skill drives this end-to-end. Coach narrates + floats; skill does the workflow.

| Stage | Time | What happens |
|---|---|---|
| 1. Discovery | 5 min | Skill asks 3 questions: existing GA4? existing GTM? website URL (or pulls from business-context) |
| 2. GA4 setup | 10-15 min | Verify existing property OR walk attendee through creating one at analytics.google.com |
| 3. GTM container | 15-20 min | Walk attendee through GTM container creation, hand them a tailored JSON to import |
| 4. Looker Studio | 5-10 min | Provide template URL, attendee clones, bookmarks |
| 5. Verify | 5 min | Attendee visits their site in another tab, GA4 Real-time shows them active |

---

## Stage 1 — Discovery (5 min)

Read `./business-context.md` if it exists. Pull:
- Website URL (from `## The basics`)
- Business type — classify as **service** or **ecom** based on `## Services / products` (if descriptions include "products" / "shop" / "category" / "shipping" / typical ecom verbs → ecom; otherwise service)

Then ask the attendee these 3 questions, one at a time:

### Q1. Do you have GA4 set up already?

Options:
- **Yes, fully working** → ask for Measurement ID (looks like `G-XXXXXXXXXX`)
- **Yes, but I don't think it's tracking properly** → ask for Measurement ID, plan to verify in Stage 5
- **No / Don't know** → go to GA4 creation walkthrough in Stage 2

### Q2. Do you have Google Tag Manager on your site?

Options:
- **Yes** → ask for Container ID (looks like `GTM-XXXXXXX`). Will guide them to import a workspace into their existing container.
- **No / Don't know** → walk them through creating a new GTM container in Stage 3

### Q3. Confirm business type from business-context

Read the `## Services / products` section. Show what you classified them as:

> Based on your business context, you're a **service / ecom** business. Is that right? *(yes / no / hybrid)*

If hybrid: ask which mode to bias toward. Default to ecom (more complex tracking, easier to remove than add). Note in the GTM container that some tags are "service mode only" or "ecom mode only" so attendee can disable later.

---

## Stage 2 — GA4 setup (10-15 min)

If attendee answered **Yes / fully working** in Q1: skip to verification.
- Ask for Measurement ID
- Confirm it follows the `G-XXXXXXXXXX` pattern
- Note: real verification happens in Stage 5

If attendee answered **No / Don't know**: walk them through creating a property.

Reference: [`references/ga4-setup.md`](references/ga4-setup.md) — full step-by-step.

Top-level flow:
1. Open `https://analytics.google.com/` in a new tab
2. Sign in with the email they want to own the GA4 property
3. Admin (gear icon) → Create → Account (if no account) → Property
4. Enter property name, reporting time zone (Australia/Melbourne for cohort 1), currency (AUD)
5. Business details → industry category, business size
6. Business objectives → pick "Generate leads" (service) or "Drive online sales" (ecom) or both
7. Data stream → Web → enter their URL + a stream name → Create stream
8. Copy the **Measurement ID** (G-XXXXXXXXXX) — they'll need this in Stage 3

Tell them: *"Don't try to install the GA4 tracking code yet — GTM handles that for you in the next stage."*

---

## Stage 3 — GTM container setup (15-20 min)

Reference: [`references/gtm-setup.md`](references/gtm-setup.md) — full step-by-step.

### 3a. Get a GTM container

If attendee answered **Yes** to Q2: they already have a container. Ask for the GTM ID.

If **No**: walk them through creating one:
1. Open `https://tagmanager.google.com/` in a new tab
2. Sign in (same email as GA4 property owner)
3. Create Account → enter Account Name (their business name) → Country: Australia
4. Container Name: their website URL → Target platform: **Web** → Create
5. Accept Terms of Service
6. They see two snippets — these go in the `<head>` and `<body>` of their site (we install them in step 3b)

### 3b. Install GTM on their website

This is the friction point — varies by platform.

- **WordPress + Yoast / Rank Math / All-in-One SEO**: most SEO plugins have a GTM container ID field. Paste the GTM-XXXXXXX, save.
- **WordPress + GTM4WP plugin** (recommended): install GTM4WP plugin → settings → paste container ID. Best for ecom because it auto-populates the dataLayer.
- **WordPress without a helper plugin**: paste the head + body snippets into your theme's header.php / via a hook. Coach helps if attendee gets stuck.
- **Squarespace / Wix / Webflow**: each has a settings field for GTM. Walk through their specific UI.
- **Shopify** (ecom): use the official Google & YouTube channel app OR paste snippets in theme.liquid. Note: Shopify has its own quirks with GA4 ecommerce — flag that we may need extra setup in a future Skool drop.

If attendee genuinely can't install GTM during the module (no admin access, platform restrictions), park their GTM install as homework and skip to Stage 4 with a note that they'll need to come back to Stage 3 before tags start firing.

### 3c. Import the Hawk Academy starter container

Pick the right template based on Q3's business type:

- **Service mode**: `templates/gtm-container-service.json`
- **Ecom mode**: `templates/gtm-container-ecom.json`

Generate a customised version of the template with the attendee's Measurement ID:

```bash
python3 <skill-dir>/scripts/customise_gtm.py \
  --template <skill-dir>/templates/gtm-container-<service|ecom>.json \
  --measurement-id <G-XXXXXXXXXX> \
  --out ~/Downloads/hawk-academy-gtm-container.json
```

This swaps `{{GA4_MEASUREMENT_ID}}` placeholders in the template for the attendee's actual Measurement ID and saves a ready-to-import JSON.

Then walk attendee through importing into GTM:
1. In GTM: Admin → Import Container
2. Choose Container File → select `~/Downloads/hawk-academy-gtm-container.json`
3. Workspace → New (call it "Hawk Academy Setup")
4. Import option: **Merge** (preserves any existing tags they have)
5. Click Confirm
6. Review the imported tags + triggers + variables — show them what each does
7. Click **Submit** in top-right → Container Version Name "Hawk Academy initial setup" → Publish

### 3d. What's in each container

**Service container** (`gtm-container-service.json`):
- GA4 Configuration tag (with measurement ID)
- Phone click tracking (auto-fires on tel: links)
- Email click tracking (auto-fires on mailto: links)
- Outbound link click tracking
- Form submission tracking (generic — fires on any form)
- File download tracking (PDF, DOC, ZIP)
- Scroll depth (50%, 75%, 90%)

**Ecom container** (`gtm-container-ecom.json`):
- Everything in service container, plus:
- GA4 Ecommerce events: `view_item`, `add_to_cart`, `begin_checkout`, `purchase`, `view_item_list`, `select_item`
- DataLayer variables to pull ecommerce data
- **Requires:** a plugin on the attendee's site that populates the dataLayer (GTM4WP + WooCommerce, Google & YouTube channel for Shopify, etc.) — note this clearly to the attendee

---

## Stage 4 — Looker Studio dashboard (5-10 min)

Reference: [`references/looker-studio.md`](references/looker-studio.md) — full step-by-step.

1. Open the Hawk Academy Looker Studio template URL: https://datastudio.google.com/reporting/83f2f965-9d54-4480-b770-1de0a1baea95
2. Click **Use template**
3. In the data source mapping: select **GA4** → pick their property (the one they verified/created in Stage 2)
4. Click **Copy report**
5. Rename: "[Business name] — Hawk Academy SEO Dashboard"
6. Bookmark the URL — they'll come back to it weekly

The template shows:
- Total organic sessions (last 30 days) + WoW comparison
- Top 10 organic landing pages
- Top 10 organic search queries (pulled from GSC connection — set up later if not yet linked)
- Goal completions / ecommerce revenue (service vs ecom — different scorecards)
- Mobile vs desktop split
- New vs returning user split

---

## Stage 5 — Verify (5 min)

1. Attendee opens their website in a **new tab** (not where they're configuring GTM)
2. Browses 2-3 pages on their own site
3. Goes back to GA4 → Reports → Realtime
4. They should see **1 active user** (themselves), 2-3 page views

If they DO see themselves in Realtime: ✅ working. Module complete.

If they DON'T:
- Common cause: GTM not actually installed on the live site (preview/staging only) → check the `Google Tag Assistant` Chrome extension on their live site
- GTM workspace not published → go back to GTM, click Submit + Publish
- Adblocker on attendee's browser → try Incognito + disable extensions
- WordPress caching → clear cache

Coaches float to help with the Realtime debug.

---

## Hard rules

1. **Don't ask attendees for their Google password.** Everything happens in their browser, in their account. The skill is read-only / guidance.
2. **Don't promise specific conversion tracking will work** until attendee verifies in Realtime — too many edge cases per platform.
3. **Don't store the attendee's Measurement ID anywhere sensitive.** It's not strictly secret but treat as PII. The customised GTM JSON goes to `~/Downloads/` and the attendee deletes it after import if they want.
4. **If attendee can't install GTM on Day 1** (platform restriction, no admin), park it — skip to Stage 4 with a note. Better to leave with a Looker Studio template + a homework note than blow the module.

---

## Output

After this module the attendee has on their machine:
- `~/Downloads/hawk-academy-gtm-container.json` — customised GTM container (can delete after import)
- A bookmark to their Looker Studio dashboard
- An entry in their browser history confirming GA4 Realtime saw them as an active user

We don't write anything to the project folder — this is all in their Google accounts + browser.

Optionally: save `./ga4-setup/<domain>-<date>.md` with:
- Their Measurement ID
- Their GTM Container ID
- Their Looker Studio dashboard URL
- Notes from any stage that needed a workaround

So future skills (like Skool Month 2's `gsc-audit-7`) can read it for context.

---

## Files in this skill

```
ga4-gtm-setup/
├── SKILL.md                          this file
├── references/
│   ├── ga4-setup.md                  GA4 property creation walkthrough
│   ├── gtm-setup.md                  GTM container creation + install + import
│   └── looker-studio.md              Looker Studio clone walkthrough
├── templates/
│   ├── gtm-container-service.json    starter container for service businesses
│   └── gtm-container-ecom.json       starter container for ecom businesses
└── scripts/
    └── customise_gtm.py              swaps {{GA4_MEASUREMENT_ID}} in template, outputs ready-to-import JSON
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Attendee has no Google account | They need one before this module. Have them set up one on the spot (5 min) — Gmail account is fastest. |
| GA4 property creation rejected by Google | Usually a 2FA / verification step on their Google account. Have them check email/phone for verification prompts. |
| GTM "Import Container" fails | Container JSON format error — re-run `customise_gtm.py`. If still fails, check the Measurement ID format (must be `G-XXXXXXXXXX`, all caps after G-). |
| Tags imported but not firing | GTM workspace needs to be Submitted + Published. Common miss. |
| Realtime report empty | See Stage 5 troubleshooting list — usually adblock or GTM not installed live. |
| Looker Studio template asks for data source | Pick the GA4 property they just created. If it's not showing up, refresh — sometimes takes a minute to propagate. |
| Ecom mode but no dataLayer | Their ecom platform doesn't auto-populate. Service mode tags will work; ecom events won't fire until they install a helper plugin. Note as homework. |

---

## What's next (after this module)

Attendee proceeds to **Module 6 — Keyword Research.** Their analytics is now measuring; the research they're about to do has somewhere to be tracked.

In the 6-month Skool window, related drops:
- **Month 2 — `gsc-audit-7`**: pull Google Search Console data, surface quick wins (requires linking GSC to GA4 — covered in that drop's setup tutorial).
- **Month 3 — `gbp-post-scheduling`**: pairs with the GBP audit (Day 2 Module 13) and tracks GBP-driven traffic in GA4.

---

## Hawk Academy positioning

Frame this module as: *"You captured WHO you are in Module 4. Now we set up the dashboards so you can measure if the next 6 months of work is paying off. You can't manage what you can't measure — and you're about to start managing your SEO."*

This is the "infrastructure" module — no immediate visible win, but every subsequent module's results show up here.
