---
name: business-context
description: >
  First-run setup for the Hawk Academy Workshop. Walks the attendee through
  10 questions about their business, then writes ./business-context.md to
  the project root. Every other workshop skill (keyword-research, site-audit,
  content-briefs, etc.) reads this file on activation so the attendee never
  re-states "I'm a plumber in Geelong" every query. Trigger when the
  attendee says "set up my business", "first time", "I'm new", "let's get
  started", "build my context", or when any other skill activates and
  ./business-context.md doesn't exist.
---

# Business Context (First-Run Setup)

The first thing every workshop attendee does. This skill walks them through
10 questions about their business, then writes the answers to
`./business-context.md` at the project root. From that point on, every other
workshop skill reads the file automatically — no more re-stating the basics.

---

## When to run this

Trigger this skill when:

- The attendee says any of: *"set up my business"*, *"first time"*, *"I'm new"*, *"let's get started"*, *"build my business context"*, *"capture my business"*
- The attendee asks for **any** workshop skill (keyword-research, site-audit, etc.) AND `./business-context.md` doesn't exist in the project root → silently route through this skill first, then return to their original request.
- The attendee says *"my business has changed"*, *"redo my context"*, *"update my business details"* — restart the flow.

---

## Before you start

1. **Check if `./business-context.md` already exists.** If it does, ask the attendee:
   > You already have a business context file. Want to (a) keep it as-is, (b) edit a specific section, or (c) start over?
   - **(a)** — tell them which file it's in, end the skill, return to whatever they were trying to do
   - **(b)** — open the file in their editor (`open ./business-context.md`) and let them edit directly. Tell them to save when done.
   - **(c)** — proceed with the 10 questions below (you'll overwrite the existing file at the end)
2. **Set expectations** before question 1:
   > I'm going to ask you 10 questions about your business — should take about 15 minutes. Every other workshop skill reads your answers, so this is the foundation. Take your time. Answer "I don't know" if you genuinely don't — we'll work around it.

---

## The 10 questions

Ask one at a time. Wait for the answer. Acknowledge briefly ("got it", "nice", "ok") then move on. **Don't paste the whole list at once** — the attendee should feel like a conversation, not a form.

If they answer "I don't know" or "I'm not sure", help them through it (see "Handling unknown answers" below). Don't skip questions silently.

### 1. Business name and website URL

> What's your business called, and what's your website URL?

Capture both. If they give you a URL without `https://`, prepend it. If they say "I don't have a website yet", note that — it changes which workshop skills work for them.

### 2. One-sentence pitch

> In one sentence, what does your business do?

This becomes the seed for keyword research and the anchor for content briefs. If they ramble for three sentences, gently push: *"give me the shortest version of that".*

### 3. Geographic scope

> Where do you serve customers? List the specific suburbs, cities, regions, or "all of Australia online" if you're not location-based.

Be specific. *"Melbourne"* is not as useful as *"Melbourne CBD, Richmond, Fitzroy, Carlton, South Yarra"*. Push for specifics — these become location pages and Local Pack targets.

If they're online-only, note that (e.g. *"all of Australia online — no physical service area"*).

### 4. Services or products

> What are the top 3–5 services or products you offer? List them.

For service businesses: think page titles. *"Emergency plumbing"*, *"Hot water systems"*, *"Blocked drains"*. For ecommerce: top product categories.

If they list 10, ask which 3–5 they want to focus on. If they list 1, ask if they really only do one thing.

### 5. Ideal customer

> Describe your ideal customer in 1–2 sentences. Who are they, what do they need, what's their typical situation when they're looking for someone like you?

Push past *"anyone who needs plumbing"*. Better: *"homeowners aged 35–65 in the Geelong region, usually calling in a panic — burst pipe, no hot water, blocked toilet. Want fast response, fair price, certified plumber."*

This drives intent matching in keyword research and tone in content.

### 6. Top 10 customer questions

> What are the top 10 questions your customers actually ask you, day to day? Be specific — *"how much does X cost"*, *"how long will X take"*, *"do you service Y suburb"*, *"what happens if Z"*. Aim for 10, fewer is fine if you genuinely can't think of more.

**This is the gold question.** Each one becomes:
- A potential FAQ entry on a service page
- A potential blog post or knowledge-base article
- A potential AI Search citation (Claude / Perplexity / ChatGPT love question-format content)

Push for 10. If they stall at 5, prompt them with category hints: *"What do they ask about pricing? Timing? Process? Warranties? Locations? Qualifications? After-service?"*

### 7. Competitors

> Who are your top 3 competitors? URLs preferred if you know them.

If they say *"I don't really have competitors"*, push back: *"Whoever shows up on Google when someone searches for what you do. Try searching '[your top service] [your suburb]' and tell me the top 3 businesses."*

If they still can't name any, offer to run `/v1/domain/competitors` later (via the keyword-research skill) once basics are captured.

### 8. What makes you different

> What makes you different from those competitors? Don't tell me *"we care more"* — give me the specific reason a customer would pick you over the others. One or two sentences.

Push for concrete differentiators. Examples of good answers:
- *"20 years local. Geelong-born tradesmen who actually live in the suburbs we service. Same-tradesman guarantee."*
- *"We're the only clinic in CBD with bulk-billing for new patients."*
- *"Fixed-fee pricing, no hourly rates, quoted upfront."*

Examples of useless answers to push back on: *"better customer service"*, *"quality work"*, *"we care"*.

### 9. SEO goal (next 6 months)

> What's the specific outcome you want from SEO in the next 6 months? More leads? More sales of a specific product? Brand awareness for a new service? Be concrete.

Help them be specific:
- *"30–50% more inbound leads from organic search, especially for emergency plumbing"* — good
- *"Rank #1 for [keyword]"* — they don't actually want a rank, they want the customers. Re-frame.
- *"More traffic"* — push for what the traffic should do (leads? sales? bookings?)

### 10. Brand voice

> How does your business sound — formal, casual, technical, friendly? And give me 2–3 phrases or words you'd never say. Helps us avoid sounding off-brand in your content.

Voice descriptors that are useful: *"casual, no-bullshit, like a mate who happens to be a plumber"*, *"professional but warm, like a family GP"*, *"technical and confident, written for engineers"*.

The *"words you'd never say"* prompt is the most useful — it's faster to define a voice by what it's NOT than what it IS. Common avoid lists: corporate jargon (*"solutions", "leverage", "synergies"*), fluff (*"world-class", "industry-leading"*), aggressive sales talk.

---

## Handling unknown answers

If the attendee says *"I don't know"* on a question, don't skip silently. Either:

- **For questions 1, 2, 4, 5** — push gently. These are foundational. *"Take your best guess, you can edit it later."*
- **For question 6 (top 10 questions)** — prompt with categories. *"What do customers ask about pricing? Timing? Process? After-service?"*
- **For question 7 (competitors)** — offer to find them via `/v1/domain/competitors` later. Note "TBD — to be discovered" in the file for now.
- **For question 9 (SEO goal)** — suggest a default: *"More qualified leads from organic search — let's go with that for now, you can refine after Day 1."*

Always note in the file when something is provisional, e.g. `**SEO goal:** [TBD — placeholder set on day 1, will refine]`.

---

## After all 10 answers — confirm before writing

Summarise the answers back in this format:

> Here's what I've got:
>
> - **Business:** Acme Plumbing (acmeplumbing.com.au)
> - **What you do:** Emergency plumbing and hot water repairs across Geelong
> - **Service area:** Geelong, Lara, Ocean Grove, Drysdale, Leopold
> - **Top services:** Emergency plumbing, hot water systems, blocked drains, bathroom renos, gas fitting
> - **Ideal customer:** Homeowners 35-65 in Geelong region, usually in a panic situation
> - **Top customer questions:** [list the 10]
> - **Competitors:** plumbingmate.com.au, drainsplumbinggeelong.com.au, geelongplumbing.com.au
> - **Differentiator:** 20 years local, Geelong-born tradesmen, same-tradesman guarantee
> - **SEO goal:** 30-50% more inbound leads in 6 months, especially emergency plumbing
> - **Voice:** Casual, no-bullshit, mate-who-happens-to-be-a-plumber. Avoid "solutions", "leverage", "world-class"
>
> Anything to correct before I save this?

Wait for confirmation. Apply corrections. Then write the file.

---

## Writing the file

Save to `./business-context.md` at the **project root** (not inside any subfolder). This is the canonical location every other workshop skill reads from.

```markdown
# Business context

## The basics
- **Business name:** [from Q1]
- **Website:** [from Q1 URL]
- **What we do:** [from Q2]

## Geographic scope
[from Q3]

## Services / products
- [Q4 item 1]
- [Q4 item 2]
- [Q4 item 3]
- [...]

## Ideal customer
[from Q5]

## Top 10 customer questions
1. [Q6 item 1]
2. [Q6 item 2]
3. [...]

## Competitors
- [Q7 URL 1]
- [Q7 URL 2]
- [Q7 URL 3]

## What makes us different
[from Q8]

## SEO goal (next 6 months)
[from Q9]

## Brand voice
[from Q10]

---
Captured: YYYY-MM-DD
Skill: business-context v1.0
```

---

## After the file is written

Tell the attendee:

> You're set up. From here, just ask Claude what you want to do — every workshop skill will use this context automatically.
>
> Suggested first moves:
>
> - **"Find me keywords for my business"** → keyword research using your services + location
> - **"How is my site doing on Google?"** → domain overview using your URL
> - **"Who are my competitors in search?"** → SE Ranking's view of who you're actually competing with
> - **"Audit my site for technical issues"** → site audit (when that skill is available)

Don't auto-trigger any of those — let the attendee pick.

---

## Editing the file

The attendee can edit `./business-context.md` directly at any time. Tell them:

> If your business changes, just open `./business-context.md` and edit it. Every skill picks up changes on its next run.

---

## Notes for skill maintainers

- **File location is sacred.** Keep it at project root (`./business-context.md`). Other skills are hard-coded to read from this path.
- **Section headings are sacred.** Other skills grep for `## Services / products`, `## Competitors`, etc. Don't rename sections without updating consumers.
- **Adding fields:** if you add a question (Q11+), add a new section heading and document it here. Backwards-compatible additions are fine; renames break dependents.
- **Audience:** SMB owner, in-person at Day 1 of a 2-day workshop. Time-boxed to ~15 min. Coach is in the room if they get stuck.
