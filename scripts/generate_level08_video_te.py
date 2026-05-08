"""
Level 8 Telugu Intro Video Generator
Produces: content/assets/videos/level-08-intro-te.mp4
Run: .venv/bin/python scripts/generate_level08_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_08"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-08-intro-te.mp4"

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
        "img-l8-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 8 కి స్వాగతం — వ్యాపారం కోసం ఏఐ. "
        "ఏఐ తో మీ వ్యాపారాన్ని ముందుకు తీసుకెళ్ళండి. "
        "మంచి ప్రమోషన్లు రాయండి. కస్టమర్లను నమ్మకంగా హ్యాండిల్ చేయండి. తెలివిగా మార్కెట్ చేయండి. "
        "టెక్ నైపుణ్యాలు అక్కరలేదు — ఫోన్, మంచి ప్రాంప్ట్ చాలు.",
        9,
    ),
    (
        "img-l8-s02-ravi-whatsapp.jpg",
        "రవి హైదరాబాద్ లో మొబైల్ యాక్సెసరీస్ దుకాణం నడుపుతాడు. "
        "ఏఐ తో వాట్సాప్ ప్రమోషన్లు రాస్తాడు — నిజంగా రిప్లైలు వచ్చే మెసేజ్లు. "
        "కొత్త ఆఫర్ వివరాలు చెప్తే చాలు — ఏఐ పంపడానికి రెడీగా ఉన్న మెసేజ్ ఇస్తుంది. "
        "అతని సేల్స్ పెరిగాయి. కస్టమర్లు అతన్ని గుర్తు పెట్టుకుంటున్నారు.",
        10,
    ),
    (
        "img-l8-s03-meena-tiffin.jpg",
        "మీనా టిఫిన్ సర్వీస్ నడుపుతుంది. "
        "బిజీగా ఉన్నప్పుడు కూడా ఏఐ తో కస్టమర్ ప్రశ్నలకు వేగంగా మర్యాదగా జవాబిస్తుంది. "
        "కంప్లైంట్లు హ్యాండిల్ చేయడం, మెనూ అప్డేట్లు పంపడం, రెగ్యులర్ కస్టమర్లను సంతోషంగా ఉంచడం — "
        "ఆమె వ్యాపారం మరింత సజావుగా నడుస్తోంది.",
        9,
    ),
    (
        "img-l8-s04-suresh-complaint.jpg",
        "సురేష్ ఎలక్ట్రానిక్స్ రిపేర్ షాప్ నడుపుతాడు. "
        "కష్టమైన కంప్లైంట్లు హ్యాండిల్ చేయడానికి ఏఐ వాడతాడు. "
        "ఏఐ శాంతంగా, ప్రొఫెషనల్ గా జవాబులు సూచిస్తుంది — కోపంగా ఉన్న కస్టమర్లు లాయల్ కస్టమర్లుగా మారతారు.",
        9,
    ),
    (
        "img-l8-s05-divya-instagram.jpg",
        "దివ్య హోమ్ బేకర్. "
        "ఇన్స్టాగ్రామ్ పోస్ట్లు ప్రొఫెషనల్ గా కనపడటానికి ఏఐ వాడుతుంది. "
        "ఫొటో, వివరాలు చెప్పింది — ఏఐ కాప్షన్, హ్యాష్ ట్యాగ్లు రాసింది. "
        "ఆమె ఫాలోవర్లు పెరుగుతున్నారు. ప్రతి వారం ఎక్కువ ఆర్డర్లు వస్తున్నాయి.",
        9,
    ),
    (
        "img-l8-s06-ravi-calendar.jpg",
        "రవి నెలవారీ సేల్స్ క్యాలెండర్ ప్లాన్ చేయడానికి ఏఐ వాడతాడు. "
        "పండగలు, స్టాక్ వివరాలు చెప్పాడు — ప్రమోషన్ ప్లాన్ అందింది. "
        "ఇప్పుడు ఏ సేల్స్ అవకాశమూ తప్పిపోవడం లేదు.",
        9,
    ),
    (
        "img-l8-s07-practice.jpg",
        "ఈ స్థాయిలో 4 నిజమైన వ్యాపార సన్నివేశాలు సాధన చేస్తారు: "
        "వాట్సాప్ ప్రమోషన్లు, కస్టమర్ ప్రశ్నలు, కంప్లైంట్ రిప్లైలు, ఇన్స్టాగ్రామ్ పోస్ట్లు. "
        "ఏఐ ని మీ వ్యాపార పార్టనర్ గా ఎలా వాడాలో నేర్చుకుంటారు.",
        9,
    ),
    (
        "img-l8-s08-celebration.jpg",
        "ఇదే స్థాయి 8. ఏఐ తో మీ వ్యాపారం మెరుగయింది. "
        "ప్రమోషన్లు, కస్టమర్ రిప్లైలు, సోషల్ మీడియా — అన్నీ ఏఐ తో. "
        "స్థాయి 9 లో మీ ఏఐ నైపుణ్యాలు డబ్బు సంపాదించే విధానం నేర్చుకుంటారు. కలుద్దాం!",
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
