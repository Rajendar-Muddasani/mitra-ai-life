"""
Level 1 Telugu Intro Video Generator
Produces: content/assets/videos/level-01-intro-te.mp4
Runtime: ~100 seconds, 1280×720, narrated slideshow in Telugu

Uses:
- OpenAI TTS (tts-1, voice=nova) for Telugu narration
- moviepy + imageio_ffmpeg (no system ffmpeg needed)
- Same L1 scene images from content/assets/scenes/

Run: .venv/bin/python scripts/generate_level01_video_te.py
"""

import os
import sys
import time
import urllib.request
from pathlib import Path

# ── Load .env ────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.parent
SCENES_DIR = ROOT / "content" / "assets" / "scenes"
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-01-intro-te.mp4"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Script: 10 scenes in Telugu, ~100 seconds total ─────────────────────────
SCENES = [
    (
        "img-s01-hero.jpg",
        "Mitra AI Life యొక్క స్థాయి 1 కి స్వాగతం. "
        "ఇతను రవి — హైదరాబాద్ లో ఒక చిన్న కిరాణా దుకాణదారు. "
        "అతను తన కొడుకు school కి ఒక letter రాయాలి. కానీ ఎలా మొదలుపెట్టాలో తెలియడం లేదు.",
        10,
    ),
    (
        "img-s03-frustrated.jpg",
        "45 నిమిషాలు గడిచాయి. పేపర్ ఖాళీగా ఉంది. "
        "ఒక సాధారణ formal letter రాయడానికి రవి చాలా కష్టపడుతున్నాడు — "
        "ఎక్కడ మొదలుపెట్టాలో అర్థం కావడం లేదు.",
        9,
    ),
    (
        "img-s04-priya-entering.jpg",
        "అతని neighbor ప్రియ వస్తుంది. ఆమె చెప్తుంది — AI try చేయి. "
        "రవికి అనుమానంగా ఉంది. కానీ ప్రయత్నించాల్సిన అవసరం ఉంది. అందుకే try చేశాడు.",
        9,
    ),
    (
        "img-s07-typing-phone.jpg",
        "రవి తన phone తీసి AI కి తన problem type చేశాడు — "
        "simple words లో, తన భాషలో. "
        "Special training అవసరం లేదు. English degree అవసరం లేదు.",
        9,
    ),
    (
        "img-s08-ravi-amazed.jpg",
        "2 నిమిషాల్లో — letter ready అయింది. "
        "Perfect English. సరైన tone. Polite మరియు professional. "
        "రవి ఒక్క పేరు మరియు date మాత్రమే మార్చాడు. పని అయిపోయింది.",
        9,
    ),
    (
        "img-s06-library-analogy.jpg",
        "అయితే — AI అంటే ఏమిటి? "
        "ఒక చాలా పెద్ద library గురించి imagine చేయండి — "
        "అది ప్రపంచంలో రాసిన అన్ని పుస్తకాలు, articles, conversations చదివింది — "
        "మరియు ఏ question అడిగినా వెంటనే జవాబు ఇవ్వగలదు.",
        11,
    ),
    (
        "img-s09-priya-kitchen.jpg",
        "ప్రియ తన diabetic అత్తమ్మ కోసం healthy snack recipe Telugu లో AI అడిగింది. "
        "AI Telugu లోనే జవాబు ఇచ్చింది — పూర్తి recipe తో, కొన్ని seconds లోనే.",
        9,
    ),
    (
        "img-s10-rahul-studying.jpg",
        "రాహుల్ photosynthesis ని simple words లో explain చేయమని AI అడిగాడు. "
        "AI చపాతీ example తో explain చేసింది. "
        "5 నిమిషాల్లో రాహుల్ అర్థం చేసుకున్నాడు — textbook లో week అయినా అర్థం కాలేదు.",
        10,
    ),
    (
        "img-s11-safety-warning.jpg",
        "కానీ గుర్తుంచుకోండి — AI ఒక helper, సర్వజ్ఞుడు కాదు. "
        "తప్పులు చేయవచ్చు. ముఖ్యమైన విషయాలు మళ్ళీ check చేయండి. "
        "మీ Aadhaar number, bank details, లేదా passwords ఏ AI తో share చేయకండి.",
        10,
    ),
    (
        "img-s13-celebration.jpg",
        "అది స్థాయి 1. "
        "AI అంటే ఏమిటో, ఎలా వాడాలో, సురక్షితంగా ఉండటం ఎలాగో ఇప్పుడు మీకు తెలుసు. "
        "Quiz వెంటనే వస్తుంది. మీ మొదటి try కి ready గా ఉన్నారా? పదండి!",
        10,
    ),
]

# ── Step 1: Generate TTS audio for each scene ────────────────────────────────
print("Step 1: Telugu TTS narration audio generate అవుతోంది...")
audio_files = []

for i, (img, text, _) in enumerate(SCENES, start=1):
    audio_path = AUDIO_DIR / f"scene-{i:02d}.mp3"
    if audio_path.exists():
        print(f"  [SKIP] Scene {i} audio already exists")
    else:
        print(f"  [{i}/{len(SCENES)}] TTS: {text[:50]}...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",        # nova handles Telugu text well
            input=text,
            speed=0.92,          # slightly slower for Telugu clarity
        )
        response.stream_to_file(str(audio_path))
        print(f"    Saved: {audio_path.name}")
        if i < len(SCENES):
            time.sleep(1)

    audio_files.append(audio_path)

print(f"  Audio ready: {len(audio_files)} files\n")

# ── Step 2: Build video with moviepy ────────────────────────────────────────
print("Step 2: Video build చేస్తున్నాం...")

import imageio_ffmpeg
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_bin
print(f"  Using ffmpeg: {ffmpeg_bin}")

from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    TextClip,
)
from PIL import Image, ImageFilter
import numpy as np

VIDEO_W, VIDEO_H = 1280, 720
FPS = 24

def make_clip(img_name, audio_path, scene_idx):
    img_path = SCENES_DIR / img_name

    # Load & resize image
    pil_img = Image.open(img_path).convert("RGB")
    pil_img = pil_img.resize((VIDEO_W, VIDEO_H), Image.LANCZOS)
    frame = np.array(pil_img)

    audio = AudioFileClip(str(audio_path))
    duration = audio.duration + 0.5  # small trailing pause

    clip = ImageClip(frame, duration=duration).with_fps(FPS)
    clip = clip.with_audio(audio)

    # Subtle Ken Burns zoom: 1.0 → 1.06
    def zoom(t):
        scale = 1.0 + 0.06 * (t / duration)
        new_w = int(VIDEO_W * scale)
        new_h = int(VIDEO_H * scale)
        pil_z = Image.fromarray(frame).resize((new_w, new_h), Image.LANCZOS)
        x = (new_w - VIDEO_W) // 2
        y = (new_h - VIDEO_H) // 2
        cropped = np.array(pil_z)[y:y+VIDEO_H, x:x+VIDEO_W]
        return cropped

    clip = clip.image_transform(zoom)

    # Level counter overlay (bottom-left)
    label = TextClip(
        text=f"స్థాయి 1  •  {scene_idx}/{len(SCENES)}",
        font_size=22,
        color="white",
        font="DejaVu-Sans",
    ).with_duration(duration).with_position((30, VIDEO_H - 50))

    return CompositeVideoClip([clip, label])


print("  Clips build చేస్తున్నాం...")
clips = []
for i, ((img, _, _), audio_path) in enumerate(zip(SCENES, audio_files), start=1):
    print(f"  [{i}/{len(SCENES)}] {img}")
    clips.append(make_clip(img, audio_path, i))

print("\n  Clips concatenate చేస్తున్నాం...")
final = concatenate_videoclips(clips, method="compose")

print(f"  Writing: {VIDEO_OUT}")
final.write_videofile(
    str(VIDEO_OUT),
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"),
    remove_temp=True,
    logger="bar",
)

print(f"\n✅ Telugu video ready: {VIDEO_OUT}")
print(f"   Duration: ~{final.duration:.0f}s")
print(f"\nNext: upload to S3 with:")
print(f"  source .env && aws s3 cp {VIDEO_OUT} s3://mitra-ai-life-assets/videos/level-01-intro-te.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")
