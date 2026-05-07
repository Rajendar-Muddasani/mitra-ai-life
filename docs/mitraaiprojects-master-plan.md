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

### Color Theme — Dark Technical (different from mitraailife.com warm purple)
```css
--bg:         #0f0f17;   /* near-black background */
--surface:    #1a1a2e;   /* card backgrounds */
--primary:    #00d4aa;   /* teal/cyan — the "engineering green" */
--secondary:  #7c3aed;   /* purple (shared brand color) */
--accent:     #f59e0b;   /* amber for highlights/warnings */
--text:       #e2e8f0;   /* light gray text */
--muted:      #64748b;   /* subdued text */
--border:     rgba(0,212,170,0.15);
```

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
