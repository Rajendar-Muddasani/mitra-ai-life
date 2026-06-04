# mitraaiprojects.com — Complete Master Plan

> Purpose: this is the single source of truth for the new mitraaiprojects.com workspace. Carry this one file into the new repo. It replaces the older separate PRD. No second planning file is needed.

---

## 1. Product Decision

Build mitraaiprojects.com as a separate public website under the Mitra family.

This site should not live as a visible top-level learning track inside mitraailife.com.

Reason:
- mitraailife.com is beginner-first, family-safe, and broad
- mitraaiprojects.com is technical, code-first, notebook-first, and project-first
- the page structure, copy tone, and learner expectations are different
- separating the site reduces confusion for school learners, parents, and casual AI users

At launch, the site should be openly accessible. Do not build commerce, checkout, or gated delivery flows in v1.

---

## 2. Who This Is For

Primary users:
- B.Tech, BCA, MCA, diploma, and engineering students in India
- final-year students who need a serious build, explanation path, and viva confidence
- freshers who need portfolio projects for placements
- third-year students who want guided mini-projects before final year

Secondary users:
- college teams building group projects
- faculty or mentors reviewing technical outcomes
- learners outside India using the same English-first technical content

Not for:
- school students
- casual AI learners
- users looking for generic AI theory only
- users asking for unethical academic cheating or fake submission help

---

## 3. Core Promise

Plain-language promise:

**Build real AI projects with code, explanation, deployment guidance, viva prep, and a clear path from idea to demo.**

What problem it solves:
- many students can copy code but cannot explain it
- many project sellers and random tutorials are shallow, fragmented, or unclear
- students need a structured path: build, understand, present, and prove

Simple explanation:
- this is not just a code dump
- this is not just a theory course
- each project kit is a guided build system with teaching, code, notes, demo assets, and explanation support
- each course page is meant to make technical topics easier to learn through plain English, tabs, notebooks, quizzes, and linked projects

---

## 4. Product Shape

mitraaiprojects.com has two parallel lanes:

1. **Courses**
Concept-first learning with tabs, notebooks, quizzes, certificates, and cheatsheets.

2. **Projects**
Outcome-first guided builds with architecture, milestone breakdowns, code paths, deployment guidance, demo prep, viva prep, and supporting assets.

Do not organize the whole platform only by academic year labels.

Better organizing principle:
- concept learning lives under Courses
- outcome-driven builds live under Projects
- both should cross-link to each other

---

## 5. Platform Goals

Launch goals:
- make the site credible enough that a student understands the offer in under 90 seconds
- show clear lanes: courses, project kits, cheatsheets, and contact
- make each course page easy to scan and each project page easy to trust
- create a reusable production system for course pages, project pages, posters, videos, cheatsheets, and support docs
- keep the codebase manageable for one founder plus AI coding agents

Release goals:
- one polished home page
- one polished courses index page
- one polished Programming page
- one polished ML page with OneNote-style tab UX
- one polished cheatsheets page
- three strong public project pages
- one working contact form
- one repeatable generation system for projects and related assets

Non-goals for v1:
- full LMS complexity
- multi-instructor dashboards
- heavy custom backend before demand is proven
- Telugu full-site duplication at launch
- large social/community systems

---

## 6. Shared Infrastructure — Use Exactly These

### AWS S3
```
Bucket:     mitra-ai-life-assets
Region:     us-west-2
CDN base:   https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/
```

Use these prefixes:
- `projects/` for project assets
- `cheatsheets/` for PDFs
- `shared/` for logos, OG images, and reusable visuals

Access keys already exist in the current mitraailife.com `.env`.

### Google Analytics
```
GA4 Measurement ID: G-QGY0LH6W93
```

Use the same GA4 property on every page of mitraaiprojects.com.

### Disqus
```
Shortname: mitra-ai-life
```

Reuse this for project pages if comments are enabled.

### Supabase
```
URL:       https://kuriwaysdlqnzqqzabts.supabase.co
Anon key:  already available in current workspace
```

Recommended usage:
- reuse auth pattern from mitraailife.com
- store course completion and project completion separately
- add `course_id` and `project_id` fields instead of reusing only `level_id`

### Cloudflare Worker
```
Existing worker: https://mitra-chat-worker.rajendar-mi46.workers.dev
```

Reuse the same pattern, but create a separate worker for project context if needed:
- `mitra-projects-worker`

### OpenAI
Use the same key and workflow patterns already used in mitraailife.com.

Current planned model usage:
- `gpt-4o-mini` for chatbot and lightweight content transforms
- `tts-1` for narration drafts
- `dall-e-3` for generated visuals when needed

### Python Environment
```
Python 3.14
```

Base packages:
- openai
- boto3
- moviepy
- imageio-ffmpeg
- pillow
- python-dotenv
- pyyaml
- reportlab

---

## 7. Domain and Hosting

| Item | Value |
|---|---|
| Domain | mitraaiprojects.com |
| Launch hosting | GitHub Pages |
| GitHub org | Rajendar-Muddasani |
| Repo | `mitra-ai-projects` |
| Branch | `main` |

Important launch rule:
- do not block development on buying or wiring the custom domain
- build first in GitHub Pages
- add the domain later

Initial deploy target:
- `https://rajendar-muddasani.github.io/mitra-ai-projects/`

Later:
- attach `mitraaiprojects.com`
- add `CNAME`
- enforce HTTPS in Pages settings

---

## 8. Design Direction

Visual direction:
- technical
- sharp
- credible
- clean
- notebook-friendly
- code-first without looking intimidating

It should not look like:
- generic startup SaaS
- school-learning pastel site
- fake-corporate template

### Core color system

```css
--primary:    #00d4aa;
--bg-dark:    #0d1117;
--surface:    #161b22;
--accent:     #f0b429;
--text:       #e6edf3;
--muted:      #7d8590;
--border:     rgba(0,212,170,0.12);
--border-dim: rgba(255,255,255,0.06);
--purple:     #7c3aed;
```

Color discipline:
- teal is the main action color
- amber is only for badges and callouts
- purple is reserved for certificate or rare brand accents
- avoid rainbow UI and extra brand colors

### Hero gradient

```css
background: linear-gradient(160deg, #0d1117 0%, #0d2818 50%, #0a2520 100%);
```

### Typography

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Baloo+2:wght@700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet" />
```

Usage:
- `Baloo 2` for headings
- `Nunito` for body text
- `JetBrains Mono` for code, labels, notebook UI, and technical tags

### Reusable UI patterns

- home hero with dual lane emphasis
- course track cards
- left-tab plus right-content notebook layout
- project detail hero with trust strip and milestone cards
- code example panels
- quiz module pattern
- certificate/completion banner
- cheatsheet download cards
- compact top nav with auth area

---

## 9. Site Map

Primary navigation:

```
Home | Courses | Projects | Cheatsheets | Contact
```

Planned public routes:

1. `/` Home
2. `/courses/` Course track index
3. `/courses/programming.html`
4. `/courses/ml.html`
5. `/courses/dl.html`
6. `/courses/genai.html`
7. `/courses/agentic.html`
8. `/courses/mlops.html`
9. `/courses/rl.html`
10. `/projects/` Projects catalog
11. `/projects/<slug>.html` Individual project pages
12. `/cheatsheets.html`
13. `/how-it-works.html`
14. `/faq.html`
15. `/contact.html`
16. `/about.html`
17. `/privacy.html`
18. `/terms.html`

Optional later:
- `/compare/`
- `/stories/`
- `/blog/`

Do not include pricing or payment pages in v1.

---

## 10. Courses Overview

### 10.1 Track Table

| Track | Audience | Content source | Status |
|---|---|---|---|
| Programming | Complete beginners to intermediate developers | New content | Build first |
| Machine Learning | Engineering students, analysts | AIML-Engineering-Lab notebooks 001–010 | Content ready |
| Deep Learning | ML practitioners | AIML-Engineering-Lab notebooks 014, 015, 034, 054, 073 | Content ready |
| Reinforcement Learning | Advanced learners | New content | Planned |
| Generative AI | Developers and builders | AIML-Engineering-Lab + private repos | Partial |
| Agentic AI and MCP | Developers building tools and agents | Private repos + new content | Partial |
| MLOps and Tools | Production-minded learners | AIML-Engineering-Lab + private repos | Partial |

### 10.2 Courses Page Requirement

The Courses index page must:
- show all tracks as clear cards
- explain in plain language what each track teaches
- indicate which tracks are ready first
- route into detailed topic pages

Each course page must include:
- overview section
- left-side topic tabs
- topic content panel
- quiz
- cheatsheet link
- completion certificate flow
- links to relevant projects

---

## 11. Programming Track

URL: `/courses/programming.html`

Purpose:
- this is the practical programming foundation lane
- it is separate from the beginner-only mitraailife.com student content
- it should support both fresh learners and working learners

Tab structure:

| Tab | Audience | Content |
|---|---|---|
| Python Basics | Complete beginners | Variables, loops, functions, files |
| Python for Data | Students and analysts | Pandas, NumPy, Matplotlib |
| Shell / Bash | Developers | Essential commands, scripting, pipes, cron |
| SQL | Everyone | SELECT, JOINs, GROUP BY, windows |
| Excel Formulas | Office users | VLOOKUP, XLOOKUP, pivots, IF/COUNTIF |
| C / C++ | Engineering students | Pointers, memory, structs |
| Perl | Legacy engineers | Regex, file processing, CPAN basics |
| JavaScript | Web developers | DOM, fetch, async/await, Node basics |

For each tab include:
1. what it is
2. when to use it
3. essential commands or patterns
4. 10 AI learning prompts
5. code examples or notebook block
6. cheatsheet download
7. 5-question quiz
8. completion record

---

## 12. Machine Learning Course — OneNote-Style UX

URL: `/courses/ml.html`

This page is critical. It must use a OneNote-style two-panel layout.

Layout:

```text
┌─────────────────────────────────────────────────────────────────┐
│ nav bar                                                        │
├──────────────┬──────────────────────────────────────────────────┤
│ LEFT TABS    │ CONTENT AREA                                    │
│              │                                                  │
│ Linear Reg   │ What it is                                      │
│ Classification│ When to use                                    │
│ Trees        │ Metrics                                          │
│ Boosting     │ Notebook / runnable demo                         │
│ SVM          │ Watch-outs                                       │
│ Clustering   │ Project idea                                     │
│ Anomaly      │ Quiz + cheatsheet                                │
│ NB / LDA     │                                                  │
│ Time Series  │                                                  │
│ Hyper Opt    │                                                  │
└──────────────┴──────────────────────────────────────────────────┘
```

Each tab contains:
1. plain-English explanation
2. when to use it / when not to use it
3. algorithm variants
4. metric table
5. executable notebook area using Pyodide or embedded Colab
6. common mistakes
7. one concrete project idea
8. 5-question quiz
9. cheatsheet download button

ML source mapping from AIML-Engineering-Lab:

| Topic tab | Source repo |
|---|---|
| Linear Regression | 001_linear_regression_engine |
| Classification | 002_classification_engine |
| Tree-Based Learning | 003_tree_based_learning |
| Boosting | 004_boosting_revolution |
| SVM | 005_support_vector_machines |
| Clustering / Unsupervised | 006_unsupervised_discovery |
| Anomaly Detection | 007_anomaly_detection_dimensionality |
| Naive Bayes / LDA | 008_naive_bayes_lda |
| Time Series | 009_time_series_forecasting |
| Hyperparameter Optimization | 010_hyperparameter_optimization |

---

## 13. Deep Learning Course

URL: `/courses/dl.html`

Topic tabs:

| Tab | Source / notes |
|---|---|
| Neural Network Basics | new content |
| CNNs | 054_wafer_defect_yolo_detection_mlops |
| RNNs / LSTMs | 015_time_series_deep_learning |
| Autoencoders & GANs | 014_autoencoders_and_gans |
| Transformers | 073_dtfs_transformer_system |
| Multimodal (Vision + Language) | 034_multimodal_vision_language |
| Transfer Learning | new content |
| Model Compression | new content |

Use the same tabbed notebook UX as the ML page.

---

## 14. Generative AI Course

URL: `/courses/genai.html`

Topic tabs:

| Tab | Source / notes |
|---|---|
| What is GenAI | plain-English overview |
| Prompt Engineering | prompt patterns and prompting systems |
| RAG | 074_postsilicon_validation_rag + chromadb-rag-tutorials |
| Fine-Tuning | 075_domain_llm_finetuning |
| Embeddings and Vector DBs | Chroma, Pinecone, Supabase pgvector |
| LLM Evaluation | BLEU, ROUGE, LLM-as-judge |
| HuggingFace Ecosystem | Transformers, Datasets, Spaces |
| Kaggle with LLMs | workflow and competition guidance |

---

## 15. Agentic AI and MCP Course

URL: `/courses/agentic.html`

Topic tabs:

| Tab | Source / notes |
|---|---|
| What is an Agent | planning, memory, tools |
| LangGraph | state machines, nodes, checkpointing |
| CrewAI | crewai-course-materials repo |
| MCP | mcp-learning-guide repo |
| OpenAI Assistants API | tool use and file workflows |
| Multi-Agent Systems | handoffs, supervisor patterns |
| Evaluation and Safety | guardrails and loop prevention |

---

## 16. MLOps and Tools Course

URL: `/courses/mlops.html`

Topic tabs:

| Tab | Source / notes |
|---|---|
| Airflow Orchestration | AIML-Engineering-Lab 053 patterns |
| Spark and Big Data | spark-learning-guide |
| Experiment Tracking | MLflow concepts from advanced notebooks |
| Kubernetes for ML | production deployment overview |
| AWS SageMaker | future content, not PRD-only repo |
| Docker for ML | new content |
| CI/CD for Models | new content |

---

## 17. Reinforcement Learning Course

URL: `/courses/rl.html`

Topic tabs:

| Tab | Content |
|---|---|
| What is RL | agent, environment, reward |
| Q-Learning | tabular RL basics |
| Deep Q Networks | replay and approximation |
| Policy Gradients | REINFORCE and actor-critic |
| PPO | modern practical RL overview |
| Real-world RL | recommendation and optimization examples |

This track is planned later. There is currently no real repo content in Rajendar-Muddasani for RL.

---

## 18. Cheatsheets Plan

All launch cheatsheets are openly accessible.

Format:
- A4 PDF
- 1 to 2 pages for most sheets
- dark theme matching the site

Hosting:
- S3 path `cheatsheets/<slug>.pdf`

Cheatsheets list:

| Cheatsheet | Content |
|---|---|
| Python Basics | data types, loops, functions, common patterns |
| Python for Data | Pandas, NumPy, Matplotlib top operations |
| SQL Quick Reference | SELECT, JOIN, GROUP BY, windows |
| Shell / Bash | commands, pipes, variables, scripts |
| Excel Formula Bible | high-value formulas and examples |
| C/C++ Memory Cheatsheet | pointers, structs, allocation |
| ML Models at a Glance | model choice, metrics, watch-outs |
| Deep Learning Layers | dense, conv, recurrent, attention |
| GenAI Prompt Patterns | zero-shot, CoT, RAG, tool use |
| AI for Developers Prompts | refactor, test, document, explain |
| AIML Interview Prep | ML, DL, GenAI interview Q and A |

Generation plan:
- Phase 1: design in Canva and export PDF
- Phase 2: generate PDFs from Markdown using `reportlab`
- keep Markdown source in GitHub
- keep generated PDFs in S3 only

---

## 19. Projects Catalog

### 19.1 Catalog lanes

| Lane | Target learner | Goal | Typical duration |
|---|---|---|---|
| Guided Mini Projects | second and third year students | build a scoped working project quickly | 2 to 4 weeks |
| Major Project Kits | third and fourth year students | thesis-ready final-year submission | 8 to 16 weeks |
| Portfolio Builds | final-year students and freshers | company-ready demo plus GitHub proof | 4 to 8 weeks |
| Viva and Submission Packs | final-year students | report, PPT, demo script, viva defense | support layer |

### 19.2 What every serious project kit includes

- problem statement and scope boundaries
- architecture diagram
- milestone-wise implementation plan
- starter code plus final code path
- README and setup guide
- deployment guide
- report template
- PPT / seminar deck template
- viva questions and answers
- testing checklist and known limitations
- extension ideas

### 19.3 First six projects to build

| ID | Project name | Outcome |
|---|---|---|
| project-01 | Document Q&A Assistant | RAG system with admin upload flow |
| project-02 | AI Resume Screener and Interview Copilot | placement-focused portfolio build |
| project-03 | Inventory Forecasting Dashboard | forecasting plus dashboard plus report |
| project-04 | Multilingual Customer Support Assistant | deployable chatbot with escalation path |
| project-05 | AI Attendance and Analytics Dashboard | reporting-oriented dashboard |
| project-06 | Vision-Based Quality Inspection Demo | company-style computer vision project |

### 19.4 Product rule

If a project cannot strengthen at least one of these outcomes, it should not be the lead offer:
- final-year project submission
- viva explanation
- internship interviews
- fresher AI or software roles

---

## 20. Project 01 — Build First

Project: **Document Q&A Assistant**

Story frame:
- final-year student Arjun needs a real project and a strong explanation path

What the learner builds:
- a web app that answers questions from uploaded documents

Tech shape:
- Python
- FastAPI or Streamlit depending launch choice
- vector store
- OpenAI API

Page requirements:
- project hero
- what you build
- prerequisites
- architecture diagram
- milestone breakdown
- code snippets
- deployment notes
- common viva questions
- quiz
- completion record

---

## 21. Repo-to-Course Mapping

### 21.1 AIML-Engineering-Lab public repos

These are the main source repos for ML, DL, GenAI, and MLOps topics.

| Course area | Repos |
|---|---|
| Machine Learning | 001 to 010 |
| Deep Learning | 014, 015, 034, 054, 073 |
| Generative AI | 034, 074, 075 |
| MLOps / production examples | 053, 054, 070s |

### 21.2 Rajendar-Muddasani private repos with real content

| Repo | File count | Use in site |
|---|---:|---|
| langchain-learning-guide | 23 | GenAI course reference material |
| mcp-learning-guide | 20 | Agentic AI and MCP course |
| crewai-course-materials | 16 | Agentic AI course |
| pydantic-learning-guide | 19 | Programming track support material |
| chromadb-rag-tutorials | 7 | GenAI RAG section |
| spark-learning-guide | 12 | MLOps course |
| pytorch-semiconductor-guide | 10 | Deep Learning support material |
| tensorflow-semiconductor-guide | 8 | Deep Learning support material |
| stable-diffusion-media-generator | 12 | future GenAI image generation unit |
| research-papers-analysis | 7 | optional blog/reference material |
| docs | 16 | internal reference only |
| aiml-complete-guide | 1 | optional extraction source |

Deleted PRD-only repos should not be referenced anymore.

---

## 22. Content Model

Each project page should be manifest-driven.

Recommended YAML shape:

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
  hero_image: https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/projects/project-01/hero.jpg
  poster_image: https://...
  overview_video: https://...
seo:
  title: Document Q&A Assistant — Final Year AI Project
  description: Build a document chatbot with code, deployment notes, report support, and viva preparation.
```

Recommended course metadata shape:

```yaml
course_id: ml
title: Machine Learning
layout: onenote-tabs
topics:
  - slug: linear-regression
    title: Linear Regression
    source_repo: 001_linear_regression_engine
    cheatsheet: ml-models-at-a-glance
```

---

## 23. Repo Skeleton for the New Workspace

```text
mitra-ai-projects/
  README.md
  .gitignore
  .env.example
  CNAME
  site/
    index.html
    courses/
      index.html
      programming.html
      ml.html
      dl.html
      genai.html
      agentic.html
      mlops.html
      rl.html
    projects/
      index.html
      project-template.html
      document-qa-assistant.html
      resume-screener.html
      multilingual-support-bot.html
    cheatsheets.html
    how-it-works.html
    faq.html
    about.html
    contact.html
    privacy.html
    terms.html
    assets/
      css/
      js/
      icons/
    auth.js
    mitra-chat.js
  data/
    projects/
      project-01.yaml
      project-02.yaml
      project-03.yaml
    courses/
      ml.yaml
      dl.yaml
      genai.yaml
      agentic.yaml
      programming.yaml
    featured-projects.json
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
    cheatsheets/
      python-basics.md
      python-for-data.md
      sql-quick-reference.md
      shell-bash.md
  scripts/
    build_project_pages.py
    build_catalog.py
    build_course_pages.py
    generate_project_hero_images.py
    generate_project_overview_video.py
    generate_cheatsheets.py
    upload_project_assets.py
    validate_project_manifests.py
    deploy_s3.py
    cloudflare-worker/
      mitra-projects-worker.js
  prompts/
    project-page.prompt.md
    project-video.prompt.md
    project-image.prompt.md
    cheatsheet.prompt.md
  docs/
    mitraaiprojects-master-plan.md
    content-production-workflow.md
    launch-checklist.md
```

---

## 24. Scripts to Reuse from mitraailife.com

Copy and adapt these:
- `scripts/deploy_s3.py`
- `site/auth.js`
- `site/mitra-chat.js`
- `scripts/cloudflare-worker/mitra-chat-worker.js`

Adaptations needed:
- use `project_id` and `course_id`
- change S3 prefix to `projects/` and `cheatsheets/`
- change worker system prompt to project/course context

---

## 25. Tech Stack Recommendation

### v1
- static site in plain HTML, CSS, and small JavaScript
- Python build scripts for repeatable page generation
- S3 for assets
- GitHub Pages for hosting
- Supabase for auth and completion records
- GA4 for analytics

### v2 only if needed later
- Vite or Next.js
- protected assets and dashboards
- deeper automation layers

Do not introduce framework complexity in the first build unless a specific need appears.

---

## 26. Content Production Workflow

English is the source of truth.

For each project:
1. define learner outcome
2. define scope boundary
3. write English master brief
4. create module outline
5. create code milestones
6. create deliverables list
7. create FAQ and objections
8. generate public page copy
9. generate hero image and poster
10. generate overview video
11. human review for technical accuracy and promise clarity
12. publish

For each course page:
1. define topic list
2. define plain-English explanation per topic
3. link source repos / notebooks
4. write cheatsheet notes
5. build quiz
6. connect project ideas
7. publish

---

## 27. Video Workflow

Recommended launch video types:
- 60 to 90 second site overview video
- 60 to 120 second project overview video per project
- optional module preview videos later

Video recipe:
1. read project manifest
2. generate narration script
3. generate scene prompts
4. create visuals or code composites
5. create TTS draft narration
6. assemble with MoviePy or ffmpeg
7. add captions
8. export poster frame
9. upload to S3
10. write asset URLs back into manifests

Recommended outputs:
- `overview-en.mp4`
- `overview-en-poster.jpg`
- `overview-en.vtt`
- `hero-16x9.jpg`
- `thumb-1x1.jpg`

---

## 28. Image and Asset Workflow

Images to produce per project:
- hero image
- catalog card image
- overview poster
- architecture diagram
- milestone graphic
- social share image

S3 structure:

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
cheatsheets/
  python-basics.pdf
  sql-quick-reference.pdf
```

---

## 29. Contact Flow

Launch with a simple manual-first contact model.

Use cases:
- contact about a project
- ask which course or project lane fits me
- request roadmap or syllabus guidance

Recommended fields:
- name
- email
- college or company
- interest area
- message

No checkout flow in v1.

---

## 30. SEO and Analytics

Priority pages:
- home
- courses index
- programming page
- ML page
- top 3 project pages
- cheatsheets page

Analytics events to track:
- home CTA click
- course page view
- course tab change
- project page view
- cheatsheet download click
- quiz attempt
- certificate claimed
- contact form submission
- video start and 50% completion

SEO rules:
- every project page must target a real learner search intent
- descriptions should mention actual outcomes and deliverables
- use FAQ and breadcrumb schema where helpful
- link related courses to related projects

---

## 31. Legal and Ethical Rules

- add Privacy Policy
- add Terms of Service
- state that projects are learning exercises and real production use needs more review
- do not claim guaranteed job placement
- do not claim guaranteed marks
- do not position the site as unethical submission help
- guided build support, explanation, templates, and mentoring-style guidance are allowed
- all AI-generated images should be declared in the footer or credits area

---

## 32. Certificate Rules

Allowed:
- completion certificates for your own courses and projects
- unique certificate IDs verified on your site
- clear wording that this is a platform-issued completion record

Not allowed:
- degree or diploma claims
- accredited certification claims
- implying government or university recognition without basis

Recommended wording:

> This certificate confirms that [Name] completed the [Course Name] on mitraaiprojects.com on [Date]. This is a course completion record issued by Mitra AI Life, an independent education platform.

---

## 33. Build Sequence for the First Development Session

1. create repo skeleton and shared CSS system
2. build `site/index.html`
3. build `site/courses/index.html`
4. build `site/courses/programming.html`
5. build `site/cheatsheets.html`
6. build `site/courses/ml.html` with OneNote-style tab layout
7. build `site/projects/index.html`
8. build `site/projects/document-qa-assistant.html`
9. wire analytics, auth, contact form, and chat widget
10. push to GitHub Pages

If time remains in the first session:
11. build `genai.html`
12. build `dl.html`
13. build `agentic.html`

---

## 34. Exact New-Workspace Setup Steps

From your Mac terminal:

```bash
cd /Users/rajendarmuddasani
mkdir mitra-ai-projects
cd mitra-ai-projects
git init
git remote add origin git@github.com:Rajendar-Muddasani/mitra-ai-projects.git
mkdir -p docs
```

Then copy only this file into the new repo:

```bash
cp /Users/rajendarmuddasani/Mitra_AI_Life/docs/mitraaiprojects-master-plan.md docs/
```

Then create the environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install openai boto3 moviepy imageio-ffmpeg pillow python-dotenv pyyaml reportlab
```

Then start Claude Code:

```bash
claude
```

Choose login option 1: Claude account with subscription.

---

## 35. First Prompt to Give Claude Code

Use this prompt in the new workspace:

```text
Read docs/mitraaiprojects-master-plan.md fully. This file is the single source of truth and replaces any older PRD. Build the full production-ready static website for mitraaiprojects.com in this repo using plain HTML, CSS, small JavaScript, and Python helper scripts where needed.

Requirements:
- create all planned pages from the master plan
- implement the dark teal design system
- build the Courses index page
- build Programming and ML pages first
- implement the ML OneNote-style two-panel tab layout
- build the Cheatsheets page
- build the Projects catalog and the first project page: Document Q&A Assistant
- add reusable CSS, JS, manifests, and simple build scripts
- keep everything mobile-friendly
- do not add commerce, pricing, or payment flows
- wire in GA4 placeholders, auth.js integration points, and contact form structure
- make the site ready to deploy on GitHub Pages

Before writing code, summarize the plan briefly. Then build the site completely.
```

---

## 36. Copilot / Claude Code Working Rules

When an AI coding agent works in the new repo:
- always treat this master plan as the single source of truth
- do not recreate or split planning into multiple conflicting files
- do not add pricing, fees, checkout, or payment pages
- do not create new cloud accounts
- do not commit `.env`, generated assets, videos, audio, or PDFs
- use S3 for generated assets
- keep GitHub for source files only
- finish English pages first
- preserve the dark teal visual system
- keep the first version static and simple

---

## 37. Acceptance Criteria

The first build is complete when:
- the site clearly reads as separate from beginner-family learning
- the home page, courses index, programming page, ML page, cheatsheets page, projects catalog, and one project page all exist
- the ML page has a true left-tab plus right-content notebook-style layout
- at least one project page is fully structured from manifest-style content
- the site is mobile-friendly
- analytics hooks exist
- contact form structure exists
- the repo can be pushed directly to GitHub Pages and render correctly

---

## 38. Final Rule

For the new workspace, carry only this file:

- `docs/mitraaiprojects-master-plan.md`

Do not carry the older separate PRD.

This file already includes:
- the full product decision
- site map
- design system
- Programming plan
- ML OneNote-style tab UX
- DL plan
- GenAI plan
- Agentic AI and MCP plan
- MLOps plan
- RL plan
- cheatsheets plan
- projects plan
- repo-to-course mapping
- workflows
- hosting and infrastructure
- new-workspace startup steps
- the first Claude Code prompt

---

*Last updated: 04 Jun 2026. This file replaces the older separate PRD and is the only planning document needed for the new mitra-ai-projects workspace.*
