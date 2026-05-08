"""
Level 3 Telugu Intro Video Generator
Produces: content/assets/videos/level-03-intro-te.mp4
Run: .venv/bin/python scripts/generate_level03_video_te.py
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
AUDIO_DIR  = ROOT / "content" / "assets" / "videos" / "audio_tmp_te_03"
VIDEO_OUT  = ROOT / "content" / "assets" / "videos" / "level-03-intro-te.mp4"

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
        "img-l3-s01-hero.jpg",
        "మిత్ర ఏఐ లైఫ్ స్థాయి 3 కి స్వాగతం — స్మార్ట్ బేసిక్స్. "
        "ఏఐ జవాబు పొందడం సులభమే. ఆ జవాబును నమ్మాలా వద్దా అని నిర్ణయించడం ఒక నైపుణ్యం. "
        "ఈ స్థాయి మీకు స్పష్టంగా ఆలోచించడం నేర్పుతుంది.",
        9,
    ),
    (
        "img-l3-s02-arjun-mistake.jpg",
        "అర్జున్ ఒక మందు మోతాదు గురించి ఏఐ ని అడిగాడు. ఏఐ నమ్మకంగా జవాబు ఇచ్చింది. "
        "కానీ అర్జున్ డాక్టర్ ను అడిగాడు — జవాబు తప్పు అని తెలిసింది. "
        "ఆరోగ్యం, చట్టం, డబ్బు విషయాల్లో ఏఐ జవాబులు ఎల్లప్పుడూ నిపుణులతో తనిఖీ చేయండి.",
        10,
    ),
    (
        "img-l3-s03-meena-factcheck.jpg",
        "మీనా ఒక సులభమైన ట్రిక్ నేర్చుకుంది. "
        "ఏఐ కి అడుగుతుంది: ఇది నిర్ధారించడానికి ఎక్కడ చూడాలో చెప్పగలవా? "
        "ఏఐ సోర్స్ లింకులు ఇస్తుంది. ఈ ఒక్క అలవాటు మిమ్మల్ని చాలా తెలివైన ఏఐ యూజర్ ని చేస్తుంది.",
        9,
    ),
    (
        "img-l3-s04-rahul-steps.jpg",
        "రాహుల్ సైకిల్ రిపేర్ చేయడం ఎలా అని తెలియదు. "
        "ఏఐ కి అడిగాడు: ఒక్కో అడుగుగా వివరించు. "
        "పనులను అడుగులుగా విభజించడం ఏఐ జవాబులను అనుసరించడానికి చాలా సులభం చేస్తుంది.",
        9,
    ),
    (
        "img-l3-s05-priya-tone.jpg",
        "ప్రియ తన హౌస్ ఓనర్ కి ఏఐ తో కంప్లైంట్ రాసింది. "
        "మొదటి డ్రాఫ్ట్ చాలా కఠినంగా వచ్చింది. "
        "ఆమె అడిగింది: దీన్ని మర్యాదగా కానీ గట్టిగా తిరిగి రాయి. "
        "టోన్ కంట్రోల్ అత్యంత శక్తివంతమైన ప్రాంప్టింగ్ నైపుణ్యాల్లో ఒకటి.",
        9,
    ),
    (
        "img-l3-s06-kiran-compare.jpg",
        "కిరణ్ ఒకే ప్రశ్నకు రెండు ఏఐ జవాబులు పోల్చాడు — సాధారణ ప్రాంప్ట్ తో ఒకటి, వివరమైన ప్రాంప్ట్ తో ఒకటి. "
        "వివరమైన ప్రాంప్ట్ జవాబు పది రెట్లు ఉపయోగకరంగా ఉంది. "
        "మీ జవాబు నాణ్యత మీ ప్రశ్న నాణ్యతపై ఆధారపడి ఉంటుంది.",
        9,
    ),
    (
        "img-l3-s07-prompt-library.jpg",
        "అనుభవజ్ఞులైన యూజర్ల రహస్యం: వారు తమ మంచి ప్రాంప్టులు సేవ్ చేస్తారు. "
        "రాయడానికి, ప్లాన్ చేయడానికి, నేర్చుకోవడానికి మంచి ప్రాంప్ట్ దొరికితే — నోట్స్ యాప్ లో సేవ్ చేయండి. "
        "మీరు మీ స్వంత ప్రాంప్ట్ లైబ్రరీ నిర్మిస్తున్నారు.",
        10,
    ),
    (
        "img-l3-s08-practice.jpg",
        "ఈ స్థాయిలో 5 నిజమైన నైపుణ్యాలు సాధన చేస్తారు: "
        "ఏఐ జవాబు ఫాక్ట్ చెక్ చేయడం, అడుగు అడుగు సహాయం అడగడం, "
        "మెసేజ్ టోన్ మార్చడం, రెండు జవాబులు పోల్చడం, మీ మొదటి ప్రాంప్ట్ సేవ్ చేయడం. "
        "ప్రతి నైపుణ్యం ఐదు నిమిషాల్లో చేయవచ్చు.",
        10,
    ),
    (
        "img-l3-s09-celebration.jpg",
        "ఇదే స్థాయి 3. మీరు ఇప్పుడు కేవలం ఏఐ వాడటం లేదు — దానితో ఆలోచిస్తున్నారు. "
        "క్విజ్ పూర్తి చేసి స్థాయి 3 సర్టిఫికేట్ తీసుకోండి. "
        "స్థాయి 4 లో ఏఐ మీ వర్క్ పార్టనర్ అవుతుంది. కలుద్దాం!",
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
print(f"Upload: source .env && aws s3 cp {VIDEO_OUT} s3://mitra-ai-life-assets/videos/level-03-intro-te.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")
