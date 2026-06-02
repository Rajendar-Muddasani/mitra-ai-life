#!/usr/bin/env python3
"""
generate_small_business_overview_video.py

Generates the "2 minutes overview" video for the AI for Small Business track.
Produces two MP4s:
  - small-business-overview-en-charon.mp4   (English · Chirp3-HD-Charon)
  - small-business-overview-te-standard-a.mp4  (Telugu  · te-IN-Standard-A)

Each video = 8 branded slide images (1920×1080) + Google Cloud TTS voiceover,
muxed per-segment and losslessly concatenated.

Run:
    source .venv/bin/activate
    python scripts/generate_small_business_overview_video.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content" / "assets" / "videos" / "small-business-overview"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VERSION_SUFFIX_BY_LANG = {
    "en": "-en-charon",
    "te": "-te-standard-a",
}
TTS_BY_LANG = {
    "en": ("en-US", "en-US-Chirp3-HD-Charon", 1.0),
    "te": ("te-IN", "te-IN-Standard-A", 0.90),
}

# ── load .env ──────────────────────────────────────────────────────────────────
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

W, H = 1920, 1080
BG     = (6, 17, 31)
AMBER  = (245, 158, 11)
CYAN   = (104, 225, 255)
TEXT   = (245, 248, 252)
MUTED  = (170, 190, 210)

# ── fonts ──────────────────────────────────────────────────────────────────────
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
FONT_TE = _find_font([
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Bold.ttf"),
    "/System/Library/Fonts/KohinoorTelugu.ttc",
    "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc",
])

# ── slide content ──────────────────────────────────────────────────────────────
SLIDES_EN = [
    ("MITRA AI LIFE",
     "AI for Small Business",
     "Free · Early Access · Start today"),
    ("YOUR PHONE IS FULL",
     "Customer messages all day.",
     "Enquiries. Complaints. Offers. Reviews. No time to write each one well."),
    ("ONE PACK, FOUR MODULES",
     "Customer Replies and Promotions",
     "Module 1: Fast replies  ·  Module 2: Offers  ·  Module 3: Reviews  ·  Module 4: Planning"),
    ("MODULE 1",
     "Fast customer replies",
     "Type what you want to say. AI drafts it. You read, edit, send."),
    ("MODULE 2",
     "Offers and promotions",
     "WhatsApp offers · Instagram captions · Poster text · Festival promotions"),
    ("MODULE 3",
     "Reviews and complaint handling",
     "Google reviews · WhatsApp complaints · Right tone every time"),
    ("MODULE 4",
     "Weekly and festival planning",
     "5-message weekly plan · Festival calendar · One idea, many messages"),
    ("FREE · EARLY ACCESS",
     "For every small business in India",
     "Kirana · Tiffin · Salon · Bakery · Tuition · Repair shop"),
]

SLIDES_TE = [
    ("MITRA AI LIFE",
     "Small Business కోసం AI",
     "Free · Early Access · ఇవాళే మొదలు పెట్టండి"),
    ("మీ phone నిండా messages",
     "రోజూ customer messages.",
     "Enquiries. Complaints. Offers. Reviews. ప్రతిదానికి reply రాయడానికి time లేదు."),
    ("ఒక pack, నాలుగు modules",
     "Customer Replies and Promotions",
     "Module 1: Fast replies  ·  Module 2: Offers  ·  Module 3: Reviews  ·  Module 4: Planning"),
    ("MODULE 1",
     "వేగంగా customer replies",
     "మీకు ఏం చెప్పాలో type చేయండి. AI draft ఇస్తుంది. మీరు చదివి send చేయండి."),
    ("MODULE 2",
     "Offers మరియు promotions",
     "WhatsApp offers · Instagram captions · Poster text · Festival promotions"),
    ("MODULE 3",
     "Reviews మరియు complaints",
     "Google reviews · WhatsApp complaints · సరైన tone తో respond చేయండి"),
    ("MODULE 4",
     "Weekly మరియు festival planning",
     "5-message weekly plan · Festival calendar · ఒక idea, చాలా messages"),
    ("FREE · EARLY ACCESS",
     "India లో ప్రతి small business కోసం",
     "Kirana · Tiffin · Salon · Bakery · Tuition · Repair shop"),
]

NARR_EN = [
    "Mitra A I Life — A I for Small Business. Free during early access. Start today.",
    "You run a business. Every day your phone is full — enquiries, complaints, offers, reviews. Writing a good reply every time takes time you don't have.",
    "The Customer Replies and Promotions Starter Pack has four modules. Fast replies. Offers. Reviews. And weekly planning.",
    "Module one. Fast customer replies. You describe what you want to say in plain words. A I gives you a polished draft in seconds. You read it, edit if needed, and send.",
    "Module two. Offers and promotions. Write WhatsApp offer messages, Instagram captions, poster text, and festival promotions faster — without hype.",
    "Module three. Reviews and complaint handling. Respond to positive reviews, negative Google reviews, and WhatsApp complaints with the right tone — not defensive, not robotic.",
    "Module four. Weekly and festival planning. Build a simple five-message plan for one week. Map it to festivals and local events. One idea reused in many short messages.",
    "Free during early access. For every small business in India. Kirana. Tiffin. Salon. Home bakery. Tuition centre. Repair shop. Start today at mitra A I life dot com.",
]

NARR_TE = [
    "మిత్ర ఏ ఐ లైఫ్ — Small Business కోసం ఏ ఐ. Early access లో free. ఇవాళే మొదలు పెట్టండి.",
    "మీకు business ఉంది. రోజూ phone నిండా messages — enquiries, complaints, offers, reviews. ప్రతి reply బాగా రాయడానికి time లేదు.",
    "Customer Replies and Promotions Starter Pack లో నాలుగు modules ఉన్నాయి. Fast replies. Offers. Reviews. మరియు weekly planning.",
    "Module one. వేగంగా customer replies. మీకు ఏం చెప్పాలో plain words లో type చేయండి. AI seconds లో draft ఇస్తుంది. మీరు చదివి edit చేసి send చేయండి.",
    "Module two. Offers మరియు promotions. WhatsApp offers, Instagram captions, poster text, మరియు festival promotions వేగంగా రాయండి. Hype లేకుండా.",
    "Module three. Reviews మరియు complaint handling. Positive reviews, negative Google reviews, మరియు WhatsApp complaints కి right tone తో respond చేయండి.",
    "Module four. Weekly మరియు festival planning. ఒక week కి simple five-message plan build చేయండి. Festivals మరియు local events తో connect చేయండి.",
    "Early access లో free. India లో ప్రతి small business కోసం. Kirana. Tiffin. Salon. Home bakery. Tuition centre. Repair shop. ఇవాళే mitra A I life dot com చూడండి.",
]

assert len(SLIDES_EN) == len(NARR_EN) == 8
assert len(SLIDES_TE) == len(NARR_TE) == 8


# ── slide rendering ────────────────────────────────────────────────────────────
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

    d.rectangle([0, 0, W, 14], fill=AMBER)
    d.rectangle([0, H - 14, W, H], fill=CYAN)

    is_te = lang == "te"
    f_eye   = ImageFont.truetype(FONT_BODY, 38)
    f_title = ImageFont.truetype(FONT_TE if is_te else FONT_HEADING, 110)
    f_sub   = ImageFont.truetype(FONT_TE if is_te else FONT_BODY, 52)

    eye_bbox = d.textbbox((0, 0), eyebrow, font=f_eye)
    eye_w = eye_bbox[2] - eye_bbox[0]
    d.rectangle(
        [(W - eye_w) / 2 - 28, 110, (W + eye_w) / 2 + 28, 110 + 70],
        outline=AMBER, width=3,
    )
    d.text(((W - eye_w) / 2, 122), eyebrow, fill=AMBER, font=f_eye)

    title_lines = wrap_text(title, f_title, int(W * 0.86), d)
    line_h = f_title.size + 22
    title_total_h = line_h * len(title_lines)
    y = (H - title_total_h) / 2 - 60
    for line in title_lines:
        bb = d.textbbox((0, 0), line, font=f_title)
        lw = bb[2] - bb[0]
        d.text(((W - lw) / 2, y), line, fill=TEXT, font=f_title)
        y += line_h

    sub_lines = wrap_text(subline, f_sub, int(W * 0.84), d)
    sub_line_h = f_sub.size + 14
    y_sub = y + 50
    for line in sub_lines:
        bb = d.textbbox((0, 0), line, font=f_sub)
        lw = bb[2] - bb[0]
        d.text(((W - lw) / 2, y_sub), line, fill=MUTED, font=f_sub)
        y_sub += sub_line_h

    f_brand = ImageFont.truetype(FONT_BODY, 30)
    brand = "mitraailife.com"
    bb = d.textbbox((0, 0), brand, font=f_brand)
    d.text((W - (bb[2] - bb[0]) - 60, H - 70), brand, fill=MUTED, font=f_brand)

    img.save(path, "JPEG", quality=92)


# ── TTS ────────────────────────────────────────────────────────────────────────
def tts_to_file(text: str, out_path: Path, lang: str) -> None:
    """Synthesise speech via Google Cloud TTS (service account) and save as MP3."""
    if out_path.exists():
        return
    from google.cloud import texttospeech
    lang_code, voice_name, speed = TTS_BY_LANG[lang]
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
        ),
        timeout=45,
    )
    out_path.write_bytes(response.audio_content)
    print(f"    [tts:{lang}] {out_path.name}")


# ── ffmpeg helpers ─────────────────────────────────────────────────────────────
def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(result.stderr.decode(), file=sys.stderr)
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:4])}")


def mux_slide(img_path: Path, audio_path: Path, out_path: Path) -> None:
    _run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(audio_path),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-pix_fmt", "yuv420p",
        str(out_path),
    ])


def extract_poster(video_path: Path, poster_path: Path) -> None:
    _run([
        "ffmpeg", "-y", "-ss", "2",
        "-i", str(video_path),
        "-frames:v", "1", "-q:v", "3",
        str(poster_path),
    ])


def concat_segments(segment_paths: list[Path], out_path: Path) -> None:
    list_file = out_path.parent / f"_concat_{out_path.stem}.txt"
    list_file.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in segment_paths)
    )
    _run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(out_path),
    ])
    list_file.unlink(missing_ok=True)


# ── S3 upload ──────────────────────────────────────────────────────────────────
def upload_to_s3(local: Path, s3_key: str) -> None:
    bucket = "mitra-ai-life-assets"
    cmd = ["aws", "s3", "cp", str(local), f"s3://{bucket}/{s3_key}",
           "--content-type", "video/mp4" if local.suffix == ".mp4" else "image/jpeg",
           "--cache-control", "public, max-age=31536000"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  S3 upload warning: {result.stderr.decode()[:200]}", file=sys.stderr)
    else:
        print(f"  ✓ uploaded → s3://{bucket}/{s3_key}")


# ── main ───────────────────────────────────────────────────────────────────────
def build_lang(lang: str) -> Path:
    slides = SLIDES_EN if lang == "en" else SLIDES_TE
    narr   = NARR_EN   if lang == "en" else NARR_TE
    suffix = VERSION_SUFFIX_BY_LANG[lang]
    lang_dir = OUT_DIR / lang
    lang_dir.mkdir(exist_ok=True)

    segments: list[Path] = []
    for i, ((eye, title, sub), text) in enumerate(zip(slides, narr)):
        print(f"  [{lang}] slide {i + 1}/8 …")
        img_p   = lang_dir / f"slide_{i:02d}.jpg"
        mp3_p   = lang_dir / f"slide_{i:02d}.mp3"
        seg_p   = lang_dir / f"seg_{i:02d}.mp4"

        render_slide(eye, title, sub, img_p, lang)
        tts_to_file(text, mp3_p, lang)
        mux_slide(img_p, mp3_p, seg_p)
        segments.append(seg_p)

    final_name = f"small-business-overview{suffix}.mp4"
    final_path = OUT_DIR / final_name
    print(f"  [{lang}] concatenating → {final_name}")
    concat_segments(segments, final_path)

    poster_path = OUT_DIR / final_name.replace(".mp4", "-poster.jpg")
    extract_poster(final_path, poster_path)

    # Upload to S3
    s3_prefix = "videos/track-overviews"
    upload_to_s3(final_path,   f"{s3_prefix}/{final_name}")
    upload_to_s3(poster_path,  f"{s3_prefix}/{poster_path.name}")

    print(f"  [{lang}] done → {final_path}")
    return final_path


def main() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg not found. Install with: brew install ffmpeg")
    for lang in ("en", "te"):
        print(f"\n─── Building {lang.upper()} video ───")
        build_lang(lang)
    print("\n✓ Both videos built and uploaded to S3.")
    print("  HTML src/poster URLs:")
    print("  EN: https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/videos/track-overviews/small-business-overview-en-charon.mp4")
    print("  TE: https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/videos/track-overviews/small-business-overview-te-standard-a.mp4")


if __name__ == "__main__":
    main()
