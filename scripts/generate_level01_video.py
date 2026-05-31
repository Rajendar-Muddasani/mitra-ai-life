"""
Level 1 Intro Video Generator
Produces: content/assets/videos/level-01-intro-charon.mp4
Runtime: ~90 seconds, 1280×720, narrated slideshow

Uses:
- Google Cloud TTS (en-US-Chirp3-HD-Charon) for narration
- moviepy + imageio_ffmpeg (no system ffmpeg needed)
- L1 scene images from content/assets/scenes/

Run: .venv/bin/python scripts/generate_level01_video.py
"""

import os
import sys
import urllib.request
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / f"audio_tmp_l1{VERSION_SUFFIX}"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / f"level-01-intro{VERSION_SUFFIX}.mp4"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Script: 10 scenes, ~90 seconds total ────────────────────────────────────
# Each scene: (image_filename, narration_text, duration_hint_seconds)
SCENES = [
    (
        "img-s01-hero.jpg",
        "Welcome to Level 1 of Mitra AI Life. "
        "Meet Ravi — a shopkeeper from Hyderabad. "
        "He needs to write a letter to his son's school. But he is stuck.",
        9,
    ),
    (
        "img-s03-frustrated.jpg",
        "45 minutes. A blank page. "
        "Ravi has been trying to write a simple formal letter — "
        "and he just cannot start.",
        8,
    ),
    (
        "img-s04-priya-entering.jpg",
        "His neighbour Priya walks in. She says — try AI. "
        "Ravi is sceptical. But he is desperate. So he tries.",
        8,
    ),
    (
        "img-s07-typing-phone.jpg",
        "Ravi picks up his phone and types his problem into AI — "
        "in simple words, in his own way. "
        "No special training. No English degree needed.",
        9,
    ),
    (
        "img-s08-ravi-amazed.jpg",
        "In under 2 minutes — the letter is ready. "
        "Perfect English. Right tone. Polite and professional. "
        "Ravi just changed his name and date. Done.",
        9,
    ),
    (
        "img-s06-library-analogy.jpg",
        "So — what exactly is AI? "
        "Think of a giant library that read everything ever written — "
        "every book, every article, every conversation — "
        "and can answer any question, instantly.",
        10,
    ),
    (
        "img-s09-priya-kitchen.jpg",
        "Priya asks AI in Telugu for a healthy snack recipe for her diabetic mother-in-law. "
        "AI replies in Telugu — with a full recipe, in seconds.",
        8,
    ),
    (
        "img-s10-rahul-studying.jpg",
        "Rahul asks AI to explain photosynthesis in simple words. "
        "AI explains it using a chapati-making analogy. "
        "In 5 minutes, Rahul understood what his textbook could not teach in a week.",
        9,
    ),
    (
        "img-s11-safety-warning.jpg",
        "But remember — AI is a helper, not a god. "
        "It can be wrong. Always check important facts. "
        "And never share your Aadhaar number, bank details, or passwords with any AI.",
        10,
    ),
    (
        "img-s13-celebration.jpg",
        "That is Level 1. "
        "You now know what AI is, how to use it, and how to stay safe. "
        "The quiz is just ahead. Ready for your first try? Let us go!",
        9,
    ),
]

# ── Step 1: Generate TTS audio for each scene ────────────────────────────────
print("Step 1: Generating TTS narration audio...")
audio_files = []
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

for i, (img, text, _) in enumerate(SCENES, start=1):
    audio_path = AUDIO_DIR / f"scene-{i:02d}.mp3"
    if audio_path.exists():
        print(f"  [SKIP] Scene {i} audio already exists")
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

# ── Step 2: Build video with moviepy ────────────────────────────────────────
print("Step 2: Building video...")

# Set imageio_ffmpeg binary path so moviepy can find it
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

def make_scene_clip(img_path: Path, audio_path: Path, scene_index: int, scene_text: str):
    """Create a video clip: image fills frame, audio determines duration."""
    # Load audio first to get real duration
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration + 0.4   # tiny tail silence

    # Open and fill-fit the image to 1280×720
    img = Image.open(img_path).convert("RGB")
    img_w, img_h = img.size
    scale = max(VIDEO_W / img_w, VIDEO_H / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # Centre-crop
    left = (new_w - VIDEO_W) // 2
    top  = (new_h - VIDEO_H) // 2
    img  = img.crop((left, top, left + VIDEO_W, top + VIDEO_H))

    # Slight bottom gradient overlay for legibility
    gradient = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(gradient)
    for y in range(VIDEO_H // 2, VIDEO_H):
        alpha = int(180 * ((y - VIDEO_H // 2) / (VIDEO_H // 2)))
        draw.line([(0, y), (VIDEO_W, y)], fill=(0, 0, 0, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(gradient, (0, 0), gradient)
    img_final = img_rgba.convert("RGB")

    frame = np.array(img_final)

    # Image clip
    clip = ImageClip(frame, duration=duration)

    # Subtle zoom-in (Ken Burns): scale from 1.0 to 1.04 over duration
    def zoom_frame(get_frame, t):
        f = get_frame(t)
        scale = 1.0 + 0.04 * (t / duration)
        h, w = f.shape[:2]
        new_w2 = int(w * scale)
        new_h2 = int(h * scale)
        img2 = Image.fromarray(f).resize((new_w2, new_h2), Image.LANCZOS)
        ox = (new_w2 - w) // 2
        oy = (new_h2 - h) // 2
        return np.array(img2.crop((ox, oy, ox + w, oy + h)))

    clip = clip.transform(zoom_frame, apply_to="video")
    clip = clip.with_audio(audio)

    return clip

clips = []
for i, (img_name, narr_text, _) in enumerate(SCENES, start=1):
    img_path   = SCENES_DIR / img_name
    audio_path = audio_files[i - 1]
    print(f"  [{i}/{len(SCENES)}] Compositing scene: {img_name}")
    clip = make_scene_clip(img_path, audio_path, i, narr_text)
    clips.append(clip)

print("\nStep 3: Concatenating clips and writing video...")
final = concatenate_videoclips(clips, method="compose")

final.write_videofile(
    str(VIDEO_OUT),
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"),
    remove_temp=True,
    logger="bar",
)

print(f"\nDone! Video saved to: {VIDEO_OUT}")
total = sum(c.duration for c in clips)
print(f"Total duration: {total:.1f} seconds")
print(f"File size: {VIDEO_OUT.stat().st_size / 1024 / 1024:.1f} MB")
