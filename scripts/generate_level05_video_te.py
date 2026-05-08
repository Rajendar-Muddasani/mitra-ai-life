"""
Level 5 Telugu Intro Video Generator
Produces: content/assets/videos/level-05-intro-te.mp4
Run: .venv/bin/python scripts/generate_level05_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_05"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-05-intro-te.mp4"

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
        "img-l5-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 5 కి స్వాగతం — లైఫ్ అప్గ్రేడ్. "
        "ఇల్లు నిర్వహించడం, పిల్లల చదువు, ట్రావెల్, ఇన్స్యూరెన్స్, రోజువారీ అలవాట్లు — "
        "ఈ స్థాయి ఏఐ తో మీ ఇంటి జీవితాన్ని మెరుగుపరుస్తుంది. "
        "నిజమైన మార్పులు, ఈ రోజు నుండే.",
        9,
    ),
    (
        "img-l5-s02-lakshmi-budget.jpg",
        "లక్ష్మి నాలుగు మంది కుటుంబాన్ని నడుపుతుంది. "
        "ఆమె ఏఐ కి చెప్పింది: నెలకు 30,000 రూపాయలు. అద్దె, కిరాణా, స్కూల్ ఫీజు చెల్లించి 3,000 రూపాయలు ఆదా చేయాలి. "
        "ఏఐ కొన్ని సెకండ్లలో స్పష్టమైన ప్లాన్ ఇచ్చింది — గంటల పని నిమిషంలో అయింది.",
        10,
    ),
    (
        "img-l5-s03-ramaiah-homework.jpg",
        "రమయ్య కూతురికి 7వ తరగతిలో భిన్నాలు అర్థం కావడం లేదు. "
        "ఆయన అడిగాడు: 12 సంవత్సరాల పిల్లకు పిజ్జా ఉదాహరణతో భిన్నాలు వివరించి, 5 ప్రాక్టీస్ ప్రశ్నలు ఇవ్వు. "
        "ఒక సాయంత్రంలో అమ్మాయికి అర్థమైంది.",
        9,
    ),
    (
        "img-l5-s04-kavitha-travel.jpg",
        "కావిత కుటుంబం ఊటీ 5 రోజులు వెళ్ళాలనుకుంటోంది. "
        "ఆమె అడిగింది: 10,000 రూపాయల బడ్జెట్ లో, 10 ఏళ్ళ లోపు ఇద్దరు పిల్లలతో 5 రోజుల ఊటీ ట్రిప్ ప్లాన్ చేయి. "
        "ఏఐ రోజువారీ ప్లాన్, బడ్జెట్ బ్రేక్ డౌన్ ఇచ్చింది — ఏ ట్రావెల్ ఏజెంట్ కంటే మంచిది.",
        9,
    ),
    (
        "img-l5-s05-srinivas-compare.jpg",
        "శ్రీనివాస్ తన కార్ ఇన్స్యూరెన్స్ రిన్యూ చేయాలి. "
        "ఆయన అడిగాడు: థర్డ్ పార్టీ మరియు కాంప్రహెన్సివ్ ఇన్స్యూరెన్స్ తేడా సులభంగా వివరించు. 5 సంవత్సరాల కారుకు ఏది మంచిది? "
        "ఏఐ స్పష్టంగా వివరించింది. నమ్మకంగా నిర్ణయం తీసుకున్నాడు.",
        9,
    ),
    (
        "img-l5-s06-meera-habits.jpg",
        "మీరా ఉదయం వ్యాయామం, తక్కువ స్క్రీన్ టైమ్, ఎక్కువ కుటుంబ సమయం కోసం అలవాట్లు ఏర్పరచుకోవాలి. "
        "ఆమె అడిగింది: ఇద్దరు పిల్లలతో పని చేసే అమ్మకు నిజంగా సాధ్యమయ్యే రోజువారీ రొటీన్ తయారుచేయి. "
        "ఏఐ సూచించిన రొటీన్ ఆమె జీవితానికి సరిగ్గా సరిపోయింది.",
        9,
    ),
    (
        "img-l5-s07-practice.jpg",
        "ఈ స్థాయిలో 5 నిజమైన జీవిత పనులు సాధన చేస్తారు: "
        "ఇంటి బడ్జెట్, పిల్లల హోంవర్క్ సహాయం, కుటుంబ ట్రిప్ ప్లాన్, ఇన్స్యూరెన్స్ పోలిక, రోజువారీ రొటీన్. "
        "ప్రతి పని మీ స్వంత నంబర్లు, మీ పరిస్థితి వాడుతుంది.",
        10,
    ),
    (
        "img-l5-s08-celebration.jpg",
        "ఇదే స్థాయి 5. ఏఐ ఇప్పుడు మీ మొత్తం కుటుంబానికి సహాయపడుతోంది. "
        "తెలివైన బడ్జెట్, మంచి చదువు, సంతోషమైన ట్రిప్లు. "
        "స్థాయి 6 లో మీరు నిజమైన పవర్ యూజర్ అవుతారు. కలుద్దాం!",
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
