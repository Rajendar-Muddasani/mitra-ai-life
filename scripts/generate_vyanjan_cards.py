"""
Generate Hindi vyanjan (consonant) letter card images and a narrated video.

For each of the 33 standard vyanjan:
  - A PIL-rendered PNG card (exact Devanagari, no AI image generation)
  - TTS audio saying the letter name 7 times slowly

The cards and audio are assembled into a single vyanjan-letters.mp4.

Outputs:
  content/assets/images/vyanjan/<roman>-card.png
  content/assets/videos/hindi-h1/vyanjan-letters.mp4

Run:
  .venv/bin/python scripts/generate_vyanjan_cards.py --cards-only
  .venv/bin/python scripts/generate_vyanjan_cards.py
  .venv/bin/python scripts/generate_vyanjan_cards.py --voice shimmer
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
CARD_DIR = ROOT / "content" / "assets" / "images" / "vyanjan"
VIDEO_DIR = ROOT / "content" / "assets" / "videos" / "hindi-h1"
AUDIO_DIR = VIDEO_DIR / "audio_tmp" / "vyanjan"
VIDEO_OUT = VIDEO_DIR / "vyanjan-letters.mp4"

DEVANAGARI_FONT = Path("/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc")
LATIN_FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

VIDEO_W, VIDEO_H = 1280, 720
CARD_W, CARD_H = 400, 400
FPS = 24

# Theme palettes per varga so each row of the chart has a unified color
PALETTES = {
    "ka_varga":   {"bg_a": "#fff7d3", "bg_b": "#ffd966", "text": "#2d1f00"},
    "cha_varga":  {"bg_a": "#dff7ff", "bg_b": "#5cc8ff", "text": "#0a2a3d"},
    "Ta_varga":   {"bg_a": "#eafff0", "bg_b": "#6ed98a", "text": "#0d2e17"},
    "ta_varga":   {"bg_a": "#ffe6f0", "bg_b": "#ff7eb3", "text": "#3a0f22"},
    "pa_varga":   {"bg_a": "#f2e8ff", "bg_b": "#b57bee", "text": "#1e0545"},
    "antastha":   {"bg_a": "#fef9c3", "bg_b": "#f7c948", "text": "#2d1800"},
    "ushma":      {"bg_a": "#e0fff6", "bg_b": "#2ec4a0", "text": "#033d2d"},
}

# 33 standard vyanjan with Roman labels and varga grouping
VYANJAN = [
    # क-varga (kanthya)
    {"letter": "क", "roman": "ka",  "label": "ka",  "varga": "ka_varga"},
    {"letter": "ख", "roman": "kha", "label": "kha", "varga": "ka_varga"},
    {"letter": "ग", "roman": "ga",  "label": "ga",  "varga": "ka_varga"},
    {"letter": "घ", "roman": "gha", "label": "gha", "varga": "ka_varga"},
    {"letter": "ङ", "roman": "nga", "label": "nga", "varga": "ka_varga"},
    # च-varga (talavya)
    {"letter": "च", "roman": "cha",  "label": "cha",  "varga": "cha_varga"},
    {"letter": "छ", "roman": "chha", "label": "chha", "varga": "cha_varga"},
    {"letter": "ज", "roman": "ja",   "label": "ja",   "varga": "cha_varga"},
    {"letter": "झ", "roman": "jha",  "label": "jha",  "varga": "cha_varga"},
    {"letter": "ञ", "roman": "nya",  "label": "nya",  "varga": "cha_varga"},
    # ट-varga (murdhanya) — double letters to avoid macOS case-insensitive filename collisions
    {"letter": "ट", "roman": "tta",  "label": "Ta",  "varga": "Ta_varga"},
    {"letter": "ठ", "roman": "ttha", "label": "Tha", "varga": "Ta_varga"},
    {"letter": "ड", "roman": "dda",  "label": "Da",  "varga": "Ta_varga"},
    {"letter": "ढ", "roman": "ddha", "label": "Dha", "varga": "Ta_varga"},
    {"letter": "ण", "roman": "nna",  "label": "Na",  "varga": "Ta_varga"},
    # त-varga (dantya)
    {"letter": "त", "roman": "ta",  "label": "ta",  "varga": "ta_varga"},
    {"letter": "थ", "roman": "tha", "label": "tha", "varga": "ta_varga"},
    {"letter": "द", "roman": "da",  "label": "da",  "varga": "ta_varga"},
    {"letter": "ध", "roman": "dha", "label": "dha", "varga": "ta_varga"},
    {"letter": "न", "roman": "na",  "label": "na",  "varga": "ta_varga"},
    # प-varga (oshthya)
    {"letter": "प", "roman": "pa",  "label": "pa",  "varga": "pa_varga"},
    {"letter": "फ", "roman": "pha", "label": "pha", "varga": "pa_varga"},
    {"letter": "ब", "roman": "ba",  "label": "ba",  "varga": "pa_varga"},
    {"letter": "भ", "roman": "bha", "label": "bha", "varga": "pa_varga"},
    {"letter": "म", "roman": "ma",  "label": "ma",  "varga": "pa_varga"},
    # antastha (semi-vowels)
    {"letter": "य", "roman": "ya", "label": "ya", "varga": "antastha"},
    {"letter": "र", "roman": "ra", "label": "ra", "varga": "antastha"},
    {"letter": "ल", "roman": "la", "label": "la", "varga": "antastha"},
    {"letter": "व", "roman": "va", "label": "va", "varga": "antastha"},
    # ushma (sibilants + h)
    {"letter": "श", "roman": "sha", "label": "sha", "varga": "ushma"},
    {"letter": "ष", "roman": "ssha", "label": "Sha", "varga": "ushma"},
    {"letter": "स", "roman": "sa",  "label": "sa",  "varga": "ushma"},
    {"letter": "ह", "roman": "ha",  "label": "ha",  "varga": "ushma"},
]


def _resolve_colors(entry: dict) -> dict:
    return PALETTES[entry["varga"]]


def load_env() -> None:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def font_path(path: Path) -> str:
    if path.exists():
        return str(path)
    raise FileNotFoundError(f"Font not found: {path}")


def _gradient_bg(draw, w: int, h: int, bg_a: str, bg_b: str) -> None:
    start = tuple(int(bg_a.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    end = tuple(int(bg_b.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    for y in range(h):
        ratio = y / max(h - 1, 1)
        blended = tuple(int(start[i] * (1 - ratio) + end[i] * ratio) for i in range(3))
        draw.line((0, y, w, y), fill=blended)


def render_card_image(entry: dict, width: int, height: int):
    from PIL import Image, ImageDraw, ImageFont

    colors = _resolve_colors(entry)
    img = Image.new("RGB", (width, height), colors["bg_a"])
    draw = ImageDraw.Draw(img)
    _gradient_bg(draw, width, height, colors["bg_a"], colors["bg_b"])

    big_size = int(height * 0.50)
    label_size = int(height * 0.10)
    badge_size = int(height * 0.055)

    big_font = ImageFont.truetype(font_path(DEVANAGARI_FONT), big_size)
    label_font = ImageFont.truetype(font_path(LATIN_FONT), label_size)
    badge_font = ImageFont.truetype(font_path(LATIN_FONT), badge_size)

    cx = width // 2
    cy = height // 2

    draw.text((cx, cy - int(height * 0.05)), entry["letter"], font=big_font,
              fill=colors["text"], anchor="mm")
    draw.text((cx, cy + int(height * 0.42)), entry["label"], font=label_font,
              fill=colors["text"], anchor="mm")

    if width > 500:
        draw.text((40, 36), "Hindi Vyanjan  ·  व्यंजन", font=badge_font, fill=colors["text"])
        idx = next(i for i, v in enumerate(VYANJAN) if v["roman"] == entry["roman"])
        draw.text((width - 40, 36), f"{idx + 1} / {len(VYANJAN)}", font=badge_font,
                  fill=colors["text"], anchor="ra")

    return img


def generate_card_pngs() -> None:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    for entry in VYANJAN:
        out = CARD_DIR / f"{entry['roman']}-card.png"
        img = render_card_image(entry, CARD_W, CARD_H)
        img.save(out, format="PNG")
        print(f"  [PNG] {out.name}")


def generate_audio(client, voice: str) -> list[Path]:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for entry in VYANJAN:
        out = AUDIO_DIR / f"{entry['roman']}.mp3"
        if out.exists():
            print(f"  [SKIP] {out.name}")
        else:
            text = "  ".join([entry["letter"]] * 7)
            print(f"  [TTS] {entry['label']}  →  {text[:30]}")
            with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=0.68,
            ) as response:
                response.stream_to_file(str(out))
            time.sleep(0.6)
        files.append(out)
    return files


def generate_video(audio_files: list[Path]) -> None:
    import sys, tempfile
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    print("  Building atomic clips…")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        atoms: list[Path] = []
        for entry, af in zip(VYANJAN, audio_files):
            frame_png = tmp / f"{entry['roman']}.png"
            render_card_image(entry, VIDEO_W, VIDEO_H).save(str(frame_png))
            atom = tmp / f"{entry['roman']}.mp4"
            make_atomic_mp4(frame_png, af, atom, head_sil=0.3, tail_sil=0.6)
            atoms.append(atom)
        print(f"  Concatenating {len(atoms)} clips → {VIDEO_OUT}")
        concat_mp4s(atoms, VIDEO_OUT)
    print("  Done.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate vyanjan letter card PNGs and video.")
    parser.add_argument("--cards-only", action="store_true",
                        help="Generate PNG cards only; skip TTS and video")
    parser.add_argument("--voice", default="nova",
                        help="OpenAI TTS voice (nova, shimmer, alloy, echo, fable, onyx)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_env()

    print("Generating vyanjan letter card PNGs…")
    generate_card_pngs()

    if args.cards_only:
        print("Cards done. Run without --cards-only to generate TTS audio and video.")
        return

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Add it to .env or export before running.")

    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    print("Generating TTS audio (7× per letter)…")
    audio_files = generate_audio(client, args.voice)

    print("Assembling video…")
    generate_video(audio_files)


if __name__ == "__main__":
    main()
