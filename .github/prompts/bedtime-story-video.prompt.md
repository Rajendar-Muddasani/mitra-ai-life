---
description: "Generate a complete faceless YouTube bedtime story video: AI voice narration + 10 illustrated slides, 7-10 minutes, YouTube-ready MP4."
name: "Bedtime Story Video Generator"
argument-hint: "Story title and language (e.g. 'The Clever Crow - English' or 'The Magic Tree - Telugu')"
tools: [read, edit, create, run_in_terminal]
---

# Bedtime Story Video Generator

Generate a fully automated, faceless YouTube bedtime story video.
Output is a single YouTube-ready MP4 — no S3 needed, upload directly.

## What you will build

A Python script `scripts/generate_story_<slug>.py` that produces:
- 10 illustrated slide images (1920×1080 JPEG) using PIL
- Per-slide narration MP3s via Google Cloud TTS (Chirp3-HD voices)
- Per-segment MP4s (slide + audio, padded with silence)
- One final concatenated MP4: `output/story_<slug>.mp4`
  - Target duration: **7–10 minutes** (aim for ~8 min total)
  - Format: H.264 / AAC, 1920×1080, 30fps, ready for YouTube upload

## Story content structure

Story title: {{story_title}}
Language: {{lang}}  (en = English, te = Telugu, hi = Hindi)

### Slide breakdown (10 slides)

| # | Type | Duration | Content |
|---|------|----------|---------|
| 01 | Title card | 20–25s | Story title + channel name + soft intro music note in narration |
| 02 | Setting the scene | 45–60s | Describe the world, time of night, the main character introduced |
| 03 | The character's world | 45–60s | Character's daily life, what they love, what they want |
| 04 | The problem begins | 50–65s | Something changes — a challenge, a mystery, a wish |
| 05 | First attempt | 50–65s | Character tries to solve it — doesn't fully work |
| 06 | A helper arrives | 45–60s | A friend, animal, or wise elder gives a clue |
| 07 | The journey | 50–65s | Action rises — character faces the hardest part |
| 08 | The turning point | 50–65s | Character does something brave, kind, or clever |
| 09 | Resolution | 45–60s | Problem solved, everyone is safe and happy |
| 10 | Closing card | 20–25s | Gentle moral/lesson + "Goodnight" sign-off + channel name |

**Total target: 470–600 seconds (~8 min)**

## Slide visual design rules

```python
W, H = 1920, 1080
BG_NIGHT   = (8, 12, 35)      # deep midnight blue
STAR_GOLD  = (255, 215, 80)   # warm gold for title text
MOON_WHITE = (230, 240, 255)  # cool white for body text
ACCENT     = (140, 100, 220)  # soft purple for eyebrow/footer
```

Each slide:
1. Background: solid `BG_NIGHT` with a subtle gradient (draw a rectangle from top with alpha blend, darker at bottom)
2. Decorative elements drawn with PIL shapes:
   - **Title card**: large centered title in `STAR_GOLD`, 3-5 small star dots drawn as tiny circles around the text
   - **Story slides**: eyebrow label top-left (e.g. "Part 2"), main scene description text centered, scene illustration as simple geometric shapes (moon as a circle, tree as a triangle + rectangle, character as a stick figure built from ellipses and lines — all drawn with `ImageDraw`)
3. Footer: channel name bottom-right in small `ACCENT` text
4. Font: use `scripts/_fonts/NotoSansTelugu-Bold.ttf` for Telugu; for English use Arial Bold from system

**Important:** Draw ALL scene elements with PIL primitives only — no external image generation API. Make the images "illustrated storybook" style using only shapes, polygons, and text. This keeps cost zero and style consistent.

## Narration writing rules

Write narration for each slide in the specified language:
- **English**: warm, slow, soothing bedtime tone. Simple vocabulary. Sentences short. Pace: 120–140 words per minute (speaking rate 0.88 in TTS).
- **Telugu**: natural spoken Telugu, not literal translation. Use simple words. Pace: 0.90 speaking rate.
- **Hindi**: natural spoken Hindi. Pace: 0.90 speaking rate.

Each narration string must be long enough to fill the target slide duration. Aim for:
- Title/closing cards: 30–40 words
- Story slides: 80–120 words each

## TTS configuration

```python
# English
voice_en = VoiceSelectionParams(language_code="en-US", name="en-US-Chirp3-HD-Aoede")
rate_en  = 0.88  # slow, soothing

# Telugu
voice_te = VoiceSelectionParams(language_code="te-IN", name="te-IN-Chirp3-HD-Kore")
rate_te  = 0.90

# Hindi
voice_hi = VoiceSelectionParams(language_code="hi-IN", name="hi-IN-Chirp3-HD-Wavenet-A")
rate_hi  = 0.90
```

Fallback if Chirp3-HD unavailable:
- EN: `en-US-Neural2-F` (feminine, calming)
- TE: `te-IN-Standard-B`
- HI: `hi-IN-Neural2-A`

## Segment construction (silence padding)

```python
head_sil = 0.5   # longer lead-in for story feel
tail_sil = 1.2   # longer breath between slides — feels like turning a page
```

Use the same `make_segment()` pattern from `scripts/generate_teachers_overview_video.py`.

## Concatenation

Use `-c copy` (lossless) since all segments share identical codec params.
If lossless fails, fall back to re-encode (`-c:v libx264 -c:a aac`).

```python
def concat_mp4s(mp4s, out_mp4):
    listfile = out_mp4.parent / "_concat_list.txt"
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in mp4s))
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
           "-c", "copy", str(out_mp4)]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        # fallback re-encode
        cmd[-3:-1] = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                      "-c:a", "aac", "-b:a", "192k"]
        subprocess.run(cmd[:-2] + [str(out_mp4)], check=True, capture_output=True)
    listfile.unlink()
```

## Output directory structure

```
output/
  stories/
    <slug>/
      en/              ← or te/ or hi/
        slide-01.jpg
        narr-01.mp3
        seg-01.mp4
        ...
      story_<slug>.mp4   ← final YouTube upload file
```

No S3 upload needed. Final MP4 is uploaded directly to YouTube.

## YouTube metadata to generate alongside

Write a companion file `output/stories/<slug>/youtube_metadata.txt` with:

```
TITLE: <Story title> | Bedtime Story for Kids | Mitra AI Life
DESCRIPTION:
<3-paragraph description>
Line 1: What the story is about (1 sentence).
Line 2: Values the story teaches (kindness, courage, honesty, etc.).
Line 3: Call to action — "Subscribe to Mitra AI Life for more bedtime stories."

TAGS: bedtime story, kids story, short story for children, story in English, moral story, animated story, Mitra AI Life, <story-specific tags>

CATEGORY: Education
LANGUAGE: <language>
THUMBNAIL_IDEA: <1 sentence describing an eye-catching thumbnail — character face close-up, bright moon background, title text large>
```

## Script structure to generate

```python
#!/usr/bin/env python3
"""
generate_story_<slug>.py
Story: <title>
Language: <lang>
Run: source .venv/bin/activate && python scripts/generate_story_<slug>.py
"""

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "output" / "stories" / "<slug>"

STORY_SLIDES = [
    # (eyebrow, scene_description_for_drawing, narration_text)
    ("", "<title>", "<narration>"),
    ...
]

def draw_scene(slide_num, eyebrow, scene_desc, out_path, lang):
    # PIL drawing — build the scene from shapes
    ...

def build_story(lang):
    ...

if __name__ == "__main__":
    build_story("<lang>")
    print("Done! Upload output/stories/<slug>/story_<slug>.mp4 to YouTube.")
```

## Checklist before running

- [ ] `GOOGLE_APPLICATION_CREDENTIALS` set in `.env`
- [ ] `.venv` active with `google-cloud-texttospeech`, `Pillow`, `ffmpeg` available
- [ ] Font file present at `scripts/_fonts/NotoSansTelugu-Bold.ttf` (for Telugu)
- [ ] `output/` directory in `.gitignore` (large files, not for git)

## How to use this prompt

1. Open a new Copilot Agent session
2. Say: **"Use the bedtime-story-video prompt. Story: The Clever Crow. Language: English."**
3. Copilot will generate the full script, run it, and produce `output/stories/clever-crow/story_clever-crow.mp4`
4. Upload that MP4 directly to YouTube on the Mitra AI Life Bedtime Stories channel
