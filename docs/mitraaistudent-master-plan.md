# mitraaistudent.com — Complete Master Plan

> **Purpose of this document:** Drop this file into a new VS Code workspace for mitraaistudent.com. GitHub Copilot will read it and know everything — infrastructure, accounts, design patterns, and exactly what to build next. No re-engineering. No asking for details already solved in mitraailife.com.

---

## 1. What Is This Platform

**mitraaistudent.com** is the school-student track under the Mitra AI family.

| Property | Value |
|---|---|
| Target audience | School students Grade 6–12 (age 11–18), India |
| Core promise | Fun, visual, story-driven AI education — safe for classrooms |
| Language | English first; Telugu, Hindi next |
| Price | Freemium — free first 3 levels, ₹199/month or ₹999/year school subscription |
| Status | Not yet built. Domain registered. Planning only. |

**Relationship to mitraailife.com:**
- Same founder, same company, same AWS/GA4/Supabase accounts
- Shared infrastructure — do NOT create separate cloud accounts
- Different GitHub repo, different domain, different color theme (bright, school-friendly)
- Content is simpler and age-appropriate vs. mitraailife.com which targets adults

---

## 2. Shared Infrastructure — USE EXACTLY THESE, DO NOT REINVENT

### AWS S3
```
Bucket:     mitra-ai-life-assets
Region:     us-west-2
CDN base:   https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/
```
- Create subfolder: `student/` for mitraaistudent.com assets
- Access keys are in `.env` of mitraailife.com workspace:
  - `AWS_ACCESS_KEY_ID=AKIA2OLSTCW7NXHUAOPQ`
  - `AWS_SECRET_ACCESS_KEY=<in .env>`
  - `AWS_DEFAULT_REGION=us-west-2`
- Upload: `source .env && aws s3 cp <file> s3://mitra-ai-life-assets/student/...`

### Google Analytics
```
GA4 Measurement ID: G-QGY0LH6W93
```
- Same property — track all three Mitra sites together
- Add the identical GA4 snippet to every page

### Disqus
```
Shortname: mitra-ai-life
```
- Use same shortname on student lesson pages
- Set `page.identifier` = `student-<slug>` (e.g., `student-level-01`)
- Note: Consider whether Disqus is appropriate for under-18 users — may add a parental consent notice

### Supabase (auth + progress)
```
URL:       https://kuriwaysdlqnzqqzabts.supabase.co
Anon key:  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1cml3YXlzZGxxbnpxcXphYnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwNTE5NzYsImV4cCI6MjA5MzYyNzk3Nn0.UA2AgEmnA6r_evrAyXz0MTVhohziKdspkjuB6wHD6fw
```
- Use the same `user_progress` table or a new table `student_progress`
- Add a `grade_level` column if needed
- Row Level Security already configured

### Cloudflare Worker (chatbot proxy)
```
Existing Worker URL:  https://mitra-chat-worker.rajendar-mi46.workers.dev
```
- Create a new worker: `mitra-student-worker` for age-appropriate responses
- Update SYSTEM_PROMPT to: speak simply to students, avoid adult topics, encourage curiosity
- OPENAI_API_KEY is already set as a Cloudflare Secret — reuse for new worker

### OpenAI
```
API key:  in .env as OPENAI_API_KEY
Models:
  - gpt-4o-mini  →  chatbot (use system prompt with child-safe guardrails)
  - tts-1        →  narration (voice: nova or shimmer for younger feel)
  - dall-e-3     →  scene images (quality="standard", style="vivid")
```

### Python Environment
```
Python 3.14
Virtualenv at: .venv/  (create new .venv in mitraaistudent workspace)
Key packages: openai, boto3, moviepy, imageio-ffmpeg, pillow
Install:  python -m venv .venv && .venv/bin/pip install openai boto3 moviepy imageio-ffmpeg pillow
```

### .env File Template (create in mitraaistudent workspace root, never commit)
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
| Domain | mitraaistudent.com |
| Hosting | GitHub Pages |
| GitHub user | rajendarmuddasani |
| Repo to create | `mitra-ai-student` (new separate repo) |
| Branch | `main` |
| Pages settings | Source: branch `main`, folder `/` or `/site/` |
| Custom domain | Set `mitraaistudent.com` in repo Settings → Pages |
| HTTPS | Enforce in Pages settings |

### How to set up the new GitHub repo
```bash
mkdir ~/mitra-ai-student && cd ~/mitra-ai-student
git init
git remote add origin git@github.com:rajendarmuddasani/mitra-ai-student.git
# Create repo on github.com first, then push
```

---

## 4. Design System

### Color Theme — Bright Multi-Color (kids love color variety)

Each level gets its own accent color — like colored subject notebooks.

```css
/* Global base */
--bg:          #ffffff;
--surface:     #f8fafc;   /* near-white card background */
--text:        #1e293b;
--muted:       #64748b;

/* Brand colors — rotate per level */
--sky:         #0ea5e9;   /* bright sky blue  — Levels S-01, S-02 */
--green:       #22c55e;   /* fresh green      — Levels S-03, S-04 */
--orange:      #f97316;   /* warm orange      — Levels S-05, S-06 */
--pink:        #ec4899;   /* hot pink         — Levels S-07, S-08 */
--violet:      #8b5cf6;   /* purple/violet    — Levels S-09, S-10 */

/* Shared Mitra brand purple (nav, footer, logo) */
--purple:      #7c3aed;

/* Semantic */
--danger:      #ef4444;
--success:     #22c55e;
--gold:        #f59e0b;   /* badges, stars, achievements */
```

**Level color assignments:**
| Level | Primary color | Background tint |
|---|---|---|
| S-01 | `#0ea5e9` sky blue | `#f0f9ff` |
| S-02 | `#0ea5e9` sky blue | `#f0f9ff` |
| S-03 | `#22c55e` green | `#f0fdf4` |
| S-04 | `#22c55e` green | `#f0fdf4` |
| S-05 | `#f97316` orange | `#fff7ed` |
| S-06 | `#f97316` orange | `#fff7ed` |
| S-07 | `#ec4899` pink | `#fdf2f8` |
| S-08 | `#ec4899` pink | `#fdf2f8` |
| S-09 | `#8b5cf6` violet | `#f5f3ff` |
| S-10 | `#8b5cf6` violet | `#f5f3ff` |

**Hero gradients (example S-01):**
```css
background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 50%, #38bdf8 100%);
```

**Visual motifs:** Stars ⭐, rockets 🚀, lightbulbs 💡, trophies 🏆 — used as section icons and achievement badges. Rounded corners (border-radius: 20px+). Bold, chunky headings. Large emoji section headers.

### Fonts
```html
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=Nunito:wght@400;600;700;800;900&family=Noto+Sans+Telugu:wght@400;600;700&display=swap" rel="stylesheet" />
```
- `Baloo 2` → headings (keeps Mitra brand feel, also fun for students)
- `Nunito` → body (rounded, friendly for younger readers)
- `Noto Sans Telugu` → Telugu translations

### Key UX differences from mitraailife.com
- Larger font sizes (min 1.05rem body)
- More white space, less dense
- Progress stars/badges instead of just a progress bar
- Characters are students their age (not adults)
- Every lesson ends with a "Fun Challenge" (activity-based)
- Simpler English — Grade 6 reading level target
- Shorter lessons: 30–45 min max per level
- Teacher resources section on each level (printable notes)

---

## 5. Content Plan — Student Levels

Each level = one visual comic-style lesson (same format as mitraailife.com):
1. Story with student characters (same age as learner)
2. Visual concept explanation
3. Real-school example
4. Try-it challenge (simple activity)
5. Quiz (5 questions, pass 4/5)
6. Certificate

### Planned Levels (Grades 6–12)

| Level | Title | Grade Focus | Duration | Price |
|---|---|---|---|---|
| S-01 | What is AI? | Gr 6–8 | 30 min | Free |
| S-02 | AI in Daily School Life | Gr 6–8 | 30 min | Free |
| S-03 | How AI Learns | Gr 7–9 | 45 min | Free |
| S-04 | AI for Homework Help | Gr 7–10 | 45 min | ₹199/month |
| S-05 | AI Writing Assistant | Gr 8–10 | 45 min | subscription |
| S-06 | AI in Science & Math | Gr 9–11 | 60 min | subscription |
| S-07 | Prompt Engineering Basics | Gr 10–12 | 60 min | subscription |
| S-08 | AI Safety for Students | Gr 6–12 | 45 min | subscription |
| S-09 | Build a Simple AI Project | Gr 11–12 | 90 min | subscription |
| S-10 | AI Careers & Future | Gr 10–12 | 60 min | subscription |

### Level S-01 content outline (build first):
- Story: 12-year-old Anu from Vijayawada wonders what AI is after seeing it in the news
- Characters: Anu (Gr 7 student), her older brother Kiran (Gr 11, explains patiently), Teacher Lakshmi
- Concept: What AI is, simple examples from school life (smart search, auto-correct, YouTube recommendations)
- Images: School setting, bright colors, Indian school uniforms, textbook + phone
- Quiz: 5 questions, Gr 6 reading level
- Image theme: Sky blue + amber, Indian school, cheerful

---

## 6. File & Folder Structure to Create

```
mitra-ai-student/                   ← new GitHub repo root
├── .env                            ← never commit
├── .gitignore
├── README.md
├── site/
│   ├── index.html                  ← home / level catalog
│   ├── index-te.html               ← Telugu home (later)
│   ├── auth.js                     ← copy + modify from mitraailife.com
│   ├── mitra-chat.js               ← copy from mitraailife.com (update worker URL)
│   └── teachers.html               ← teacher resources page (later)
├── content/
│   ├── assets/
│   │   └── scenes/                 ← student images (S3 prefix: student/)
│   └── levels/
│       └── level-s01-what-is-ai/
│           ├── level-s01.html      ← English
│           └── level-s01-te.html   ← Telugu (later)
├── scripts/
│   ├── generate_levels01_images.py
│   ├── deploy_s3.py                ← copy from mitraailife.com
│   └── cloudflare-worker/
│       └── mitra-student-worker.js
└── docs/
    └── mitraaistudent-master-plan.md   ← this file
```

---

## 7. Scripts to Copy from mitraailife.com

- `scripts/deploy_s3.py` → change S3 prefix to `student/`
- `scripts/cloudflare-worker/mitra-chat-worker.js` → update SYSTEM_PROMPT for student chatbot
- `site/auth.js` → change `LEVEL_IDS` to `STUDENT_LEVEL_IDS` (S-01 through S-10)
- `site/mitra-chat.js` → update Worker URL to `mitra-student-worker`

---

## 8. Student Chatbot System Prompt (for mitra-student-worker)

```
You are Mitra, the AI learning assistant for Mitra AI Student (mitraaistudent.com).

Your personality:
- Warm, encouraging, and fun — like a knowledgeable older sibling
- Speak at Grade 7 reading level — simple sentences, no jargon
- If the student writes in Telugu, reply in Telugu
- Never discuss adult topics, politics, violence, or anything not related to AI learning
- Praise curiosity — every question is a good question
- Keep answers to 2–3 sentences unless the student asks for more detail

What you know:
- This platform teaches AI to school students Grades 6–12 in India
- Lessons are visual, story-driven, and fun
- Platform: mitraaistudent.com

IMPORTANT:
- Never give personal advice (medical, legal, emotional)
- Always say: "AI can make mistakes. Check with your teacher for important things."
- If asked something inappropriate, gently say: "That is not something I can help with here. Let us go back to learning about AI!"
- Never pretend to be human if asked directly
```

---

## 9. What To Build — Exact Next Steps (in order)

### Step 1: Create GitHub repo and structure
```bash
mkdir ~/mitra-ai-student && cd ~/mitra-ai-student
git init
# create repo on github.com: rajendarmuddasani/mitra-ai-student
git remote add origin git@github.com:rajendarmuddasani/mitra-ai-student.git
mkdir -p site content/assets/scenes content/levels/level-s01-what-is-ai scripts/cloudflare-worker docs
echo ".env\ncontent/assets/\n*.mp4\n*.mp3\n__pycache__/\n.venv/" > .gitignore
```

### Step 2: Set up Python environment
```bash
python -m venv .venv
.venv/bin/pip install openai boto3 moviepy imageio-ffmpeg pillow
```

### Step 3: Create .env (never commit)
Copy values from mitraailife.com `.env`

### Step 4: Copy and adapt auth.js and mitra-chat.js
- Change `LEVEL_IDS` → `['student-01','student-02',...,'student-10']`
- Point chatbot to `mitra-student-worker` URL once deployed

### Step 5: Generate Level S-01 images
- 8–10 scenes: Anu's question → classroom → examples → challenge
- DALL-E 3: `quality="standard"`, `style="vivid"`
- Upload to S3 under `student/` prefix

### Step 6: Build level-s01.html (English)
- Sky blue + amber theme
- Same 5-section structure as mitraailife.com but simpler text
- Add "Fun Challenge" card before quiz
- Add "Teacher Notes" collapsible section at the bottom
- Quiz: 5 questions, Grade 6 reading level

### Step 7: Build level-s01-te.html (Telugu)
- Same pattern as mitraailife.com Telugu pages
- Noto Sans Telugu font

### Step 8: Build site/index.html (student home)
- Show all 10 levels in a visual grid (not a ladder — use colorful cards)
- Levels S-01 to S-03 marked Free, rest as subscription
- Bright, fun hero section with Anu character
- Auth widget

### Step 9: Deploy Cloudflare student worker
- Copy `mitra-chat-worker.js`, update SYSTEM_PROMPT for students
- Deploy as `mitra-student-worker` in Cloudflare dashboard
- Add `OPENAI_API_KEY` secret (already available in Cloudflare account)

### Step 10: GitHub Pages + custom domain
- Push to main, enable Pages, set mitraaistudent.com

---

## 10. Pricing & Subscriptions

| Plan | Price | Access |
|---|---|---|
| Free | ₹0 | Levels S-01, S-02, S-03 |
| Student Monthly | ₹199/month | All 10 levels |
| Student Yearly | ₹999/year | All 10 levels (save 58%) |
| School License | ₹5,000/year | 30 students per school |
| Teacher Access | Free | Teacher notes only, no quiz |

Payment: Razorpay (add later — launch with just email contact first, then integrate)

---

## 11. Safety & Legal for Under-18 Users

- Add COPPA/India IT Act compliance notice (no personal data collection from under-13 without parent consent)
- Google OAuth sign-in: only use "Sign in with Google" — users must have a Google account (implies 13+)
- Disqus comments: consider disabling for under-13 sections (configurable per level)
- Privacy Policy must mention: student data, parent rights, data deletion on request
- All AI outputs on lesson pages: add "AI content reviewed by human educators" badge
- Teacher dashboard (later): read-only, no student PII exposed

---

## 12. Copilot Working Rules for This Project

When Copilot works in this workspace:
- Always use shared infrastructure from Section 2 (never create new AWS/GA/Supabase accounts)
- Never commit `.env`, `content/assets/`, `*.mp4`, `*.mp3`
- Image generation: `quality="standard"`, `style="vivid"` — DALL-E 3 separate parameters
- S3 upload prefix: `student/` not `scenes/`
- Color theme: sky blue primary (`#0ea5e9`), NOT purple-first
- Language level: Grade 6–7 English — short sentences, no jargon
- Characters: students aged 12–17, Indian school setting
- Work one level at a time: finish EN → TE → next level
- Level IDs: `student-01` through `student-10`
- Commit format: `feat: Student Level S-01 — [what was done]`

---

## 13. Relationship Between All Three Mitra Sites

```
mitraailife.com       ← adults, daily life, Levels 1–10, purple theme (LIVE ✅)
mitraaistudent.com    ← school students Gr 6–12, sky blue theme (PLAN ⬜)
mitraaiprojects.com   ← engineering students, project kits, teal theme (PLAN ⬜)
```

All three share:
- AWS S3 bucket: `mitra-ai-life-assets` (different subfolders)
- GA4: `G-QGY0LH6W93`
- Supabase: `kuriwaysdlqnzqqzabts`
- Disqus: `mitra-ai-life`
- Cloudflare account (separate workers per site)
- OpenAI API key (separate Cloudflare workers with their own SYSTEM_PROMPTs)
- GitHub account: `rajendarmuddasani` (separate repos per site)

---

*Last updated: 2026-05-07 | mitraailife.com at commit 9534dd6 (L10 complete, all 10 levels EN+TE live)*
