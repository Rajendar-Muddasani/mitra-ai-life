"""
Level 2 English Intro Video Generator
Produces: content/assets/videos/level-02-intro-charon.mp4
Runtime: ~100 seconds, 1280×720, narrated slideshow

Uses:
- Google Cloud TTS (en-US-Chirp3-HD-Charon) for narration
- moviepy + imageio_ffmpeg
- L2 scene images from content/assets/scenes/ (img-l2-s01 through img-l2-s10)

Run: .venv/bin/python scripts/generate_level02_video.py
"""

import os
from pathlib import Path

# ── Load .env ────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.parent
SCENES_DIR = ROOT / "content" / "assets" / "scenes"
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / f"audio_tmp_l2{VERSION_SUFFIX}"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / f"level-02-intro{VERSION_SUFFIX}.mp4"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Script: 10 scenes, ~100 seconds total ────────────────────────────────────
SCENES = [
    (
        "img-l2-s01-hero.jpg",
        "Welcome to Level 2 of Mitra AI Life — Daily Help. "
        "You have already learned what AI is. Now it is time to put it to real, daily use. "
        "The people you met in Level 1? They are back — and their lives just got easier.",
        10,
    ),
    (
        "img-l2-s02-ravi-phone.jpg",
        "Ravi needs to message his supplier about a delayed order. "
        "He cannot write English well. He types his problem in simple words — "
        "and AI replies with a perfectly worded professional message in seconds.",
        9,
    ),
    (
        "img-l2-s03-supplier-reply.jpg",
        "Ravi copies the message, sends it to his supplier, and gets a positive reply the same day. "
        "He did not need to hire anyone. He did not need to visit a cybercafe. "
        "He did it himself, on his phone, in under 5 minutes.",
        9,
    ),
    (
        "img-l2-s04-priya-grocery.jpg",
        "Priya asks AI to plan a healthy weekly menu for a family of four — "
        "on a budget of 1,500 rupees — using vegetables available in the local market. "
        "AI gives her a full 7-day plan, with a shopping list included.",
        9,
    ),
    (
        "img-l2-s05-market-scene.jpg",
        "She takes the AI-generated shopping list to the vegetable market. "
        "Every item is local, seasonal, and within budget. "
        "The family eats well. No food is wasted. She saved 300 rupees compared to last week.",
        9,
    ),
    (
        "img-l2-s06-rahul-exam.jpg",
        "Rahul has exams in two weeks. He asks AI to make a revision schedule — "
        "subject by subject, day by day — given the time he has available. "
        "AI creates a detailed, realistic plan that actually fits his life.",
        9,
    ),
    (
        "img-l2-s07-prompt-tips.jpg",
        "Here is the key skill in this level: the better your prompt, the better your answer. "
        "Tell AI who you are, what you need, and any important details. "
        "Be specific. Use simple language. You are having a conversation, not filling a form.",
        9,
    ),
    (
        "img-l2-s08-complaint-letter.jpg",
        "Priya's neighbour has a problem with her electricity bill — overcharged by 800 rupees. "
        "She asks AI to write a formal complaint letter to the electricity board. "
        "Professional, polite, and ready to send in under one minute.",
        9,
    ),
    (
        "img-l2-s09-practice-arena.jpg",
        "In this level you will practice five real tasks: "
        "writing a professional message, planning a grocery budget, "
        "creating a study schedule, drafting a complaint, and writing a WhatsApp reply. "
        "Every task is something you may actually need this week.",
        10,
    ),
    (
        "img-l2-s10-celebration.jpg",
        "That is Level 2. "
        "AI is now your daily helper — for writing, planning, studying, and solving small problems. "
        "Complete the quiz below to earn your Level 2 certificate. You are doing great — let us go!",
        9,
    ),
]

# ── Step 1: Generate TTS audio ────────────────────────────────────────────────
print("Step 1: Generating TTS narration audio...")
audio_files = []

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

for i, (img, text, _) in enumerate(SCENES, start=1):
    audio_path = AUDIO_DIR / f"scene-{i:02d}.mp3"
    if audio_path.exists():
        print(f"  [{i}/{len(SCENES)}] Skipping (exists): {audio_path.name}")
    else:
        print(f"  [{i}/{len(SCENES)}] TTS: {text[:60]}...")
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text),
            voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANGUAGE_CODE, name=TTS_VOICE),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=TTS_SPEAKING_RATE,
            ),
            timeout=45,
        )
        audio_path.write_bytes(response.audio_content)
        print(f"    Saved: {audio_path.name}")

    audio_files.append(audio_path)

print(f"  Audio ready: {len(audio_files)} files\n")

# ── Step 2: Build video ────────────────────────────────────────────────────────
print("Step 2: Building video...")

import imageio_ffmpeg
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_bin
print(f"  Using ffmpeg: {ffmpeg_bin}")

from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import numpy as np

VIDEO_W, VIDEO_H = 1280, 720
FPS = 24


def make_scene_clip(img_name, audio_path):
    img_path = SCENES_DIR / img_name

    # Fill-fit + centre-crop to VIDEO_W × VIDEO_H
    pil = Image.open(img_path).convert("RGB")
    iw, ih = pil.size
    scale = max(VIDEO_W / iw, VIDEO_H / ih)
    pil = pil.resize((int(iw * scale), int(ih * scale)), Image.LANCZOS)
    left = (pil.width  - VIDEO_W) // 2
    top  = (pil.height - VIDEO_H) // 2
    pil  = pil.crop((left, top, left + VIDEO_W, top + VIDEO_H))
    frame = np.array(pil)

    audio    = AudioFileClip(str(audio_path))
    duration = audio.duration + 0.4

    clip = ImageClip(frame, duration=duration)

    # Ken Burns zoom: 1.0 → 1.04
    def zoom_frame(get_frame, t):
        f  = get_frame(t)
        s  = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw, nh = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw, nh), Image.LANCZOS)
        ox, oy = (nw - w) // 2, (nh - h) // 2
        return np.array(zoomed.crop((ox, oy, ox + w, oy + h)))

    clip = clip.transform(zoom_frame, apply_to="video")
    clip = clip.with_audio(audio)
    return clip


print("  Building clips...")
clips = []
for i, ((img, _, _), audio_path) in enumerate(zip(SCENES, audio_files), start=1):
    print(f"  [{i}/{len(SCENES)}] {img}")
    clips.append(make_scene_clip(img, audio_path))

print("\n  Concatenating clips...")
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

print(f"\n✅ Video ready: {VIDEO_OUT}")
print(f"   Duration: ~{final.duration:.0f}s")
print(f"\nNext — upload to S3:")
print(f"  source .env && aws s3 cp {VIDEO_OUT} s3://mitra-ai-life-assets/videos/level-02-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")
