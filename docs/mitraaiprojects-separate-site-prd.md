# mitraaiprojects.com — Separate Website PRD

> Purpose: this file is the implementation-ready PRD for a new standalone project-kits website that can be built in a fresh VS Code workspace with GitHub Copilot.

## 1. Product Decision

Build `mitraaiprojects.com` as a separate public website.

This site should not live as a visible top-level track inside `mitraailife.com`.

Reason:
- the Mitra AI Life public site is beginner-first, family-safe, and broad
- project kits are premium, technical, higher-support, and outcome-driven
- the buyer intent, page design, copy tone, pricing, and support expectations are different
- separating the site reduces confusion for parents, school learners, and beginner users

## 2. Who This Is For

Primary users:
- B.Tech, BCA, MCA, diploma, and engineering students in India
- final-year students who need a serious build, explanation path, and viva confidence
- freshers who need portfolio projects for placements
- third-year students who want guided mini-projects before final year

Secondary users:
- college teams building group projects
- faculty or project mentors reviewing project outcomes
- learners outside India who can use the same English-first technical content

Not for:
- school students
- casual AI learners
- users looking for generic AI theory only
- users asking for unethical academic cheating or fake submissions

## 3. Core Promise

Plain-language promise:

**Build real AI projects with code, explanation, deployment guidance, viva prep, and a clear path from idea to demo.**

What problem it solves:
- many students can copy code but cannot explain it
- many project sellers offer weak quality, weak documentation, or unethical shortcuts
- students need a structured path: build, understand, present, and prove

Simple explanation:
- this is not just a course
- this is not just a code dump
- each project kit is a guided build system with teaching, code, reports, demo assets, and explanation support

## 4. Business Position

| Item | Decision |
|---|---|
| Business lane | Premium project services and technical learning |
| Launch language | English only at launch |
| Telugu plan | Later for subtitles, support docs, and select landing assets |
| Free tier | Very limited free previews only |
| Paid model | Premium paid project kits and add-ons |
| Brand relationship | "Part of the Mitra family" but operationally separate public site |
| Risk posture | No fake guarantees, no done-for-you cheating claims |

## 5. Product Goals

Launch goals:
- make the site credible enough that a student understands the offer in under 90 seconds
- show clear lanes: mini projects, major projects, portfolio builds, viva packs
- make each project page conversion-ready with strong clarity, not hype
- create a reusable production system for project pages, videos, posters, and support docs
- keep the codebase easy for a single founder plus Copilot workflow

Success metrics for first release:
- at least 1 polished home page
- at least 1 polished catalog page
- at least 3 strong public project pages
- 1 working lead capture flow
- 1 working payment-intent or enquiry flow
- 1 repeatable project-page generation system

## 6. Non-Goals

Do not build these in v1:
- full LMS complexity
- multi-instructor dashboards
- complex student communities
- heavy custom backend before demand is proven
- Telugu full-site duplication at launch
- dozens of projects before the first few are excellent

## 7. Offer Structure

Recommended commercial lanes:

| Lane | Buyer need | Format | Price direction |
|---|---|---|---|
| Guided Mini Projects | quick working build | smaller kit + explanation | lower premium |
| Major Project Kits | final-year submission | full kit + docs + demo | core premium |
| Portfolio Builds | placement proof | polished deployable build | core premium |
| Viva and Submission Packs | explanation + reporting | add-on templates and prep | add-on |
| Mentor Support | higher confidence | review calls / doubt support | optional upsell |

## 8. Site Map

Public information architecture:

1. `/` Home
2. `/projects/` Catalog
3. `/projects/<slug>.html` Project detail pages
4. `/lanes/mini-projects.html`
5. `/lanes/major-projects.html`
6. `/lanes/portfolio-builds.html`
7. `/lanes/viva-packs.html`
8. `/pricing.html`
9. `/how-it-works.html`
10. `/faq.html`
11. `/contact.html`
12. `/about.html`
13. `/privacy.html`
14. `/payment-policy.html`
15. `/terms.html`

Optional later:
- `/compare/` project comparisons
- `/stories/` learner case studies
- `/blog/` technical explainers and SEO pages
- `/login/` and `/dashboard/` only after paid usage is real

## 9. Page Requirements

### Home

Must answer quickly:
- who this is for
- what kind of project outcomes are available
- how this differs from random project sellers
- what is free vs paid
- how to pick the right lane

Sections:
- hero with one-line promise
- trust strip: code + docs + viva + deployment
- lane cards
- featured projects
- 90-second overview video
- how it works in 4 steps
- pricing summary
- FAQ
- final CTA

### Catalog

Must support:
- filter by lane
- filter by difficulty
- filter by tech stack
- filter by delivery goal
- quick scan without overload

Each catalog card should show:
- project name
- short result statement
- tech stack
- lane
- difficulty
- price starting point
- status badge
- CTA

### Project Detail Page

Every public project page should include:
- clear problem statement
- who it is for
- what the student will actually build
- demo visuals or short overview video
- tech stack
- prerequisites
- modules / milestones
- deliverables included
- what support is included and not included
- learning outcomes
- viva / report / deployment support summary
- pricing or enquiry CTA
- FAQ
- related projects

### Pricing Page

Must be extremely clear:
- what the buyer gets
- what is not included
- whether the offer is self-paced, guided, or reviewed
- what happens after purchase
- refund policy boundary

### How It Works

Simple step flow:
1. choose lane
2. review project page
3. submit interest or buy
4. receive access / repo / docs
5. build with milestones
6. prepare demo, report, and viva

## 10. Content Model

Each project should be manifest-driven.

Recommended fields:

```yaml
project_id: project-01
slug: document-qa-assistant
title: Document Q&A Assistant
lane: major-project-kit
difficulty: intermediate
audience:
  - final-year students
  - placement-focused learners
language_launch: en
translation_status:
  te: planned
price_inr: 2999
status: featured
duration_weeks: 6
core_problem: Answer questions from uploaded documents
demo_type: web-app
tech_stack:
  - Python
  - FastAPI
  - OpenAI API
  - Vector store
deliverables:
  - source code
  - README
  - setup guide
  - deployment guide
  - PPT template
  - report template
  - viva questions
assets:
  hero_image: https://...
  poster_image: https://...
  overview_video: https://...
seo:
  title: ...
  description: ...
```

## 11. Repo Skeleton For New Workspace

```text
mitra-ai-projects/
  README.md
  .gitignore
  .env.example
  CNAME
  package.json
  site/
    index.html
    projects/
      index.html
      project-template.html
      document-qa-assistant.html
      resume-screener.html
      multilingual-support-bot.html
    lanes/
      mini-projects.html
      major-projects.html
      portfolio-builds.html
      viva-packs.html
    pricing.html
    how-it-works.html
    faq.html
    about.html
    contact.html
    privacy.html
    payment-policy.html
    terms.html
    assets/
      css/
      js/
      icons/
  data/
    projects/
      project-01.yaml
      project-02.yaml
      project-03.yaml
    featured-projects.json
    pricing.json
    faq.json
  content/
    projects/
      project-01/
        script.md
        overview.md
        module-01.md
        module-02.md
        demo-notes.md
        viva.md
        report-template.md
        ppt-outline.md
      project-02/
      project-03/
  scripts/
    build_project_pages.py
    build_catalog.py
    generate_project_hero_images.py
    generate_project_overview_video.py
    generate_project_posters.py
    upload_project_assets.py
    validate_project_manifests.py
  prompts/
    project-page.prompt.md
    project-video.prompt.md
    project-image.prompt.md
    viva-questions.prompt.md
  docs/
    prd.md
    content-production-workflow.md
    launch-checklist.md
```

## 12. Tech Stack Recommendation

For v1 use the leanest setup that still feels premium.

Recommended v1:
- static site in `site/`
- plain HTML, CSS, and small JavaScript
- Python build scripts for page generation
- S3 for media hosting using existing asset workflow
- Formspree or simple contact form for leads
- Razorpay payment link or enquiry-first flow before full checkout
- Google Analytics or PostHog for measurement

Recommended v2:
- Vite or Next.js if content volume and protected access become meaningful
- Supabase for auth, progress, and gated assets
- proper order and delivery workflow

## 13. Design Direction

Visual direction:
- technical, sharp, credible, and clean
- should feel professional, not student-cheap and not fake-corporate
- use strong typography, code motifs, milestone diagrams, and outcome-first copy

Suggested visual system:
- base colors: graphite, off-white, deep teal
- accent color: amber for pricing and warnings only
- code blocks and architecture diagrams as part of the design language
- project cards should show real structure, not generic marketing boxes

Tone:
- direct
- credible
- outcome-first
- no exaggerated promises

## 14. Content Production Workflow

English is the source of truth.

For each project:
1. define buyer outcome
2. define project scope boundary
3. write English master brief
4. create module outline
5. create code milestones
6. create deliverable list
7. create FAQ and objections
8. generate public page copy
9. generate hero image and poster
10. generate overview video
11. human review for technical accuracy and promise clarity
12. publish

Source files to maintain:
- project manifest
- English master script
- visual prompt inputs
- video narration script
- FAQ source
- pricing metadata
- review checklist

## 15. Video Generation Workflow

Use simple, repeatable production.

Do not start with expensive cinematic video.

Recommended launch video types:
- 60 to 90 second site overview video
- 60 to 120 second project overview videos
- optional 3 to 6 minute module preview videos later

Video recipe:
1. read project manifest
2. generate narration script
3. generate 5 to 8 scene prompts
4. create still visuals or code-screen composites
5. create TTS draft narration
6. assemble with MoviePy or ffmpeg
7. add captions
8. export poster frame
9. upload to S3
10. write asset URLs back into manifest

Scene types to reuse:
- project problem
- workflow diagram
- UI preview
- code snippet zoom
- deployment proof
- viva / report support summary
- CTA

Recommended file outputs:
- `overview-en.mp4`
- `overview-en-poster.jpg`
- `overview-en.vtt`
- `hero-16x9.jpg`
- `thumb-1x1.jpg`

## 16. Image and Asset Workflow

Images to produce per project:
- hero image
- catalog card image
- overview video poster
- architecture diagram
- milestone graphic
- social share image

Keep GitHub for source only.

Store generated media in S3 under a stable structure:

```text
projects/
  project-01/
    hero/
    posters/
    videos/
    diagrams/
  project-02/
  shared/
    og/
    logos/
```

## 17. Lead Capture and Payment Flow

Launch recommendation:
- do not block launch on full e-commerce
- allow enquiry-first flow and manual fulfilment first

v1 options:
- `Contact about this project`
- `Ask which lane fits me`
- `Request syllabus / kit outline`
- `Get pricing and delivery timeline`

v1.5 options:
- Razorpay payment link per project
- lightweight post-payment confirmation flow
- manual email onboarding

v2 options:
- account creation
- gated downloads
- purchase history
- progress tracking

## 18. SEO Plan

Priority pages:
- home
- catalog
- top 3 project pages
- pricing
- how it works

SEO rules:
- every project page must target a real search intent
- titles should combine outcome + technology + audience relevance
- descriptions should mention real deliverables
- use schema where helpful: `Course`, `Product`, `FAQPage`, or `BreadcrumbList`
- create internal linking between related lanes and projects

Example search-intent page ideas:
- AI chatbot project for final year students
- resume screener project with Python
- document question answering final year project
- AI project with deployment and viva support

## 19. Analytics and Measurement

Track these events:
- home CTA click
- catalog filter usage
- project page view
- pricing CTA click
- contact submission
- payment link click
- video start and 50% completion

Use metrics that matter:
- project page to enquiry conversion
- enquiry to sale conversion
- top-performing project lanes
- video watch impact on conversion

## 20. Legal and Ethical Rules

Critical rules:
- do not claim guaranteed job placement
- do not claim guaranteed marks
- do not position the product as fake academic submission help
- do not hide limitations of AI-generated systems
- do not sell unethical plagiarism support

Public messaging rule:
- guided build support is allowed
- explanation, documentation, templates, and mentoring are allowed
- misleading done-for-you cheating language is not allowed

## 21. Implementation Phases

### Phase 0 — Foundation
- create new repo
- create site skeleton
- add shared analytics
- add legal pages
- set up S3 asset paths
- set up manifest format

### Phase 1 — Public Launch Shell
- build home page
- build catalog page
- build one lane page
- build contact page
- build pricing page

### Phase 2 — First Sellable Projects
- publish 3 project pages
- create overview videos
- create enquiry flows
- create manual fulfilment checklist

### Phase 3 — Conversion Improvement
- add testimonials or proof when real
- improve FAQs
- add comparison pages
- add better structured pricing

### Phase 4 — Protected Access
- add auth
- add gated downloads
- add learner dashboard

## 22. First 3 Public Projects To Build

Recommended launch set:

| ID | Project | Why this first |
|---|---|---|
| project-01 | Document Q&A Assistant | clear RAG use case, high relevance, easy to explain |
| project-02 | Resume Screener | placement relevance, strong student demand |
| project-03 | Multilingual Customer Support Assistant | business relevance, chatbot relevance, demo-friendly |

## 23. Copilot Build Prompts For New Workspace

### Prompt 1 — Repo Setup

"Create a production-ready static website repo for `mitraaiprojects.com` using the PRD in `docs/prd.md`. Build the folder structure, shared CSS variables, reusable card patterns, project manifest loader, and placeholder pages for Home, Catalog, Pricing, How It Works, Contact, Privacy, Payment Policy, and Terms. Keep the implementation manifest-driven and mobile-first."

### Prompt 2 — Home and Catalog

"Using the PRD and the project manifest structure, build the Home page and Catalog page for `mitraaiprojects.com`. The site should look technical, premium, and credible. Do not use generic startup copy. Show clear project lanes, featured projects, trust points, and strong enquiry CTAs."

### Prompt 3 — Project Template System

"Create a reusable project-detail page template driven by project YAML or JSON data. Each project page must render hero, outcomes, tech stack, milestones, deliverables, support boundaries, FAQ, and CTA sections from structured data."

### Prompt 4 — Asset Automation

"Create Python scripts to validate project manifests, generate overview narration scripts, assemble short overview videos, upload assets to S3, and write asset URLs back into the manifest. Keep GitHub as source-of-truth only and store generated media outside Git."

### Prompt 5 — Lead Capture

"Create contact and enquiry flows for project pages with project-specific subject lines, structured forms, and analytics events. Keep fulfilment manual-first, but architect it so payments and gated access can be added later without restructuring the whole site."

## 24. Acceptance Criteria

The v1 PRD is satisfied when:
- the site clearly reads as separate from beginner-family learning
- at least 3 projects can be published from manifests without manual HTML duplication
- videos, posters, and page assets follow a repeatable pipeline
- the public site is honest about what is included
- the buyer can understand fit, price direction, and next step quickly
- technical and legal promises are precise

## 25. Migration Note From Current Repo

Current Mitra AI Life repo actions already aligned with this PRD:
- public navigation no longer exposes Spoken English or Project Kits on `mitraailife.com`
- project-kit work can now continue as a separate-site build stream
- any existing project content in the current repo should be treated as migration source material, not as the final public architecture

## 26. Recommended Next Build Order In The New Workspace

1. repo skeleton and base styles
2. home page
3. catalog page
4. project manifest schema and loader
5. first project detail page
6. asset-generation scripts
7. contact and pricing flows
8. remaining two project pages
9. deploy to GitHub Pages with custom domain
