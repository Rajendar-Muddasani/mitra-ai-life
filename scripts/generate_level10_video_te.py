"""
Level 10 Telugu Intro Video Generator
Produces: content/assets/videos/level-10-intro-te.mp4
Run: .venv/bin/python scripts/generate_level10_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_10"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-10-intro-te.mp4"

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
        "img-l10-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 10 కి స్వాగతం — ఏఐ సేఫ్టీ మరియు సమాజం. "
        "ఇది మీ తెలుగు ఏఐ నిత్యజీవిత యాత్రలో చివరి అడుగు. "
        "రోజువారీ సహాయం, పని, వ్యాపారం, సంపాదన కోసం ఏఐ ఎలా వాడాలో నేర్చుకున్నారు. "
        "ఇప్పుడు ఏఐ ని తెలివిగా వాడడం, కుటుంబాన్ని రక్షించడం, సురక్షితంగా ఉండటం నేర్చుకుంటారు.",
        10,
    ),
    (
        "img-l10-s02-deepfake.jpg",
        "డీప్ ఫేక్లు అంటే ఏఐ తో తయారైన నకిలీ ఫొటోలు, వీడియోలు లేదా ఆడియో. "
        "చాలా నిజంగా కనపడతాయి, కానీ అబద్ధాలు. "
        "వాట్సాప్ లో లేదా సోషల్ మీడియా లో షాకింగ్ వీడియో వస్తే — వెంటనే ఫార్వర్డ్ చేయకండి. "
        "ఆగి, సోర్స్ చెక్ చేయండి. ఎవరికి లాభం అని ఆలోచించండి.",
        10,
    ),
    (
        "img-l10-s03-fact-check.jpg",
        "తప్పుడు సమాచారం వేగంగా వ్యాపిస్తుంది — ఎన్నికలు, ఎమర్జెన్సీలు, ఆరోగ్య భయాలు, స్థానిక గొడవల సమయంలో. "
        "ఏఐ ఫాక్ట్ చెక్ కు సహాయపడుతుంది, కానీ విశ్వసనీయ సోర్సులు కూడా చెక్ చేయాలి. "
        "చర్య తీసుకోవడానికి ముందు అధికారిక వెబ్సైట్లు, నమ్మకమైన వార్తలు, నేరుగా నిర్ధారణ చేయండి.",
        9,
    ),
    (
        "img-l10-s04-voice-clone-scam.jpg",
        "వాయిస్ క్లోనింగ్ స్కామ్లు సాధారణమవుతున్నాయి. "
        "మీ పిల్లాడిలా, స్నేహితుడిలా లేదా బంధువులా మాట్లాడే కాలర్ అర్జెంట్ డబ్బు అడగవచ్చు. "
        "కంగారుపడకండి. వారు తెలిసిన నంబర్ కు మళ్ళీ కాల్ చేయండి. "
        "ఫ్యామిలీ సేఫ్టీ ప్రశ్న వాడండి. గొంతు మాత్రమే విన్నందుకు డబ్బు పంపకండి.",
        10,
    ),
    (
        "img-l10-s05-consent-privacy.jpg",
        "ప్రైవసీ ముఖ్యమైనది. ఆధార్ కార్డు, బ్యాంక్ వివరాలు, మెడికల్ రిపోర్ట్లు, పిల్లల ఫొటోలు, "
        "ప్రైవేట్ కుటుంబ సమాచారం యాదృచ్ఛికమైన ఏఐ టూల్స్ లో అప్లోడ్ చేయకండి. "
        "ఏదైనా షేర్ చేయడానికి ముందు: ఇది అవసరమా? పేర్లు, నంబర్లు తీసివేయగలనా? అని అడగండి.",
        9,
    ),
    (
        "img-l10-s06-meera-integrity.jpg",
        "మీరా చదువు, పని కోసం ఏఐ వాడుతుంది — కానీ అంధంగా కాపీ చేయదు. "
        "ఫాక్ట్లు చెక్ చేస్తుంది, తన మాటల్లో తిరిగి రాస్తుంది, అవసరమైతే క్రెడిట్ ఇస్తుంది. "
        "ఏఐ మీ ఆలోచనను సపోర్ట్ చేయాలి — మీ నిజాయితీని రిప్లేస్ చేయకూడదు.",
        9,
    ),
    (
        "img-l10-s07-5-rules.jpg",
        "ఈ స్థాయిలో 5 సేఫ్టీ నియమాలు సాధన చేస్తారు: "
        "ఫార్వర్డ్ చేయడానికి ముందు ఆగడం, నమ్మడానికి ముందు నిర్ధారించడం, "
        "ప్రైవేట్ డేటా రక్షించడం, అర్జెంట్ డబ్బు అభ్యర్థనలు చెక్ చేయడం, ఏఐ నిజాయితీగా వాడటం. "
        "ఈ అయిదు అలవాట్లు మీ కుటుంబాన్ని, డబ్బును, పేరును, సమాజాన్ని రక్షిస్తాయి.",
        10,
    ),
    (
        "img-l10-s08-celebration.jpg",
        "ఇదే స్థాయి 10. తెలుగు ఏఐ నిత్యజీవిత యాత్ర పూర్తి చేశారు. "
        "సహాయం, చదువు, పని, వ్యాపారం, సంపాదన, సురక్షితత కోసం ఏఐ వాడగలరు. "
        "చివరి సాధన పూర్తి చేయండి. "
        "అభినందనలు — మీరు ఇప్పుడు నమ్మకంగా, జాగ్రత్తగా ఏఐ వాడగలరు!",
        10,
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
