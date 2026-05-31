"""
Generate Level 6 English narrated intro video.
Topic: Power User — Same AI. 10× the Results. Half the Time.
8 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-06-intro-charon.mp4
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
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l6{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-06-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l6-s01-hero.jpg",
        "text": (
            "Welcome to Level 6 — Power User. "
            "You already know how to use AI. This level teaches you how to use it like an expert. "
            "Same AI, ten times the results, half the time. "
            "Five habits that separate power users from everyone else."
        ),
    },
    {
        "image": "img-l6-s02-pradeep-routine.jpg",
        "text": (
            "Pradeep starts every workday with an AI routine. "
            "He has a saved prompt that says: Summarise my tasks for today, "
            "identify the top three priorities, and suggest one thing I can delegate. "
            "This single routine saves him thirty minutes every morning. "
            "Power users build routines, not one-off questions."
        ),
    },
    {
        "image": "img-l6-s03-ananya-structure.jpg",
        "text": (
            "Ananya noticed that AI gives better answers when she structures her request. "
            "Instead of asking: Tell me about marketing, "
            "she says: You are a marketing expert. Give me five ideas to promote a small tea shop "
            "in Hyderabad with a budget under two thousand rupees. "
            "Role plus context plus constraint — that is the power user formula."
        ),
    },
    {
        "image": "img-l6-s04-venkat-sheets.jpg",
        "text": (
            "Venkat runs a small hardware store. "
            "He asks AI to generate an Excel formula that automatically calculates "
            "profit margin for each product. "
            "AI writes the formula, explains it, and Venkat's spreadsheet is now automated. "
            "You do not need to be a tech expert — you need the right prompt."
        ),
    },
    {
        "image": "img-l6-s05-divya-templates.jpg",
        "text": (
            "Divya runs a tutoring centre. She asked AI once to create a template "
            "for parent progress reports. Now she uses that template every month. "
            "She fills in the student name and scores — AI formats the rest. "
            "Templates are how power users make AI work for them repeatedly, not just once."
        ),
    },
    {
        "image": "img-l6-s06-rajan-limits.jpg",
        "text": (
            "Rajan is a doctor. He uses AI for research summaries and patient education materials — "
            "but he never trusts AI for diagnoses. "
            "Knowing when not to use AI is itself a power skill. "
            "Health, legal, and financial decisions always need a human expert. "
            "AI is a tool, not a replacement for judgement."
        ),
    },
    {
        "image": "img-l6-s07-practice.jpg",
        "text": (
            "In this level you will build five power-user systems: "
            "a personal daily AI routine, a role-context-constraint prompt, "
            "a spreadsheet formula using AI, a reusable template for your work, "
            "and a personal list of situations where you will not rely on AI alone. "
            "Each one is a system you will use for years."
        ),
    },
    {
        "image": "img-l6-s08-celebration.jpg",
        "text": (
            "That is Level 6. You are now a power user. "
            "Routines, structures, spreadsheets, templates, and clear limits — "
            "these are your five weapons. "
            "Scroll down to build your five systems. "
            "See you in Level 7, where you start building with AI."
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
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-06-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
