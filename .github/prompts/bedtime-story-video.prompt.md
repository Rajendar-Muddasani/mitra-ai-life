---
description: "Generate a complete faceless YouTube bedtime story video using DALL-E 3 images + Google TTS narration. 10 beautiful illustrated scenes, 7-10 minutes, YouTube-ready MP4."
name: "Bedtime Story Video Generator"
argument-hint: "Story title and language, e.g. 'The Clever Crow - English'"
tools: [read, edit, create, run_in_terminal]
---

# Bedtime Story Video Generator
## Self-contained — open in a fresh VS Code Copilot session and generate immediately

---

## STEP 0 — What you need before running

### API keys (add to `.env` in the project root)
```
OPENAI_API_KEY=sk-...
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-tts-key.json
```

**Google TTS — commercial use:** Fully legal. Google Cloud TTS Terms of Service
allow synthesized audio in monetized YouTube videos. ✅

**OpenAI DALL-E 3 — commercial use:** Fully legal. OpenAI Terms allow commercial
use of generated images in YouTube content. ✅

### Cost per 10-minute story
| Item | Cost |
|------|------|
| 10 × DALL-E 3 images (1792×1024, standard) | ~$0.80 |
| Google TTS (~10,000 chars Chirp3-HD) | ~$0.16 |
| **Total per story** | **~$1.00** |

### Install dependencies
```bash
source .venv/bin/activate
pip install openai google-cloud-texttospeech Pillow
# ffmpeg: brew install ffmpeg (mac) or apt install ffmpeg (linux)
```

---

## STEP 1 — Paste this to Copilot in a new session

```
I want to generate a bedtime story YouTube video.
Read .github/prompts/bedtime-story-video.prompt.md for full instructions.

Story: The Clever Crow
Language: English
Output folder: output/stories/clever-crow/

Please:
1. Write all 10 slides (DALL-E image prompt + narration text per slide)
2. Generate the full Python script: scripts/generate_story_clever_crow.py
3. Run it
4. Tell me the output MP4 path and estimated duration
```

---

## STEP 2 — Story structure (10 slides, 7–10 minutes)

| Slide | Role | Target duration | Narration words (EN 0.85x rate) |
|-------|------|-----------------|----------------------------------|
| 01 | Title card | 20–25s | 40–50 |
| 02 | Setting the scene | 50–65s | 110–130 |
| 03 | Meet the character | 50–65s | 110–130 |
| 04 | The problem begins | 55–70s | 120–140 |
| 05 | First attempt fails | 55–70s | 120–140 |
| 06 | A helper / idea arrives | 50–65s | 110–130 |
| 07 | The hard work | 55–70s | 120–140 |
| 08 | The turning point | 55–70s | 120–140 |
| 09 | Resolution + joy | 50–65s | 110–130 |
| 10 | Goodnight + moral | 20–25s | 40–50 |

**Total: 460–600 seconds (~8 min)**

---

## STEP 3 — DALL-E 3 image generation

```python
from openai import OpenAI
import urllib.request

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Prepend to ALL image prompts for visual consistency across slides:
ART_STYLE = (
    "Soft watercolor children's book illustration, warm pastel colors, "
    "gentle brushstrokes, cozy magical Indian forest setting, "
    "golden and moonlit lighting, dreamlike and safe for children, "
    "no text or letters in the image. "
)

def generate_image(scene_prompt: str, out_path: Path) -> None:
    if out_path.exists():
        return  # skip if cached — saves cost on re-runs
    response = client.images.generate(
        model="dall-e-3",
        prompt=ART_STYLE + scene_prompt,
        size="1792x1024",   # 16:9 landscape — perfect for YouTube
        quality="standard", # "hd" for richer detail at 2x cost
        n=1,
    )
    urllib.request.urlretrieve(response.data[0].url, out_path)
    print(f"  [img] {out_path.name}")
```

### Text overlay with PIL (channel name + slide title over the DALL-E image)

```python
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(raw_img: Path, title: str, eyebrow: str,
                     channel: str, out_path: Path, lang: str) -> None:
    img = Image.open(raw_img).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    W, H = 1920, 1080
    d = ImageDraw.Draw(img)

    # dark gradient bar at bottom (readability)
    bar = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    for y in range(220):
        alpha = int(180 * (y / 220))
        ImageDraw.Draw(bar).line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img.paste(bar, (0, H - 220), bar)

    f_sm    = ImageFont.truetype(FONT_BODY, 28)
    f_eye   = ImageFont.truetype(FONT_BODY, 32)
    f_title = ImageFont.truetype(FONT_TE if lang == "te" else FONT_HEADING, 66)

    # channel top-right
    d.text((W - 24, 24), channel, fill=(255,255,255,200), font=f_sm, anchor="ra")

    # eyebrow bottom-left
    if eyebrow:
        d.text((44, H - 200), eyebrow.upper(), fill=(245,158,11), font=f_eye)

    # title (word-wrapped, centered, bottom)
    words, lines, current = title.split(), [], ""
    for w in words:
        t = f"{current} {w}".strip()
        if d.textbbox((0,0), t, font=f_title)[2] < W - 120:
            current = t
        else:
            if current: lines.append(current)
            current = w
    if current: lines.append(current)
    y = H - 155
    for ln in lines:
        bb = d.textbbox((0,0), ln, font=f_title)
        x = (W - (bb[2]-bb[0])) / 2
        d.text((x+2, y+2), ln, fill=(0,0,0,220), font=f_title)   # shadow
        d.text((x, y), ln, fill=(255,255,255), font=f_title)
        y += f_title.size + 10

    img.save(out_path, "JPEG", quality=95)
```

---

## STEP 4 — Google TTS voices

```python
VOICE_CONFIG = {
    "en": {
        "language_code": "en-US",
        "name": "en-US-Chirp3-HD-Aoede",  # warm feminine — best for bedtime
        "speaking_rate": 0.85,             # slow and soothing
        "pitch": -2.0,
        "fallback": "en-US-Neural2-F",
    },
    "te": {
        "language_code": "te-IN",
        "name": "te-IN-Chirp3-HD-Kore",
        "speaking_rate": 0.88,
        "pitch": -1.0,
        "fallback": "te-IN-Standard-B",
    },
    "hi": {
        "language_code": "hi-IN",
        "name": "hi-IN-Chirp3-HD-Wavenet-A",
        "speaking_rate": 0.88,
        "pitch": -1.0,
        "fallback": "hi-IN-Neural2-A",
    },
}

def tts_to_file(text: str, out_path: Path, lang: str) -> None:
    if out_path.exists():
        return
    from google.cloud import texttospeech
    cfg = VOICE_CONFIG[lang]
    client = texttospeech.TextToSpeechClient()
    for voice_name in [cfg["name"], cfg["fallback"]]:
        try:
            resp = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=cfg["language_code"], name=voice_name),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=cfg["speaking_rate"],
                    pitch=cfg["pitch"],
                ),
            )
            out_path.write_bytes(resp.audio_content)
            print(f"  [tts:{lang}] {out_path.name}  ({voice_name})")
            return
        except Exception as e:
            print(f"  [WARN] {voice_name} failed: {e}")
    raise RuntimeError(f"All TTS voices failed for lang={lang}")
```

**To try a different voice:** change the `name` field.
**One Google account** works for all projects. No need to create separate accounts.
Full voice list: https://cloud.google.com/text-to-speech/docs/voices

---

## STEP 5 — Video assembly (ffmpeg)

```python
import subprocess

def audio_duration(p: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)])
    return float(out.strip())

def make_segment(img: Path, audio: Path, out: Path,
                 head_sil: float = 0.6, tail_sil: float = 1.5) -> None:
    """Longer silence than educational videos — bedtime pacing."""
    a_dur = audio_duration(audio)
    total = head_sil + a_dur + tail_sil
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{total:.3f}", "-i", str(img),
        "-i", str(audio),
        "-f", "lavfi", "-t", f"{head_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-f", "lavfi", "-t", f"{tail_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex", "[2:a][1:a][3:a]concat=n=3:v=0:a=1[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", str(out),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())
    print(f"  [seg] {out.name}")

def concat_mp4s(mp4s: list, out_mp4: Path) -> None:
    listfile = out_mp4.parent / "_concat.txt"
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in mp4s))
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
           "-movflags", "+faststart", str(out_mp4)]
    subprocess.run(cmd, check=True, capture_output=True)
    listfile.unlink()
    dur = audio_duration(out_mp4)
    sz  = out_mp4.stat().st_size / (1024*1024)
    print(f"\n  ✅ {out_mp4.name}  {dur:.0f}s ({dur/60:.1f} min)  {sz:.1f} MB")
```

---

## STEP 6 — "The Clever Crow" — full content reference

Classic story: Thirsty crow finds a pot with water too deep to reach.
Drops pebbles until water rises. Moral: clever thinking beats brute force.

### DALL-E image prompts for each slide

```python
SLIDES = [
    (
        "",  # eyebrow
        "The Clever Crow",  # title overlay
        # DALL-E scene prompt:
        "A majestic black crow perched on a moonlit banyan branch, glowing "
        "full moon behind, silver stars, warm golden light, title card feel",
        # narration:
        "Once upon a time, in a beautiful green forest in India, there lived "
        "a very clever crow. He was known for his bright eyes and quick mind. "
        "Tonight, we follow the crow on a very special day...",
    ),
    (
        "Part 1",
        "A Hot Summer Day",
        "A lush Indian forest under a blazing summer sun, dust on the path, "
        "wilting flowers, a small dry riverbed, warm amber and yellow tones",
        "It was the hottest day of summer. The sun blazed down on the forest "
        "like a great fire in the sky. The leaves drooped. The river had dried up. "
        "Every creature was searching for water. The crow was very, very thirsty.",
    ),
    (
        "Part 2",
        "The Thirsty Crow",
        "A tired crow with drooping wings flying over a dry Indian village, "
        "searching, looking down with worried bright eyes, golden sky",
        "The crow flew here and there, searching everywhere. He checked the "
        "riverbed — dry. He checked the old pond — empty. His wings grew heavy "
        "and his throat burned. But the clever crow did not give up.",
    ),
    (
        "Part 3",
        "Water! But So Far Down",
        "A crow peering into a tall clay pot sitting on dry ground, "
        "beak reaching in but too short to touch the water far below, "
        "late afternoon light, a few clouds",
        "At last! Near an old cottage, the crow spotted a tall clay pot. "
        "He flew down and looked inside. There was water — cool, beautiful water! "
        "But it was deep, deep at the bottom. No matter how far the crow stretched, "
        "he could not reach it. What would he do?",
    ),
    (
        "Part 4",
        "Think, Crow, Think",
        "A crow sitting quietly beside a clay pot, eyes closed in thought, "
        "a contemplative expression, soft evening light, pebbles nearby on the ground",
        "The crow sat very still. He did not panic. He thought carefully. "
        "He looked at the pot. He looked at his wings. He looked around him. "
        "And then — he looked down at the ground. Pebbles! Small round pebbles "
        "were scattered all around. An idea began to shine in his clever mind.",
    ),
    (
        "Part 5",
        "One Pebble at a Time",
        "A crow carefully picking up a small pebble with its beak, "
        "a clay pot nearby, water level very low inside, "
        "gentle determination in the crow's eyes, warm evening light",
        "The crow picked up one pebble with his beak. He walked to the pot "
        "and dropped it in. Plop. The water barely moved. He picked up another. "
        "Plop. And another. Plop plop plop. It was slow work. But the crow "
        "kept going, one pebble at a time, never stopping.",
    ),
    (
        "Part 6",
        "The Water is Rising!",
        "A crow excitedly dropping pebbles into a clay pot, "
        "the water level noticeably higher now, joy and hope on the crow's face, "
        "golden hour light, beautiful Indian forest background",
        "After many, many pebbles, something wonderful happened. The water began "
        "to rise! Slowly, slowly, it crept up toward the top. The crow worked "
        "faster now, his heart beating with excitement. Higher and higher the "
        "cool water climbed. The crow's clever plan was working.",
    ),
    (
        "Part 7",
        "One Last Pebble",
        "A crow holding the final pebble, looking at a nearly full clay pot, "
        "water very close to the top, a magical glowing light around the pot, "
        "triumphant but tender expression",
        "The crow picked up one last pebble. He held it for a moment, looking "
        "at the pot. The water was almost — almost — at the top. He took a deep "
        "breath. He dropped the pebble in. Plop. And the cool, clear water "
        "rose right up to the very brim.",
    ),
    (
        "Part 8",
        "Sweet Water, Sweet Victory",
        "A happy crow drinking water from a full clay pot, "
        "eyes closed with joy, evening sunlight, forest glowing warmly, "
        "relief and happiness, fireflies appearing in background",
        "The crow dipped his beak into the cool water and drank. Oh, how sweet "
        "it was! He drank and drank until his thirst was completely gone. "
        "He looked up at the golden sky, and felt very proud — not because he "
        "was strong, but because he had been patient and clever.",
    ),
    (
        "",
        "Goodnight, Little One",
        "A crow sleeping peacefully on a moonlit branch, "
        "bright stars, a soft glowing moon, fireflies, "
        "a cozy peaceful forest at night, gentle and dreamy",
        "And so, dear child, the clever crow taught us something important. "
        "When a problem feels too hard, sit quietly and think. Look around you. "
        "The answer is often right there, waiting. Now close your eyes, "
        "dream of cool water and kind forests. Goodnight.",
    ),
]
```

---

## STEP 7 — YouTube metadata

```
TITLE: The Clever Crow | Bedtime Story for Kids | Mitra AI Stories
DESCRIPTION:
A thirsty crow finds a pot of water — but the water is too deep to reach.
Watch how clever thinking and patience save the day in this beautiful classic fable.

This gentle bedtime story teaches children that calm thinking and persistence
always find a way — even when a problem seems impossible.

🌙 New story every day. Subscribe to Mitra AI Stories.
🦚 More stories → [playlist link]

TAGS: bedtime story, clever crow story, crow and pitcher, moral story for kids,
animated story, story in English, Mitra AI Stories, fable for children,
Aesop fable, bedtime stories for toddlers, short story with moral

CATEGORY: Education
LANGUAGE: English
THUMBNAIL: Crow drinking from pot, full moon background, title text large
```

---

## STEP 8 — Daily upload plan (1 video/day)

### 7-story starter queue
```
Mon  The Clever Crow (EN)
Tue  The Tortoise and the Hare (EN)
Wed  The Lion and the Mouse (EN)
Thu  The Ant and the Grasshopper (EN)
Fri  The Fox and the Grapes (EN)
Sat  The Kind Elephant (EN)
Sun  ఒంటె మరియు నక్క (Telugu)
```

### Daily workflow (15 min total)
1. Run script: `python scripts/generate_story_<next>.py` (~10 min, mostly waiting for TTS+DALL-E)
2. YouTube Studio → Upload → paste `youtube_metadata.txt`
3. Set thumbnail (use `slide-01.jpg` or `slide-09.jpg` — the happy resolution)
4. Schedule for 8pm local time

### To automate YouTube upload (optional later)
Ask Copilot: *"Add YouTube Data API v3 upload to the story generator."*
YouTube API free quota: 6 uploads/day — enough for daily schedule.
