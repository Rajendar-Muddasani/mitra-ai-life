"""
Level 6 Telugu Intro Video Generator
Produces: content/assets/videos/level-06-intro-te.mp4
Run: .venv/bin/python scripts/generate_level06_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_06"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-06-intro-te.mp4"

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
        "img-l6-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 6 కి స్వాగతం — పవర్ యూజర్. "
        "ఇప్పటికే ఏఐ వాడటం తెలుసు. ఇప్పుడు నిపుణుల్లా వాడటం నేర్చుకుందాం. "
        "అదే ఏఐ, పది రెట్లు ఎక్కువ ఫలితాలు, సగం సమయంలో.",
        9,
    ),
    (
        "img-l6-s02-pradeep-routine.jpg",
        "ప్రదీప్ రోజూ ఉదయం ఏఐ రొటీన్ తో మొదలుపెడతాడు. "
        "సేవ్ చేసిన ప్రాంప్ట్: ఈ రోజు పనులు సారాంశం చేయి, టాప్ 3 ప్రాయారిటీలు చెప్పు, ఒక పని డెలిగేట్ చేయగలిగేది సూచించు. "
        "ఈ ఒక్క రొటీన్ అతనికి ప్రతి రోజు 30 నిమిషాలు ఆదా చేస్తుంది. "
        "పవర్ యూజర్లు ఒకసారి అడగరు — రొటీన్లు నిర్మిస్తారు.",
        10,
    ),
    (
        "img-l6-s03-ananya-structure.jpg",
        "అనన్య ఏఐ కి నిర్మాణాత్మకంగా అడిగినప్పుడు బెటర్ జవాబులు వస్తాయని తెలుసుకుంది. "
        "మార్కెటింగ్ గురించి చెప్పు అని అడగడానికి బదులు: నువ్వు మార్కెటింగ్ నిపుణుడివి. "
        "హైదరాబాద్ లో 2000 రూపాయల బడ్జెట్ లో చిన్న టీ షాప్ ప్రమోట్ చేయడానికి 5 ఐడియాలు ఇవ్వు అని అడిగింది. "
        "రోల్ + కాంటెక్స్ట్ + కండీషన్ — ఇదే పవర్ యూజర్ ఫార్ములా.",
        10,
    ),
    (
        "img-l6-s04-venkat-sheets.jpg",
        "వెంకట్ చిన్న హార్డ్ వేర్ దుకాణం నడుపుతాడు. "
        "ఏఐ ని అడిగాడు: ప్రతి ప్రొడక్ట్ కు ప్రాఫిట్ మార్జిన్ స్వయంచాలకంగా లెక్కించే Excel ఫార్ములా రాయి. "
        "ఏఐ ఫార్ములా రాసింది, వివరించింది. వెంకట్ స్ప్రెడ్ షీట్ ఇప్పుడు ఆటోమేటిక్. "
        "టెక్ నిపుణుడు అవసరం లేదు — సరైన ప్రాంప్ట్ చాలు.",
        9,
    ),
    (
        "img-l6-s05-divya-templates.jpg",
        "దివ్య ట్యూటరింగ్ సెంటర్ నడుపుతుంది. ఒకసారి ఏఐ తో పేరెంట్ ప్రోగ్రెస్ రిపోర్ట్ టెంప్లేట్ తయారుచేసింది. "
        "ఇప్పుడు ప్రతి నెలా అదే టెంప్లేట్ వాడుతుంది — స్టూడెంట్ పేరు, స్కోర్లు మాత్రమే మారుస్తుంది. "
        "టెంప్లేట్లు పవర్ యూజర్లు ఏఐ ని మళ్ళీ మళ్ళీ పని చేయించే విధానం.",
        9,
    ),
    (
        "img-l6-s06-rajan-limits.jpg",
        "రాజన్ వైద్యుడు. రీసర్చ్ సారాంశాలు, పేషెంట్ ఎడ్యుకేషన్ మెటీరియల్ కు ఏఐ వాడతాడు. "
        "కానీ నిర్ధారణ కు ఎప్పుడూ ఏఐ నమ్మడు. "
        "ఎప్పుడు ఏఐ వాడకూడదో తెలియడం కూడా ఒక పవర్ స్కిల్. "
        "ఆరోగ్యం, చట్టం, డబ్బు నిర్ణయాలకు ఎల్లప్పుడూ నిపుణులే కావాలి.",
        10,
    ),
    (
        "img-l6-s07-practice.jpg",
        "ఈ స్థాయిలో 5 పవర్ యూజర్ సిస్టమ్లు నిర్మిస్తారు: "
        "రోజువారీ ఏఐ రొటీన్, రోల్-కాంటెక్స్ట్ ప్రాంప్ట్, "
        "స్ప్రెడ్ షీట్ ఫార్ములా, పనికి వచ్చే టెంప్లేట్, "
        "ఏఐ వాడకూడని పరిస్థితుల జాబితా. "
        "ఇవి సంవత్సరాలు వాడగలిగే సిస్టమ్లు.",
        10,
    ),
    (
        "img-l6-s08-celebration.jpg",
        "ఇదే స్థాయి 6. మీరు ఇప్పుడు పవర్ యూజర్. "
        "రొటీన్లు, నిర్మాణం, స్ప్రెడ్ షీట్లు, టెంప్లేట్లు, స్పష్టమైన పరిమితులు — ఇవే మీ ఐదు ఆయుధాలు. "
        "స్థాయి 7 లో ఏఐ తో నిజమైన వస్తువులు నిర్మిస్తారు. కలుద్దాం!",
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
