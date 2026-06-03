# mitraaiprojects.com — Complete Master Plan

> **Purpose of this document:** Drop this file into a new VS Code workspace for mitraaiprojects.com. GitHub Copilot will read it and know everything — infrastructure, accounts, design patterns, and exactly what to build next. No re-engineering. No asking for details already solved in mitraailife.com.

---

## 1. What Is This Platform

**mitraaiprojects.com** is the premium engineering project track under the Mitra AI family.

| Property | Value |
|---|---|
| Target audience | Engineering / CS students (B.Tech, BCA, MCA, diploma), final year projects |
| Core promise | Complete AI-powered project kits with code, deployment guide, demo, and certificate |
| Language | English first; Telugu subtitles on videos eventually |
| Price | ₹2,000–₹5,000 per project kit (premium, no free tier by default) |
| Status | Not yet built. Domain registered. Planning only. |

**Relationship to mitraailife.com:**
- Same founder, same company, same AWS/GA4/Supabase accounts
- Shared infrastructure — do NOT create separate cloud accounts
- Different GitHub repo, different domain, different color theme
- Content is technical (code, APIs, deployment) vs. mitraailife.com which is non-technical (daily life usage)

---

## 2. Shared Infrastructure — USE EXACTLY THESE, DO NOT REINVENT

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

## 3. Domain & Hosting

| Item | Value |
|---|---|
| Domain | mitraaiprojects.com |
| Hosting | GitHub Pages (same as mitraailife.com) |
| GitHub org/user | rajendarmuddasani |
| Repo to create | `mitra-ai-projects` (new separate repo) |
| Branch | `main` |
| Pages settings | Source: Deploy from branch `main`, folder `/` (root) or `/site/`) |
| Custom domain | Set `mitraaiprojects.com` in repo Settings → Pages → Custom domain |
| HTTPS | Enforce HTTPS in Pages settings |

### How to set up the new GitHub repo
```bash
# In a NEW folder (not mitraailife.com):
mkdir mitra-ai-projects && cd mitra-ai-projects
git init
git remote add origin git@github.com:rajendarmuddasani/mitra-ai-projects.git
# Create the repo first on github.com then push
```

---

## 4. Design System

### Color Theme — Professional Dark (2 main colors + 1 accent)

Inspired by GitHub Dark + terminal aesthetic. Clean, focused, no distraction.

```css
/* 2 main colors + 1 accent — never add more */
--primary:    #00d4aa;   /* teal/cyan — THE engineering color, CTAs, highlights */
--bg-dark:    #0d1117;   /* GitHub-style near-black — page background */
--surface:    #161b22;   /* slightly lighter — card/section backgrounds */

/* 1 accent only */
--accent:     #f0b429;   /* warm amber — warnings, badges, pricing only */

/* Supporting (neutral, not brand colors) */
--text:       #e6edf3;   /* primary text */
--muted:      #7d8590;   /* secondary text */
--border:     rgba(0,212,170,0.12);
--border-dim: rgba(255,255,255,0.06);

/* Shared Mitra purple — used sparingly, e.g. completion certificates only */
--purple:     #7c3aed;
```

**Color discipline rules:**
- `--primary` (teal): buttons, links, active states, code highlights, progress bars
- `--accent` (amber): price tags, warning callouts, "new" badges only
- `--purple`: certificates and brand footer only — never as main page color
- All other UI is black/white/gray — no reds, no greens, no blues
- Code blocks: dark background `#0d1117`, teal syntax highlights

**Hero gradient:**
```css
background: linear-gradient(160deg, #0d1117 0%, #0d2818 50%, #0a2520 100%);
/* subtle teal tint — not bright, professional */
```

**Visual motifs:** Terminal window chrome `>_`, circuit lines, clean monospace code snippets shown as actual UI elements, minimal iconography (▶ Play, ✓ Done, ⚡ Fast).

### Fonts (same CDN, different selection)
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Baloo+2:wght@700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet" />
```
- `JetBrains Mono` → code blocks, technical labels
- `Baloo 2` → headings (shared brand font)
- `Nunito` → body text (shared brand font)

### Component patterns (copy from mitraailife.com and restyle):
- Progress bar (top, scrolling)
- Top nav with brand + level tag + auth area
- Hero section (dark background, teal accent)
- Card grid for project modules
- Code block sections (new — with syntax highlighting via Prism.js)
- Quiz (same format, different styling)
- Certificate / completion (same Supabase saveProgress pattern)
- Disqus (same embed pattern)

### Auth (copy `site/auth.js` from mitraailife.com, update LEVEL_IDS to PROJECT_IDS)
- Google OAuth via Supabase (same config)
- Progress tracking pattern is identical

---

## 5. Content Plan — Project Kits

Each "Project Kit" = one self-contained page covering:
1. What you'll build (visual demo)
2. Tools & prerequisites
3. Step-by-step comic-style walkthrough
4. Code snippets (copy-paste ready)
5. Deployment guide
6. Quiz (5 questions)
7. Certificate

### Planned Project Kits

| ID | Project Name | Tech Stack | Price | Status |
|---|---|---|---|---|
| project-01 | AI Chatbot with Python | Python, OpenAI API, Streamlit | ₹2,000 | Build next |
| project-02 | Resume Screener | Python, OpenAI, Pandas | ₹2,000 | Planned |
| project-03 | Image Caption Generator | Python, DALL-E / GPT-4o Vision | ₹2,500 | Planned |
| project-04 | Telugu Voice Assistant | Python, Whisper, TTS, Gradio | ₹3,000 | Planned |
| project-05 | AI Customer Support Bot | Node.js, OpenAI, Supabase | ₹3,000 | Planned |
| project-06 | Fake News Detector | Python, GPT-4o, Flask | ₹3,500 | Planned |
| project-07 | AI Data Analyst | Python, OpenAI, Pandas, Matplotlib | ₹3,500 | Planned |
| project-08 | Agriculture Disease Detector | Python, Vision API, Gradio | ₹4,000 | Planned |
| project-09 | Full Stack AI App | React + FastAPI + OpenAI + Supabase | ₹5,000 | Planned |
| project-10 | Capstone: Deploy on Cloud | Any of above + AWS deployment | ₹5,000 | Planned |

### Positioning update

Do not organize this track primarily by year or by subject labels like ML, DL, or GenAI.

Reason:
- the student track already covers most of the concept teaching in Class 11 and Class 12
- engineering students need outcomes, not another theory ladder
- the real buying moment is usually third-year mini-projects, final-year major projects, internship demos, and thesis submission support

Better organizing principle: organize by project outcome.

### Recommended catalog structure

| Lane | Target learner | Goal | Typical duration |
|---|---|---|---|
| Guided Mini Projects | 2nd/3rd year students | build one working scoped project fast | 2 to 4 weeks |
| Major Project Kits | 3rd/4th year students | thesis-ready final-year submission | 8 to 16 weeks |
| Portfolio Builds | final-year students and freshers | company-ready deployed demo + GitHub proof | 4 to 8 weeks |
| Viva and Submission Packs | final-year students | report, PPT, demo script, viva defense | add-on |

### What every serious project kit should include

- problem statement and scope boundaries
- dataset or data-collection plan
- architecture diagram
- milestone-wise implementation plan
- starter code plus final code path
- README and setup guide
- deployment guide
- project report template
- PPT / seminar deck template
- viva questions and answers
- testing checklist and known limitations
- extension ideas for internship or startup version

### Recommended first six kits for this track

| ID | Project Name | Delivery goal |
|---|---|---|
| project-01 | Document Q&A Assistant for Colleges or Offices | thesis-ready RAG system + admin upload flow |
| project-02 | AI Resume Screener and Interview Copilot | portfolio build + placement relevance |
| project-03 | Inventory Forecasting Dashboard for Local Business | thesis-ready forecasting + dashboard + report |
| project-04 | Multilingual Customer Support Assistant | deployable chatbot + escalation workflow |
| project-05 | AI Attendance and Analytics Dashboard | college-friendly dashboard + reporting pack |
| project-06 | Vision-Based Quality Inspection Demo | company-style CV project + deployment story |

### Product rule

This track should make a student stronger for:
- final-year project submission
- viva explanation
- internship interviews
- fresher AI or software roles

If a kit looks like a toy demo that cannot support at least one of those four outcomes, it should not be the lead offer.

### Project 01 content outline (build first):
- Story: Final year student Arjun needs a project. Builds a chatbot in a weekend.
- Prerequisites: Python basics, an OpenAI API key
- What you build: A Streamlit web app that answers questions about any topic
- Code: ~100 lines of Python
- Deploy: Streamlit Cloud (free tier, no server needed)
- Image theme: Dark teal, code on screens, college campus India setting
- Characters: Arjun (final year, Hyderabad), Professor Rao (mentor)

---

## 6. File & Folder Structure to Create

```
mitra-ai-projects/                  ← new GitHub repo root
├── .env                            ← never commit (same keys as mitraailife.com)
├── .gitignore
├── README.md
├── site/
│   ├── index.html                  ← home / project catalog
│   ├── index-te.html               ← Telugu home (later)
│   ├── auth.js                     ← copy + modify from mitraailife.com
│   ├── mitra-chat.js               ← copy from mitraailife.com
│   └── pitch-deck.html             ← (later)
├── content/
│   ├── assets/
│   │   └── scenes/                 ← project images (uploaded to S3 /projects/)
│   └── projects/
│       └── project-01-chatbot/
│           ├── project-01.html     ← English
│           └── project-01-te.html  ← Telugu (later)
├── scripts/
│   ├── generate_project01_images.py
│   ├── deploy_s3.py                ← copy from mitraailife.com scripts/
│   └── cloudflare-worker/
│       └── mitra-projects-worker.js
└── docs/
    └── mitraaiprojects-master-plan.md   ← this file
```

---

## 7. Scripts to Copy from mitraailife.com

Copy these scripts exactly, then modify as needed:
- `scripts/deploy_s3.py` → works as-is (just change S3 prefix to `projects/`)
- `scripts/cloudflare-worker/mitra-chat-worker.js` → update SYSTEM_PROMPT for projects
- `site/auth.js` → change `LEVEL_IDS` to `PROJECT_IDS`, change `level_id` column to `project_id`
- `site/mitra-chat.js` → works as-is (chatbot widget)

---

## 8. What To Build — Exact Next Steps (in order)

### Step 1: Create GitHub repo and folder structure
```bash
mkdir ~/mitra-ai-projects && cd ~/mitra-ai-projects
git init
# create repo on github.com: rajendarmuddasani/mitra-ai-projects
git remote add origin git@github.com:rajendarmuddasani/mitra-ai-projects.git
mkdir -p site content/assets/scenes content/projects/project-01-chatbot scripts/cloudflare-worker docs
touch .gitignore README.md
echo ".env\ncontent/assets/\n*.mp4\n*.mp3\n__pycache__/\n.venv/" > .gitignore
```

### Step 2: Set up Python environment
```bash
python -m venv .venv
.venv/bin/pip install openai boto3 moviepy imageio-ffmpeg pillow python-dotenv
```

### Step 3: Create .env file (never commit)
Copy the same values from mitraailife.com `.env`

### Step 4: Copy shared scripts from mitraailife.com
- `scripts/deploy_s3.py`
- `site/auth.js` (modify PROJECT_IDS)
- `site/mitra-chat.js`

### Step 5: Build site/index.html (project catalog home page)
- Dark theme (teal + purple)
- List all 10 planned projects
- Show Project 01 as available, rest as "coming soon"
- Auth widget (Google sign-in)
- Chatbot widget

### Step 6: Generate Project 01 images
- Create `scripts/generate_project01_images.py`
- 8–10 scenes: Arjun's problem → choosing tools → writing code → testing → deploying
- Upload to S3 under `projects/` prefix

### Step 7: Build project-01.html
- Same pattern as mitraailife.com level pages
- Dark teal theme
- Code blocks with Prism.js syntax highlighting
- Quiz, certificate, Disqus

### Step 8: Set up Cloudflare Worker for projects chatbot
- Copy mitra-chat-worker.js, update SYSTEM_PROMPT to mention project kits
- Deploy as `mitra-projects-worker` in Cloudflare dashboard
- Update mitra-chat.js Worker URL on project pages

### Step 9: GitHub Pages deploy
- Push to main branch
- Enable GitHub Pages in repo settings
- Add custom domain: mitraaiprojects.com

### Step 10: Link from mitraailife.com
- Update `site/index.html` footer/nav: "Engineering projects → mitraaiprojects.com"
- Update Cloudflare worker system prompt to mention mitraaiprojects.com

---

## 9. Expanded Vision — Crisp Courses + Cheatsheets + Notebook UX

> Added: 03 Jun 2026. This section supersedes the "project kits only" framing. mitraaiprojects.com will have two distinct lanes: **Crisp Courses** (concept + code + quiz + cert) and **Project Kits** (full guided builds). Both are premium but bite-sized.

---

### 9.1 Site Navigation (mitraaiprojects.com)

```
Home  |  Courses  |  Projects  |  Cheatsheets  |  Contact
```

- **Home** — hero + what you get + two lanes (Courses vs Projects) + sign-in
- **Courses** — landing grid listing all course tracks: Programming, ML, DL, RL, GenAI, Agentic AI, MLOps/Tools
- **Projects** — existing project kit catalog (unchanged from Section 5)
- **Cheatsheets** — downloadable PDF reference cards (see Section 9.4)
- **Contact** — simple form

When **Courses** is pressed → course index page showing track cards.
When a track card (e.g. "Machine Learning") is pressed → OneNote-style page with left-side topic tabs.

---

### 9.2 Course Tracks

| Track | Audience | Content source | Status |
|---|---|---|---|
| **Programming** | Complete beginners → intermediate developers | New content (see Section 9.3) | Plan first |
| **Machine Learning** | Engineering students, analysts | AIML-Engineering-Lab notebooks 001–010 | Content ready |
| **Deep Learning** | ML practitioners | AIML-Engineering-Lab notebooks 011–020 | Content ready |
| **Reinforcement Learning** | Advanced DL learners | New — build fresh | Planned |
| **Generative AI** | Anyone building with LLMs | AIML-Engineering-Lab notebooks 034, 075 | Partial |
| **Agentic AI** | Developers building agents | New — LangGraph, CrewAI, MCP | Planned |
| **MLOps & Tools** | Practitioners going production | AIML-Engineering-Lab notebooks 050s, Kaggle, HuggingFace | Partial |

---

### 9.3 Programming Track (new — lives in mitraaiprojects.com/courses/programming)

This is a separate track from mitraailife.com students page. It serves all skill levels through a single tabbed page.

**Tab structure inside Programming course page:**

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

### 9.4 Cheatsheets Plan

**Format:** A4 PDF, 1–2 pages per cheatsheet, dark theme matching site.
**Hosting:** S3 at `mitra-ai-life-assets/cheatsheets/<slug>.pdf`
**Download link:** Direct for free cheatsheets; Supabase auth + S3 signed URL (24h expiry) for paid.

| Cheatsheet | Free / Paid | Content |
|---|---|---|
| Python Basics | Free | Data types, loops, functions, common patterns — 1 page |
| Python for Data | Free | Pandas/NumPy/Matplotlib top 30 operations — 2 pages |
| SQL Quick Reference | Free | SELECT, JOIN, GROUP BY, window functions — 2 pages |
| Shell / Bash | Free | 40 commands, pipes, variables, scripts — 2 pages |
| Excel Formula Bible | Free | 25 formulas with syntax + example — 2 pages |
| C/C++ Memory Cheatsheet | Free | Pointers, structs, malloc/free, RAII — 1 page |
| ML Models at a Glance | Free | 12 models: when to use, metric, watch-out — 2 pages |
| Deep Learning Layers | Free | Dense, Conv2D, LSTM, Attention — visual 2 pages |
| GenAI Prompt Patterns | Free | 15 patterns: zero-shot, CoT, RAG, tool use — 2 pages |
| AI for Developers: 25 Prompts | Paid ₹99 | Refactor, test, document, explain, generate — 4 pages |
| AIML Interview Prep | Paid ₹199 | Top 50 ML/DL/GenAI interview Q+A — 6 pages |

**Generation plan:**
- Phase 1: Design in Canva → export PDF → upload to S3 → add download card to page
- Phase 2: Python script using `reportlab` generates PDFs from Markdown source → automated updates
- Source files live in `docs/cheatsheets/` as Markdown (in GitHub); generated PDFs go to S3 only

---

### 9.5 Machine Learning Course — OneNote-Style Page UX

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
│   Boosting   │  │  EXECUTABLE NOTEBOOK (Pyodide)             │  │
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
5. **Executable notebook** — Pyodide (Python in browser, no server needed) OR embedded Colab link
6. **Watch-outs** — common mistakes, data prep requirements
7. **Project idea** — 1 concrete project that connects to the Projects lane
8. **5-question quiz**
9. **Cheatsheet download button**

**Content source mapping (AIML-Engineering-Lab → ML course tabs):**

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

### 9.6 Deep Learning Course Topics

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

---

### 9.7 Generative AI Course Topics

URL: `mitraaiprojects.com/courses/genai`

| Tab | Content |
|---|---|
| What is GenAI | LLMs, diffusion, multimodal — plain English |
| Prompt Engineering | Zero-shot, few-shot, CoT, system prompts |
| RAG (Retrieval Augmented Gen) | 074_postsilicon_validation_rag |
| Fine-Tuning | 075_domain_llm_finetuning |
| Embeddings & Vector DBs | Chroma, Pinecone, Supabase pgvector |
| LLM Evaluation | BLEU, ROUGE, LLM-as-judge |
| HuggingFace Ecosystem | Transformers, Datasets, Spaces — hands-on |
| Kaggle with LLMs | Competition strategy + submission workflow |

---

### 9.8 Agentic AI & MCP Course Topics

URL: `mitraaiprojects.com/courses/agentic`

| Tab | Content |
|---|---|
| What is an Agent | ReAct, tool use, memory, planning |
| LangGraph | State machines, nodes, edges, checkpointing |
| CrewAI | Roles, tasks, crew orchestration |
| MCP (Model Context Protocol) | What it is, building MCP servers, tool registration |
| OpenAI Assistants API | Function calling, code interpreter, file search |
| Multi-Agent Systems | Supervisor pattern, handoffs, state sharing |
| Evaluation & Safety | Agent evals, guardrails, looping prevention |

---

### 9.9 Certification — Non-Registered Organization Rules

**Question:** Can you provide certifications as a non-registered organization?

**Answer: Yes, with caveats.**

| What you CAN do | What you CANNOT do |
|---|---|
| Issue "completion certificates" for your own courses — this is just a PDF/image with your branding | Call it a "degree", "diploma", or "accredited certification" |
| State: "Completed [Course Name] on mitraaiprojects.com" | Claim recognition by AICTE, UGC, or any government body |
| Add a unique certificate ID verified on your site | Imply it is equivalent to university credit |
| Use Supabase to record completion and display a shareable URL | Use words like "certified professional" in a misleading way |

**Recommended wording on every certificate:**
> "This certificate confirms that [Name] completed the [Course Name] on mitraaiprojects.com on [Date]. This is a course completion record issued by Mitra AI Life, an independent education platform."

**Safe to do right now** — no company registration needed to issue course completion certificates. Many platforms (Coursera, Udemy) started this way.

**When registration matters:** If you want the certificate to say "Mitra AI Education Pvt Ltd" or if employers start asking about the issuing body, register then. Until then, "Mitra AI Life" as a brand name is sufficient.

---

### 9.10 Build Sequence for Next Development Session

| Priority | Item | Why first |
|---|---|---|
| 1 | `site/courses.html` — course index page with track cards | Entry point — everything links from here |
| 2 | `site/courses/programming.html` — Python + SQL + Shell tabs | Widest audience, clearest demand |
| 3 | `site/cheatsheets.html` — free download cards | Quick win, shareable, drives sign-ups |
| 4 | `site/courses/ml.html` — ML OneNote-style page | Core technical course, content already exists |
| 5 | Generate first 3 free cheatsheets (Python, SQL, Shell) as PDFs | Launch asset |
| 6 | `site/courses/genai.html` — GenAI course | Highest commercial interest |
| 7 | `site/courses/dl.html`, `site/courses/agentic.html` | Complete the lineup |

**Do NOT build:** mitraailife.com students page changes for coding — that stays beginner-only (AI prompts to learn code). The actual code + notebook experience belongs on mitraaiprojects.com.

---

## 9. Pricing Strategy

| Product | Price | Notes |
|---|---|---|
| Individual project kit | ₹2,000–₹5,000 | One-time access |
| Bundle: Any 3 projects | 20% off | Combo deal |
| Full 10-project bundle | ₹25,000 | ~40% off |
| Mentoring add-on | ₹1,000/hr | 1-on-1 review via Google Meet |
| College licensing | Custom | Contact form on site |

Payment: Razorpay (add later — launch with "contact to enroll" first)

---

## 10. Legal & Ethics

- Add Privacy Policy page (copy/adapt from mitraailife.com)
- Add Terms of Service (code is for learning, not commercial resale)
- Add disclaimer: "Projects are learning exercises. Production use requires additional security review."
- Student project certificates are certificates of completion, not professional certifications
- All AI-generated images: declare AI-generated in page footer

---

## 11. Copilot Working Rules for This Project

When Copilot works in this workspace:
- Always use the shared infrastructure from Section 2 (never create new AWS/GA/Supabase accounts)
- Never commit `.env`, `content/assets/`, `*.mp4`, `*.mp3` to git
- Image generation: `quality="standard"`, `style="vivid"` (separate DALL-E 3 parameters)
- S3 upload prefix: `projects/` (not `scenes/` which is mitraailife.com)
- Color theme: dark teal (`#00d4aa`), not purple-first like mitraailife.com
- Work one project at a time: finish EN page → TE page → next project
- Commit message format: `feat: Project 01 Chatbot — [what was done]`

---

*Last updated: 2026-05-07 | mitraailife.com is at commit 9534dd6 (L10 complete, all 10 levels live)*
