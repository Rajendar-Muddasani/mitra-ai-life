"""
Generate Level 10 English narrated intro video.
Topic: AI Safety and Society - Use AI Wisely. Stay Safe.
8 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-10-intro-charon.mp4
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
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l10{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-10-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l10-s01-hero.jpg",
        "text": (
            "Welcome to Level 10 - AI Safety and Society. "
            "This is the final step in your AI Daily Life journey. "
            "You have learned how to use AI for daily help, work, business, and income. "
            "Now you will learn how to use AI wisely, protect your family, and stay safe."
        ),
    },
    {
        "image": "img-l10-s02-deepfake.jpg",
        "text": (
            "Deepfakes are fake photos, videos, or audio created with AI. "
            "They can look real, but still be false. "
            "If a shocking video appears on WhatsApp or social media, do not forward it immediately. "
            "Pause, check the source, and ask: who benefits if I believe this?"
        ),
    },
    {
        "image": "img-l10-s03-fact-check.jpg",
        "text": (
            "Misinformation spreads fast, especially during elections, emergencies, health scares, and local conflicts. "
            "AI can help you fact-check, but you must still use trusted sources. "
            "Compare with official websites, reliable news, and direct confirmation before taking action. "
            "Being careful is not slow - it is smart."
        ),
    },
    {
        "image": "img-l10-s04-voice-clone-scam.jpg",
        "text": (
            "Voice cloning scams are becoming common. "
            "A caller may sound like your child, friend, or relative, and ask for urgent money. "
            "Do not panic. Call the person back on their known number. "
            "Use a family safety question. Never send money only because a voice sounded familiar."
        ),
    },
    {
        "image": "img-l10-s05-consent-privacy.jpg",
        "text": (
            "Privacy matters. Do not upload Aadhaar cards, bank details, medical reports, children's photos, or private family information into random AI tools. "
            "Before sharing any data, ask: do I need to share this? Can I remove names and numbers? "
            "Good AI use starts with protecting personal information."
        ),
    },
    {
        "image": "img-l10-s06-meera-integrity.jpg",
        "text": (
            "Meera uses AI for study and work, but she does not copy blindly. "
            "She checks facts, rewrites in her own words, and gives credit when needed. "
            "AI can support your thinking, but it should not replace your honesty. "
            "Integrity is part of being a responsible AI user."
        ),
    },
    {
        "image": "img-l10-s07-5-rules.jpg",
        "text": (
            "In this level, you will practise five safety rules: "
            "pause before forwarding, verify before believing, protect private data, check urgent money requests, and use AI honestly. "
            "These five habits can protect your family, your money, your reputation, and your community."
        ),
    },
    {
        "image": "img-l10-s08-celebration.jpg",
        "text": (
            "That is Level 10. You have completed the English AI Daily Life journey. "
            "You can now use AI for help, learning, work, business, income, and safety. "
            "Scroll down to finish the final practice. "
            "Congratulations - you are ready to use AI with confidence and care."
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
    scale = max(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - W) // 2
    top = (nh - H) // 2
    img = img.crop((left, top, left + W, top + H))
    frame0 = np.array(img)

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
    print(f"\nVideo ready: {OUT}")
    print(f"   Duration: ~{dur_s}s")
    print(f"\nNext - upload to S3:")
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-10-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
