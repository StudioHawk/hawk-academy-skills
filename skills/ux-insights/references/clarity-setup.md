# Setup Mode — Install Microsoft Clarity (and connect other tools)

Microsoft Clarity is a free, unlimited behavioural-analytics tool: heatmaps, session recordings,
and friction signals (rage clicks, dead clicks, quick-backs, JS errors). Goal of this mode: get the
attendee's tracking code live and verified, then point them at the right dashboards.

## Step 1 — Create the project
1. Go to **https://clarity.microsoft.com** and sign in (Microsoft, Google, Facebook or email).
2. **Create new project** → enter the website **name** and **URL**, pick the **site category**.
3. Open **Settings → Overview / Setup** to find the **tracking code** (a short JS snippet with a unique Project ID).

## Step 2 — Install the tracking code (pick the attendee's platform)
Always confirm which CMS/stack they use, then give the matching path:

- **Google Tag Manager (recommended, works anywhere):** GTM → New Tag → **Microsoft Clarity** template (or Custom HTML) → paste the snippet/Project ID → Trigger: **All Pages** → Submit & Publish.
- **WordPress:** install the **Microsoft Clarity** plugin → paste the Project ID; or paste the snippet into the `<head>` via the theme/header plugin.
- **Shopify:** Clarity has a built-in Shopify integration (Settings → Setup → Shopify), or paste the snippet into `theme.liquid` just before `</head>`.
- **Squarespace:** Settings → **Advanced → Code Injection → Header** → paste the snippet. (This is how fitforlifefitness.com.au, a Squarespace site, would do it.)
- **Wix:** Settings → **Custom Code** → add to **Head**, **All pages**, load once.
- **Webflow:** Project Settings → **Custom Code → Head Code** → paste → Publish.
- **Manual / custom site:** paste the snippet into the `<head>` of every page (or the shared layout/template).

## Step 3 — Verify it's working
- In Clarity, the project status flips to **"Tracking"** once it receives data (can take a few minutes to ~2 hours).
- Visit the live site yourself, click around, then check **Recordings** for your session.
- Confirm the snippet fires with the browser dev-tools Network tab (look for `clarity.ms`) or the Tag Assistant if using GTM.

## Step 4 — First-run configuration
- **Masking / privacy:** set content masking to **Balanced** (default) or **Strict** if the site shows sensitive data. Clarity is GDPR/CCPA-friendly but the attendee should still mention it in their privacy policy and respect their cookie-consent tool.
- **GA4 integration (optional, recommended):** Clarity → Settings → **Google Analytics** → connect, so you can jump from a GA4 segment straight into the matching Clarity recordings.
- **Set up a Funnel** for the key conversion path (e.g. Home → Service page → Contact/Booking) so drop-off is measurable.

## Step 5 — What to watch (point them here before they leave)
- **Dashboard:** dead clicks, rage clicks, excessive scrolling, quick-backs, JS errors, scroll depth.
- **Heatmaps:** click + scroll maps on the top pages.
- **Recordings:** filter by rage clicks / quick-backs / specific pages to watch real friction.
Give it a few days to gather data before diagnosing.

## Connecting other tools (so Diagnose mode can use them)
The attendee may also run **Hotjar** (heatmaps + recordings + surveys), **GA4** (funnels, exit pages,
engagement), **PostHog**, **FullStory**, or **Mouseflow**. They don't need all of them — Clarity alone is
plenty. Note what they have; Diagnose mode is tool-agnostic and reads exports/pastes from any of them.
