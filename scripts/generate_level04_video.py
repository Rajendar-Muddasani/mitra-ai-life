"""
Generate Level 4 English narrated intro video.
Topic: Work Smart — Save Time. Look Professional. Work Smarter.
8 scenes, ~120s, voice: en-US-Chirp3-HD-Charon
Output: content/assets/videos/level-04-intro-charon.mp4
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
AUDIO_DIR = ROOT / f"content/assets/videos/audio_tmp_l4{VERSION_SUFFIX}"
OUT       = ROOT / f"content/assets/videos/level-04-intro{VERSION_SUFFIX}.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ── video spec ───────────────────────────────────────────────────────
W, H  = 1280, 720
FPS   = 24

# ── narration script ─────────────────────────────────────────────────
SCENES_DATA = [
    {
        "image": "img-l4-s01-hero.jpg",
        "text":  (
            "Welcome to Level 4 — Work Smart. "
            "This level teaches you how to use AI for real work tasks: "
            "emails, reports, resumes, interview preparation, and study plans. "
            "These are skills that save you hours every week."
        ),
    },
    {
        "image": "img-l4-s02-deepa-email.jpg",
        "text":  (
            "Deepa needs to write a professional email to a client about a delayed project. "
            "She tells AI: Write a polite email to a client explaining a one-week delay "
            "due to supplier issues, and offer a discount as goodwill. "
            "In thirty seconds she has a draft that would take most people twenty minutes."
        ),
    },
    {
        "image": "img-l4-s03-sunitha-report.jpg",
        "text":  (
            "Sunitha needs to write a monthly sales report. "
            "She gives AI her raw numbers and says: "
            "Turn these figures into a one-page professional report with key insights. "
            "AI structures it, adds headings, and highlights what matters. "
            "Her manager is impressed."
        ),
    },
    {
        "image": "img-l4-s04-anand-resume.jpg",
        "text":  (
            "Anand is applying for a new job. "
            "He pastes his old resume and the job description into AI and says: "
            "Rewrite my resume to match this job — highlight relevant skills. "
            "The result is a targeted, clean resume in minutes, not hours."
        ),
    },
    {
        "image": "img-l4-s05-anand-interview.jpg",
        "text":  (
            "Anand also uses AI to prepare for his interview. "
            "He asks: Give me ten common interview questions for a sales manager role "
            "and suggest strong answers based on my background. "
            "He practises the answers and walks into the interview with confidence."
        ),
    },
    {
        "image": "img-l4-s06-vikram-study.jpg",
        "text":  (
            "Vikram has a professional certification exam in three weeks. "
            "He asks AI: Create a three-week study plan with daily topics and short quizzes. "
            "AI builds a structured plan he can follow every evening after work. "
            "He passes on his first attempt."
        ),
    },
    {
        "image": "img-l4-s07-practice.jpg",
        "text":  (
            "In this level you will practise five real work tasks: "
            "writing a professional email, creating a report from raw data, "
            "updating a resume for a specific job, preparing interview answers, "
            "and building a study plan. "
            "Each task includes a template you can reuse immediately."
        ),
    },
    {
        "image": "img-l4-s08-celebration.jpg",
        "text":  (
            "That is Level 4. AI is now your professional partner — "
            "faster emails, better reports, smarter preparation. "
            "Scroll down to start your five work tasks. "
            "See you in Level 5, where AI helps you upgrade your everyday life."
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
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-04-intro{VERSION_SUFFIX}.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
