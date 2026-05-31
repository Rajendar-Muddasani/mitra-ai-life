"""
Generate Level 5 English narrated intro video.
Topic: Life Upgrade — Smarter Budget. Better Decisions. Happier Family.
8 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-05-intro-charon.mp4
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

# ── paths ────────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
SCENES    = ROOT / "content/assets/scenes"
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l5{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-05-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l5-s01-hero.jpg",
        "text": (
            "Welcome to Level 5 — Life Upgrade. "
            "This level shows you how AI can improve your everyday home life: "
            "budget planning, children's homework, travel, insurance comparison, "
            "and daily habits. Real improvements, starting today."
        ),
    },
    {
        "image": "img-l5-s02-lakshmi-budget.jpg",
        "text": (
            "Lakshmi manages the household budget for her family of four. "
            "She tells AI: My monthly income is thirty thousand rupees. "
            "Help me plan a budget that covers rent, groceries, school fees, "
            "and saves at least three thousand rupees each month. "
            "AI gives her a clear plan in seconds — something that used to take her hours."
        ),
    },
    {
        "image": "img-l5-s03-ramaiah-homework.jpg",
        "text": (
            "Ramaiah's daughter is in Class 7 and struggling with fractions. "
            "He asks AI: Explain fractions to a twelve-year-old using a pizza example. "
            "Then give five practice questions. "
            "AI explains it simply, and his daughter understands in one evening."
        ),
    },
    {
        "image": "img-l5-s04-kavitha-travel.jpg",
        "text": (
            "Kavitha's family wants to visit Ooty for five days. "
            "She asks AI: Plan a five-day Ooty trip for a family with two children "
            "under ten. Budget is ten thousand rupees including travel. "
            "AI gives a day-by-day itinerary with budget breakdown — better than any travel agent."
        ),
    },
    {
        "image": "img-l5-s05-srinivas-compare.jpg",
        "text": (
            "Srinivas is renewing his car insurance. "
            "He asks AI: Explain the difference between third-party and comprehensive insurance "
            "in simple terms. Which one is better for a five-year-old car? "
            "AI explains clearly and helps him make a confident decision, saving him money."
        ),
    },
    {
        "image": "img-l5-s06-meera-habits.jpg",
        "text": (
            "Meera wants to build better daily habits — morning exercise, less screen time, "
            "and more family time. She asks AI: Create a simple daily routine "
            "for a working mother with two kids. Make it realistic, not perfect. "
            "The routine AI suggests actually fits her life."
        ),
    },
    {
        "image": "img-l5-s07-practice.jpg",
        "text": (
            "In this level you will practise five real life tasks: "
            "building a household budget, helping a child with homework, "
            "planning a family trip, comparing insurance options, "
            "and creating a personal daily routine. "
            "Every task uses your own numbers and your own situation."
        ),
    },
    {
        "image": "img-l5-s08-celebration.jpg",
        "text": (
            "That is Level 5. AI is now helping your whole family — "
            "not just you. Smarter budget, better learning, happier trips. "
            "Scroll down to begin your five life tasks. "
            "See you in Level 6, where you become a true AI power user."
        ),
    },
]

def generate_audio():
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    print("Step 1: Generating TTS narration audio...")
    for i, sc in enumerate(SCENES_DATA, 1):
        path = AUDIO_DIR / f"scene-{i:02d}.mp3"
        if path.exists():
            print(f"  [{i}/{len(SCENES_DATA)}] Skipping (exists): {path.name}")
            continue
        preview = sc["text"][:60].replace("\n", " ")
        print(f"  [{i}/{len(SCENES_DATA)}] TTS: {preview}...")
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=sc["text"]),
            voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANGUAGE_CODE, name=TTS_VOICE),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=TTS_SPEAKING_RATE,
            ),
            timeout=45,
        )
        path.write_bytes(response.audio_content)
        print(f"    Saved: {path.name}")
    print(f"  Audio ready: {len(SCENES_DATA)} files\n")

def make_zoom_clip(img_path: Path, duration: float):
    img = Image.open(img_path).convert("RGB")
    iw, ih = img.size
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(img, ((W - nw) // 2, (H - nh) // 2))
    frame0 = np.array(canvas)

    def zoom_frame(get_frame, t):
        f = get_frame(t)
        s = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw2, nh2 = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw2, nh2), Image.LANCZOS)
        ox2, oy2 = (nw2 - w) // 2, (nh2 - h) // 2
        return np.array(zoomed.crop((ox2, oy2, ox2 + w, oy2 + h)))

    clip = ImageClip(frame0, duration=duration)
    return clip.transform(zoom_frame, apply_to="video")

def build_video():
    import moviepy
    print("Step 2: Building video...")
    print(f"  Using ffmpeg: {moviepy.config.FFMPEG_BINARY}")
    print("  Building clips...")
    clips = []
    for i, sc in enumerate(SCENES_DATA, 1):
        print(f"  [{i}/{len(SCENES_DATA)}] {sc['image']}")
        audio = AudioFileClip(str(AUDIO_DIR / f"scene-{i:02d}.mp3"))
        dur   = audio.duration + 0.4
        clip  = make_zoom_clip(SCENES / sc["image"], dur).with_audio(audio)
        clips.append(clip)

    print("\n  Concatenating clips...")
    final = concatenate_videoclips(clips, method="compose")
    print(f"  Writing: {OUT}")
    final.write_videofile(
        str(OUT), fps=FPS, codec="libx264", audio_codec="aac",
        temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"),
        remove_temp=True, logger="bar",
    )
    dur_s = int(final.duration)
    print(f"\n✅ Video ready: {OUT}")
    print(f"   Duration: ~{dur_s}s")
    print(f"\nNext — upload to S3:")
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-05-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
