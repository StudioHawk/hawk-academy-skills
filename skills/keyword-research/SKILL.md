---
name: keyword-research
description: >
  Workshop keyword research skill — backed by the SE Ranking Data API.
  Every query loads attendee business context, calls the right endpoint,
  translates SEO jargon to plain English, and saves both a markdown summary
  and a spreadsheet to ./keyword-research/. Use this for ANY keyword,
  competitor, or domain research task — including phrases like "find me
  keywords", "what does competitor.com rank for", "give me blog ideas
  around X", "what am I missing vs competitors", "how is my site doing
  on Google", "map keywords to my pages". Defaults to AU source DB
  (Melbourne-based workshop), limit=25, sort by on-topic relevance.
---

# Keyword Research (SE Ranking Data API)

You have full access to the SE Ranking Data API. **Pick the endpoint yourself**
from the decision table — don't ask the attendee which tool to use. After
every API call, run the formatter script so the attendee gets a readable
markdown table + a spreadsheet they can open in Excel/Numbers/Sheets.

---

## Workshop standard workflow (every query follows this)

Every keyword research query in the workshop must do these 8 steps in order:

1. **Load attendee business context.** Read `./business-context.md`. If it doesn't exist, run the **First-run setup** below before doing anything else.
2. **Pick the endpoint** from the decision table.
3. **Pick the seed — and narrate it.** When the attendee says something vague like *"find me keywords for my emergency plumbing work"*, look at their business context and build a specific seed by combining their top service with their priority suburb/region. Then **announce the choice before running** so the attendee knows what you picked and can redirect.

   Example: an attendee whose context lists "Emergency plumbing 24/7" as service #1 and Brighton as the top-priority suburb in their SEO goal would get:

   > I'm using **`emergency plumber brighton`** as the seed — pairs your top service with your top-priority suburb. Want me to also run other suburbs (Hampton, Sandringham, Elwood) or other services (hot water systems, blocked drains) after this one? Or different seed entirely?

   Wait for confirmation OR proceed if the attendee said "just go". Never silently substitute a seed without telling them.
4. **Apply workshop defaults:**
   - `source=au` (Melbourne-based primarily — override only if attendee explicitly says US/UK/etc.)
   - `limit=25` for `/keywords/related`, `/similar`, `/questions`
   - `limit=50` for `/keywords/longtail` (cheap at 1 cr/row)
   - `sort=-volume` on the API request, then re-sorted by relevance × volume in the formatter
5. **Save the raw JSON** to `/tmp/kw-<slug>.json`.
6. **Run the formatter:**
   ```bash
   python3 <skill-dir>/scripts/format_results.py \
     --json /tmp/kw-<slug>.json \
     --mode <keywords|longtail|domain-keywords|domain-overview|gap> \
     --seed "<seed-or-domain>" \
     --out-dir ./keyword-research
   ```
7. **Present the markdown summary** (the Top picks + table) inline to the attendee. **Mention the spreadsheet path** explicitly so they know they can open it.
8. **If the formatter reports fewer than 3 strong picks**, suggest 3 specific follow-up queries built from the business context (see "Handling sparse results" below). Don't leave the attendee with a vague "try a different seed."

The formatter handles: translating intent codes (L→Local, C→Commercial, T→Transactional, I→Informational, N→Navigational), translating SERP feature codes (gmb→Google Business Profile, sge→Google AI Overview, local_pack→Local Pack (map), etc.), sorting by on-topic relevance squared × volume, surfacing top picks that meet on-topic ≥30% + difficulty ≤60, calling out high-CPC keywords ($10+) as commercial-value plays, and ending with "What to do next" guidance.

---

## Handling sparse results

When the formatter says **"Only N strong picks in this batch"** (N < 3), don't leave the attendee hanging. Use their business context to propose 3 concrete next queries. Use this template:

> Only N strong picks here. Want me to also try:
> - **`[seed variant — next un-tried suburb]`** ([reason from their SEO goal or services list])
> - **`[seed variant — next un-tried service]`** ([reason from their services list])
> - **Long-tail phrases for `[broader version of seed]`** (50 cheap variations, then we pull metrics on the ones you pick)

Concrete example, OB Plumbing got 2 picks for `emergency plumber brighton`:

> Only 2 strong picks here. Want me to also try:
> - **`emergency plumber hampton`** (next priority suburb from your SEO goal — Brighton, Hampton, Sandringham, Elwood, Caulfield)
> - **`hot water systems melbourne`** (next service from your list — gives us a second service-page candidate)
> - **Long-tail phrases for `emergency plumber`** (50 cheap variations, then we pull metrics on the ones you pick)

**Wait for the attendee to choose.** Don't run all three automatically — each is 250 credits, and they should drive direction.

---

## Business context dependency

This skill **reads** `./business-context.md` at the project root — it does not capture it. Context capture is handled by the separate **`business-context`** skill (10 questions, run once per project at the start of Day 1).

**If `./business-context.md` doesn't exist when this skill activates:**

1. Stop. Don't run any queries yet.
2. Tell the attendee:
   > Before we do keyword research, we need to capture your business context. It takes 5 minutes and feeds every workshop skill.
3. Hand off to the `business-context` skill (the user can re-trigger by saying *"set up my business"* or any other trigger phrase listed in that skill).
4. Once `./business-context.md` exists, return to the original keyword research request — read the file, use the relevant sections.

**Sections this skill cares about** (grep these from `./business-context.md`):

- `## The basics` → website URL for domain queries, business name for context
- `## Geographic scope` → comma-separated locations for `filter[multi_keyword_included]=` and seed-building
- `## Services / products` → seeds for keyword/longtail/questions queries
- `## Ideal customer` → intent filter hints (e.g., commercial vs informational)
- `## Top 10 customer questions` → direct input for `/keywords/export` to get metrics on real customer phrasing
- `## Competitors` → domains for `/domain/keywords` and `/domain/competitors` queries
- `## SEO goal` → frames the "what to do next" recommendations

---

## Step 0 — Verify the API key

```bash
[ -z "$SE_RANKING_API_KEY" ] && echo "MISSING_KEY" || echo "ok"
```

If `MISSING_KEY`:

> The shared workshop SE Ranking key isn't in your shell. Add it once:
> ```
> echo 'export SE_RANKING_API_KEY=<key>' >> ~/.zshrc && source ~/.zshrc
> ```
> Workshop attendees: copy the shared key from the workshop hub (hawkos-lite.pages.dev, under SE Ranking Key) — set it once with:
> `echo 'export SE_RANKING_API_KEY=<key-from-the-hub>' >> ~/.zshrc && source ~/.zshrc`
> (Or just ask Claude: "set up my SE Ranking key" and paste it — Claude will do it for you.)

**Free smoke test (0 credits):**

```bash
curl -sS "https://api.seranking.com/v1/account/subscription" \
  -H "Authorization: Token $SE_RANKING_API_KEY"
```

Expected: JSON with subscription details. HTTP 401/403 means the key is invalid. Use this anytime you want to confirm without burning credits.

---

## API basics

- **Base URL:** `https://api.seranking.com/v1/`
- **Auth:** `Authorization: Token YOUR_API_KEY` header
- **Output:** JSON exclusively
- **Rate limit:** 10 RPS rolling window. 429 → back off with jitter
- **Source DB codes:** `au` (workshop default), `us`, `uk`, `ca`, `nz`, `sg`, `de`, `fr`, `es`, `it`, `br`, `in`, `jp`
- **Response fields seen in workshop queries:**
  - `keyword`, `volume`, `cpc`, `difficulty` (KD 0–100), `competition` (0.0–1.0), `relevance` (0–100, how on-topic to the seed)
  - `intents` — array: `I`/`C`/`T`/`L`/`N` (formatter translates these)
  - `serp_features` — array of feature codes (formatter translates these)
  - `history_trend` — `YYYY-MM-DD: volume` time series (often null)

---

## Decision table

| Attendee says… | Endpoint | Mode arg for formatter |
|---|---|---|
| "find me keywords for my business" / "give me keyword ideas" | `/v1/keywords/related` | `keywords` |
| "long-tail variations" / "give me lots of phrases cheaply" | `/v1/keywords/longtail` | `longtail` |
| "similar / semantic keywords" | `/v1/keywords/similar` | `keywords` |
| "blog ideas" / "what questions do people ask about X" | `/v1/keywords/questions` | `keywords` |
| "metrics for these specific keywords I already have" | `POST /v1/keywords/export` | `keywords` |
| "what does [competitor.com] rank for" / "show me their keywords" | `/v1/domain/keywords` | `domain-keywords` |
| "how is my site doing" / "domain overview" | `/v1/domain/overview/db` | `domain-overview` |
| "what am I missing vs my competitors" / "who are my competitors" / "keyword gap" | `/v1/domain/competitors` | `gap` |
| "top pages on my site" / "top pages on competitor.com" | `/v1/domain/pages` | (no formatter mode yet — present inline) |
| "map keywords to these URLs" | Batch script — see section below | (script writes its own CSV) |

---

## Operation recipes

Every recipe below assumes:
- Business context is loaded (read `./business-context.md` first)
- Workshop defaults applied (`source=au`, sensible limits)
- After the curl, **save to JSON file then run formatter** (step 5 of the standard workflow)

### 1. Keyword research — `/v1/keywords/related`

Cost: ~10 credits per keyword returned.

```bash
# Save raw JSON to temp file
curl -sSG "https://api.seranking.com/v1/keywords/related" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "source=au" \
  --data-urlencode "keyword=SEED" \
  --data-urlencode "limit=25" \
  --data-urlencode "sort=-volume" \
  -o /tmp/kw-SLUG.json

# Format → ./keyword-research/SLUG-YYYY-MM-DD.{md,csv}
python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG.json \
  --mode keywords \
  --seed "SEED" \
  --out-dir ./keyword-research
```

Server-side filters (free — apply before paying for rows you'd discard):
- `filter[volume][from]=500` — only return ≥500 volume
- `filter[difficulty][to]=40` — only return KD ≤ 40
- `filter[intents][]=C&filter[intents][]=T` — only commercial/transactional
- `filter[multi_keyword_included]=melbourne` — must contain word

Variants (same `--mode keywords` for the formatter):
- **`/v1/keywords/similar`** — semantic similar, 10 cr/row
- **`/v1/keywords/questions`** — question-form only, 10 cr/row, great for blog topics

### 2. Longtail — `/v1/keywords/longtail` (cheap discovery)

Cost: **1 credit per row**. Returns phrases only, no metrics.

```bash
curl -sSG "https://api.seranking.com/v1/keywords/longtail" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "source=au" \
  --data-urlencode "keyword=SEED" \
  --data-urlencode "limit=50" \
  -o /tmp/kw-SLUG-longtail.json

python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG-longtail.json \
  --mode longtail \
  --seed "SEED" \
  --out-dir ./keyword-research
```

The formatter writes a markdown phrase list + CSV with a "what to do next" pointing the attendee to the keywords/export flow for getting metrics on the phrases they pick.

### 3. Metrics for a known keyword list — `POST /v1/keywords/export`

Cost: **100 credits flat per batch** (up to ~1000 keywords per call).

```bash
curl -sS -X POST "https://api.seranking.com/v1/keywords/export" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "au",
    "keywords": ["melbourne plumber", "emergency plumber geelong", "hot water service melbourne"]
  }' \
  -o /tmp/kw-SLUG-export.json

python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG-export.json \
  --mode keywords \
  --seed "SEED-or-batch-name" \
  --out-dir ./keyword-research
```

Use this after `/longtail` (cheap discovery → pick phrases → batch metrics).

### 4. Domain overview — `/v1/domain/overview/db`

Cost: **100 credits flat per request**.

```bash
curl -sSG "https://api.seranking.com/v1/domain/overview/db" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "source=au" \
  --data-urlencode "domain=DOMAIN" \
  --data-urlencode "with_subdomains=true" \
  -o /tmp/kw-SLUG-overview.json

python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG-overview.json \
  --mode domain-overview \
  --seed "DOMAIN" \
  --out-dir ./keyword-research
```

Returns: keyword count, traffic estimate, traffic value (Google Ads equivalent), top-3 / top-10 / pos-11-20 counts.

### 5. Organic rankings — `/v1/domain/keywords`

Cost: **100 credits flat per request** (regardless of limit). Always pull `limit=1000` (max) — you pay the same.

```bash
curl -sSG "https://api.seranking.com/v1/domain/keywords" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "source=au" \
  --data-urlencode "domain=DOMAIN" \
  --data-urlencode "type=organic" \
  --data-urlencode "limit=1000" \
  --data-urlencode "order_field=traffic" \
  --data-urlencode "order_direction=desc" \
  -o /tmp/kw-SLUG-rankings.json

python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG-rankings.json \
  --mode domain-keywords \
  --seed "DOMAIN" \
  --out-dir ./keyword-research
```

The formatter surfaces **Quick wins** — keywords currently ranking positions 4–15 (the page-1 frontier).

### 6. Competitor gap — `/v1/domain/competitors`

Cost: **100 credits flat**. Returns SE Ranking's detected competitors for the attendee's domain plus, for each, the count of `missing_keywords` (keywords the competitor ranks for that the attendee doesn't).

```bash
curl -sSG "https://api.seranking.com/v1/domain/competitors" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "source=au" \
  --data-urlencode "domain=ATTENDEE-DOMAIN" \
  --data-urlencode "limit=20" \
  -o /tmp/kw-SLUG-competitors.json

python3 <skill-dir>/scripts/format_results.py \
  --json /tmp/kw-SLUG-competitors.json \
  --mode gap \
  --seed "ATTENDEE-DOMAIN" \
  --out-dir ./keyword-research
```

The formatter sorts by `missing_keywords` desc — biggest opportunity first — and surfaces the top 5 competitors to study. Attendees use this to discover **who they're actually competing with in search** (often surprising — it's not their named competitors, it's whoever's ranking for their keywords).

**Note on `/v1/domain/keywords/comparison`:** the official "keyword gap" endpoint exists but its param shape is currently unclear (returns "Bad request" for the documented forms — `compare=`, `domain[]=`, `domains=` all rejected). `/domain/competitors` gives workshop-friendly data in a single 100-cr call, so that's what the skill uses for "what am I missing vs competitors". If you nail down `/comparison`'s actual params, swap it in for keyword-level detail.

---

## Batch keyword mapping (1–1000 URLs)

For mapping keywords to a URL list (e.g., the attendee's full sitemap), write the embedded Python script below to `/tmp/keyword_mapper.py` and run it. The script is self-contained — stdlib only, no pip install.

**Setup once per session:**

```bash
cat > /tmp/keyword_mapper.py <<'PYEOF'
#!/usr/bin/env python3
"""Batch keyword mapper — SE Ranking Data API.

Usage:
    python3 /tmp/keyword_mapper.py <urls_file> [source_db] [--resume <existing_csv>]

Auto-detects source DB from TLD if [source_db] omitted (au/uk/nz/ca/sg/us).
Output: ~/Desktop/keyword_mapping_<timestamp>.csv
"""
import csv, json, os, random, re, sys, time, urllib.parse, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

API_KEY = os.environ.get("SE_RANKING_API_KEY", "").strip()
if not API_KEY:
    print("ERROR: SE_RANKING_API_KEY not set. Run: export SE_RANKING_API_KEY=your-key", file=sys.stderr)
    sys.exit(1)

BASE = "https://api.seranking.com/v1"
MIN_SPACING = 0.12  # 10 RPS cap
_last_call = 0.0
_total_credits = 0

GENERIC = {
    "services","service","about","aboutus","about us","contact","contactus","contact us",
    "blog","news","home","page","pages","index","index.html","index.php",
    "category","categories","tag","tags","author","archive","archives",
    "au","en","us","uk","ca","nz","sg",
    "thankyou","thank you","thanks","privacy","privacypolicy","privacy policy",
    "terms","termsofservice","terms of service","termsandconditions","terms and conditions",
    "faq","faqs","help","support","sitemap","404","search","results",
    "login","logout","signup","register","cart","checkout","account","dashboard",
    "get","getstarted","get started","start","free","freetrial","free trial",
    "demo","book","booking","quote","getaquote","get a quote","enquiry","enquire",
    "resources","resource","downloads","download","portfolio","work","projects","project",
    "team","staff","people","careers","jobs","join","culture","gallery","photos",
    "videos","media","press","partners","partner","clients","client",
    "case studies","case study","testimonials","reviews","legal","disclaimer",
    "cookie","cookies","landing","lp","sp","offer","promo","promotion","special",
    "collections","collection","products","product","shop","store","all",
    "all-products","all-collections","featured","new","sale","bestsellers",
}


class APIError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(f"HTTP {status}: {message}")


def normalise(s):
    s = re.sub(r"[-_]+", " ", s).lower().strip()
    return re.sub(r"[^\w\s]", "", s).strip()


def tld_to_db(url):
    host = urlparse(url).netloc.lower()
    if re.search(r"\.(com\.au|net\.au|org\.au|edu\.au)$", host): return "au"
    if re.search(r"\.(co\.uk|org\.uk|me\.uk)$", host): return "uk"
    if re.search(r"\.(co\.nz|net\.nz|org\.nz)$", host): return "nz"
    if host.endswith(".ca"): return "ca"
    if re.search(r"\.(sg|com\.sg)$", host): return "sg"
    return "us"


def derive_seed(url):
    parsed = urlparse(url)
    raw = [s for s in parsed.path.strip("/").split("/") if s]
    norm = [(s, normalise(s)) for s in raw]
    meaningful = [(r, n) for r, n in norm if n not in GENERIC and len(n) > 2]
    if meaningful:
        slug = meaningful[-2][0] + " " + meaningful[-1][0] if len(meaningful) >= 2 else meaningful[-1][0]
    else:
        domain = re.sub(r"^www\.", "", parsed.netloc.lower())
        domain = re.sub(
            r"\.(com\.au|co\.uk|co\.nz|com\.sg|net\.au|org\.au|edu\.au"
            r"|com|net|org|au|uk|nz|ca|sg|io|co|me|app|ai)$", "", domain)
        slug = domain
    seed = re.sub(r"[-_]+", " ", slug).strip()
    seed = re.sub(r"[^\w\s]", "", seed).lower().strip()
    seed = " ".join(seed.split()[:5])
    return seed if seed and len(seed) > 2 else "digital marketing"


def call_api(path, params, max_retries=4):
    """GET request with rate limiting and 429 backoff."""
    global _last_call, _total_credits
    url = BASE + path + "?" + urllib.parse.urlencode(params, doseq=True)
    headers = {"Authorization": f"Token {API_KEY}", "Accept": "application/json"}

    for attempt in range(max_retries):
        now = time.monotonic()
        elapsed = now - _last_call
        if elapsed < MIN_SPACING: time.sleep(MIN_SPACING - elapsed)
        _last_call = time.monotonic()

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
            if e.code == 429 and attempt < max_retries - 1:
                wait = (2 ** attempt) + random.random()
                time.sleep(wait)
                continue
            raise APIError(e.code, body[:300])
        except urllib.error.URLError as e:
            raise APIError(0, f"Network error: {e.reason}")


def lookup(seed, source):
    attempt = seed
    for _ in range(3):
        try:
            data = call_api("/keywords/related", {
                "source": source, "keyword": attempt, "limit": 20, "sort": "-volume",
            })
        except APIError as e:
            if e.status in (404, 422): data = {"keywords": []}
            else: raise
        rows = data.get("keywords", [])
        _total_credits += max(len(rows), 1) * 10
        if rows: return rows, attempt
        words = attempt.split()
        if len(words) <= 1: break
        attempt = " ".join(words[:-1])
    return [], attempt


def score(kw):
    vol = int(kw.get("volume") or 0)
    kd = float(kw.get("difficulty") or 50)
    intents = [i.upper() for i in (kw.get("intents") or [])]
    if "C" in intents or "T" in intents: bonus = 1.3
    elif "I" in intents: bonus = 1.1
    else: bonus = 1.0
    penalty = max(0.0, (kd - 60) * 0.5) if kd > 60 else 0.0
    return (vol * bonus) - penalty


def pick(rows):
    if not rows: return None
    ranked = sorted(rows, key=score, reverse=True)
    p = ranked[0]
    sup = [s.get("keyword", "") for s in ranked[1:5]]
    while len(sup) < 4: sup.append("")
    primary_intent = ",".join(p.get("intents") or [])
    return {"kw": p.get("keyword",""), "vol": p.get("volume",""), "kd": p.get("difficulty",""),
            "intent": primary_intent, "cpc": p.get("cpc",""), "sup": sup}


def main(argv):
    urls_file = db_arg = resume = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--resume":
            if i + 1 >= len(argv): print("ERROR: --resume requires a path"); sys.exit(1)
            resume = argv[i+1]; i += 2; continue
        if a.startswith("-"): print(f"unknown flag: {a}"); sys.exit(1)
        if not urls_file: urls_file = a
        elif not db_arg: db_arg = a
        i += 1
    if not urls_file:
        print(__doc__); sys.exit(1)

    urls = [ln.strip() for ln in Path(urls_file).expanduser().read_text().splitlines()
            if ln.strip() and not ln.strip().startswith("#")]
    total = len(urls)

    already = set()
    if resume and Path(resume).expanduser().exists():
        with Path(resume).expanduser().open(newline="") as fh:
            for i, row in enumerate(csv.reader(fh)):
                if i == 0 or not row: continue
                already.add(row[0])
        out_path = Path(resume).expanduser()
        write_header = False
        print(f"Resuming: {len(already)} URLs already mapped")
    else:
        out_path = Path.home() / "Desktop" / f"keyword_mapping_{datetime.now():%Y%m%d_%H%M%S}.csv"
        write_header = True

    header = ["URL","Primary Keyword","Primary Volume","Primary KD%","Primary Intent","Primary CPC",
              "Supporting KW 1","Supporting KW 2","Supporting KW 3","Supporting KW 4","Status"]
    if write_header:
        with out_path.open("w", newline="") as fh: csv.writer(fh).writerow(header)

    print(f"Mapping {total} URLs → {out_path}")
    print(f"Budget estimate: up to ~{total*3*20*10:,} credits (worst case)")
    print("─" * 60)

    mapped = failed = 0
    started = time.monotonic()
    with out_path.open("a", newline="") as fh:
        w = csv.writer(fh)
        for idx, url in enumerate(urls, 1):
            if url in already:
                print(f"[{idx}/{total}] {url} ... SKIPPED (already mapped)"); continue
            db = db_arg or tld_to_db(url)
            seed = derive_seed(url)
            try:
                rows, final_seed = lookup(seed, db)
            except APIError as e:
                if e.status in (402, 403):
                    print(f"[{idx}/{total}] FATAL: {e}")
                    w.writerow([url] + [""]*9 + [f"error - {e.message}"])
                    print("Credits exhausted or key disabled. Tell your workshop coach.")
                    break
                print(f"[{idx}/{total}] {url} ... ERROR: {e}")
                w.writerow([url] + [""]*9 + [f"error - HTTP {e.status}"]); failed += 1; continue
            picked = pick(rows)
            if not picked:
                print(f"[{idx}/{total}] {url} ... SKIPPED (no keywords) [db={db}, seed={seed}]")
                w.writerow([url] + [""]*9 + ["skipped - no keywords found"]); failed += 1; continue
            w.writerow([url, picked["kw"], picked["vol"], picked["kd"], picked["intent"], picked["cpc"],
                        *picked["sup"], "ok"])
            fh.flush()
            mapped += 1
            print(f"[{idx}/{total}] {url} ... OK [db={db}, seed={final_seed}]")

    print("─" * 60)
    print(f"Done. Mapped {mapped}/{total}, skipped {failed}, ~{_total_credits:,} credits used in {time.monotonic()-started:.1f}s")
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main(sys.argv[1:])
PYEOF
chmod +x /tmp/keyword_mapper.py
```

**Run it:**

```bash
python3 /tmp/keyword_mapper.py /tmp/urls.txt au                            # explicit AU
python3 /tmp/keyword_mapper.py /tmp/urls.txt                                # auto-detect from TLD
python3 /tmp/keyword_mapper.py /tmp/urls.txt au --resume ~/Desktop/keyword_mapping_old.csv
```

Output: `~/Desktop/keyword_mapping_<timestamp>.csv` with 11 columns. Cost: ~10–600 credits per URL.

---

## Backlinks (occasional)

Cost: summary ~100 cr per target; refdomains 1 cr per row.

```bash
curl -sSG "https://api.seranking.com/v1/backlinks/summary" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "target=DOMAIN" \
  --data-urlencode "mode=domain" | jq '.summary[0]'

curl -sSG "https://api.seranking.com/v1/backlinks/refdomains" \
  -H "Authorization: Token $SE_RANKING_API_KEY" \
  --data-urlencode "target=DOMAIN" \
  --data-urlencode "limit=500" \
  --data-urlencode "order_by=domain_inlink_rank" | jq
```

No formatter mode for these yet — present inline if the attendee asks. If demand is high in cohort 1, add a `backlinks` mode.

---

## Translations (handled automatically by the formatter)

The formatter translates these so attendees never see raw codes. Reference for editing the script:

| Intent code | Plain English |
|---|---|
| I | Informational |
| C | Commercial |
| T | Transactional |
| L | Local |
| N | Navigational |

| SERP feature code | Plain English |
|---|---|
| local_pack | Local Pack (map) |
| gmb | Google Business Profile |
| people_also_ask | People Also Ask |
| sge / ai_overview | Google AI Overview |
| featured_snippets | Featured snippet |
| reviews | Reviews |
| video | Video carousel |
| images | Image carousel |
| related_searches | Related searches |
| tads | Ads (top) |
| bads | Ads (bottom) |

Add more in `scripts/format_results.py` (`SERP_FEATURE_NAMES` dict).

---

## Tips

- **Default source is `au`** for the workshop. Override only on explicit attendee request.
- **Sort the API request by `-volume`** then let the formatter re-sort by `relevance² × volume` to surface on-topic matches over generic head terms.
- **Server-side filters are free** — use `filter[volume][from]=500` to avoid paying for low-volume rows you'd discard anyway.
- **Domain endpoints cost 100 cr flat** regardless of limit — always pull `limit=1000`.
- **Keyword endpoints cost per-row** — start at `limit=25`, escalate only if the attendee asks for more.
- **HTTP 429** → mapper auto-backs-off; in inline curl, wait 1–2s before retrying.
- **HTTP 402/403** → credit pool empty or key revoked; tell your workshop coach.
- **HTTP 401** → key invalid; check for stray whitespace, re-paste.

---

## Workshop etiquette (shared key — 300,000 credits)

The workshop runs on a single shared SE Ranking key with a 300k annual credit pool. That's the whole pool for everyone — staff, all cohorts, all attendees.

Rough costs to keep in your head:
- `/keywords/related` at limit=25 → ~250 credits
- `/keywords/longtail` at limit=50 → 50 credits (cheap)
- `/keywords/export` (batch metrics for ≤1000 keywords) → 100 credits flat
- `/domain/keywords` at limit=1000 → 100 credits flat (best value)
- `/domain/overview/db` → 100 credits flat
- `/domain/keywords/comparison` (gap) → 100 credits flat
- Batch URL mapper → ~10–600 credits per URL

The pool isn't enforced per-attendee, so be sensible:
- Don't run `/keywords/related` at `limit=1000` (10,000 credits) unless there's a reason. `limit=25` is enough for most workshop discovery queries.
- Domain-level endpoints are cheap (100 cr flat) — use them freely.
- If `units_left` in the smoke test gets below 50k, mention it to your workshop coach before doing wide queries.
- HTTP 402 means pool is empty. Stop. Don't keep retrying.

The `units_left` field in the smoke test endpoint updates on a delay (~5-15 min), so a freshly-spent credit won't show in `units_left` immediately. Run another smoke test later to see the true balance.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `MISSING_KEY` | `export SE_RANKING_API_KEY=...` (or add to `~/.zshrc`) |
| HTTP 401 | Key invalid — re-paste, check for whitespace |
| HTTP 402 | Credit pool empty — stop, tell your workshop coach |
| HTTP 403 | Key revoked or endpoint not in plan |
| HTTP 429 | Rate limit hit — wait 2s, batch script handles automatically |
| Empty `keywords` array | Seed too narrow — try a broader phrase or `/longtail` |
| Formatter errors on weird mode | The endpoint shape didn't match the mode arg — check the decision table |
| `business-context.md` not loading | First-run setup wasn't completed — re-run it |
