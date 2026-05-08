"""
Level 2 Telugu Intro Video Generator
Produces: content/assets/videos/level-02-intro-te.mp4
Runtime: ~100 seconds, 1280×720, narrated slideshow in Telugu

Uses:
- Google Cloud TTS (te-IN-Standard-A) for genuine Telugu voice narration
- moviepy + imageio_ffmpeg (no system ffmpeg needed)

Requires in .env:
  GOOGLE_APPLICATION_CREDENTIALS=/path/to/mitra-tts-key.json

Run: .venv/bin/python scripts/generate_level02_video_te.py
"""

import os
import sys
import time
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_02"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-02-intro-te.mp4"

GTTS_LANGUAGE = "te-IN"
GTTS_VOICE    = "te-IN-Standard-A"
GTTS_SPEED    = 0.90
AUDIO_GAIN    = 1.15

cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
if not cred_path or not Path(cred_path).exists():
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS not set or file not found.")
    sys.exit(1)

google_tts_client = gtts.TextToSpeechClient()
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Script: 10 scenes in Telugu ──────────────────────────────────────────────
SCENES = [
    (
        "img-l2-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 2 కి స్వాగతం — రోజువారీ సహాయం. "
        "స్థాయి 1 లో ఏఐ అంటే ఏమిటో తెలుసుకున్నారు. ఇప్పుడు దానిని నిజంగా ఉపయోగించే సమయం వచ్చింది. "
        "రవి, ప్రియ, రాహుల్ తిరిగొచ్చారు. వారి జీవితాలు ఇప్పుడు మరింత సులభంగా మారాయి.",
        10,
    ),
    (
        "img-l2-s02-ravi-phone.jpg",
        "రవికి తన సప్లయర్ కి ఆర్డర్ ఆలస్యం గురించి మెసేజ్ పంపాల్సి వచ్చింది. "
        "ఇంగ్లీష్ బాగా రాయలేడు. సాధారణ మాటల్లో సమస్య చెప్పాడు. "
        "ఏఐ కొన్ని సెకండ్లలోనే చక్కని ప్రొఫెషనల్ మెసేజ్ తయారు చేసింది.",
        9,
    ),
    (
        "img-l2-s03-supplier-reply.jpg",
        "రవి ఆ మెసేజ్ పంపాడు. అదే రోజు సప్లయర్ నుండి మంచి జవాబు వచ్చింది. "
        "సైబర్ కేఫ్ అవసరం లేదు. ఎవరి సహాయం అవసరం లేదు. "
        "తన ఫోన్ లో తానే చేశాడు. ఐదు నిమిషాల్లో పని అయిపోయింది.",
        9,
    ),
    (
        "img-l2-s04-priya-grocery.jpg",
        "ప్రియ నాలుగు మంది కుటుంబానికి 1500 రూపాయల బడ్జెట్ లో "
        "ఆరోగ్యకరమైన వారపు మెనూ అడిగింది. "
        "ఏఐ 7 రోజుల పూర్తి ప్లాన్, షాపింగ్ లిస్ట్ తో సహా ఇచ్చింది.",
        9,
    ),
    (
        "img-l2-s05-market-scene.jpg",
        "ఆ లిస్ట్ తో మార్కెట్ కి వెళ్ళింది. అన్ని కూరలు స్థానికంగా, సీజన్ లో ఉన్నవే. "
        "బడ్జెట్ లోపే అయింది. ఆహారం వృథా కాలేదు. "
        "ఆ వారం 300 రూపాయలు మిగిలాయి.",
        9,
    ),
    (
        "img-l2-s06-rahul-exam.jpg",
        "రాహుల్ కి రెండు వారాల్లో పరీక్షలు ఉన్నాయి. "
        "ఏఐ ని సబ్జెక్ట్ వారీగా, రోజువారీగా రివిజన్ ప్లాన్ అడిగాడు. "
        "తన సమయానికి సరిగ్గా సరిపోయే వివరమైన ప్లాన్ అందింది.",
        9,
    ),
    (
        "img-l2-s07-prompt-tips.jpg",
        "ఇక్కడ ముఖ్యమైన నైపుణ్యం: మీరు బాగా అడిగితే, ఏఐ బాగా జవాబు ఇస్తుంది. "
        "మీరు ఎవరు, ఏం కావాలి, ముఖ్యమైన వివరాలు చెప్పండి. "
        "స్పష్టంగా, సాధారణ భాషలో అడగండి. ఒక సంభాషణ లాగా చేయండి.",
        9,
    ),
    (
        "img-l2-s08-complaint-letter.jpg",
        "ప్రియ పక్కింటివారికి లైట్ బిల్ లో 800 రూపాయలు అదనంగా వసూలయ్యాయి. "
        "ఏఐ ఒక్క నిమిషంలో విద్యుత్ బోర్డ్ కి పంపడానికి సరైన ఫార్మల్ కంప్లైంట్ లెటర్ రాసింది. "
        "మర్యాదగా, స్పష్టంగా, పంపడానికి రెడీగా ఉంది.",
        9,
    ),
    (
        "img-l2-s09-practice-arena.jpg",
        "ఈ స్థాయిలో 5 నిజమైన పనులు సాధన చేస్తారు: "
        "ప్రొఫెషనల్ మెసేజ్, గ్రాసరీ బడ్జెట్, స్టడీ షెడ్యూల్, కంప్లైంట్ లెటర్, వాట్సాప్ రిప్లై. "
        "ఇవన్నీ ఈ వారమే మీకు అవసరం పడవచ్చు.",
        10,
    ),
    (
        "img-l2-s10-celebration.jpg",
        "ఇదే స్థాయి 2. "
        "రాయడం, ప్లాన్ చేయడం, చదవడం, చిన్న సమస్యలు పరిష్కరించడం — ఇవన్నీ ఏఐ ఇప్పుడు మీకు సహాయపడుతుంది. "
        "క్విజ్ పూర్తి చేసి స్థాయి 2 సర్టిఫికేట్ తీసుకోండి. చాలా బాగా చేస్తున్నారు!",
        9,
    ),
]


def scene_audio_path(scene_idx, text):
    cache_key = hashlib.sha1(
        f"{GTTS_VOICE}|{GTTS_SPEED}|{text}".encode("utf-8")
    ).hexdigest()[:10]
    return AUDIO_DIR / f"scene-{scene_idx:02d}-{cache_key}.mp3"


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

print("Step 2: Video build చేస్తున్నాం...")

import imageio_ffmpeg
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_bin

from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import numpy as np

VIDEO_W, VIDEO_H = 1280, 720
FPS = 24


def make_clip(img_name, audio_path):
    img_path = SCENES_DIR / img_name
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


clips = []
for i, ((img, _, _), audio_path) in enumerate(zip(SCENES, audio_files), start=1):
    print(f"  [{i}/{len(SCENES)}] {img}")
    clips.append(make_clip(img, audio_path))

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
print(f"\nNext — upload to S3:")
print(f"  source .env && aws s3 cp {VIDEO_OUT} s3://mitra-ai-life-assets/videos/level-02-intro-te.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")
