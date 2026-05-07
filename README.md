# Mitra AI Life

Mitra AI Life is a beginner-first AI education platform for India. The public site is designed around one simple strategy:

**One brand, one URL, many focused learning tracks.**

Main domain: `mitraailife.com`

## Current status

The repository now contains both planning documents and a working static website.

Completed site structure:
- unified Home page at `site/index.html`
- shared top-banner navigation across the new track pages
- AI for Daily Life page at `site/daily-life.html`
- placeholder pages for Students, AI Tuition, Spoken English, Project Kits, Small Business, Teachers, and Contact
- branded `404.html`
- `robots.txt` and `sitemap.xml`
- mobile layout fixes for Home and track pages

Completed content status:
- AI for Daily Life English Levels 1-10 are live in `content/english/`
- English intro videos for Levels 1-10 are generated, uploaded to S3, and embedded
- Telugu pages exist for the Daily Life track
- Telugu video production is next, starting with Level 1 voice and pacing fine-tune

## Platform tracks

The top navigation uses these public tracks:
- Home
- AI for Daily Life
- AI for Students
- AI Tuition
- Spoken English
- AI Project Kits
- AI for Small Business
- AI for Teachers
- Contact

Keep each track separate in audience, tone, and content path. Do not merge every idea into one course ladder.

## Product rules

- English remains the source language for lessons.
- Telugu is the first translation language.
- The first two Daily Life levels remain free unless the founder changes the launch strategy.
- Beginner public learning stays separate from premium engineering project support.
- Public lessons need human review before publishing.
- AI outputs should never be presented as guaranteed truth.
- Large generated media should stay outside GitHub, usually in object storage.

## Important files

- `site/index.html` — unified Home page
- `site/track-page.css` — shared styling for track pages
- `site/sitemap.xml` — public sitemap
- `content/english/` — AI for Daily Life English lesson pages
- `content/telugu/` — Telugu lesson pages
- `docs/mitraailife-unified-platform-plan.md` — one-site platform strategy
- `docs/mitraaituition-master-plan.md` — AI Tuition strategy
- `docs/mitra-ai-language-learning-master-plan.md` — Spoken English and language-learning strategy
- `docs/github-pages-deployment-checklist.md` — public site deployment checklist
- `docs/telugu-video-production-checklist.md` — Telugu intro video production workflow
- `docs/level-content-plan.md` — AI Daily Life curriculum plan
- `site/pitch-deck.html` — pitch deck page

## Current next move

After the site hygiene pass, return to production for the first finished track:

1. Fine-tune the AI for Daily Life Level 1 Telugu intro video.
2. Generate Telugu intro videos for Levels 2-10.
3. Complete AI for Daily Life as the first fully polished track.
4. Then move to the next top-banner track.
