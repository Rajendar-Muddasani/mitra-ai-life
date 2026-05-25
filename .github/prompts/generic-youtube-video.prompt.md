---
description: "Generate any faceless YouTube video: AI voice + illustrated slides for any topic. Works for educational, tutorial, story, or explainer content."
name: "Faceless YouTube Video Generator"
argument-hint: "Topic, style (educational/story/tutorial), language, target duration in minutes"
tools: [read, edit, create, run_in_terminal]
---

# Faceless YouTube Video Generator

Generate a complete faceless YouTube video for any topic.
Output: one YouTube-ready MP4 with AI voice narration and illustrated slides.
No camera, no face, no external image API — all visuals drawn with PIL.

## Usage in a new Copilot session

```
Use the generic-youtube-video prompt.
Topic: How AI helps small businesses
Style: educational
Language: Telugu
Duration: 8 minutes
Channel: Mitra AI Life - Small Business AI
```

## Input parameters

| Parameter | Required | Example |
|-----------|----------|---------|
| `topic` | yes | "How AI helps small businesses" |
| `style` | yes | `educational` / `tutorial` / `story` / `explainer` |
| `lang` | yes | `en` / `te` / `hi` |
| `duration_min` | yes | `8` (target minutes, 6–15 acceptable for YouTube) |
| `slide_count` | no | defaults to `10` |
| `channel_name` | no | shown in footer of every slide |
| `thumbnail_style` | no | `bold-title` / `question` / `character` |

## Slide count and timing formula

```
slides        = max(8, min(15, duration_min * 1.25))
seconds_each  = (duration_min * 60) / slides
narration_wpm = 130   # for EN; 110 for TE/HI
words_per_slide = int(narration_wpm * (seconds_each / 60))
```

For an 8-min video at 10 slides: each slide ~48s, ~104 words of narration.

## Slide structure by style

### educational / explainer
| Slide | Purpose |
|-------|---------|
| 01 | Hook — Bold question or surprising fact |
| 02 | What we cover today (agenda) |
| 03–08 | One key idea per slide with example |
| 09 | Summary — bullet recap |
| 10 | Call to action — subscribe, visit website |

### tutorial
| Slide | Purpose |
|-------|---------|
| 01 | What you will learn |
| 02 | What you need (tools/setup) |
| 03–08 | Step-by-step instructions, one step per slide |
| 09 | Common mistakes to avoid |
| 10 | Next steps + call to action |

### story / narrative
| Slide | Purpose |
|-------|---------|
| 01 | Title card |
| 02 | Setting + characters |
| 03–07 | Story arc (setup → conflict → climax) |
| 08 | Resolution |
| 09 | Lesson or takeaway |
| 10 | Closing + channel sign-off |

## Visual design system

Define a color palette based on the topic/style:

```python
# Educational — dark navy + amber (matches Mitra AI Life brand)
PALETTES = {
    "educational": {
        "bg":      (6, 17, 31),    # #06111f navy
        "title":   (245, 158, 11), # amber
        "body":    (220, 230, 245),# soft white
        "accent":  (104, 225, 255),# cyan
        "eyebrow": (150, 170, 200),# muted blue
    },
    "story": {
        "bg":      (8, 12, 35),
        "title":   (255, 215, 80),
        "body":    (230, 240, 255),
        "accent":  (140, 100, 220),
        "eyebrow": (180, 160, 240),
    },
    "tutorial": {
        "bg":      (15, 20, 30),
        "title":   (52, 211, 153), # green
        "body":    (220, 230, 245),
        "accent":  (99, 179, 255), # blue
        "eyebrow": (150, 170, 200),
    },
}
```

### Slide layout (PIL only — no external image API)

```
1920 × 1080 px
┌─────────────────────────────────────────────────────┐
│ [accent bar 12px top]                               │
│                                                     │
│    EYEBROW TEXT (small caps, top center)            │
│                                                     │
│         TITLE LINE 1 (large, centered)              │
│         TITLE LINE 2 (if wraps)                     │
│                                                     │
│    body text line 1 (medium, centered)              │
│    body text line 2                                 │
│    body text line 3                                 │
│                                                     │
│    [decorative shape — topic-specific, see below]   │
│                                                     │
│ [accent bar 12px bottom]       channel name (small) │
└─────────────────────────────────────────────────────┘
```

### Decorative shapes per slide type

Draw all shapes with `ImageDraw`. No image files or APIs. Examples:

```python
# Progress bar — shows slide number as a filled rectangle
bar_w = int(W * (slide_num / total_slides))
d.rectangle([0, H - 80, bar_w, H - 68], fill=palette["accent"])

# Icon: lightbulb (circle + rectangle base)
cx, cy, r = W // 2, H - 200, 60
d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=palette["accent"])
d.rectangle([cx-20, cy+r, cx+20, cy+r+30], fill=palette["accent"])

# Icon: checkmark (polygon)
d.polygon([(cx-40, cy), (cx, cy+40), (cx+60, cy-40)], fill=palette["accent"])
```

Choose icon style based on slide content:
- Key concept slide → lightbulb or star
- Step/action slide → numbered circle
- Warning slide → triangle with "!"
- Summary slide → checklist marks
- CTA slide → arrow pointing right

## Narration writing rules

Generate narration for each slide following these rules:
1. **First sentence** = the hook or transition (draws viewer in or connects to previous slide)
2. **Middle sentences** = the core information, one idea at a time, no jargon
3. **Last sentence** = a mini-summary or lead-in to the next slide
4. Use **active voice** throughout
5. Avoid filler phrases: "In this video...", "As we can see...", "Obviously..."
6. For Telugu/Hindi: write as natural spoken language, NOT a translation of the English

```python
NARRATION = {
    "en": [
        "slide 1 narration...",  # ~100 words
        ...
    ],
    "te": [
        "స్లైడ్ 1 నారేషన్...",
        ...
    ],
}
```

## TTS voice selection

```python
VOICES = {
    "en": {
        "primary":  ("en-US", "en-US-Chirp3-HD-Charon"),  # male, clear
        "fallback": ("en-US", "en-US-Neural2-D"),
        "rate": 1.0,
    },
    "te": {
        "primary":  ("te-IN", "te-IN-Chirp3-HD-Kore"),
        "fallback": ("te-IN", "te-IN-Standard-B"),
        "rate": 0.95,
    },
    "hi": {
        "primary":  ("hi-IN", "hi-IN-Chirp3-HD-Wavenet-A"),
        "fallback": ("hi-IN", "hi-IN-Neural2-A"),
        "rate": 0.95,
    },
}
```

## Timing and silence padding

```python
# Adjust per style
STYLE_TIMING = {
    "educational": {"head_sil": 0.30, "tail_sil": 0.50},
    "tutorial":    {"head_sil": 0.30, "tail_sil": 0.60},
    "story":       {"head_sil": 0.50, "tail_sil": 1.20},
    "explainer":   {"head_sil": 0.30, "tail_sil": 0.50},
}
```

## Font paths

```python
def _find_font(candidates):
    for c in candidates:
        if Path(c).exists():
            return c
    raise SystemExit(f"Font not found: {candidates}")

FONT_HEADING = _find_font([
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
FONT_BODY = _find_font([
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
FONT_TE = _find_font([
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Bold.ttf"),
    "/System/Library/Fonts/KohinoorTelugu.ttc",
])
FONT_HI = _find_font([
    "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc",
    "/System/Library/Fonts/Kohinoor.ttc",
])
```

## Output structure

```
output/
  youtube/
    <topic-slug>/
      <lang>/
        slide-01.jpg ... slide-10.jpg
        narr-01.mp3  ... narr-10.mp3
        seg-01.mp4   ... seg-10.mp4
      <topic-slug>-<lang>.mp4        ← upload this to YouTube
      youtube_metadata.txt           ← copy-paste into YouTube Studio
```

## YouTube metadata file to generate

```
TITLE: <compelling 60-char title with keyword at start>
Example: "AI for Small Business: Save 3 Hours a Week | Mitra AI Life"

DESCRIPTION (500 words max):
Paragraph 1 — What this video covers (2-3 sentences)
Paragraph 2 — Who it helps and what they will gain
Paragraph 3 — What's in each section (brief outline)
Paragraph 4 — Call to action: subscribe, visit website, watch related video

TAGS (15 max, comma separated):
<topic keyword>, <language keyword>, Mitra AI Life, AI for beginners, <style keyword>

PLAYLIST: <which Mitra AI Life playlist this belongs to>
LANGUAGE: <ISO code>
THUMBNAIL_IDEA: <1 sentence: what image, what text overlay, what mood>
END_SCREEN_IDEA: Subscribe button + link to related video at 20s before end
```

## Script template

```python
#!/usr/bin/env python3
"""
generate_yt_<slug>_<lang>.py
Topic: <topic>
Style: <style>
Language: <lang>
Duration target: <N> min
Run: source .venv/bin/activate && python scripts/generate_yt_<slug>_<lang>.py
"""
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

# Load .env
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

# ── CONFIG ────────────────────────────────────────────────────────────────────
LANG     = "<lang>"
STYLE    = "<style>"
SLUG     = "<slug>"
CHANNEL  = "Mitra AI Life"
OUT_DIR  = ROOT / "output" / "youtube" / SLUG

W, H = 1920, 1080
PALETTE  = {...}   # from PALETTES dict above
TIMING   = {...}   # from STYLE_TIMING dict above

SLIDES = [
    # (eyebrow, title, body_text)
    ...
]
NARRATION = [...]

# ── FUNCTIONS (copy from generate_teachers_overview_video.py) ─────────────────
# _find_font, render_slide, tts_to_file, audio_duration, make_segment, concat_mp4s

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lang_dir = OUT_DIR / LANG
    lang_dir.mkdir(exist_ok=True)

    segments = []
    for i, ((eye, title, body), narr) in enumerate(zip(SLIDES, NARRATION), 1):
        idx  = f"{i:02d}"
        img  = lang_dir / f"slide-{idx}.jpg"
        aud  = lang_dir / f"narr-{idx}.mp3"
        seg  = lang_dir / f"seg-{idx}.mp4"
        render_slide(eye, title, body, img, LANG)
        tts_to_file(narr, aud, LANG)
        if not seg.exists():
            make_segment(img, aud, seg, **TIMING)
        segments.append(seg)

    out_mp4 = OUT_DIR / f"{SLUG}-{LANG}.mp4"
    concat_mp4s(segments, out_mp4)
    print(f"\n✅ {out_mp4}")
    print("Upload to YouTube → see youtube_metadata.txt for title/description/tags")

if __name__ == "__main__":
    main()
```

## Add output/ to .gitignore

```
# YouTube video output (large files — upload to YouTube directly, not git)
output/
```

## Checklist

- [ ] `.env` has `GOOGLE_APPLICATION_CREDENTIALS` pointing to service account JSON
- [ ] Service account has `Cloud Text-to-Speech API` enabled
- [ ] `source .venv/bin/activate` before running
- [ ] `pip install google-cloud-texttospeech Pillow boto3` already done (or run it)
- [ ] `ffmpeg` installed (`which ffmpeg` should return a path)
- [ ] `output/` is in `.gitignore`
- [ ] Final MP4 is at least 300MB or 8+ minutes for best YouTube monetization eligibility

## How to start a new session

Tell Copilot:
```
Use the generic-youtube-video prompt.
Topic: <your topic>
Style: educational
Language: en
Duration: 8 minutes
Channel name: Mitra AI Life
Generate the script, run it, and tell me the output file path when done.
```

Copilot will:
1. Write all 10 slide texts + narration
2. Generate `scripts/generate_yt_<slug>_en.py`
3. Run the script (TTS calls + ffmpeg)
4. Output the final MP4 and `youtube_metadata.txt`
5. You upload the MP4 manually to YouTube Studio
