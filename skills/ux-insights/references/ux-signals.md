# Diagnose Mode — UX signal dictionary & diagnosis framework

Tool-agnostic. The attendee pastes or exports data from whatever they use (Microsoft Clarity,
Hotjar, GA4, PostHog, FullStory, Mouseflow). Your job: read the signals, infer the likely UX
problem, and recommend a concrete fix — prioritised by impact × effort.

## How to run a diagnosis
1. **Confirm the goal of each page** under review (what should the user DO — book, buy, enquire, read?).
2. **Read the signals** the attendee provides (below). Map each to a likely cause.
3. **Corroborate across sources** — a Clarity rage-click cluster + a GA4 high exit rate on the same page is a strong signal; one alone is a hypothesis.
4. **Watch/ask for recordings** where the data is ambiguous — recordings turn a hypothesis into a confirmed cause.
5. **Prioritise** fixes: quick wins first (high impact, low effort), then bigger rebuilds.
6. **Be honest about confidence.** Behavioural data shows *what* happens, rarely *why* — label inferences as hypotheses and suggest how to confirm (recording, survey, A/B test).

## Signal → likely cause → fix

### Microsoft Clarity signals
| Signal | What it usually means | Typical fix |
|---|---|---|
| **Rage clicks** (rapid repeated clicks) | User expects something to be clickable/work and it isn't responding | Make the element actually clickable; fix the broken control; add affordance (cursor, hover state) |
| **Dead clicks** (click, no effect) | Non-interactive element looks clickable (image, heading, fake button) | Link it, or restyle so it doesn't look interactive |
| **Quick-backs** (enter page, leave almost immediately, return) | Page didn't match the click's promise; wrong/poor landing | Align headline + content to the link/ad; fix slow load; improve above-the-fold clarity |
| **Excessive scrolling** | Users hunting for something they can't find | Surface the key info/CTA higher; add anchors or a sticky CTA |
| **JavaScript errors** | Broken script blocking interaction (form, button, widget) | Fix the error; test the form/CTA path end-to-end |
| **Low scroll depth on a long page** | Content/CTA below the fold never seen | Move the CTA + key proof up; tighten the intro |
| **High click count on a dead area** | Misleading design / users want an action that isn't there | Add the expected action or remove the misleading cue |

### Hotjar signals
| Signal | What it usually means | Typical fix |
|---|---|---|
| **Click heatmap concentrated off-CTA** | Attention going to the wrong elements | Strengthen CTA contrast/placement; remove competing cues |
| **Scroll heatmap drops before CTA** | CTA below where most users stop | Raise the CTA; add a mid-page CTA |
| **Recordings: hesitation/form abandonment** | Confusing field, too many fields, error not shown | Reduce fields; inline validation; clearer labels/errors |
| **On-site survey/feedback themes** | Direct voice-of-customer friction | Fix the most-mentioned blocker first |
| **Rage clicks (Hotjar)** | Same as Clarity — broken/unresponsive element | Fix the control; add feedback state |

### GA4 / analytics signals
| Signal | What it usually means | Typical fix |
|---|---|---|
| **High exit rate on a step** | Drop-off point in the journey | Diagnose that page with heatmap/recording; remove the blocker |
| **Low engagement rate / short avg time** | Content mismatch or weak relevance | Align content to intent; stronger hook above the fold |
| **Funnel drop between steps** | Friction or missing reassurance at that step | Add trust/clarity at the drop step; reduce required actions |
| **High mobile vs desktop gap** | Mobile UX broken (tap targets, layout, speed) | Mobile-first fixes: tap size, layout, load time |
| **Slow page / poor Core Web Vitals** | Speed driving abandonment | Compress images, lazy-load, reduce scripts |

## Common UX problems & the pattern that reveals them
- **Broken/unresponsive control:** rage clicks + JS errors + form abandonment on the same page.
- **Misleading design:** dead clicks on non-links + high clicks on a static element.
- **Wrong landing / message mismatch:** quick-backs + high exit + low engagement time.
- **Buried CTA:** excessive scrolling + scroll-depth drop before the CTA + low conversion.
- **Mobile-only breakage:** desktop fine, mobile exit/quick-backs spike.

## Output format (what to hand the attendee)
A prioritised table: **Page/Area · Signal (with evidence) · Likely cause · Recommended fix · Severity · Effort · Impact**, plus a 3–5 sentence summary and a "fix these 3 first" quick-win list. Use `scripts/build_ux_report.py` to render it as a polished report. Always note which findings are confirmed vs hypotheses and how to validate the latter (recording, survey, or A/B test).
