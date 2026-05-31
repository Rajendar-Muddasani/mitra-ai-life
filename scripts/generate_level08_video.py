"""
Generate Level 8 English narrated intro video.
Topic: AI for Business — Grow Your Business with AI by Your Side.
8 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-08-intro-charon.mp4
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

ROOT      = Path(__file__).parent.parent
SCENES    = ROOT / "content/assets/scenes"
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l8{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-08-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l8-s01-hero.jpg",
        "text": (
            "Welcome to Level 8 — AI for Business. "
            "Grow your business with AI by your side. "
            "Write better promotions. Handle customers confidently. Market smarter. Plan with clarity. "
            "No tech skills needed — just your phone and a good prompt."
        ),
    },
    {
        "image": "img-l8-s02-ravi-whatsapp.jpg",
        "text": (
            "Ravi runs a mobile accessories shop in Hyderabad. "
            "He uses AI to write WhatsApp promotions that actually get replies. "
            "He just tells AI about his new offer, and gets a message ready to send. "
            "His sales have gone up, and his customers remember him."
        ),
    },
    {
        "image": "img-l8-s03-meena-tiffin.jpg",
        "text": (
            "Meena runs a tiffin service. "
            "She uses AI to answer customer questions quickly and politely, even when she is busy. "
            "AI helps her handle complaints, send menu updates, and keep her regulars happy. "
            "Her business runs smoother, and she has more time for her family."
        ),
    },
    {
        "image": "img-l8-s04-suresh-complaint.jpg",
        "text": (
            "Suresh owns a small electronics repair shop. "
            "He uses AI to handle tough customer complaints. "
            "AI suggests calm, professional replies that turn angry customers into loyal ones. "
            "Suresh now feels confident, even in difficult situations."
        ),
    },
    {
        "image": "img-l8-s05-divya-instagram.jpg",
        "text": (
            "Divya is a home baker. "
            "She uses AI to create Instagram posts that look and sound professional. "
            "She just shares her product photo and a few details — AI writes the caption and hashtags. "
            "Her followers are growing, and she gets more orders every week."
        ),
    },
    {
        "image": "img-l8-s06-ravi-calendar.jpg",
        "text": (
            "Ravi uses AI to plan his monthly sales calendar. "
            "He tells AI about upcoming festivals and stock, and gets a clear plan for promotions. "
            "Now he never misses a sales opportunity, and his business is more organised."
        ),
    },
    {
        "image": "img-l8-s07-practice.jpg",
        "text": (
            "In this level, you will practise four real business scenarios: writing WhatsApp promotions, handling customer questions, replying to complaints, and creating Instagram posts. "
            "You will learn how to use AI as your business partner, not just a tool."
        ),
    },
    {
        "image": "img-l8-s08-celebration.jpg",
        "text": (
            "That is Level 8. You have learned to use AI for your business. "
            "Your promotions, your customer replies, your social media — all powered by AI. "
            "Scroll down to start practising. "
            "See you in Level 9, where you will learn to use AI for your career."
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
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-08-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
