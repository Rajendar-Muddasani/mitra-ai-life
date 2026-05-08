"""
Level 7 Telugu Intro Video Generator
Produces: content/assets/videos/level-07-intro-te.mp4
Run: .venv/bin/python scripts/generate_level07_video_te.py
"""

import os, sys, time, hashlib
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from google.cloud import texttospeech as gtts

ROOT       = Path(__file__).parent.parent
SCENES_DIR = ROOT / "content" / "assets" / "scenes"
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_07"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-07-intro-te.mp4"

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

SCENES = [
    (
        "img-l7-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 7 కి స్వాగతం — ఏఐ తో నిర్మించండి. "
        "చిన్న పనులు ఆపి, నిజమైన వస్తువులు నిర్మించే సమయం వచ్చింది. "
        "వెబ్సైట్, చాట్ బాట్, వ్యాపార పోస్టర్, పోర్ట్ ఫోలియో — ఏఐ మీ కో-బిల్డర్. "
        "ఐడియా మీది. నిర్మించడంలో ఏఐ సహాయం చేస్తుంది.",
        10,
    ),
    (
        "img-l7-s02-nandini-website.jpg",
        "నందిని తన హోమ్ బేకరీ కు వెబ్సైట్ కావాలి. "
        "తన వ్యాపారం ఏఐ కి వివరించింది, స్టైల్ ఎంచుకుంది — వెబ్సైట్ డ్రాఫ్ట్ రెడీ అయింది. "
        "కోడింగ్ అవసరం లేదు, డిజైన్ అనుభవం అవసరం లేదు. "
        "ఇప్పుడు ఆమె బేకరీ ఆన్ లైన్ లో ఉంది, ప్రతి వారం కొత్త ఆర్డర్లు వస్తున్నాయి.",
        9,
    ),
    (
        "img-l7-s03-suresh-chatbot.jpg",
        "సురేష్ కోచింగ్ సెంటర్ నడుపుతాడు. "
        "తల్లిదండ్రుల ప్రశ్నలకు — టైమింగ్లు, ఫీజులు, కోర్సులు — జవాబిచ్చే సింపుల్ చాట్ బాట్ నిర్మించాడు. "
        "బాట్ 24/7 పని చేస్తుంది. వారానికి గంటలు ఆదా అవుతున్నాయి. "
        "ఏఐ కేవలం చాటింగ్ కాదు — మీ కోసం పని చేసే టూల్స్ నిర్మించడానికి కూడా.",
        9,
    ),
    (
        "img-l7-s04-pooja-poster.jpg",
        "పూజ ఫ్రీలాన్స్ డిజైనర్. "
        "ఒక స్థానిక ఈవెంట్ కు బిజినెస్ పోస్టర్ తయారుచేయడానికి ఏఐ వాడింది. "
        "వివరాలు చెప్పింది, థీమ్ ఎంచుకుంది — ప్రింట్ కు రెడీ పోస్టర్ అయింది. "
        "ఇప్పుడు ఆమె పోస్టర్ డిజైన్ ని సర్వీస్ గా ఆఫర్ చేస్తోంది.",
        9,
    ),
    (
        "img-l7-s05-kiran-portfolio.jpg",
        "కిరణ్ ఉద్యోగాలకు దరఖాస్తు చేయాలనుకుంటున్నాడు. "
        "ఏఐ తో తన ప్రాజెక్ట్లు, రెజ్యూమ్, కాంటాక్ట్ ఫామ్ తో పోర్ట్ ఫోలియో సైట్ నిర్మించాడు. "
        "ఒక వారంలో ఇంటర్వ్యూ కాల్స్ వచ్చాయి. "
        "ఏఐ తో నిర్మించడం మీన్స్ వేగంగా లాంచ్ చేసి, నిలబడటం.",
        9,
    ),
    (
        "img-l7-s06-practice.jpg",
        "ఈ స్థాయిలో 4 నిజమైన ప్రాజెక్ట్లు నిర్మిస్తారు: వెబ్సైట్, చాట్ బాట్, బిజినెస్ పోస్టర్, మీ పోర్ట్ ఫోలియో. "
        "మీ ఐడియాలను ఏఐ సహాయంతో నిజంగా మార్చే విధానం నేర్చుకుంటారు. "
        "అనుభవం అక్కరలేదు — అడుగులు అనుసరించి నిర్మించండి.",
        9,
    ),
    (
        "img-l7-s07-celebration.jpg",
        "ఇదే స్థాయి 7. ఏఐ తో నిజమైన వస్తువులు నిర్మించారు. "
        "మీ వెబ్సైట్, చాట్ బాట్, పోస్టర్, పోర్ట్ ఫోలియో — అన్నీ సిద్ధంగా ఉన్నాయి. "
        "స్థాయి 8 లో వ్యాపారం కోసం ఏఐ నేర్చుకుంటారు. కలుద్దాం!",
        9,
    ),
]


def scene_audio_path(scene_idx, text):
    cache_key = hashlib.sha1(
        f"{GTTS_VOICE}|{GTTS_SPEED}|{text}".encode("utf-8")
    ).hexdigest()[:10]
    return AUDIO_DIR / f"scene-{scene_idx:02d}-{cache_key}.mp3"


print("Step 1: Telugu TTS narration audio generate అవుతోంది (Google Cloud TTS)...")
audio_files = []

for i, (img, text, _) in enumerate(SCENES, start=1):
    audio_path = scene_audio_path(i, text)
    if audio_path.exists():
        print(f"  [SKIP] Scene {i} audio already exists")
    else:
        print(f"  [{i}/{len(SCENES)}] TTS: {text[:50]}...")
        response = google_tts_client.synthesize_speech(
            input=gtts.SynthesisInput(text=text),
            voice=gtts.VoiceSelectionParams(language_code=GTTS_LANGUAGE, name=GTTS_VOICE),
            audio_config=gtts.AudioConfig(audio_encoding=gtts.AudioEncoding.MP3, speaking_rate=GTTS_SPEED),
        )
        audio_path.write_bytes(response.audio_content)
        print(f"    Saved: {audio_path.name}")
        if i < len(SCENES):
            time.sleep(0.3)
    audio_files.append(audio_path)

print(f"  Audio ready: {len(audio_files)} files\n")
print("Step 2: Video build చేస్తున్నాం...")

import imageio_ffmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import numpy as np

VIDEO_W, VIDEO_H, FPS = 1280, 720, 24


def make_clip(img_name, audio_path):
    pil_img = Image.open(SCENES_DIR / img_name).convert("RGB")
    iw, ih = pil_img.size
    scale = max(VIDEO_W / iw, VIDEO_H / ih)
    pil_img = pil_img.resize((int(iw * scale), int(ih * scale)), Image.LANCZOS)
    left = (pil_img.width - VIDEO_W) // 2
    top  = (pil_img.height - VIDEO_H) // 2
    frame = np.array(pil_img.crop((left, top, left + VIDEO_W, top + VIDEO_H)))
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
    return clip.transform(zoom_frame, apply_to="video").with_audio(audio)


clips = []
for i, ((img, _, _), ap) in enumerate(zip(SCENES, audio_files), start=1):
    print(f"  [{i}/{len(SCENES)}] {img}")
    clips.append(make_clip(img, ap))

final = concatenate_videoclips(clips, method="compose")
print(f"  Writing: {VIDEO_OUT}")
final.write_videofile(str(VIDEO_OUT), fps=FPS, codec="libx264", audio_codec="aac",
    temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"), remove_temp=True, logger="bar")
print(f"\n✅ Telugu video ready: {VIDEO_OUT}  (~{final.duration:.0f}s)")
