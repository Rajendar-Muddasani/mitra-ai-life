"""
Level 1 Telugu Intro Video Generator
Produces: content/assets/videos/level-01-intro-te.mp4
Runtime: ~100 seconds, 1280×720, narrated slideshow in Telugu

Uses:
- Google Cloud TTS (te-IN-Standard-A) for genuine Telugu voice narration
- moviepy + imageio_ffmpeg (no system ffmpeg needed)
- Same L1 scene images from content/assets/scenes/

Requires in .env:
  GOOGLE_APPLICATION_CREDENTIALS=/path/to/mitra-tts-key.json

Run: .venv/bin/python scripts/generate_level01_video_te.py
"""

import os
import sys
import time
import urllib.request
import hashlib
from pathlib import Path

# ── Load .env ────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from google.cloud import texttospeech as gtts

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.parent
SCENES_DIR = ROOT / "content" / "assets" / "scenes"
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-01-intro-te.mp4"

# Google Cloud TTS — genuine Telugu female voice
GTTS_LANGUAGE  = "te-IN"
GTTS_VOICE     = "te-IN-Standard-A"   # female; use te-IN-Standard-B for male
GTTS_SPEED     = 0.90                 # 1.0 = normal; 0.90 = slightly slower, clearer
AUDIO_GAIN     = 1.15

# Validate credentials
cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
if not cred_path or not Path(cred_path).exists():
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS not set or file not found.")
    print("  Add to .env:  GOOGLE_APPLICATION_CREDENTIALS=/path/to/mitra-tts-key.json")
    sys.exit(1)

google_tts_client = gtts.TextToSpeechClient()

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Script: 10 scenes in Telugu, ~100 seconds total ─────────────────────────
SCENES = [
    (
        "img-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 1 కి స్వాగతం. "
        "ఇతను రవి. హైదరాబాద్ లో చిన్న కిరాణా దుకాణం నడుపుతాడు. "
        "తన కొడుకు స్కూల్ కి ఒక లెటర్ రాయాలి. "
        "కానీ ఎలా మొదలుపెట్టాలో అతనికి తెలియడం లేదు.",
        10,
    ),
    (
        "img-s03-frustrated.jpg",
        "45 నిమిషాలు గడిచాయి. పేపర్ ఇంకా ఖాళీగానే ఉంది. "
        "ఒక చిన్న ఫార్మల్ లెటర్ కూడా రవి మొదలుపెట్టలేక ఇబ్బంది పడుతున్నాడు.",
        9,
    ),
    (
        "img-s04-priya-entering.jpg",
        "అప్పుడు అతని పక్కింటి ప్రియ వస్తుంది. "
        "ఆమె చెప్తుంది... ఏఐ ని ఒక్కసారి ట్రై చేయి. "
        "రవికి ఇంకా అనుమానం ఉంది. అయినా ఒకసారి ప్రయత్నించాలి అనుకుంటాడు.",
        9,
    ),
    (
        "img-s07-typing-phone.jpg",
        "రవి తన ఫోన్ తీసి ఏఐ కి తన సమస్య రాశాడు. "
        "చాలా సింపుల్ మాటల్లో రాశాడు. తన భాషలోనే రాశాడు. "
        "ప్రత్యేక శిక్షణ అవసరం లేదు. ఇంగ్లీష్ డిగ్రీ కూడా అవసరం లేదు.",
        9,
    ),
    (
        "img-s08-ravi-amazed.jpg",
        "రెండు నిమిషాల్లోనే లెటర్ రెడీ అయింది. "
        "చక్కని ఇంగ్లీష్. సరైన టోన్. మర్యాదగా ఉంది. స్పష్టంగా ఉంది. "
        "రవి తన పేరు, తేదీ మాత్రమే మార్చాడు. పని అయిపోయింది.",
        9,
    ),
    (
        "img-s06-library-analogy.jpg",
        "అయితే ఏఐ అంటే ఏమిటి? "
        "ఒక పెద్ద లైబ్రరీ ని ఊహించండి. "
        "అది ఎన్నో పుస్తకాలు, వ్యాసాలు, మాటలు చదివింది. "
        "మీరు ఏ ప్రశ్న అడిగినా వెంటనే జవాబు చెప్పగలదు.",
        11,
    ),
    (
        "img-s09-priya-kitchen.jpg",
        "ప్రియ తన డయాబెటిక్ అత్తమ్మ కోసం ఆరోగ్యకరమైన స్నాక్ రెసిపీని ఏఐ ని అడిగింది. "
        "ఏఐ తెలుగులోనే పూర్తి రెసిపీ ఇచ్చింది. అది కూడా కొన్ని సెకండ్లలోనే.",
        9,
    ),
    (
        "img-s10-rahul-studying.jpg",
        "రాహుల్ ఫోటోసింథసిస్ ని చాలా సులభంగా చెప్పమని ఏఐ ని అడిగాడు. "
        "ఏఐ చపాతీ ఉదాహరణతో వివరించింది. "
        "ఐదు నిమిషాల్లో రాహుల్ కి విషయం అర్థమైంది. "
        "పుస్తకం వారం రోజులుగా చెప్పలేనిది అది చెప్పింది.",
        10,
    ),
    (
        "img-s11-safety-warning.jpg",
        "కానీ గుర్తుంచుకోండి. ఏఐ ఒక సహాయకుడు మాత్రమే. అన్నీ తెలిసినవాడు కాదు. "
        "ఇది తప్పు చెప్పవచ్చు. ముఖ్యమైన విషయాలు మళ్ళీ చెక్ చేయండి. "
        "మీ ఆధార్ నంబర్, బ్యాంక్ వివరాలు, లేదా పాస్ వర్డ్లు ఏఐ తో పంచుకోకండి.",
        10,
    ),
    (
        "img-s13-celebration.jpg",
        "ఇదే స్థాయి 1. "
        "ఏఐ అంటే ఏమిటో, ఎలా వాడాలో, సురక్షితంగా ఎలా ఉండాలో ఇప్పుడు మీకు తెలుసు. "
        "క్విజ్ వెంటనే వస్తుంది. మీ మొదటి ప్రయత్నానికి సిద్ధమా? పదండి!",
        10,
    ),
]


def scene_audio_path(scene_idx, text):
    cache_key = hashlib.sha1(
        f"{GTTS_VOICE}|{GTTS_SPEED}|{text}".encode("utf-8")
    ).hexdigest()[:10]
    return AUDIO_DIR / f"scene-{scene_idx:02d}-{cache_key}.mp3"

# ── Step 1: Generate TTS audio for each scene ────────────────────────────────
print("Step 1: Telugu TTS narration audio generate అవుతోంది (Google Cloud TTS)...")
print(f"  Voice: {GTTS_VOICE} ({GTTS_LANGUAGE}) — genuine Telugu Indian voice")
audio_files = []

for i, (img, text, _) in enumerate(SCENES, start=1):
    audio_path = scene_audio_path(i, text)
    if audio_path.exists():
        print(f"  [SKIP] Scene {i} audio already exists")
    else:
        print(f"  [{i}/{len(SCENES)}] TTS: {text[:50]}...")
        synthesis_input = gtts.SynthesisInput(text=text)
        voice_params = gtts.VoiceSelectionParams(
            language_code=GTTS_LANGUAGE,
            name=GTTS_VOICE,
        )
        audio_config = gtts.AudioConfig(
            audio_encoding=gtts.AudioEncoding.MP3,
            speaking_rate=GTTS_SPEED,
        )
        response = google_tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        audio_path.write_bytes(response.audio_content)
        print(f"    Saved: {audio_path.name}")
        if i < len(SCENES):
            time.sleep(0.3)

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
    concatenate_videoclips,
)
from PIL import Image, ImageFilter
import numpy as np

VIDEO_W, VIDEO_H = 1280, 720
FPS = 24

def make_clip(img_name, audio_path, scene_idx):
    img_path = SCENES_DIR / img_name

    # Load, fill-fit and centre-crop image to VIDEO_W × VIDEO_H
    pil_img = Image.open(img_path).convert("RGB")
    iw, ih = pil_img.size
    scale = max(VIDEO_W / iw, VIDEO_H / ih)
    pil_img = pil_img.resize((int(iw * scale), int(ih * scale)), Image.LANCZOS)
    left = (pil_img.width  - VIDEO_W) // 2
    top  = (pil_img.height - VIDEO_H) // 2
    pil_img = pil_img.crop((left, top, left + VIDEO_W, top + VIDEO_H))
    frame = np.array(pil_img)

    audio = AudioFileClip(str(audio_path)).with_volume_scaled(AUDIO_GAIN)
    duration = audio.duration + 0.4

    clip = ImageClip(frame, duration=duration)

    # Subtle Ken Burns zoom using transform (get_frame, t) signature
    def zoom_frame(get_frame, t):
        f = get_frame(t)
        s = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw, nh = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw, nh), Image.LANCZOS)
        ox, oy = (nw - w) // 2, (nh - h) // 2
        return np.array(zoomed.crop((ox, oy, ox + w, oy + h)))

    clip = clip.transform(zoom_frame, apply_to="video")
    clip = clip.with_audio(audio)
    return clip


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
