#!/usr/bin/env python3
"""
generate_teachers_overview_video.py

Generates the "2 minutes overview" video for the AI for Teachers track.
Produces two MP4s:
  - teachers-overview-en.mp4 (English voiceover)
  - teachers-overview-te.mp4 (Telugu voiceover)

Each video = 8 branded slide images (1920×1080) + OpenAI TTS voiceover,
muxed per-segment and losslessly concatenated.

Run:
    source .venv/bin/activate
    python scripts/generate_teachers_overview_video.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content" / "assets" / "videos" / "teachers-overview"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VERSION_SUFFIX_BY_LANG = {"en": "", "te": "-v2"}

# ── load .env ─────────────────────────────────────────────────────────────────
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

W, H = 1920, 1080
BG     = (6, 17, 31)       # #06111f navy
AMBER  = (245, 158, 11)    # #f59e0b
CYAN   = (104, 225, 255)   # #68e1ff
TEXT   = (245, 248, 252)
MUTED  = (170, 190, 210)

# ── fonts ─────────────────────────────────────────────────────────────────────
def _find_font(candidates: list[str]) -> str:
    for c in candidates:
        if Path(c).exists():
            return c
    raise SystemExit(f"No font found among: {candidates}")

FONT_HEADING = _find_font([
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
FONT_BODY = _find_font([
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
# Telugu requires a font that covers Telugu glyphs.
FONT_TE = _find_font([
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Bold.ttf"),
    "/System/Library/Fonts/KohinoorTelugu.ttc",
    "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc",
])

# ── slide content ─────────────────────────────────────────────────────────────
# Each slide: (eyebrow, big_title, subline)
SLIDES_EN = [
    ("MITRA AI LIFE",
     "AI for Teachers",
     "Free course • 8 short lessons • Start today"),
    ("FOR EVERY TEACHER",
     "Save 2 to 3 hours every week",
     "Lesson plans, worksheets, question papers — in minutes."),
    ("LESSON 01 to 03",
     "Start with the basics",
     "AI overview • ChatGPT, Gemini, Claude • The simple prompt formula"),
    ("LESSON 04 to 06",
     "Build real teaching material",
     "Lesson plans • Worksheets and answer keys • Question paper drafts"),
    ("LESSON 07 and 08",
     "Safe and responsible AI use",
     "Review every AI output • Protect student privacy"),
    ("ONE PROMPT, ONE LESSON PLAN",
     "Type a topic. Get a full plan.",
     "Then you review, edit, and use it in class."),
    ("YOU STAY IN CONTROL",
     "AI helps. Teacher decides.",
     "Every lesson teaches you what to check before using AI output."),
    ("START FREE TODAY",
     "mitraailife.com/site/teachers.html",
     "8 lessons • Free • No sign-up needed"),
]

SLIDES_TE = [
    ("MITRA AI LIFE",
     "Teachers కోసం AI",
    "8 short lessons • ఇవాళే మొదలు పెట్టండి"),
    ("ప్రతి teacher కోసం",
     "వారానికి 2 నుండి 3 గంటలు ఆదా",
    "Lesson plan. Worksheet. Question paper draft. Step by step."),
    ("LESSON 01 నుండి 03",
     "Basics తో మొదలు పెట్టండి",
    "AI basics. ChatGPT. Gemini. Claude. Simple prompt formula."),
    ("LESSON 04 నుండి 06",
     "Real teaching material తయారు చేయండి",
    "Plan తయారు చేయండి. Worksheet తయారు చేయండి. Answer key check చేయండి."),
    ("LESSON 07 మరియు 08",
     "Safe మరియు responsible AI use",
    "AI output review చేయండి. Student privacy కాపాడండి."),
    ("ఒక prompt, ఒక lesson plan",
     "Topic type చేయండి. పూర్తి plan వస్తుంది.",
     "మీరు review చేసి, edit చేసి, class లో వాడండి."),
    ("ఇది మీ control లో ఉంటుంది",
    "AI help చేస్తుంది. Teacher decide చేస్తారు.",
     "AI output వాడే ముందు ఏమి check చేయాలో ప్రతి lesson నేర్పుతుంది."),
    ("ఇవాళే మొదలు పెట్టండి",
    "Teacher AI Basics",
    "Lesson plan practice. Worksheet practice. Safety practice."),
]

# Voiceover narration per slide (English + Telugu).
NARR_EN = [
    "Mitra AI Life presents — A I for Teachers. A free course with eight short lessons. You can start today.",
    "Designed for every teacher. Save two to three hours every week. Lesson plans, worksheets, and question papers in minutes.",
    "Lessons one to three. Start with the basics. An A I overview. Chat G P T, Gemini, and Claude. Then learn the simple prompt formula.",
    "Lessons four to six. Build real teaching material. Lesson plans. Worksheets with answer keys. And question paper drafts.",
    "Lessons seven and eight. Safe and responsible A I use. Review every A I output. Protect student privacy.",
    "One prompt, one lesson plan. You type a topic. A I gives you a full plan. Then you review, edit, and use it in class.",
    "You stay in control. A I helps. The teacher decides. Every lesson teaches you what to check before using A I output.",
    "Start free today. Visit mitra ai life dot com, site, teachers dot H T M L. Eight lessons. Free. No sign up needed.",
]

NARR_TE = [
    "మిత్ర ఏ ఐ లైఫ్ లో టీచర్స్ కోసం ఏ ఐ ట్రాక్. ఇది teacher కి simple starting point. ఒక్కో lesson చిన్నదిగా ఉంటుంది.",
    "ఈ ట్రాక్ preparation time తగ్గించడానికి help చేస్తుంది. ముందు lesson plan. తర్వాత worksheet. తర్వాత question paper draft. ప్రతి పని step by step.",
    "మొదట basics. ఏ ఐ అంటే ఏమిటి. ChatGPT ని ఎలా అడగాలి. Gemini ని ఎలా అడగాలి. Claude ని ఎలా compare చేయాలి.",
    "తర్వాత teaching material. ఒక topic తీసుకుంటాం. Plan చేస్తాం. Worksheet చేస్తాం. Answer key check చేస్తాం.",
    "తర్వాత safety. Student private details paste చేయకూడదు. AI answer ని blindly use చేయకూడదు. Teacher review తప్పనిసరి.",
    "మీరు topic type చేస్తారు. AI draft ఇస్తుంది. మీరు edit చేస్తారు. Class కి suit అయ్యేలా final చేస్తారు.",
    "ఇది మీ control లో ఉంటుంది. AI help చేస్తుంది. Final decision teacher తీసుకుంటారు. Use చేసే ముందు checklist follow చేస్తారు.",
    "Teacher AI Basics తో మొదలు పెట్టండి. Lesson plan practice. Worksheet practice. Safety practice. ఒక్కొక్కటి clear గా నేర్చుకుంటారు.",
]

assert len(SLIDES_EN) == len(NARR_EN) == 8
assert len(SLIDES_TE) == len(NARR_TE) == 8

# ── slide rendering ───────────────────────────────────────────────────────────
def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_w: int,
              draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines, current = [], words[0]
    for w in words[1:]:
        trial = current + " " + w
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w:
            current = trial
        else:
            lines.append(current)
            current = w
    lines.append(current)
    return lines


def render_slide(eyebrow: str, title: str, subline: str, path: Path,
                 lang: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle accent strip
    d.rectangle([0, 0, W, 14], fill=AMBER)

    # decorative side bar
    d.rectangle([0, H - 14, W, H], fill=CYAN)

    is_te = lang == "te"
    f_eye   = ImageFont.truetype(FONT_BODY, 38)
    f_title = ImageFont.truetype(FONT_TE if is_te else FONT_HEADING, 110)
    f_sub   = ImageFont.truetype(FONT_TE if is_te else FONT_BODY, 52)

    # eyebrow (always English / ASCII safe)
    eye_bbox = d.textbbox((0, 0), eyebrow, font=f_eye)
    eye_w = eye_bbox[2] - eye_bbox[0]
    d.rectangle(
        [(W - eye_w) / 2 - 28, 110, (W + eye_w) / 2 + 28, 110 + 70],
        outline=AMBER, width=3,
    )
    d.text(((W - eye_w) / 2, 122), eyebrow, fill=AMBER, font=f_eye)

    # title (centered, wrapped)
    title_lines = wrap_text(title, f_title, int(W * 0.86), d)
    line_h = f_title.size + 22
    title_total_h = line_h * len(title_lines)
    y = (H - title_total_h) / 2 - 60
    for line in title_lines:
        bb = d.textbbox((0, 0), line, font=f_title)
        lw = bb[2] - bb[0]
        d.text(((W - lw) / 2, y), line, fill=TEXT, font=f_title)
        y += line_h

    # subline
    sub_lines = wrap_text(subline, f_sub, int(W * 0.84), d)
    sub_line_h = f_sub.size + 14
    y_sub = y + 50
    for line in sub_lines:
        bb = d.textbbox((0, 0), line, font=f_sub)
        lw = bb[2] - bb[0]
        d.text(((W - lw) / 2, y_sub), line, fill=MUTED, font=f_sub)
        y_sub += sub_line_h

    # brand footer
    f_brand = ImageFont.truetype(FONT_BODY, 30)
    brand = "mitraailife.com"
    bb = d.textbbox((0, 0), brand, font=f_brand)
    d.text((W - (bb[2] - bb[0]) - 60, H - 70), brand, fill=MUTED, font=f_brand)

    img.save(path, "JPEG", quality=92)


# ── TTS ───────────────────────────────────────────────────────────────────────
def tts_to_file(text: str, out_path: Path, lang: str) -> None:
    if out_path.exists():
        return
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=text,
        speed=0.88 if lang == "te" else 0.95,
    ) as response:
        response.stream_to_file(str(out_path))
    print(f"  [tts:{lang}] {out_path.name}")


# ── ffmpeg helpers ────────────────────────────────────────────────────────────
def audio_duration(p: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p),
    ])
    return float(out.strip())


def make_segment(img: Path, audio: Path, out_mp4: Path,
                 head_sil: float = 0.30, tail_sil: float = 0.45) -> None:
    """Create a segment: still image + audio with leading/trailing silence."""
    a_dur = audio_duration(audio)
    total = head_sil + a_dur + tail_sil

    # Build a silent intro + audio + silent outro using ffmpeg filter
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{total:.3f}", "-i", str(img),
        "-i", str(audio),
        "-f", "lavfi", "-t", f"{head_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-f", "lavfi", "-t", f"{tail_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex",
        f"[2:a][1:a][3:a]concat=n=3:v=0:a=1[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def concat_mp4s(mp4s: list[Path], out_mp4: Path) -> None:
    listfile = out_mp4.parent / f"_concat_{out_mp4.stem}.txt"
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in mp4s))
    # Use re-encode (not -c copy) to ensure smooth concat with consistent encoding
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(listfile),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    listfile.unlink()


# ── main build per language ───────────────────────────────────────────────────
def build_lang(lang: str, slides: list[tuple], narration: list[str]) -> Path:
    print(f"\n══════ Building {lang.upper()} video ══════")
    work = OUT_DIR / lang
    work.mkdir(parents=True, exist_ok=True)

    segments: list[Path] = []
    for i, ((eye, title, sub), narr) in enumerate(zip(slides, narration), 1):
        idx = f"{i:02d}"
        img_p = work / f"slide-{idx}.jpg"
        aud_p = work / f"narr-{idx}.mp3"
        seg_p = work / f"seg-{idx}.mp4"

        print(f"\n[{idx}] {title}")
        render_slide(eye, title, sub, img_p, lang)
        if i == 1:
            suffix = VERSION_SUFFIX_BY_LANG[lang]
            shutil.copyfile(img_p, OUT_DIR / f"teachers-overview-{lang}{suffix}-poster.jpg")
        tts_to_file(narr, aud_p, lang)

        if not seg_p.exists():
            print(f"  [seg] {seg_p.name}")
            make_segment(img_p, aud_p, seg_p)
        segments.append(seg_p)

    suffix = VERSION_SUFFIX_BY_LANG[lang]
    out_mp4 = OUT_DIR / f"teachers-overview-{lang}{suffix}.mp4"
    print(f"\n══ Concatenating into {out_mp4.name}")
    concat_mp4s(segments, out_mp4)
    dur = audio_duration(out_mp4)
    sz_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"  ✅ {out_mp4.name}  duration={dur:.1f}s  size={sz_mb:.2f} MB")
    return out_mp4


# ── upload to S3 ──────────────────────────────────────────────────────────────
def upload_to_s3(local: Path, key: str, content_type: str) -> str:
    import boto3
    s3 = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    BUCKET = "mitra-ai-life-assets"
    s3.upload_file(
        str(local), BUCKET, key,
        ExtraArgs={"ContentType": content_type, "CacheControl": "public,max-age=31536000"},
    )
    url = f"https://{BUCKET}.s3.{os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')}.amazonaws.com/{key}"
    print(f"  📤 uploaded: {url}")
    return url


def main(langs: list[str] | None = None):
    if langs is None:
        langs = ["en", "te"]
    outputs = {}
    if "en" in langs:
        outputs["en"] = build_lang("en", SLIDES_EN, NARR_EN)
    if "te" in langs:
        outputs["te"] = build_lang("te", SLIDES_TE, NARR_TE)

    print("\n══════ Uploading to S3 ══════")
    urls = {}
    for lang, mp4_path in outputs.items():
        suffix = VERSION_SUFFIX_BY_LANG[lang]
        poster_path = OUT_DIR / f"teachers-overview-{lang}{suffix}-poster.jpg"
        urls[f"{lang}_mp4"] = upload_to_s3(mp4_path, f"videos/teachers/teachers-overview-{lang}{suffix}.mp4", "video/mp4")
        urls[f"{lang}_poster"] = upload_to_s3(poster_path, f"videos/teachers/teachers-overview-{lang}{suffix}-poster.jpg", "image/jpeg")

    print("\n══════ DONE ══════")
    for label, url in urls.items():
        print(f"{label}: {url}")
    print("\nNext: replace the 'VIDEO COMING SOON' / 'VIDEO త్వరలో' placeholders")
    print("      in site/teachers.html and site/teachers-te.html with HTML5 <video> tags.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--lang", choices=["en", "te", "both"], default="both")
    p.add_argument("--force", action="store_true", help="Delete cached segments before building")
    args = p.parse_args()
    langs = ["en", "te"] if args.lang == "both" else [args.lang]
    if args.force:
        for lang in langs:
            work = OUT_DIR / lang
            if work.exists():
                shutil.rmtree(work)
            suffix = VERSION_SUFFIX_BY_LANG[lang]
            final = OUT_DIR / f"teachers-overview-{lang}{suffix}.mp4"
            if final.exists():
                final.unlink()
            poster = OUT_DIR / f"teachers-overview-{lang}{suffix}-poster.jpg"
            if poster.exists():
                poster.unlink()
    main(langs)
