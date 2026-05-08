# Pending Actions — Requires Your Input or Run

This file tracks tasks that were skipped when you said "continue with next" — they need you to run a command, upload a file, or make a decision.

---

## Class 7 Hero Images — Not Yet Generated or Uploaded

**Why pending:** The `generate_class07_images.py` and `upload_class07_images.sh` scripts have been created (see below), but running them requires your OpenAI API key and AWS credentials in `.env`.

**When to do this:** After all 12 Class 7 lessons are built (or whenever you want images to go live). Until then, each lesson hero image simply hides itself via `onerror="this.style.display='none'"`.

**How to run:**
```bash
source .env && .venv/bin/python scripts/generate_class07_images.py
bash scripts/upload_class07_images.sh
```

**Script locations:**
- `scripts/generate_class07_images.py` — generates 12 lesson hero images to `content/assets/students/class-07/`
- `scripts/upload_class07_images.sh` — syncs to `s3://mitra-ai-life-assets/students/class-07/`

**S3 URL pattern after upload:**
`https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/students/class-07/lesson-NN-hero.jpg`

---

## Class 7 Video Walkthroughs — Not Yet Generated

**Why pending:** Lesson video walkthroughs for Class 7 follow the same pattern as Class 6 (`generate_levelNN_video.py` scripts). These need to be built one at a time using your OpenAI TTS + moviepy pipeline.

**When to do this:** After hero images are live. Lessons show a "Video coming soon" placeholder until then.

**How to run (one at a time, same as Class 6):**
```bash
source .env && .venv/bin/python scripts/generate_class07_lesson02_video.py
# then upload to S3
source .env && aws s3 cp content/assets/videos/class-07-lesson-02.mp4 \
  s3://mitra-ai-life-assets/videos/class-07-lesson-02.mp4 \
  --content-type "video/mp4" --cache-control "public, max-age=86400"
```

---

## Uncommitted: docs/task-log.md

**Why pending:** The commit hash for entry #119 was added after the main commit. Run:
```bash
cd /Users/rajendarmuddasani/Mitra_AI_Life
git add docs/task-log.md && git commit -m "docs: task-log entry 119 commit hash" && git push origin main
```
*(Copilot will do this automatically on the next build pass.)*

---

*Last updated: 11 May 2026*
