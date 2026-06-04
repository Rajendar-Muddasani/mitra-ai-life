# mitraaiprojects.com — Complete Master Plan

> **Purpose of this document:** Drop this file into a new VS Code workspace for mitraaiprojects.com. GitHub Copilot (or Claude Code / Cursor) will read it and know everything — product vision, infrastructure, design system, course structure, and exact build steps. No re-engineering. No asking for details already solved in mitraailife.com.

---

## 1. What Is This Platform

**mitraaiprojects.com** is the engineering education track under the Mitra AI family.

| Property | Value |
|---|---|
| Target audience | Engineering students (B.E., B.Tech, BCA, MCA, diploma), final year projects, freshers |
| Core promise | Build real AI projects with code, explanation, deployment guidance, and a clear path from idea to demo |
| Language | English first; Telugu subtitles on videos eventually |
| Status | Not yet built. Domain registered. Planning phase. |

**Relationship to mitraailife.com:**
- Same founder, same company, same AWS / GA4 / Supabase accounts
- Shared infrastructure — do NOT create separate cloud accounts
- Different GitHub repo, different domain, different color theme
- Content is technical (code, APIs, deployment) vs. mitraailife.com which is non-technical (daily life usage)

---

## 2. Who This Is For

Primary users:
- B.Tech, BCA, MCA, diploma, and engineering students in India
- Final-year students who need a serious build, explanation path, and viva confidence
- Freshers who need portfolio projects for placements
- Third-year students who want guided mini-projects before final year

Secondary users:
- College teams building group projects
- Faculty or project mentors reviewing project outcomes
- Learners outside India who can use the same English-first technical content

Not for:
- School students (they belong on mitraailife.com)
- Casual AI learners (also mitraailife.com)
- Users asking for unethical academic cheating or fake submissions

---

## 3. Core Promise and Business Position

Plain-language promise:

**Build real AI projects with code, explanation, deployment guidance, viva prep, and a clear path from idea to demo.**

What problem it solves:
- Many students can copy code but cannot explain it
- Many project sellers offer weak quality or unethical shortcuts
- Students need a structured path: build, understand, present, and prove

This is not just a course. This is not just a code dump. Each project kit is a guided build system with teaching, code, reports, demo assets, and explanation support.

| Item | Decision |
|---|---|
| Business lane | Engineering project education and technical skill building |
| Launch language | English only at launch |
| Telugu plan | Later for subtitles, support docs, and select landing assets |
| Brand relationship | Part of the Mitra family, but operationally separate public site |
| Risk posture | No fake guarantees, no done-for-you cheating claims |

---

## 4. Product Goals

Launch goals:
- Make the site credible enough that a student understands the offer in under 90 seconds
- Show clear lanes: courses, mini projects, major projects, portfolio builds, viva packs
- Make each project page conversion-ready with strong clarity, not hype
- Create a reusable production system for project pages, videos, posters, and support docs
- Keep the codebase easy for a single founder plus Copilot / Claude Code workflow

Success metrics for first release:
- At least 1 polished home page
- At least 1 polished course track page (Programming or ML)
- At least 3 strong public project pages
- 1 working contact / enquiry flow
- 1 repeatable project-page generation system

---

## 5. Shared Infrastructure — USE EXACTLY THESE, DO NOT REINVENT

### AWS S3
```
Bucket:     mitra-ai-life-assets
Region:     us-west-2
CDN base:   https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/
```
- Create a subfolder: `projects/` for mitraaiprojects.com assets
- Access keys are in `.env` of mitraailife.com workspace:
  - `AWS_ACCESS_KEY_ID=AKIA2OLSTCW7NXHUAOPQ`
  - `AWS_SECRET_ACCESS_KEY=<in .env>`
  - `AWS_DEFAULT_REGION=us-west-2`
- Upload with: `source .env && aws s3 cp <file> s3://mitra-ai-life-assets/projects/...`

### Google Analytics
```
GA4 Measurement ID: G-QGY0LH6W93
```
- Add the same GA4 snippet to every mitraaiprojects.com page
- Same property — track both sites in one dashboard

### Disqus
```
Shortname: mitra-ai-life
```
- Use the same Disqus shortname on project pages
- Set `page.identifier` = `project-<slug>` (e.g., `project-chatbot-python`)

### Supabase (auth + progress)
```
URL:       https://kuriwaysdlqnzqqzabts.supabase.co
Anon key:  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1cml3YXlzZGxxbnpxcXphYnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwNTE5NzYsImV4cCI6MjA5MzYyNzk3Nn0.UA2AgEmnA6r_evrAyXz0MTVhohziKdspkjuB6wHD6fw
```
- Same `user_progress` table — add a `project_id` column or use a new table `project_completions`
- Row Level Security is already configured — just add the anon key

### Cloudflare Worker (chatbot proxy)
```
Worker URL:  https://mitra-chat-worker.rajendar-mi46.workers.dev
```
- Reuse the same worker OR create a second worker: `mitra-projects-worker`
- If creating a new worker, copy `scripts/cloudflare-worker/mitra-chat-worker.js` from the mitraailife.com repo and update the SYSTEM_PROMPT for projects context
- OPENAI_API_KEY is already set as a Secret in Cloudflare dashboard

### OpenAI
```
API key:  in .env as OPENAI_API_KEY (also set as Secret in Cloudflare)
Models used:
  - gpt-4o-mini  →  chatbot
  - tts-1        →  narration videos (voice: nova)
  - dall-e-3     →  scene images (quality="standard", style="vivid")
```

### Python Environment
```
Python 3.14
Virtualenv at: .venv/  (create new .venv in mitraaiprojects.com workspace)
Key packages: openai, boto3, moviepy, imageio-ffmpeg, pillow, python-dotenv
Install:  python -m venv .venv && .venv/bin/pip install openai boto3 moviepy imageio-ffmpeg pillow
```

### .env File Template (create in mitraaiprojects.com workspace root, never commit)
```
GITHUB_TOKEN=<same token>
OPENAI_API_KEY=<same key>
AWS_ACCESS_KEY_ID=AKIA2OLSTCW7NXHUAOPQ
AWS_SECRET_ACCESS_KEY=<same secret>
AWS_DEFAULT_REGION=us-west-2
```

---

## 6. Domain & Hosting

| Item | Value |
|---|---|
| Domain | mitraaiprojects.com |
| Hosting | GitHub Pages (same as mitraailife.com) |
| GitHub org | Rajendar-Muddasani |
| Repo to create | `mitra-ai-projects` (new separate repo under Rajendar-Muddasani org) |
| Branch | `main` |
| Pages settings | Source: Deploy from branch `main`, folder `/` or `/site/` |
| Custom domain | Set `mitraaiprojects.com` in repo Settings → Pages → Custom domain |
| HTTPS | Enforce HTTPS in Pages settings |

### How to set up the new GitHub repo
```bash
# In a NEW folder (not mitraailife.com):
mkdir ~/mitra-ai-projects && cd ~/mitra-ai-projects
git init
# create repo first on github.com: Rajendar-Muddasani/mitra-ai-projects
git remote add origin git@github.com:Rajendar-Muddasani/mitra-ai-projects.git
```

---

## 7. Design System

### Color Theme — Professional Dark (2 main colors + 1 accent)

Inspired by GitHub Dark + terminal aesthetic. Clean, focused, no distraction.

```css
/* 2 main colors + 1 accent — never add more */
--primary:    #00d4aa;   /* teal/cyan — THE engineering color, CTAs, highlights */
--bg-dark:    #0d1117;   /* GitHub-style near-black — page background */
--surface:    #161b22;   /* slightly lighter — card/section backgrounds */

/* 1 accent only */
--accent:     #f0b429;   /* warm amber — badges and callouts only */

/* Supporting (neutral, not brand colors) */
--text:       #e6edf3;
--muted:      #7d8590;
--border:     rgba(0,212,170,0.12);
--border-dim: rgba(255,255,255,0.06);

/* Shared Mitra purple — used sparingly, e.g. completion certificates only */
--purple:     #7c3aed;
```

**Color discipline rules:**
- `--primary` (teal): buttons, links, active states, code highlights, progress bars
- `--accent` (amber): warning callouts, "new" badges only — not for pricing
- `--purple`: certificates and brand footer only
- All other UI is black/white/gray — no reds, no greens, no blues
- Code blocks: dark background `#0d1117`, teal syntax highlights

**Hero gradient:**
```css
background: linear-gradient(160deg, #0d1117 0%, #0d2818 50%, #0a2520 100%);
```

**Visual motifs:** Terminal window chrome `>_`, circuit lines, clean monospace code snippets, minimal iconography (▶ Play, ✓ Done, ⚡ Fast).

### Fonts
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Baloo+2:wght@700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet" />
```
- `JetBrains Mono` → code blocks, technical labels
- `Baloo 2` → headings (shared brand font)
- `Nunito` → body text (shared brand font)

### Component patterns (copy from mitraailife.com and restyle):
- Progress bar (top, scrolling)
- Top nav with brand + page label + auth area
- Hero section (dark background, teal accent)
- Card grid for project modules / course tracks
- Code block sections (with syntax highlighting via Prism.js)
- Quiz (same format, different styling)
- Certificate / completion (same Supabase saveProgress pattern)
- Disqus (same embed pattern)

### Auth
- Copy `site/auth.js` from mitraailife.com, update `LEVEL_IDS` → `PROJECT_IDS`
- Google OAuth via Supabase (same config)
- Progress tracking pattern is identical

---

## 8. Site Map

```
Home  |  Courses  |  Projects  |  Cheatsheets  |  Contact
```

Full URL structure:
```
/                            Home
/courses/                    Course track index
/courses/programming.html    Programming track (tabbed)
/courses/ml.html             Machine Learning (OneNote UX)
/courses/dl.html             Deep Learning
/courses/genai.html          Generative AI
/courses/agentic.html        Agentic AI & MCP
/courses/mlops.html          MLOps & Tools
/courses/rl.html             Reinforcement Learning
/projects/                   Project kit catalog
/projects/<slug>.html        Individual project detail pages
/cheatsheets.html            Downloadable PDF cheatsheets
/how-it-works.html           Simple step flow explainer
/faq.html                    FAQ
/contact.html                Contact / enquiry form
/about.html                  About Mitra AI
/privacy.html                Privacy Policy
/terms.html                  Terms of Service
```

Optional later:
- `/compare/` project comparisons
- `/stories/` learner case studies
- `/blog/` technical explainers and SEO articles

---

## 9. Course Tracks

### 9.1 Track Overview

| Track | Audience | Content source | Status |
|---|---|---|---|
| **Programming** | Complete beginners → intermediate developers | New content | Build first |
| **Machine Learning** | Engineering students, analysts | AIML-Engineering-Lab notebooks 001–010 | Content ready |
| **Deep Learning** | ML practitioners | AIML-Engineering-Lab notebooks 011–020 | Content ready |
| **Reinforcement Learning** | Advanced DL learners | New — build fresh | Planned |
| **Generative AI** | Anyone building with LLMs | AIML-Engineering-Lab notebooks 034, 074, 075 | Partial |
| **Agentic AI & MCP** | Developers building agents | New — LangGraph, CrewAI, MCP repos | Partial |
| **MLOps & Tools** | Practitioners going production | AIML-Engineering-Lab notebooks 050s | Partial |

---

### 9.2 Programming Track

URL: `mitraaiprojects.com/courses/programming`

Serves all skill levels through a single tabbed page. Separate from mitraailife.com students page (which stays beginner-only / AI prompts to learn code). The actual code + notebook experience belongs here.

**Tab structure:**

| Tab | Audience | Content |
|---|---|---|
| Python Basics | Complete beginners | Variables, loops, functions, files. AI-assisted learning prompts. |
| Python for Data | Students & analysts | Pandas, NumPy, Matplotlib. Exercises with AI explanations. |
| Shell / Bash | Developers | 20 essential commands, scripting basics, cron, pipes |
| SQL | Everyone | SELECT, JOINs, GROUP BY, window functions. AI query explainer. |
| Excel Formulas | Office workers | VLOOKUP, XLOOKUP, pivot tables, IF/COUNTIF. AI formula generator prompts. |
| C / C++ | Engineering students | Pointers, memory, structs. Side-by-side with Python comparisons. |
| Perl | Legacy engineers | Regex, file processing, CPAN basics |
| JavaScript | Web developers | DOM, fetch, async/await, basic Node.js |

**For each language tab:**
1. One-page reference card (what is it, when to use it)
2. 10 essential prompts to learn it with AI
3. Interactive notebook embed (Pyodide for Python; static code blocks for others)
4. Downloadable cheatsheet PDF
5. 5-question quiz
6. Completion certificate

---

### 9.3 Machine Learning Course — OneNote-Style Page UX

URL: `mitraaiprojects.com/courses/ml`

**Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│  nav bar                                                         │
├──────────────┬──────────────────────────────────────────────────┤
│ LEFT TABS    │  CONTENT AREA (scrollable)                       │
│              │                                                   │
│ ▶ Linear Reg │  ## Linear Regression                            │
│   Classif.   │  What it is · When to use · Key assumptions      │
│   Trees      │  ┌────────────────────────────────────────────┐  │
│   Boosting   │  │  EXECUTABLE NOTEBOOK (Pyodide / Colab)     │  │
│   SVM        │  │  [ Run ▶ ]  code cell + output inline      │  │
│   Clustering │  └────────────────────────────────────────────┘  │
│   Anomaly    │  Metrics: MSE · RMSE · R² · MAE                 │
│   NB / LDA   │  Gotchas: multicollinearity, outliers, scale    │
│   Time Series│  Project idea: House price predictor            │
│   Hyper Opt  │  [Quiz] [Cheatsheet ↓] [← Prev] [Next →]       │
└──────────────┴──────────────────────────────────────────────────┘
```

**Each topic tab contains:**
1. **What is it** — 3-sentence plain English explanation
2. **When to use it** — decision table (use this when..., don't use when...)
3. **Key algorithms / variants** — with source notebook link (AIML-Engineering-Lab)
4. **Metrics** — table: metric name, formula, what it means, good value range
5. **Executable notebook** — Pyodide (Python in browser) OR embedded Colab link
6. **Watch-outs** — common mistakes, data prep requirements
7. **Project idea** — 1 concrete project that connects to the Projects lane
8. **5-question quiz**
9. **Cheatsheet download button**

**Content source mapping — AIML-Engineering-Lab → ML course tabs:**

| Tab | Source repo(s) |
|---|---|
| Linear Regression | 001_linear_regression_engine |
| Classification | 002_classification_engine |
| Tree-Based Learning | 003_tree_based_learning |
| Boosting (XGBoost/LGB/Cat) | 004_boosting_revolution |
| SVM | 005_support_vector_machines |
| Clustering / Unsupervised | 006_unsupervised_discovery |
| Anomaly Detection | 007_anomaly_detection_dimensionality |
| Naive Bayes / LDA | 008_naive_bayes_lda |
| Time Series | 009_time_series_forecasting |
| Hyperparameter Optimization | 010_hyperparameter_optimization |

---

### 9.4 Deep Learning Course

URL: `mitraaiprojects.com/courses/dl`

| Tab | Source / Notes |
|---|---|
| Neural Network Basics | New — perceptron, activation, backprop |
| CNNs | 054_wafer_defect_yolo_detection_mlops (YOLOv8 level) |
| RNNs / LSTMs | 015_time_series_deep_learning |
| Autoencoders & GANs | 014_autoencoders_and_gans |
| Transformers | 073_dtfs_transformer_system |
| Multimodal (Vision+Language) | 034_multimodal_vision_language |
| Transfer Learning | New |
| Model Compression | New |

Same OneNote-style tab UX as ML course.

---

### 9.5 Generative AI Course

URL: `mitraaiprojects.com/courses/genai`

| Tab | Content / Source |
|---|---|
| What is GenAI | LLMs, diffusion, multimodal — plain English |
| Prompt Engineering | Zero-shot, few-shot, CoT, system prompts |
| RAG | 074_postsilicon_validation_rag + chromadb-rag-tutorials |
| Fine-Tuning | 075_domain_llm_finetuning |
| Embeddings & Vector DBs | Chroma, Pinecone, Supabase pgvector |
| LLM Evaluation | BLEU, ROUGE, LLM-as-judge |
| HuggingFace Ecosystem | Transformers, Datasets, Spaces — hands-on |
| Kaggle with LLMs | Competition strategy + submission workflow |

---

### 9.6 Agentic AI & MCP Course

URL: `mitraaiprojects.com/courses/agentic`

| Tab | Content / Source |
|---|---|
| What is an Agent | ReAct, tool use, memory, planning |
| LangGraph | State machines, nodes, edges, checkpointing |
| CrewAI | Roles, tasks, crew orchestration — crewai-course-materials repo |
| MCP (Model Context Protocol) | What it is, building MCP servers, tool registration — mcp-learning-guide repo |
| OpenAI Assistants API | Function calling, code interpreter, file search |
| Multi-Agent Systems | Supervisor pattern, handoffs, state sharing |
| Evaluation & Safety | Agent evals, guardrails, looping prevention |

---

### 9.7 MLOps & Tools Course

URL: `mitraaiprojects.com/courses/mlops`

| Tab | Content / Source |
|---|---|
| Airflow Orchestration | AIML-Engineering-Lab 053 (Airflow/Kafka/Spark/MLflow) |
| Spark & Big Data | spark-learning-guide repo |
| MLflow & Experiment Tracking | From 053 MLOps notebooks |
| Kubernetes Basics for ML | From 053/054 production examples |
| AWS SageMaker | aws-sagemaker-ml-deployment repo content |
| Docker for ML | New |
| CI/CD for Models | New |

---

### 9.8 Reinforcement Learning Course

URL: `mitraaiprojects.com/courses/rl`

| Tab | Content |
|---|---|
| What is RL | Agents, environments, rewards — plain English |
| Q-Learning | Tabular RL, Bellman equation |
| Deep Q-Networks | DQN, experience replay |
| Policy Gradients | REINFORCE, Actor-Critic |
| PPO | Proximal Policy Optimization |
| Real-world RL | Recommendation systems, resource scheduling |

Content to build fresh. Low priority — build after ML, DL, GenAI.

---

## 10. Cheatsheets Plan

All cheatsheets are free at launch.

**Format:** A4 PDF, 1–2 pages per cheatsheet, dark theme matching site.
**Hosting:** S3 at `mitra-ai-life-assets/cheatsheets/<slug>.pdf`
**Download link:** Direct download, no gate. Sign-in optional to track completions.

| Cheatsheet | Content |
|---|---|
| Python Basics | Data types, loops, functions, common patterns — 1 page |
| Python for Data | Pandas/NumPy/Matplotlib top 30 operations — 2 pages |
| SQL Quick Reference | SELECT, JOIN, GROUP BY, window functions — 2 pages |
| Shell / Bash | 40 commands, pipes, variables, scripts — 2 pages |
| Excel Formula Bible | 25 formulas with syntax + example — 2 pages |
| C/C++ Memory Cheatsheet | Pointers, structs, malloc/free, RAII — 1 page |
| ML Models at a Glance | 12 models: when to use, metric, watch-out — 2 pages |
| Deep Learning Layers | Dense, Conv2D, LSTM, Attention — visual 2 pages |
| GenAI Prompt Patterns | 15 patterns: zero-shot, CoT, RAG, tool use — 2 pages |
| AI for Developers: 25 Prompts | Refactor, test, document, explain, generate — 4 pages |
| AIML Interview Prep | Top 50 ML/DL/GenAI interview Q+A — 6 pages |

**Generation plan:**
- Phase 1: Design in Canva → export PDF → upload to S3 → add download card to page
- Phase 2: Python script using `reportlab` generates PDFs from Markdown source → automated updates
- Source files live in `docs/cheatsheets/` as Markdown (in GitHub); generated PDFs go to S3 only

---

## 11. Project Kit Catalog

Organize by outcome, not by subject label.

### Catalog Lanes

| Lane | Target learner | Goal | Typical duration |
|---|---|---|---|
| Guided Mini Projects | 2nd/3rd year students | Build one working scoped project fast | 2 to 4 weeks |
| Major Project Kits | 3rd/4th year students | Thesis-ready final-year submission | 8 to 16 weeks |
| Portfolio Builds | Final-year students and freshers | Company-ready deployed demo + GitHub proof | 4 to 8 weeks |
| Viva and Submission Packs | Final-year students | Report, PPT, demo script, viva defense | Add-on |

### What every project kit includes

- Problem statement and scope boundaries
- Dataset or data-collection plan
- Architecture diagram
- Milestone-wise implementation plan
- Starter code plus final code path
- README and setup guide
- Deployment guide
- Project report template
- PPT / seminar deck template
- Viva questions and answers
- Testing checklist and known limitations
- Extension ideas for internship or startup version

### First six project kits to build

| ID | Project Name | Delivery goal |
|---|---|---|
| project-01 | Document Q&A Assistant | Thesis-ready RAG system + admin upload flow |
| project-02 | AI Resume Screener and Interview Copilot | Portfolio build + placement relevance |
| project-03 | Inventory Forecasting Dashboard | Thesis-ready forecasting + dashboard + report |
| project-04 | Multilingual Customer Support Assistant | Deployable chatbot + escalation workflow |
| project-05 | AI Attendance and Analytics Dashboard | College-friendly dashboard + reporting pack |
| project-06 | Vision-Based Quality Inspection Demo | Company-style CV project + deployment story |

### Project 01 content outline (build first)
- Story: Final year student Arjun needs a project. Builds a chatbot in a weekend.
- Prerequisites: Python basics, an OpenAI API key
- What you build: A Streamlit web app that answers questions about any uploaded document
- Code: ~100 lines of Python
- Deploy: Streamlit Cloud (free tier, no server needed)
- Image theme: Dark teal, code on screens, college campus India setting
- Characters: Arjun (final year, Hyderabad), Professor Rao (mentor)

### Product rule

This track should make a student stronger for:
- Final-year project submission
- Viva explanation
- Internship interviews
- Fresher AI or software roles

If a kit cannot support at least one of those four outcomes, it should not be the lead offer.

---

## 12. Content Model

Each project kit is manifest-driven.

**Recommended fields:**

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
  description: Build a RAG-based document chatbot with Python. Includes code, deployment guide, report template and viva prep.
```

---

## 13. Repo Skeleton

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
      excel-formulas.md
  scripts/
    build_project_pages.py
    build_catalog.py
    generate_project_hero_images.py
    generate_project_overview_video.py
    generate_cheatsheets.py
    upload_project_assets.py
    validate_project_manifests.py
    deploy_s3.py
  prompts/
    project-page.prompt.md
    project-video.prompt.md
    project-image.prompt.md
    viva-questions.prompt.md
  docs/
    mitraaiprojects-master-plan.md
    content-production-workflow.md
    launch-checklist.md
```

---

## 14. Tech Stack

### v1 — Static, lean, fast to build
- Plain HTML, CSS, and small JavaScript in `site/`
- Python build scripts for page generation and asset automation
- S3 for all media hosting (existing bucket and workflow)
- Formspree or simple HTML form for contact / enquiry leads
- Google Analytics for measurement
- Supabase for auth and progress (same as mitraailife.com)
- Disqus for comments (same shortname)

### v2 — When content volume justifies it
- Vite or Next.js if protected access becomes meaningful
- Supabase for gated assets and learner dashboards
- Proper order and delivery automation

---

## 15. Content Production Workflow

English is the source of truth.

For each project kit:
1. Define student outcome
2. Define project scope boundary
3. Write English master brief
4. Create module outline
5. Create code milestones
6. Create deliverable list
7. Create FAQ and objections
8. Generate public page copy
9. Generate hero image and poster
10. Generate overview video
11. Human review for technical accuracy and promise clarity
12. Publish

Source files to maintain in GitHub:
- Project manifest (YAML)
- English master script (Markdown)
- Visual prompt inputs
- Video narration script
- FAQ source
- Review checklist

Generated files go to S3 only — never commit to GitHub:
- Images
- Videos
- PDF cheatsheets

---

## 16. Video Generation Workflow

Use simple, repeatable production.

Recommended video types at launch:
- 60–90 second site overview video
- 60–120 second project overview video per kit
- Optional 3–6 minute module preview videos later

Video recipe:
1. Read project manifest
2. Generate narration script
3. Generate 5 to 8 scene prompts
4. Create still visuals or code-screen composites
5. Create TTS draft narration (OpenAI tts-1, voice: nova)
6. Assemble with MoviePy or ffmpeg
7. Add captions
8. Export poster frame
9. Upload to S3 under `projects/<slug>/videos/`
10. Write asset URLs back into manifest

Recommended file outputs per project:
- `overview-en.mp4`
- `overview-en-poster.jpg`
- `overview-en.vtt`
- `hero-16x9.jpg`
- `thumb-1x1.jpg`

---

## 17. Image and Asset Workflow

Images to produce per project:
- Hero image (16:9)
- Catalog card image (4:3)
- Overview video poster
- Architecture diagram
- Milestone graphic
- Social share image

S3 structure:
```
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

## 18. Contact and Enquiry Flow

v1 — enquiry first, no payment needed at launch:
- "Contact about this project" form on every project page
- "Which lane fits me?" general enquiry
- "Request syllabus / kit outline"

Form fields: name, email, college/company, project interest, message.
Submit to Formspree (or Supabase table) with GA4 event `enquiry_submitted`.

No payment integration at v1. Handle first enquiries manually to understand real demand.

---

## 19. SEO Plan

Priority pages:
- Home
- Courses index
- Top 3 project pages
- Cheatsheets page
- How it works

Rules:
- Every project page targets a real search intent
- Titles combine outcome + technology + audience
- Descriptions mention real deliverables
- Use schema: `Course`, `FAQPage`, `BreadcrumbList`
- Internal linking between related course tabs and project pages

Example search intents to target:
- AI chatbot project for final year students
- Resume screener Python project with deployment
- Document Q&A assistant final year project India
- Machine learning course with executable notebooks

---

## 20. Analytics Events to Track

- Home CTA click
- Course track page view
- Course tab change (which topic clicked)
- Project page view
- Contact form submission
- Cheatsheet download click
- Video start and 50% completion
- Quiz attempt and score
- Certificate claimed

---

## 21. Legal and Ethical Rules

- Add Privacy Policy page (copy/adapt from mitraailife.com)
- Add Terms of Service (code is for learning, not commercial resale)
- Add disclaimer: "Projects are learning exercises. Production use requires additional security review."
- Do not claim guaranteed job placement or guaranteed marks
- Do not position as done-for-you academic submission
- Guided build support, explanation, documentation, templates — all allowed
- All AI-generated images: declare AI-generated in page footer

---

## 22. Certification Rules

**Can you issue certifications as a non-registered organization? Yes, with caveats.**

| What you CAN do | What you CANNOT do |
|---|---|
| Issue "completion certificates" for your own courses | Call it a "degree", "diploma", or "accredited certification" |
| State: "Completed [Course Name] on mitraaiprojects.com" | Claim recognition by AICTE, UGC, or any government body |
| Add a unique certificate ID verified on your site | Imply it is equivalent to university credit |
| Use Supabase to record completion and display a shareable URL | Use words like "certified professional" in a misleading way |

**Recommended wording on every certificate:**
> "This certificate confirms that [Name] completed the [Course Name] on mitraaiprojects.com on [Date]. This is a course completion record issued by Mitra AI Life, an independent education platform."

Safe to do right now — no company registration needed. Many platforms (Coursera, Udemy) started this way. When registration matters: if employers start asking about the issuing body, register then.

---

## 23. Build Sequence — Recommended Order

| Priority | Item | Why first |
|---|---|---|
| 1 | Repo skeleton, shared CSS, base layout | Foundation — all pages depend on it |
| 2 | `site/index.html` — home page | Entry point with hero + two lanes + sign-in |
| 3 | `site/courses/programming.html` — Programming tabs | Widest audience, clearest demand |
| 4 | `site/cheatsheets.html` — free download cards | Quick win, shareable, drives sign-ups |
| 5 | `site/courses/ml.html` — ML OneNote-style page | Core technical course, content already exists in AIML-Engineering-Lab |
| 6 | Generate first 3 cheatsheets (Python Basics, SQL, Shell) as PDFs | Launch asset |
| 7 | `site/projects/index.html` + first project page | First project kit live |
| 8 | `site/courses/genai.html` — GenAI course | High interest |
| 9 | `site/courses/dl.html`, `agentic.html` | Complete the lineup |
| 10 | GitHub Pages deploy + CNAME + HTTPS | Public launch |

---

## 24. Copilot Build Prompts for New Workspace

### Prompt 1 — Repo Setup
"Create a production-ready static website repo for `mitraaiprojects.com` using the PRD in `docs/mitraaiprojects-master-plan.md`. Build the folder structure, shared CSS variables, reusable card patterns, and placeholder pages for Home, Courses index, Cheatsheets, How It Works, Contact, Privacy, and Terms. Keep the implementation manifest-driven and mobile-first."

### Prompt 2 — Home and Course Index
"Using the master plan, build the Home page and Courses index page for `mitraaiprojects.com`. The site should look technical, professional, and credible. Show clear course tracks, featured project lane cards, and strong enquiry CTAs. Dark teal theme as specified."

### Prompt 3 — ML Course OneNote Page
"Build `site/courses/ml.html` with a two-column OneNote-style layout: left sidebar with topic tabs (Linear Regression, Classification, Trees, Boosting, SVM, Clustering, Anomaly Detection, Naive Bayes, Time Series, Hyperparameter Optimization) and a scrollable content area. Each tab renders: What is it, When to use, Metrics table, Pyodide executable snippet, Watch-outs, Project idea, Quiz, Cheatsheet download button."

### Prompt 4 — Project Template System
"Create a reusable project-detail page template driven by project YAML data. Each project page must render: hero, outcomes, tech stack, milestones, deliverables, what support is included and not included, FAQ, and contact CTA sections from structured data."

### Prompt 5 — Asset Automation
"Create Python scripts to validate project manifests, generate overview narration scripts, assemble short overview videos using MoviePy, upload assets to S3 under `projects/` prefix, and write asset URLs back into the manifest."

---

## 25. Scripts to Copy from mitraailife.com

- `scripts/deploy_s3.py` → change S3 prefix to `projects/` and `cheatsheets/`
- `scripts/cloudflare-worker/mitra-chat-worker.js` → update SYSTEM_PROMPT for projects
- `site/auth.js` → change `LEVEL_IDS` to `PROJECT_IDS` and `COURSE_IDS`
- `site/mitra-chat.js` → works as-is (chatbot widget)

---

## 26. Acceptance Criteria — v1 Done When

- The site clearly reads as separate from beginner / family learning
- At least 3 projects can be published from manifests without manual HTML duplication
- At least 1 course track page is live with working tab navigation
- All cheatsheets downloadable directly without gate
- Videos, posters, and page assets follow a repeatable pipeline
- The public site is honest about what is included
- Contact form is working and sends enquiry notifications
- Technical and legal pages are in place

---

## 27. Copilot Working Rules for This Project

When Copilot (or Claude Code / Cursor) works in this workspace:
- Always use the shared infrastructure from Section 5 (never create new AWS / GA / Supabase accounts)
- Never commit `.env`, `content/assets/`, `*.mp4`, `*.mp3`, `*.pdf` to git
- Image generation: `quality="standard"`, `style="vivid"` (separate DALL-E 3 parameters)
- S3 upload prefix: `projects/` or `cheatsheets/` (not `scenes/` which is mitraailife.com)
- Color theme: dark teal (`#00d4aa`), not purple-first like mitraailife.com
- Repo: `Rajendar-Muddasani/mitra-ai-projects`
- Work one page at a time: finish EN → TE → next page
- Commit message format: `feat: <page or feature> — <what was done>`

---

## 28. Repo-to-Course Mapping (Rajendar-Muddasani org)

Content already in private repos under `Rajendar-Muddasani` that maps directly to course tracks:

| Repo | Files | Maps to |
|---|---|---|
| langchain-learning-guide | 23 files | GenAI course — LangChain tab |
| mcp-learning-guide | 20 files | Agentic AI course — MCP tab |
| crewai-course-materials | 16 files | Agentic AI course — CrewAI tab |
| pydantic-learning-guide | 19 files | Programming track — Python for Data tab |
| chromadb-rag-tutorials | 7 files | GenAI course — RAG tab |
| spark-learning-guide | 12 files | MLOps course — Spark & Big Data tab |
| pytorch-semiconductor-guide | 10 files | Deep Learning course — CNN / transfer learning tabs |
| tensorflow-semiconductor-guide | 8 files | Deep Learning course — Neural Network Basics tab |
| stable-diffusion-media-generator | 12 files | GenAI course — Image Generation (new tab) |
| research-papers-analysis | 7 files | Reference material — blog/stories section |
| docs | 16 files | Internal docs (PDFs/PPTs) — keep private |
| aiml-complete-guide | 1 notebook | Can be extracted into Programming track |

---

*Last updated: 04 Jun 2026 — Consolidated from mitraaiprojects-master-plan.md (original) + mitraaiprojects-separate-site-prd.md. All pricing removed — everything is free at launch.*
