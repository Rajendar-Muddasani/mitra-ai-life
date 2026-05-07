# Phasewise Implementation Plan

## Mission

Teach people in India how to use AI in daily life through very simple, visual, story-driven lessons. Start in English, translate to Telugu first, and expand to more Indian languages later.

## Product direction

The strongest version of this idea is not only a course website. It is a content platform with:
- free beginner learning for mass adoption
- paid practical upskilling for working adults
- school and college-friendly AI literacy content
- premium engineering project tracks for serious student builders
- an AI-assisted content factory that can scale across languages and formats

## Core principles

- Explain AI in plain language first, not technical language.
- Use Indian daily-life examples before office examples.
- Teach outcomes, not models or jargon.
- Keep each lesson short, visual, and reusable across formats.
- Launch free content early instead of waiting for the full catalog.
- Use AI for speed, but keep human review for truth, tone, and safety.
- Design for bilingual delivery from the start, even if only English and Telugu are active in the first phase.

## Phase 0: Idea framing and validation

Timeline: 1 to 2 weeks

### Goals
- finalize brand direction and repo name
- define the first two free levels
- create a simple landing page and a waitlist
- validate whether parents, students, and working adults understand the offer

### Deliverables
- startup pitch page
- phasewise plan
- level plan and pricing model
- one landing page headline set in English
- Telugu translation glossary for core terms
- feedback form for early users

### Success signal
- at least 30 to 50 interested users from personal network, WhatsApp groups, colleges, or local communities

## Phase 1: Free launch MVP

Timeline: 2 to 4 weeks

### Goals
- publish the first two free levels
- publish basic primary-school-friendly AI awareness content
- collect user feedback before adding payments

### Product in this phase
- public website with homepage, levels page, and about page
- Level 1 and Level 2 in English
- Telugu adaptation for Level 1 and key parts of Level 2
- lead capture for future paid levels
- basic analytics to learn which topics people actually use

### Content types in this phase
- cartoon strips
- short explainer comics
- image slides
- short subtitled videos
- one-page stories
- simple worksheets or challenge cards

### Recommended tech
- static or very lightweight React site
- Cloudflare Pages or Vercel for hosting
- Cloudflare R2 or similar object storage for media
- PostHog or Plausible for analytics
- Google Forms, Tally, or Supabase forms for feedback capture

### Success signal
- first 100 users
- at least 20 users finish Level 1
- qualitative feedback shows people can understand the examples without technical guidance

## Phase 2: Paid practical curriculum

Timeline: 4 to 8 weeks

### Goals
- publish Levels 3 to 5
- introduce payment flows and combo pricing
- add progress tracking and certificates of completion

### Product in this phase
- paid level pages
- Razorpay integration
- basic user login and course access control
- downloadable worksheets and templates
- certificate generator for selected levels

### Business outcome
This is the first phase where the business tests willingness to pay.

### Success signal
- 25 paid learners
- at least one combo plan conversion each week
- refund issues stay low because promises are clear and realistic

## Phase 3: Segment expansion

Timeline: 6 to 10 weeks

### Add these content lanes
- working adults: office productivity, job search, communication, research
- homemakers and family users: budgeting, school help, health information drafting, travel planning
- primary and secondary school students: curiosity-led AI awareness
- junior college students: study planning, presentation help, career exploration
- engineering students: project ideation, datasets, documentation, demo building

### Important rule
School and student learning content can be free or low-cost, but engineering project tracks should be clearly separated from the daily-life beginner curriculum. The audience, price, support effort, and risk are different.

## Phase 4: Premium project studio

Timeline: 8 to 12 weeks

### Offerings
- guided engineering mini-projects
- 4-month capstone projects with real-world use cases
- project documentation packs
- mentor review add-ons

### Indicative pricing
- mini-project packs: 10000 to 25000 INR
- guided real-world builds: 25000 to 75000 INR
- advanced institutional or sponsored builds: 75000 to 200000 INR

### Guardrail
Do not market these as guaranteed placement or academic shortcuts. Position them as guided applied learning.

## Phase 5: Company setup and compliance

Start this after product validation, not before.

### Actions
- register the company after early traction is proven
- formalize terms of service and privacy policy
- define content disclaimer standards
- define AI safety and accuracy review policy
- define refund and support rules
- decide GST and invoicing approach with a CA

## Phase 6: Content engine and automation

### Goal
Turn the business into a repeatable AI-assisted studio.

### Pipeline
1. research a user problem
2. draft lesson in plain English
3. convert lesson into comic, slide, short video, and worksheet versions
4. generate Telugu translation pack
5. run factual and tone review
6. publish to web and social channels
7. measure engagement and refine

### Suggested AI stack
- writing and curriculum: GPT-5, Claude, Gemini for comparison and QA
- image generation: Flux, Ideogram, Midjourney, or similar
- video generation: Runway, Pika, or similar
- voice-over: ElevenLabs or similar
- workflow orchestration: n8n or LangGraph-style pipelines
- knowledge base and prompts: GitHub repo plus structured markdown content

## Phase 7: Scale to 1000 users and 100 GB content

### Traffic and product scale
- 1000 active users is manageable with a modern JAMstack or Next.js architecture
- 100 GB of media should not live in GitHub; store only metadata and prompts in the repo
- keep videos, rendered images, and large assets in object storage with CDN delivery

### Recommended architecture at scale
- frontend: Next.js or a similar framework once the product outgrows a static site
- auth and database: Supabase, Firebase, or a managed Postgres stack
- payments: Razorpay
- media storage: Cloudflare R2, S3-compatible storage, or Backblaze B2
- video delivery: Mux, Bunny Stream, or Vimeo OTT depending on economics
- analytics: PostHog
- background jobs: serverless queues or a worker-based job system

### GitHub strategy
- keep lesson source files, prompts, planning docs, and metadata in the repo
- do not commit generated videos or large binary assets to GitHub
- use one content manifest per lesson so assets can be tracked outside the repo
- use releases or tagged content versions only for milestone snapshots

## Legal, ethical, and trust requirements

- avoid exaggerated claims such as guaranteed job, guaranteed income, or guaranteed intelligence improvement
- mark AI-generated examples clearly when needed
- never publish unsafe health, legal, or financial guidance without strong disclaimers
- be careful with children-focused content, consent, and privacy

---

## Current Build Status (as of May 2026)

All decisions below are recorded from founder planning sessions. See `docs/resource-usage.md` for live numbers.

### What is live
- L1–L7 English comic pages — all live on mitraailife.com
- L1–L7 Telugu comic pages — all live
- Home page EN + TE, pitch deck — live
- Google OAuth + Supabase user_progress tracking (auth.js)
- DALL-E 3 images for all 7 levels — generated and deployed to S3
- GA4 + Disqus on all 14 content pages

### What is not yet built
- Mitra chatbot widget (bottom-right floating bot)
- Supabase progress restore on home page
- Admin dashboard to view user completions
- Videos for any level
- Jupyter notebooks for engineering track
- mitraaistudent.com and mitraaiprojects.com sites
- Languages beyond English and Telugu
- Payment activation (deliberately deferred — see pricing note below)

---

## Pricing Policy (IMPORTANT)

**All prices are currently 0 INR as an early access offer.**

The original listed prices exist as a reference for when payments are eventually activated.
Payments will NOT be activated until the founder explicitly decides the platform is ready to charge.
Until that decision is made, treat every level as free regardless of what the original price was.

Engineering project tracks and school content tracks are also priced at 0 INR under the same early offer.
Their indicative pricing is listed below purely for future reference.

| Level | Name | Original listed price | Early offer price |
|---|---|---:|---:|
| 1 | First Step | 0 INR | 0 INR |
| 2 | Daily Help | 0 INR | 0 INR |
| 3 | Smart Basics | 100 INR | **0 INR (early offer)** |
| 4 | Work Smart | 200 INR | **0 INR (early offer)** |
| 5 | Life Upgrade | 300 INR | **0 INR (early offer)** |
| 6 | Power User | 400 INR | **0 INR (early offer)** |
| 7 | Build With AI | 500 INR | **0 INR (early offer)** |

Engineering project track indicative prices (future reference only, currently 0 INR):
- mini guided project packs: 10,000–25,000 INR
- guided real-world builds: 25,000–75,000 INR
- advanced institutional or sponsored builds: 75,000–200,000 INR

School student track indicative prices (future reference only, currently 0 INR):
- AI awareness module for Gr 6–8: 99–199 INR
- AI study skills for Gr 9–12: 199–399 INR
- School or institution bulk licence: custom pricing

---

## Three-Website Strategy

Rather than putting all audiences into one website, the platform will eventually operate
across three separate, cross-linked websites. This reduces information overload per visitor
and allows each site to feel purpose-built for its audience.

| Domain | Target Audience | Content Focus | Status |
|---|---|---|---|
| mitraailife.com | Working adults, homemakers, general public | Daily life AI, L1–L7 ladder | ✅ Live |
| mitraaistudent.com | School students Gr 6–12, parents, teachers | Make students AI-ready — not just AI study, but students who think and work with AI | ❌ Planned |
| mitraaiprojects.com | Engineering/CS/IT students, final year | Portfolio project track, guided builds, notebooks | ❌ Planned |

> **Why mitraaistudent and not mitraaistudy?**
> mitraaistudy sounds like a subject — studying AI.
> mitraaistudent positions the outcome — the student becomes AI-enabled, AI-ready, AI-confident.
> The goal is not to teach AI as a topic. The goal is to transform the student into someone who
> naturally uses AI as a tool in everything they do.
> Parents and students reading "mitraaistudent" will think: my child will become an AI-capable student.
> That is exactly the right perception.

### Hosting and domain cost
- All three sites on GitHub Pages — hosting is free
- Domain registration: ~40–50 SGD/year per domain on GoDaddy
- Each site gets its own GitHub repo (or separate deploy path in monorepo)
- All three sites cross-link each other in headers and footers

### When to create each new site
- mitraaistudent.com: when at least 5 school-specific lessons are ready
- mitraaiprojects.com: when at least 3 guided engineering project briefs + notebooks are ready

---

## Mitra Chatbot Plan (custom branded widget)

### Goal
Make Mitra feel like a real AI-powered product, not a static website about AI.
A floating chatbot bottom-right on every page demonstrates exactly what the platform teaches.

### What the bot does
- Answers "where should I start?", "what does Level 3 teach?", "is this free?"
- Guides visitors toward the right level based on their background
- Responds in English or Telugu based on which page the user is on
- Does NOT impersonate a doctor, lawyer, or financial advisor
- Includes a clear disclaimer: "I am an AI assistant. Always verify important information."

### Does the bot read the website pages automatically?
No. The bot does not crawl or scrape pages in real time.
It is powered by a carefully written system prompt that describes all 7 levels,
what each teaches, current pricing (0 INR offer), FAQs, and the three-website plan.
At this scale, a well-crafted system prompt is the knowledge base — no RAG pipeline,
no fine-tuned model, no training needed. When new levels are added, the system prompt is updated.

### API key security — Cloudflare Worker proxy

Calling OpenAI directly from the browser would expose the API key in client-side code.
The solution is a Cloudflare Worker that acts as a thin proxy:

```
Browser → POST {message, history} → Cloudflare Worker (chat.mitraailife.com)
                                          ↓
                                  Worker adds OPENAI_API_KEY from env
                                          ↓
                                  POST to OpenAI API
                                          ↓
                                  Streams response back to browser
```

Cloudflare Worker free tier: 100,000 requests/day — far more than needed.
API key lives only in Cloudflare environment variables — never reaches the browser.
Setup cost: ~20 lines of JavaScript worker code + add subdomain to Cloudflare.

### Bot presence across pages
- Widget is present on every page (index.html, index-te.html, all level pages)
- Widget is subtle: a small icon bottom-right that expands on click
- Does not auto-open on every page — user must click to start
- Does not animate or bounce to avoid distraction during reading

### Build order for chatbot
1. Cloudflare Worker proxy script
2. Chatbot widget JS + CSS (inline in a shared `site/mitra-chat.js`)
3. System prompt (all level knowledge, FAQs, tone guide)
4. Inject widget into all HTML pages
5. Test EN page and TE page responses
6. Commit and deploy

---

## Language Expansion Roadmap

All translations follow the same pattern: English source page first, then translation.
Translation order is based on speaker population and platform relevance.

| Priority | Language | Status | Notes |
|---|---|---|---|
| 1 | Telugu | ✅ Complete L1–L7 | First language — Andhra Pradesh and Telangana |
| 2 | Hindi | ❌ Planned | Largest reach — 500M+ potential users — second priority after Telugu |
| 3 | Kannada | ❌ Planned | Karnataka — strong tech community |
| 4 | Tamil | ❌ Planned | Tamil Nadu + Sri Lanka + Singapore diaspora |
| 5 | Malayalam | ❌ Planned | Kerala — high literacy, high mobile usage |

Each new language adds: a translated set of all level pages + a translated home page
(e.g. index-kn.html, index-ta.html) + lang switcher links on all existing pages.

---

## Video Production Roadmap

Videos are the biggest missing piece for beginner learners.
A 90-second to 3-minute narrated walkthrough per level will increase engagement significantly.

### Planned workflow
1. Write a simple English voiceover script from the level markdown
2. Generate voice using ElevenLabs or similar TTS
3. Combine with comic panel images in a simple video editor or Runway
4. Add Telugu subtitles as a second pass
5. Upload to S3 (or Mux/Bunny for adaptive streaming later)
6. Embed in level page above the comic strip

### Priority
- L1 video first (biggest drop-off point, most important for trust-building)
- L2 video second
- Then L3–L7 in order

---

## Engineering Project Track Plan (mitraaiprojects.com — future)

### Target audience
Final-year CS/IT students who need a real portfolio project.
Junior developers looking to add an AI-powered project to their resume.

### What the track offers
- Guided project briefs with clear problem statements
- Starter Jupyter notebooks with scaffolded code
- File structure recommendations
- README templates
- Deployment walkthroughs (Streamlit Cloud, Hugging Face Spaces, Vercel)
- Peer review or mentor review as an optional add-on

### First project planned
- Canteen Menu Optimiser (Streamlit + Pandas + OpenAI) — inspired by Kiran's story in L7
- Starter notebook: data loading, OpenAI call, Streamlit UI scaffold

### Tech format
- Project brief as markdown
- Starter code as Jupyter notebook (.ipynb)
- README as markdown
- All hosted on mitraaiprojects.com once site is created

---

## School Student Track Plan (mitraaistudent.com — future)

### Target audience
Students in Grades 6–12, parents, school teachers.

### What the track offers
- Age-appropriate AI awareness lessons (no jargon, lots of visuals)
- "AI for homework help — how to do it right" module
- "What AI cannot do" safety module
- Study skill boosters: summarising, explaining, practicing
- Teacher resource pack (slides, discussion prompts)

### Important rule
School content must be reviewed for age-appropriateness before publishing.
No personally identifiable information from students should ever be collected.
Parental consent guidance must be included where relevant.

---

## Supabase — Planned Additions

### Progress restore on home page (Priority 1 after chatbot)
Currently saveProgress() writes to Supabase on quiz completion.
The home page does not yet read this back.
Plan: on login, query user_progress and mark completed levels visually on the ladder.

### Future tables (when needed)
| Table | Purpose | When |
|---|---|---|
| user_progress | Quiz scores, completions | ✅ Exists |
| purchases | Payment records | When payments activate |
| project_submissions | Engineering project uploads | When project track launches |
| newsletter | Email capture | Before any paid launch |

---

## Admin Dashboard Plan

A simple read-only view (protected by Google login, founder only) showing:
- total registered users
- level completion counts
- quiz score distributions
- most and least completed levels

Build as a lightweight HTML page querying Supabase directly with service key stored securely.

---

## Resource Usage Automation (Future CI/CD)

Plan to automate `docs/resource-usage.md` via a daily GitHub Actions workflow that:
- queries GitHub API for repo stats
- queries AWS S3 for object count and storage used
- queries Supabase for user count and row count
- commits the updated file with a `chore: daily resource snapshot` message
- do not use copyrighted cartoon characters or licensed content without permission
- create an editorial rulebook for bias, misinformation, and translation quality

## Recommended KPIs

- free user signup rate
- Level 1 completion rate
- Level 2 return rate
- paid conversion from free users
- Telugu content usage share
- average lesson completion time
- support questions per 100 users
- content production cost per lesson pack

## What Copilot should optimize over time

Copilot should be allowed to improve:
- level names
- lesson order
- tech stack choices
- asset generation workflows
- automation scripts
- translation workflow
- pricing bundles

Copilot should not change these without explicit approval:
- beginner-first positioning
- English source plus Telugu-first translation strategy
- ethics and safety rules
- free-first launch plan
