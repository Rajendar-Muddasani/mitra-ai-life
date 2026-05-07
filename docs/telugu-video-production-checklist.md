# Telugu Video Production Checklist

Use this checklist when resuming Telugu intro video production for the AI for Daily Life track.

Current priority:

1. Fine-tune Level 1 Telugu video quality.
2. Generate Levels 2-10 Telugu intro videos.
3. Upload each video to S3.
4. Embed each video in the matching Telugu lesson page.

## Known Level 1 Quality Issue

Before generating Levels 2-10, fix the Telugu delivery quality on Level 1.

Current known problems from review:
- voice sounds like it is swallowing words
- pacing feels too fast for beginner learners
- output feels low in volume or less clear than the English version

Current script anchor:
- `scripts/generate_level01_video_te.py`

Current Telugu TTS setting in that script:
- `voice="nova"`
- `speed=0.92`

## Pre-Production Check

- Confirm `.venv/` is active and dependencies are available.
- Confirm `.env` contains `OPENAI_API_KEY`.
- Confirm scene images already exist in `content/assets/scenes/`.
- Confirm the target Telugu page exists:
  `content/english/level-XX-.../level-XX-comic-te.html`
- Run `git status --short` before starting so unrelated files are not accidentally staged.

## Level 1 Fine-Tune Checklist

- Review `scripts/generate_level01_video_te.py` narration text scene by scene.
- Shorten or simplify any Telugu sentence that feels crowded when spoken.
- Adjust TTS speed if needed. Start by testing slower than `0.92` if clarity is still weak.
- Regenerate only after deciding on the smallest useful script or voice-speed change.
- Listen for:
  - clean word endings
  - stable pacing
  - clear pauses between ideas
  - better volume balance relative to the English version
- If quality is acceptable, keep that pattern for Levels 2-10.

Run Level 1 generator:

```bash
source .env && .venv/bin/python scripts/generate_level01_video_te.py
```

Expected output:

- `content/assets/videos/level-01-intro-te.mp4`

## Level 2-10 Production Pattern

For each level:

- create or adapt a Telugu video generator script using the Level 1 Telugu pattern
- keep output naming consistent: `level-XX-intro-te.mp4`
- keep video format consistent: `1280x720`, `24fps`, `H.264/AAC`
- reuse the same Ken Burns approach used in the English and Telugu video generators
- keep Telugu narration simpler than English where needed for clarity

Preferred generator pattern:

- scene images from `content/assets/scenes/`
- temporary audio in `content/assets/videos/audio_tmp_te/`
- video output in `content/assets/videos/`

## Upload Checklist

After a Telugu video looks correct locally, upload it to S3.

Command pattern:

```bash
source .env && aws s3 cp content/assets/videos/level-XX-intro-te.mp4 s3://mitra-ai-life-assets/videos/level-XX-intro-te.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'
```

Current public asset base:

- `https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/`

Expected public URL pattern:

- `https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/videos/level-XX-intro-te.mp4`

## Embed Checklist

After upload, embed the Telugu video in the matching lesson page:

- `content/english/level-01-interactive/level-01-comic-te.html`
- `content/english/level-02-daily-help/level-02-comic-te.html`
- `content/english/level-03-smart-basics/level-03-comic-te.html`
- `content/english/level-04-work-smart/level-04-comic-te.html`
- `content/english/level-05-life-upgrade/level-05-comic-te.html`
- `content/english/level-06-power-user/level-06-comic-te.html`
- `content/english/level-07-build-with-ai/level-07-comic-te.html`
- `content/english/level-08-ai-for-business/level-08-comic-te.html`
- `content/english/level-09-ai-for-income/level-09-comic-te.html`
- `content/english/level-10-ai-safety/level-10-comic-te.html`

For each embed:

- confirm the video URL points to the Telugu file, not the English one
- confirm the section label clearly shows it is Telugu
- confirm the page still loads on mobile without layout breakage

## Review Checklist Per Level

- video plays from the S3 URL
- narration is understandable for a beginner Telugu listener
- no obvious swallowed words or clipped audio
- video duration feels reasonable for the lesson
- video is embedded in the correct `-comic-te.html` page
- page changes are staged with the correct script or embed file only

## Commit Pattern

Recommended commit shape for each Telugu level:

- generator script, if a new one was created or adjusted
- matching `level-XX-comic-te.html` embed update

Example commit message pattern:

- `feat: Level 01 TE video — generated, on S3, embedded in level-01-comic-te.html`
- `feat: Level 02 TE video — generated, on S3, embedded in level-02-comic-te.html`

## Suggested Execution Order

1. Fine-tune `level-01-intro-te.mp4`.
2. Validate the voice, pacing, and clarity standard.
3. Reuse that standard for Levels 2-10.
4. Complete the full Telugu AI for Daily Life track before switching to the next top-banner track.
