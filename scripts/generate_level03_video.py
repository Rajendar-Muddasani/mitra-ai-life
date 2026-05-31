"""
Generate Level 3 English narrated intro video.
Topic: Smart Basics — Use AI smarter, not just more.
9 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-03-intro-charon.mp4
"""

import os, sys
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips, CompositeAudioClip

# ── paths ────────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
SCENES    = ROOT / "content/assets/scenes"
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l3{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-03-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ── video spec ───────────────────────────────────────────────────────
W, H  = 1280, 720
FPS   = 24

# ── narration script ─────────────────────────────────────────────────
SCENES_DATA = [
    {
        "image": "img-l3-s01-hero.jpg",
        "text":  (
            "Welcome to Level 3 — Smart Basics. "
            "Getting an AI answer is easy. Knowing whether to trust it — that is a skill. "
            "This level teaches you to think clearly about what AI gives you."
        ),
    },
    {
        "image": "img-l3-s02-arjun-mistake.jpg",
        "text":  (
            "Arjun asked AI about a medicine dosage. The AI gave a confident answer — "
            "but Arjun checked with a doctor and found it was wrong. "
            "AI can make mistakes, especially for health, legal, and financial questions. "
            "Always verify important information."
        ),
    },
    {
        "image": "img-l3-s03-meena-factcheck.jpg",
        "text":  (
            "Meena learned a simple trick. She asks AI: Can you show me where to verify this? "
            "AI then gives links and sources she can cross-check. "
            "This one habit makes you a much smarter AI user."
        ),
    },
    {
        "image": "img-l3-s04-rahul-steps.jpg",
        "text":  (
            "Rahul needed to repair his bicycle but did not know how. "
            "He asked AI: Give me step-by-step instructions with one step at a time. "
            "Breaking tasks into steps makes AI output easier to follow and harder to misunderstand."
        ),
    },
    {
        "image": "img-l3-s05-priya-tone.jpg",
        "text":  (
            "Priya wrote a complaint to her landlord using AI. "
            "The first draft was too aggressive. "
            "She said: Rewrite this in a polite but firm tone. "
            "Tone control is one of the most powerful prompting skills."
        ),
    },
    {
        "image": "img-l3-s06-kiran-compare.jpg",
        "text":  (
            "Kiran compared two AI answers for the same question — one from a basic prompt, "
            "one from a detailed prompt. The detailed one was ten times more useful. "
            "The quality of your answer depends on the quality of your question."
        ),
    },
    {
        "image": "img-l3-s07-prompt-library.jpg",
        "text":  (
            "Here is the secret of advanced users: they save their best prompts. "
            "Once you find a prompt that works well — for writing, planning, or learning — "
            "save it in your notes app. "
            "You are building a personal prompt library that gets more powerful over time."
        ),
    },
    {
        "image": "img-l3-s08-practice.jpg",
        "text":  (
            "In this level you will practice five real skills: "
            "fact-checking an AI answer, asking for step-by-step help, "
            "adjusting the tone of a message, comparing two responses, "
            "and saving your first prompt to your personal library. "
            "Each skill takes less than five minutes."
        ),
    },
    {
        "image": "img-l3-s09-celebration.jpg",
        "text":  (
            "That is Level 3. You are no longer just using AI — you are thinking with it. "
            "Scroll down to start your five practice tasks. "
            "See you in Level 4, where AI becomes your learning partner."
        ),
    },
]

# ── TTS ──────────────────────────────────────────────────────────────
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

# ── Ken Burns zoom ───────────────────────────────────────────────────
def make_zoom_clip(img_path: Path, duration: float):
    img = Image.open(img_path).convert("RGB")
    iw, ih = img.size
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    ox, oy = (W - nw) // 2, (H - nh) // 2
    canvas.paste(img, (ox, oy))
    frame0 = np.array(canvas)

    def zoom_frame(get_frame, t):
        f  = get_frame(t)
        s  = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw2, nh2 = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw2, nh2), Image.LANCZOS)
        ox2, oy2 = (nw2 - w) // 2, (nh2 - h) // 2
        return np.array(zoomed.crop((ox2, oy2, ox2 + w, oy2 + h)))

    clip = ImageClip(frame0, duration=duration)
    clip = clip.transform(zoom_frame, apply_to="video")
    return clip

# ── build video ──────────────────────────────────────────────────────
def build_video():
    import moviepy
    print("Step 2: Building video...")
    ffmpeg_bin = moviepy.config.FFMPEG_BINARY
    print(f"  Using ffmpeg: {ffmpeg_bin}")

    print("  Building clips...")
    clips = []
    for i, sc in enumerate(SCENES_DATA, 1):
        img_path   = SCENES / sc["image"]
        audio_path = AUDIO_DIR / f"scene-{i:02d}.mp3"
        print(f"  [{i}/{len(SCENES_DATA)}] {sc['image']}")
        audio = AudioFileClip(str(audio_path))
        dur   = audio.duration + 0.4
        clip  = make_zoom_clip(img_path, dur)
        clip  = clip.with_audio(audio)
        clips.append(clip)

    print("\n  Concatenating clips...")
    final = concatenate_videoclips(clips, method="compose")
    print(f"  Writing: {OUT}")
    final.write_videofile(
        str(OUT),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"),
        remove_temp=True,
        logger="bar",
    )
    dur_s = int(final.duration)
    print(f"\n✅ Video ready: {OUT}")
    print(f"   Duration: ~{dur_s}s")
    print(f"\nNext — upload to S3:")
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-03-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
