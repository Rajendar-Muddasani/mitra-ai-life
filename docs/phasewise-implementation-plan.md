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
