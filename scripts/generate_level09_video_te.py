"""
Level 9 Telugu Intro Video Generator
Produces: content/assets/videos/level-09-intro-te.mp4
Run: .venv/bin/python scripts/generate_level09_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_09"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-09-intro-te.mp4"

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
        "img-l9-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 9 కి స్వాగతం — ఏఐ తో సంపాదన. "
        "మీ ఏఐ నైపుణ్యాలు ఇప్పుడు నిజమైన డబ్బు సంపాదించగలవు. "
        "ఫ్రీలాన్స్ చేయండి. కంటెంట్ అమ్మండి. మీరు చేసే పనిలో ఏఐ సర్వీసులు జోడించండి. "
        "ఆఫీస్ అక్కరలేదు. బాస్ అక్కరలేదు. ఫోన్, నైపుణ్యాలు, నిజమైన సంపాదన.",
        10,
    ),
    (
        "img-l9-s02-kavya-gig.jpg",
        "కావ్య విజయవాడలో గృహిణి. "
        "ఫ్రీలాన్స్ ప్లాట్ ఫామ్లలో చిన్న వ్యాపారాలకు ఏఐ రాసిన కంటెంట్ అందిస్తోంది. "
        "నెలకు 10,000 నుండి 15,000 రూపాయలు ఆమె ఫోన్ లో, తీరిక సమయంలో సంపాదిస్తోంది. "
        "ఆమె ఏకైక పెట్టుబడి — మంచి ప్రాంప్ట్లు రాయడం నేర్చుకోవడం.",
        9,
    ),
    (
        "img-l9-s03-srinivas-clients.jpg",
        "శ్రీనివాస్ రిటైర్డ్ ప్రభుత్వ ఉద్యోగి. "
        "స్థానిక వ్యాపారాలకు ప్రపోజల్లు, ఫార్మల్ లెటర్లు తయారుచేయడానికి ఏఐ వాడతాడు. "
        "ఒక్కో డాక్యుమెంట్ కు 500 నుండి 1000 రూపాయలు వసూలు చేస్తాడు. "
        "క్లయింట్లు నమ్ముతారు — నాణ్యత ప్రొఫెషనల్ గా ఉంటుంది, వేగంగా అందుతుంది.",
        9,
    ),
    (
        "img-l9-s04-padma-youtube.jpg",
        "పద్మ వంట గురించి చిన్న యూట్యూబ్ ఛానల్ నడుపుతుంది. "
        "వీడియో స్క్రిప్ట్లు, టైటిళ్ళు, డిస్క్రిప్షన్లు రాయడానికి ఏఐ వాడుతుంది. "
        "అప్లోడ్ ఫ్రీక్వెన్సీ రెట్టింపు అయింది, వ్యూలు మూడు రెట్లు పెరిగాయి, ఛానల్ యాడ్లు నుండి సంపాదిస్తోంది. "
        "ఏఐ ఆమె గొంతును రిప్లేస్ చేయలేదు — వంట, రికార్డింగ్ కు సమయం ఇచ్చింది.",
        10,
    ),
    (
        "img-l9-s05-raju-studio.jpg",
        "రాజు హైదరాబాద్ లో ఫోటోగ్రాఫర్. "
        "తన స్టూడియో క్లయింట్లకు ఏఐ జెనరేటెడ్ సోషల్ మీడియా కంటెంట్ ని కొత్త సర్వీస్ గా ఆఫర్ చేస్తున్నాడు. "
        "ఇప్పుడు ప్రతి ఫోటోగ్రఫీ ప్యాకేజ్ లో ఏఐ పోస్ట్లు, కాప్షన్లు ఉంటాయి. "
        "సగటు ఆర్డర్ వేల్యూ 40% పెరిగింది.",
        9,
    ),
    (
        "img-l9-s06-pricing.jpg",
        "ఏఐ తో సంపాదించడం రహస్యం: మీ నైపుణ్యాలను ప్యాకేజ్ చేయడం. "
        "ఏఐ అమ్మకండి — ఫలితాలు అమ్మండి. "
        "వాట్సాప్ ప్రమోషన్, వ్యాపార ప్రపోజల్, సోషల్ మీడియా పోస్ట్, యూట్యూబ్ స్క్రిప్ట్ — "
        "ఇవి జనం డబ్బు చెల్లించే సర్వీసులు. మీరు ఏఐ శక్తి తో డెలివర్ చేసే నిపుణులు.",
        9,
    ),
    (
        "img-l9-s07-practice.jpg",
        "ఈ స్థాయిలో మీ ఆదాయ ప్లాన్ నిర్మిస్తారు: "
        "ఒక ఏఐ సర్వీస్ ఎంచుకోండి, ధర నిర్ణయించండి, క్లయింట్లకు చూపించే శాంపిల్ తయారుచేయండి, "
        "డెలివరీ సాధన చేయండి. "
        "చివరకు నిజంగా అమ్మగలిగే సర్వీస్ రెడీగా ఉంటుంది.",
        9,
    ),
    (
        "img-l9-s08-celebration.jpg",
        "ఇదే స్థాయి 9. మీ ఏఐ నైపుణ్యాలను ఆదాయంగా మార్చారు. "
        "మీ సర్వీస్, మీ ధర, మీ మొదటి శాంపిల్ — అన్నీ రెడీ. "
        "స్థాయి 10 — చివరి స్థాయిలో ఏఐ ని భవిష్యత్తు కోసం ఎలా వాడాలో నేర్చుకుంటారు. కలుద్దాం!",
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
