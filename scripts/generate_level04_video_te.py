"""
Level 4 Telugu Intro Video Generator
Produces: content/assets/videos/level-04-intro-te.mp4
Run: .venv/bin/python scripts/generate_level04_video_te.py
"""

import os, sys, time, hashlib
import re
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_04"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-04-intro-te.mp4"

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
        "img-l4-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 4 కి స్వాగతం — వర్క్ స్మార్ట్. "
        "ఇమెయిళ్లు, నివేదికలు, రెజ్యూమ్లు, ఇంటర్వ్యూ తయారీ, స్టడీ ప్లాన్లు — "
        "ఈ స్థాయి నిజమైన పని కోసం ఏఐ వాడటం నేర్పుతుంది. "
        "ఈ నైపుణ్యాలు వారానికి గంటలు ఆదా చేస్తాయి.",
        9,
    ),
    (
        "img-l4-s02-deepa-email.jpg",
        "దీప్ కి ప్రాజెక్ట్ ఆలస్యం గురించి క్లయింట్ కి ప్రొఫెషనల్ ఇమెయిల్ రాయాలి. "
        "ఆమె ఏఐ కి చెప్పింది: సప్లయర్ సమస్య వల్ల ఒక వారం ఆలస్యమవుతోంది, డిస్కౌంట్ ఆఫర్ చేసే ఇమెయిల్ రాయి. "
        "30 సెకండ్లలో డ్రాఫ్ట్ రెడీ. 20 నిమిషాల పని నిమిషంలో అయింది.",
        9,
    ),
    (
        "img-l4-s03-sunitha-report.jpg",
        "సునీత కి నెలవారీ సేల్స్ రిపోర్ట్ రాయాలి. "
        "తన నంబర్లు ఏఐ కి ఇచ్చింది: ఇవి ఒక పేజీ ప్రొఫెషనల్ రిపోర్ట్ గా మార్చు. "
        "ఏఐ హెడింగ్లు వేసింది, ముఖ్యమైన విషయాలు హైలైట్ చేసింది. "
        "మేనేజర్ ముగ్ధుడయ్యాడు.",
        9,
    ),
    (
        "img-l4-s04-anand-resume.jpg",
        "ఆనంద్ కి కొత్త ఉద్యోగానికి దరఖాస్తు చేయాలి. "
        "తన పాత రెజ్యూమ్, జాబ్ డిస్క్రిప్షన్ ఏఐ కి ఇచ్చాడు: ఈ జాబ్ కు సరిపోయేలా రెజ్యూమ్ మార్చు. "
        "నిమిషాల్లో టార్గెటెడ్, చక్కని రెజ్యూమ్ రెడీ అయింది.",
        9,
    ),
    (
        "img-l4-s05-anand-interview.jpg",
        "ఆనంద్ ఇంటర్వ్యూ కు కూడా ఏఐ తో తయారయ్యాడు. "
        "అడిగాడు: సేల్స్ మేనేజర్ రోల్ కు 10 సాధారణ ప్రశ్నలు, నా నేపథ్యం బట్టి జవాబులు సూచించు. "
        "సాధన చేశాడు. నమ్మకంగా ఇంటర్వ్యూ కి వెళ్ళాడు.",
        9,
    ),
    (
        "img-l4-s06-vikram-study.jpg",
        "విక్రమ్ కి మూడు వారాల్లో ప్రొఫెషనల్ సర్టిఫికేషన్ పరీక్ష ఉంది. "
        "ఏఐ కి అడిగాడు: రోజువారీ టాపిక్లు, చిన్న క్విజ్లు తో 3 వారాల స్టడీ ప్లాన్ తయారుచేయి. "
        "ఆఫీస్ తర్వాత రోజూ చదివాడు. మొదటి అటెంప్ట్ లోనే పాస్ అయ్యాడు.",
        9,
    ),
    (
        "img-l4-s07-practice.jpg",
        "ఈ స్థాయిలో 5 నిజమైన పని పనులు సాధన చేస్తారు: "
        "ప్రొఫెషనల్ ఇమెయిల్, రా డేటా నుండి రిపోర్ట్, "
        "ఉద్యోగానికి తగ్గ రెజ్యూమ్, ఇంటర్వ్యూ జవాబులు, స్టడీ ప్లాన్. "
        "ప్రతి పనితో వెంటనే వాడగలిగే టెంప్లేట్ ఉంటుంది.",
        10,
    ),
    (
        "img-l4-s08-celebration.jpg",
        "ఇదే స్థాయి 4. ఏఐ ఇప్పుడు మీ ప్రొఫెషనల్ పార్టనర్ — "
        "వేగమైన ఇమెయిళ్లు, మంచి నివేదికలు, తెలివైన తయారీ. "
        "క్విజ్ పూర్తి చేయండి. స్థాయి 5 లో ఏఐ మీ ఇంటి జీవితాన్ని మెరుగుపరుస్తుంది!",
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
            input=gtts.SynthesisInput(ssml=(
                '<speak>' +
                re.sub(r'(?<![a-zA-Z])AI(?![a-zA-Z])',
                    '<say-as interpret-as="characters">AI</say-as>',
                    text.replace('ఏఐ', '<say-as interpret-as="characters">AI</say-as>')
                ) + '</speak>'
            )),
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
