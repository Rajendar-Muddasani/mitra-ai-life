# Resource Usage Tracker

Last manual update: 2026-06-02

> Scope of this refresh: the GitHub Repository and AWS S3 sections below were
> remeasured on 2026-06-02. Other sections in this file remain historical and
> should be reviewed separately before treating them as current operational
> numbers.

> **Future plan**: automate this file via a daily CI/CD job that queries GitHub API,
> AWS S3, and Supabase, then commits the updated numbers automatically.

---

## GitHub Repository

| Metric | Value | Limit | Notes |
|---|---|---|---|
| Loose objects | 2,231 | — | Current `git count-objects -vH` loose-object count |
| Object store size | 22.26 MiB | 1 GB soft limit | Still far below Git hosting limits |
| Total commits | 203 | — | `git rev-list --count HEAD` |
| Tracked files | 360 | — | `git ls-files` |
| Working tree size (excluding `.git` and `.venv`) | 0.31 GiB | — | After pruning local S3-backed asset copies on 2026-06-02 |
| Local asset cache under `content/assets/` | 0.30 GiB | — | Remaining files are local-only caches and render intermediates |
| Large assets in repo? | No | — | `content/assets/` is gitignored; published media is hosted on S3 |
| Hosting | GitHub Pages | Free | Custom domain mitraailife.com |

---

## AWS S3 — Bucket: mitra-ai-life-assets (us-west-2)

| Metric | Value | Limit / Cost | Notes |
|---|---|---|---|
| Total objects | 608 | — | Full bucket count from `aws s3 ls --recursive --summarize` |
| Total stored | 2,173,168,653 bytes (~2.02 GiB) | 5 GB free / 12 months for eligible new accounts | Current footprint remains under the old free-tier storage cap |
| After free tier | ~$0.023/GB/mo | — | Rough storage cost at current size is about $0.05/mo |
| CDN base | https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/ | — | All pages reference this |
| Public read | Yes | — | Static public bucket, no private data |
| AWS services currently evidenced in repo workflows | S3 only | — | No concrete project deployment/config for other AWS services was found in the current repo scan |

### Breakdown by folder

| Folder | Files | Approx size |
|---|---|---|
| students/ | 178 | ~1.10 GiB |
| videos/ | 117 | ~668 MB |
| scenes/ | 96 | ~206 MB |
| images/ | 198 | ~51 MB |
| characters/ | 12 | ~13 MB |
| mitra-icons/ | 7 | ~7 MB |

---

## Supabase

| Metric | Value | Free Tier Limit | Notes |
|---|---|---|---|
| Project | kuriwaysdlqnzqqzabts | — | |
| DB storage used | Minimal | 500 MB | Only user_progress rows |
| Bandwidth used | Minimal | 2 GB/mo | |
| Tables | user_progress | — | id, user_id, level_id, quiz_score, completed_at |
| Auth | Google OAuth active | — | |
| RLS | Enabled | — | Row-level security on user_progress |

---

## Google Analytics 4

| Metric | Value | Notes |
|---|---|---|
| Measurement ID | G-QGY0LH6W93 | On all HTML pages |
| Cost | Free | Unlimited |

---

## Disqus

| Metric | Value | Notes |
|---|---|---|
| Shortname | mitra-ai-life | |
| Pages covered | L1–L7 EN + TE (14 pages) | Identifiers: level-01-comic, level-01-comic-te, etc. |
| Plan | Free (ad-supported) | |

---

## OpenAI API (DALL-E 3 image generation)

| Metric | Value | Notes |
|---|---|---|
| Images generated | 69 (L1–L7, all scenes) | Standard quality |
| Cost per standard image | ~$0.04 | |
| Total estimated spend | ~$2.76 | Images only — no GPT API calls yet |
| Chatbot API (future) | ~$0.001/conversation | Once Mitra chatbot is live via Cloudflare Worker proxy |

---

## Domain and Hosting

| Domain / Service | Provider | Cost | Notes |
|---|---|---|---|
| mitraailife.com | GitHub Pages | Free | Live |
| mitraaistudent.com | Planned | ~40–50 SGD/yr (GoDaddy) | School student platform — not purchased yet |
| mitraaiprojects.com | Planned | ~40–50 SGD/yr (GoDaddy) | Engineering project track — not purchased yet |

---

## Content Status (as of 2026-05-07)

| Level | EN Page | TE Page | Images | Videos | Notebooks |
|---|---|---|---|---|---|
| L1 First Step | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L2 Daily Help | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L3 Smart Basics | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L4 Work Smart | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L5 Life Upgrade | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L6 Power User | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | ❌ N/A |
| L7 Build With AI | ✅ Live | ✅ Live | ✅ S3 | ❌ Not yet | Planned |

---

## Language Translation Status

| Language | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|---|---|---|---|---|---|---|
| English | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Telugu | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kannada | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Tamil | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Malayalam | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Hindi | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Three-Website Status

| Website | Status | Purpose |
|---|---|---|
| mitraailife.com | ✅ Live | Adults, daily life, L1–L7 ladder |
| mitraaistudent.com | ❌ Not yet | Make students AI-ready (Gr 6–12) |
| mitraaiprojects.com | ❌ Not yet | Engineering students, portfolio project track |

---

## Mitra Chatbot Status

| Component | Status | Notes |
|---|---|---|
| Chatbot widget (bottom-right) | ❌ Not built | Planned — custom branded |
| Cloudflare Worker proxy | ❌ Not built | Keeps OpenAI key server-side |
| System prompt (knowledge base) | ❌ Not written | Will cover all levels, FAQs, guidance |
| Supabase Admin Dashboard | ❌ Not built | To view user count, quiz scores, completions |
| Supabase progress restore | ❌ Not built | Home page should show completed levels on login |
