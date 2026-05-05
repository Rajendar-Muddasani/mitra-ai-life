# Scaling and Operations Plan

## Objective
Prepare the business so it can grow from a free content website into a small but serious AI education platform serving at least 1000 users with media-heavy content.

## Recommended operating model

### Keep GitHub for source, not storage
Use GitHub for:
- markdown lesson scripts
- prompts and workflows
- page code
- metadata manifests
- thumbnail references
- automation scripts

Do not use GitHub for:
- rendered videos
- large image batches
- narration audio masters
- raw AI generation exports

## Media strategy for 100 GB

### Storage
- use object storage such as Cloudflare R2 or S3-compatible storage
- store media by language, level, lesson, and version
- keep public URLs in a lesson manifest file

### Delivery
- use a CDN in front of all images and videos
- use adaptive video delivery once watch time becomes meaningful
- compress images for mobile-first users in India

## User scale strategy for 1000 users

1000 users is still a comfortable scale if the system is designed simply.

### Stage A: early launch
- static pages
- embedded video or hosted video links
- simple forms
- no login or only very light login

### Stage B: first paid users
- authentication
- protected lesson pages
- Razorpay checkout
- a small relational database for users, purchases, and progress

### Stage C: more serious platform
- lesson APIs
- role-based content access
- background jobs for certificates, email, and asset sync
- content admin dashboard

## Suggested stack by maturity

| Maturity | Frontend | Backend | Storage | Payments | Analytics |
|---|---|---|---|---|---|
| MVP | static site or Vite React | forms only or Supabase | R2 | none | PostHog or Plausible |
| Paid launch | Next.js | Supabase or managed Postgres | R2 | Razorpay | PostHog |
| Scale | Next.js | managed API plus workers | R2 plus video service | Razorpay | PostHog |

## AI content production workflow

### Source-of-truth structure
For each lesson keep:
- source lesson markdown
- prompt inputs used to generate assets
- asset manifest with URLs and version numbers
- review checklist status
- translation status

### Recommended lifecycle
1. create lesson objective
2. write English master script
3. generate comic panels and slides
4. generate short video and voice-over
5. create Telugu adaptation notes
6. review for clarity, factual issues, and cultural fit
7. publish and measure

## Suggested lesson manifest fields

- lesson_id
- level_id
- title_en
- title_te
- audience
- duration_minutes
- learning_goal
- asset_urls
- transcript_url
- worksheet_url
- quiz_url
- review_status
- published_at
- version

## Team model

Even if AI generates most of the assets, the business still needs clear human roles.

### Founder
- brand direction
- audience interviews
- product decisions
- final publishing approval

### Copilot and AI agents
- draft lesson plans
- create first-pass scripts
- create image and video prompts
- suggest page layouts
- generate metadata and manifests

### Human reviewer
- remove factual errors
- correct unnatural Telugu
- catch cultural mismatches
- validate payment and product promises

## Risks and mitigations

### Risk: low trust in AI content
Mitigation: use transparent examples, clear disclaimers, and visible review standards.

### Risk: Telugu translation feels robotic
Mitigation: build a glossary and require human correction for public releases.

### Risk: content costs rise too quickly
Mitigation: start with still images, comics, and slide videos before expensive high-motion content.

### Risk: repo becomes messy
Mitigation: keep a strict folder structure and store only source files in GitHub.

### Risk: legal exposure from claims
Mitigation: avoid promises around jobs, income, health, law, or financial outcomes.

## API and service shortlist

### Likely first set
- LLM provider: GPT-5 or Claude for core writing
- image provider: Flux or Ideogram
- video provider: Runway or Pika
- voice provider: ElevenLabs
- payments: Razorpay
- analytics: PostHog
- storage: Cloudflare R2
- auth and DB: Supabase

## Decision rule

If a new tool does not reduce content production time, improve quality, or lower delivery cost, it should not be added. Keep the system lean until revenue justifies complexity.
