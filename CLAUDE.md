# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Mitra AI Life is a beginner-first AI education platform for India. The site is static HTML deployed via GitHub Pages at `mitraailife.com`. There is no build step, no framework, no package.json. Everything under `site/` is served directly.

Large generated media (images, videos, audio) lives in S3 at `https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/` — never committed to git.

## Commands

**Run the site locally:**
```bash
bash scripts/serve-site.sh
# serves site/ at http://localhost:4173
```

**Run the full site QA check (links, anchors, SEO tags, JSON-LD, sitemap coverage):**
```bash
node scripts/site_qa.js
```
Exit code 1 means at least one issue was found. Run this before every commit that touches `site/`.

**Python scripts** (video generation, image generation, S3 upload) all require `.env` with `OPENAI_API_KEY` and `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`. Activate the virtual environment first:
```bash
source .venv/bin/activate
# then run e.g.:
python scripts/generate_level01_video.py
```
Videos and images are written to `content/assets/` (gitignored), then uploaded to S3 separately.

**Upload images to S3 after generating:**
```bash
source .venv/bin/activate && python scripts/deploy_s3.py
# or level-specific upload scripts:
bash scripts/upload_class06_images.sh
```

## Architecture

### Site structure
- `site/` — all public HTML pages served directly by GitHub Pages
- `site/track-page.css` — shared CSS for all track pages (nav, typography, dark theme tokens)
- `site/mitra-chat.js` — chatbot widget injected into learner pages; calls the Cloudflare Worker at `mitra-chat-worker.rajendar-mi46.workers.dev`
- `site/auth.js` — Google OAuth via Supabase; reads/writes `user_progress` table
- `scripts/cloudflare-worker/mitra-chat-worker.js` — serverless proxy that holds the OpenAI API key server-side

### Content structure
- `content/english/level-NN-<name>/` — English lesson HTML pages + source markdown (storyboards, scripts, image prompts)
- `content/telugu/` — Telugu lesson markdown outlines
- `content/students/class-NN/` — School student track HTML pages (Grades 6–12)
- `content/tuition/hindi-foundation/` — Hindi tuition track

Each level folder typically contains:
- `level-NN-comic.html` — English lesson page (live, served from `content/`)
- `level-NN-comic-te.html` — Telugu lesson page
- `level-NN-storyboard.md`, `level-NN-video-script.md`, `level-NN-image-prompts.md` — production source files

### Chatbot architecture
The `site/mitra-chat.js` widget sends conversation history to the Cloudflare Worker, which adds the OpenAI API key and streams the response back. The worker is configured with a system prompt that knows all 10 levels, the three planned platforms, and business rules. CORS is locked to `mitraailife.com` origins.

### Backend services
- **GitHub Pages** — hosts `site/` on `mitraailife.com`
- **AWS S3** — `mitra-ai-life-assets` bucket (us-west-2), publicly readable, holds all generated images and videos
- **Supabase** — project `kuriwaysdlqnzqqzabts`, stores `user_progress` (id, user_id, level_id, quiz_score, completed_at), Google OAuth, RLS enabled
- **Google Analytics** — ID `G-QGY0LH6W93`, on every page
- **Disqus** — shortname `mitra-ai-life`, on comic pages L1–L7 EN + TE

## Conventions

### Navigation order — never change without founder approval
Every page top banner must list tracks in this exact order:
Home → AI for Daily Life → AI for Students → AI Tuition → Spoken English → AI Project Kits → AI for Small Business → AI for Teachers → Contact

### SEO requirements for every public page (enforced by `site_qa.js`)
All pages in `site/` (except `404.html`, `logo-options.html`, `contact-te.html`) must have:
- `<html lang="...">`, `<title>`, viewport meta, `meta description`, canonical link
- `og:title`, `og:description`, `og:image` (absolute URL), `twitter:card`
- Valid JSON-LD block(s)
- Entry in `site/sitemap.xml` (except pages in the SITEMAP_EXCLUDE set)

### CSS design tokens
Track pages import `site/track-page.css` which defines the dark theme: `--bg: #06111f`, `--cyan: #68e1ff`, `--amber: #f59e0b`, `--green: #10b981`, Nunito + Baloo 2 fonts. The home page (`site/index.html`) uses slightly different tokens inline (`--bg: #040712`). Use the shared stylesheet for all new track pages rather than inlining styles.

### Content language strategy
- English is always the master/source version
- Telugu is the first translation — translate for meaning, not literally
- Pages that are Telugu use `<html lang="te">` and the filename suffix `-te.html`
- The chatbot widget auto-detects Telugu pages by `lang="te"` or `-te.html` in the URL

### What stays out of git
- `content/assets/` (all generated images, videos, audio)
- `.env`, `*.env`, `*-key.json`, `*-credentials.json`
- `accounts.md`, `voice_tests/`

### Commit message style
`feat:`, `fix:`, `docs:`, `chore:` prefixes. Keep messages short and specific, e.g. `feat: add class-07 lesson pages`, `fix: tighten mobile layout on students page`.

## Key planning docs
- `docs/level-content-plan.md` — curriculum ladder for all 10 Daily Life levels, pricing, audience, and content structure per level
- `docs/mitraailife-unified-platform-plan.md` — one-site strategy and top-navigation spec
- `docs/github-pages-deployment-checklist.md` — pre/post-commit checklist for site changes
- `docs/telugu-video-production-checklist.md` — Telugu video generation workflow and known quality issues
- `docs/pending_actions.md` — tasks blocked on API keys or founder decisions
- `docs/resource-usage.md` — current S3, Supabase, and content completion status

## Product rules (do not change silently)
- Levels 1 and 2 remain permanently free; Levels 3–10 are currently free under early access
- English-first, Telugu-next language strategy
- Beginner consumer content (`site/`) is separate from premium engineering project services
- Public lessons need a human review step before publishing
- AI outputs must never be presented as guaranteed truth
- Medical, legal, and financial authority claims are not allowed in lesson content
