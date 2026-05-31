#!/usr/bin/env python3
"""
Generate the Telugu homepage hero video for site/index-te.html.

Output:
    content/assets/videos/home/home-hero-te-standard-a.mp4
    content/assets/videos/home/home-hero-te-standard-a-poster.jpg

Usage:
  source .venv/bin/activate
  source .env
  python scripts/generate_home_hero_te_video.py --force
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content" / "assets" / "videos" / "home"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VERSION_SUFFIX = "-standard-a"
TTS_LANGUAGE_CODE = "te-IN"
TTS_VOICE = "te-IN-Standard-A"
TTS_SPEAKING_RATE = 0.90

WIDTH, HEIGHT = 1920, 1080
NAVY  = (5, 10, 26)
INK   = (248, 251, 255)
MUTED = (180, 198, 222)
CYAN  = (104, 225, 255)
BLUE  = (83, 166, 255)
AMBER = (245, 158, 11)
GREEN = (16, 185, 129)
MITRA_URL = (
    "https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/"
    "characters/mitra-reference.png"
)

FONT_DIR = ROOT / "scripts" / "_fonts"


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()


def find_font(candidates: list[str]) -> str:
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise SystemExit(f"No font found among: {candidates}")


# Latin label font (eyebrow / brand / step counter)
FONT_LATIN = find_font([
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])

# Telugu script fonts — title and subline
FONT_TE_BOLD    = str(FONT_DIR / "NotoSansTelugu-Bold.ttf")
FONT_TE_REGULAR = str(FONT_DIR / "NotoSansTelugu-Regular.ttf")

# ──────────────────────────────────────────────────────────────────────────────
# Slide content: (eyebrow_en, title_te, subline_te, narration_te)
# eyebrow stays in English/Latin so the badge renders crisply.
# title, subline, narration are in Telugu.
# ──────────────────────────────────────────────────────────────────────────────
SLIDES = [
    (
        "MITRA AI LIFE",
        "రోజువారీ AI నైపుణ్యాలు",
        "ప్రతి భారతీయ కుటుంబానికి ఒకే సింపుల్ హోమ్",
        "మిత్ర AI లైఫ్ ప్రతి భారతీయ కుటుంబానికి "
        "రోజువారీ AI నైపుణ్యాలు ఒకే సింపుల్ హోమ్‌లో అందిస్తుంది.",
    ),
    (
        "ఒకే URL",
        "రోజువారీ AI, విద్యార్థులు, ట్యూషన్, ఇంగ్లీష్",
        "విడివిడి ట్రాక్‌లు, ఒక విశ్వసనీయ మార్గదర్శి",
        "రోజువారీ AI నైపుణ్యాలు, బడి విద్యార్థులు, AI ట్యూషన్, "
        "స్పోకెన్ ఇంగ్లీష్, చిన్న వ్యాపారం, ఉపాధ్యాయులు "
        "మరియు కళాశాల ప్రాజెక్ట్ కిట్‌ల కోసం విడివిడి ట్రాక్‌లు ఉన్నాయి.",
    ),
    (
        "ఉచిత లెర్నింగ్",
        "ఒత్తిడి లేకుండా మొదలు పెట్టండి",
        "చదవండి, చూడండి, ప్రాక్టీస్ చేయండి",
        "మొదటి వాగ్దానం ఉచిత లెర్నింగ్. అడ్వాన్స్‌డ్ ప్రాజెక్ట్‌లకు "
        "వెళ్ళే ముందు సింపుల్ పాఠాలు, చిన్న వీడియోలు "
        "మరియు ప్రాక్టికల్ ఉదాహరణలతో మొదలు పెట్టండి.",
    ),
    (
        "భారత్ కోసం",
        "రోజువారీ జీవితం నుండి నిజమైన ఉదాహరణలు",
        "కుటుంబాలు, బళ్ళు, దుకాణాలు, ఉపాధ్యాయులు",
        "ప్రతి పాఠం నిజమైన భారతీయ అవసరాలను వాడుతుంది. "
        "హోంవర్క్, వాట్సాప్ మెసేజ్‌లు, భద్రత, ప్రైవసీ, "
        "స్థానిక వ్యాపారం, పరీక్షలు మరియు కెరీర్ నైపుణ్యాలు.",
    ),
    (
        "సురక్షితంగా & నిజాయితీగా",
        "AI సహాయం చేస్తుంది. మనుషులు నిర్ణయిస్తారు.",
        "facts తనిఖీ చేయండి, privacy కాపాడుకోండి",
        "మిత్ర AI లైఫ్ సురక్షితమైన మరియు నిజాయితీగల AI వాడకాన్ని "
        "నేర్పిస్తుంది. facts తనిఖీ చేయండి, privacy కాపాడుకోండి, "
        "మోసం చేయవద్దు, మరియు మనుషులే నియంత్రణలో ఉండాలి.",
    ),
    (
        "ఈరోజే మొదలు పెట్టండి",
        "మీకు నచ్చిన ట్రాక్ ఎంచుకోండి",
        "mitraailife.com",
        "ఈరోజే మొదలు పెట్టండి. మిత్ర AI లైఫ్ తెరవండి, "
        "మీకు నచ్చిన ట్రాక్ ఎంచుకోండి, "
        "మరియు ఒకో ఉపయోగకరమైన నైపుణ్యాన్ని నేర్చుకోండి.",
    ),
]


def wrap_text(
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    draw: ImageDraw.ImageDraw,
) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def blend(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
    ratio: float,
) -> tuple[int, int, int]:
    return tuple(int(left[i] * (1 - ratio) + right[i] * ratio) for i in range(3))


def get_mitra_image() -> Image.Image | None:
    local_path = OUT_DIR / "mitra-reference.png"
    if not local_path.exists():
        try:
            urllib.request.urlretrieve(MITRA_URL, local_path)
        except Exception as exc:
            print(f"  [warn] could not download Mitra reference image: {exc}")
            return None
    return Image.open(local_path).convert("RGBA")


def paste_circle(
    base: Image.Image,
    avatar: Image.Image,
    center: tuple[int, int],
    size: int,
) -> None:
    avatar = avatar.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)
    x = center[0] - size // 2
    y = center[1] - size // 2
    ring = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse(
        (0, 0, size + 23, size + 23),
        fill=(83, 166, 255, 70),
        outline=(104, 225, 255, 180),
        width=5,
    )
    base.alpha_composite(ring, (x - 12, y - 12))
    base.paste(avatar, (x, y), mask)


def render_slide(
    slide_number: int,
    eyebrow: str,
    title: str,
    subline: str,
    path: Path,
) -> None:
    image = Image.new("RGBA", (WIDTH, HEIGHT), NAVY + (255,))
    draw = ImageDraw.Draw(image)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = blend((5, 10, 26), (15, 35, 74), ratio)
        draw.line([(0, y), (WIDTH, y)], fill=color + (255,))

    for x in range(0, WIDTH, 84):
        draw.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 10))
    for y in range(0, HEIGHT, 84):
        draw.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 10))

    draw.ellipse((WIDTH - 520, -260, WIDTH + 190, 450), outline=CYAN + (145,), width=10)
    draw.ellipse((-260, HEIGHT - 430, 380, HEIGHT + 210), outline=AMBER + (140,), width=8)
    draw.rounded_rectangle(
        (78, 74, WIDTH - 78, HEIGHT - 74),
        radius=34,
        outline=(255, 255, 255, 34),
        width=2,
    )
    draw.rectangle((0, 0, WIDTH, 16), fill=AMBER + (255,))
    draw.rectangle((0, HEIGHT - 16, WIDTH, HEIGHT), fill=CYAN + (255,))

    mitra = get_mitra_image()
    if mitra is not None:
        paste_circle(image, mitra, (WIDTH // 2, 190), 144)

    # Latin eyebrow badge
    font_eye   = ImageFont.truetype(FONT_LATIN, 34)
    font_brand = ImageFont.truetype(FONT_LATIN, 30)
    font_step  = ImageFont.truetype(FONT_LATIN, 28)

    # Telugu title and subline — use Bold for title, Regular for subline
    font_title = ImageFont.truetype(FONT_TE_BOLD,    78)
    font_sub   = ImageFont.truetype(FONT_TE_REGULAR, 44)

    eye_width = draw.textbbox((0, 0), eyebrow, font=font_eye)[2]
    eye_y = 290
    draw.rounded_rectangle(
        (
            (WIDTH - eye_width) / 2 - 28,
            eye_y - 12,
            (WIDTH + eye_width) / 2 + 28,
            eye_y + 52,
        ),
        radius=20,
        outline=BLUE + (180,),
        width=3,
    )
    draw.text(((WIDTH - eye_width) / 2, eye_y), eyebrow, fill=CYAN + (255,), font=font_eye)

    title_lines = wrap_text(title, font_title, int(WIDTH * 0.78), draw)
    title_y = 390
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        line_width = bbox[2] - bbox[0]
        draw.text(
            ((WIDTH - line_width) / 2 + 4, title_y + 4),
            line,
            fill=(0, 0, 0, 190),
            font=font_title,
        )
        draw.text(
            ((WIDTH - line_width) / 2, title_y),
            line,
            fill=INK + (255,),
            font=font_title,
        )
        title_y += font_title.size + 14

    sub_lines = wrap_text(subline, font_sub, int(WIDTH * 0.72), draw)
    sub_y = title_y + 32
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        line_width = bbox[2] - bbox[0]
        draw.text(
            ((WIDTH - line_width) / 2, sub_y),
            line,
            fill=MUTED + (255,),
            font=font_sub,
        )
        sub_y += font_sub.size + 12

    step = f"{slide_number:02d} / {len(SLIDES):02d}"
    draw.text((88, HEIGHT - 74), step, fill=(255, 255, 255, 110), font=font_step)
    brand = "mitraailife.com"
    brand_width = draw.textbbox((0, 0), brand, font=font_brand)[2]
    draw.text(
        (WIDTH - brand_width - 88, HEIGHT - 76),
        brand,
        fill=MUTED + (210,),
        font=font_brand,
    )

    image.convert("RGB").save(path, "JPEG", quality=92)


def tts_to_file(text: str, out_path: Path) -> None:
    if out_path.exists():
        return
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANGUAGE_CODE, name=TTS_VOICE),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=TTS_SPEAKING_RATE,
        ),
        timeout=45,
    )
    out_path.write_bytes(response.audio_content)
    print(f"  [tts] {out_path.name}")


def audio_duration(path: Path) -> float:
    output = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ])
    return float(output.strip())


def make_segment(image_path: Path, audio_path: Path, output_path: Path) -> None:
    if output_path.exists():
        return
    lead_silence = 0.25
    tail_silence = 0.45
    total_duration = lead_silence + audio_duration(audio_path) + tail_silence
    command = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{total_duration:.3f}", "-i", str(image_path),
        "-i", str(audio_path),
        "-f", "lavfi", "-t", f"{lead_silence:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-f", "lavfi", "-t", f"{tail_silence:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex", "[2:a][1:a][3:a]concat=n=3:v=0:a=1[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", str(output_path),
    ]
    subprocess.run(command, check=True, capture_output=True, timeout=120)
    print(f"  [seg] {output_path.name}")


def concat_segments(segment_paths: list[Path], output_path: Path) -> None:
    list_file = output_path.parent / f"_concat_{output_path.stem}.txt"
    list_file.write_text(
        "".join(f"file '{segment.resolve()}'\n" for segment in segment_paths)
    )
    command = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart", str(output_path),
    ]
    subprocess.run(command, check=True, capture_output=True, timeout=180)
    list_file.unlink()


def build(force: bool = False) -> tuple[Path, Path]:
    work_dir = OUT_DIR / f"work-te{VERSION_SUFFIX}"
    output_path = OUT_DIR / f"home-hero-te{VERSION_SUFFIX}.mp4"
    poster_path = OUT_DIR / f"home-hero-te{VERSION_SUFFIX}-poster.jpg"

    if force and work_dir.exists():
        shutil.rmtree(work_dir)
    if force:
        for path in (output_path, poster_path):
            if path.exists():
                path.unlink()
    work_dir.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and poster_path.exists() and not force:
        print(f"skip final exists: {output_path}")
        return output_path, poster_path

    segments: list[Path] = []
    for index, (eyebrow, title, subline, narration) in enumerate(SLIDES, 1):
        scene_id = f"{index:02d}"
        image_path   = work_dir / f"slide-{scene_id}.jpg"
        audio_path   = work_dir / f"narr-{scene_id}.mp3"
        segment_path = work_dir / f"seg-{scene_id}.mp4"
        print(f"[{scene_id}] {title}")
        render_slide(index, eyebrow, title, subline, image_path)
        if index == 1:
            shutil.copyfile(image_path, poster_path)
        tts_to_file(narration, audio_path)
        make_segment(image_path, audio_path, segment_path)
        segments.append(segment_path)

    concat_segments(segments, output_path)
    duration = audio_duration(output_path)
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"done: {output_path} duration={duration:.1f}s size={size_mb:.2f} MB")
    return output_path, poster_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Regenerate cached media")
    args = parser.parse_args()
    video_path, poster_path = build(force=args.force)
    print("\nUpload commands:")
    print(
        f"  aws s3 cp {video_path} "
        f"s3://mitra-ai-life-assets/videos/home/home-hero-te{VERSION_SUFFIX}.mp4 "
        "--content-type 'video/mp4' --cache-control 'public, max-age=86400'"
    )
    print(
        f"  aws s3 cp {poster_path} "
        f"s3://mitra-ai-life-assets/videos/home/home-hero-te{VERSION_SUFFIX}-poster.jpg "
        "--content-type 'image/jpeg' --cache-control 'public, max-age=86400'"
    )


if __name__ == "__main__":
    main()
