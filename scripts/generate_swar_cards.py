"""
Generate Hindi swar (vowel) letter card images and a narrated video.

For each of the 12 swar:
  - A PIL-rendered PNG card (exact Devanagari, no AI image generation)
  - TTS audio saying the letter name 7 times slowly

The cards and audio are assembled into a single swar-letters.mp4.

Outputs:
  content/assets/images/swar/<roman>-card.png   (400x400 for page display)
  content/assets/videos/hindi-h1/swar-letters.mp4

Run:
  .venv/bin/python scripts/generate_swar_cards.py --cards-only   (PNGs only, no TTS)
  .venv/bin/python scripts/generate_swar_cards.py                 (PNGs + video)
  .venv/bin/python scripts/generate_swar_cards.py --voice shimmer
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
CARD_DIR = ROOT / "content" / "assets" / "images" / "swar"
VIDEO_DIR = ROOT / "content" / "assets" / "videos" / "hindi-h1"
AUDIO_DIR = VIDEO_DIR / "audio_tmp" / "swar"
VIDEO_OUT = VIDEO_DIR / "swar-letters.mp4"

DEVANAGARI_FONT = Path("/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc")
LATIN_FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

VIDEO_W, VIDEO_H = 1280, 720
CARD_W, CARD_H = 400, 400
FPS = 24

# 12 swar with colors chosen for child-friendly, distinct appearance
SWAR = [
    {"letter": "अ",  "roman": "a",  "label": "a",  "bg_a": "#fff7d3", "bg_b": "#ffd966", "text": "#2d1f00"},
    {"letter": "आ",  "roman": "aa", "label": "aa", "bg_a": "#dff7ff", "bg_b": "#5cc8ff", "text": "#0a2a3d"},
    {"letter": "इ",  "roman": "i",  "label": "i",  "bg_a": "#eafff0", "bg_b": "#6ed98a", "text": "#0d2e17"},
    {"letter": "ई",  "roman": "ee", "label": "ee", "bg_a": "#ffe6f0", "bg_b": "#ff7eb3", "text": "#3a0f22"},
    {"letter": "उ",  "roman": "u",  "label": "u",  "bg_a": "#f2e8ff", "bg_b": "#b57bee", "text": "#1e0545"},
    {"letter": "ऊ",  "roman": "oo", "label": "oo", "bg_a": "#e0fff6", "bg_b": "#2ec4a0", "text": "#033d2d"},
    {"letter": "ए",  "roman": "e",  "label": "e",  "bg_a": "#fff3e0", "bg_b": "#ff8c42", "text": "#3d1500"},
    {"letter": "ऐ",  "roman": "ai", "label": "ai", "bg_a": "#e0f2fe", "bg_b": "#29b6f6", "text": "#082840"},
    {"letter": "ओ",  "roman": "o",  "label": "o",  "bg_a": "#fef9c3", "bg_b": "#f7c948", "text": "#2d1800"},
    {"letter": "औ",  "roman": "au", "label": "au", "bg_a": "#f0fdf4", "bg_b": "#34d399", "text": "#052e16"},
    {"letter": "अं", "roman": "an", "label": "an", "bg_a": "#fef0cc", "bg_b": "#f5a623", "text": "#2a1400"},
    {"letter": "अः", "roman": "ah", "label": "ah", "bg_a": "#eef2ff", "bg_b": "#818cf8", "text": "#1e1b4b"},
]


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
    """Render a PIL image for one swar at the given pixel size."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (width, height), entry["bg_a"])
    draw = ImageDraw.Draw(img)
    _gradient_bg(draw, width, height, entry["bg_a"], entry["bg_b"])

    # Scale fonts relative to card height
    big_size = int(height * 0.50)
    label_size = int(height * 0.10)
    badge_size = int(height * 0.055)

    big_font = ImageFont.truetype(font_path(DEVANAGARI_FONT), big_size)
    label_font = ImageFont.truetype(font_path(LATIN_FONT), label_size)
    badge_font = ImageFont.truetype(font_path(LATIN_FONT), badge_size)

    cx = width // 2
    cy = height // 2

    # Large letter centred slightly above middle
    draw.text((cx, cy - int(height * 0.05)), entry["letter"], font=big_font,
              fill=entry["text"], anchor="mm")

    # Roman transliteration below
    draw.text((cx, cy + int(height * 0.42)), entry["label"], font=label_font,
              fill=entry["text"], anchor="mm")

    # Top-left label for video cards
    if width > 500:
        draw.text((40, 36), "Hindi Swar  ·  स्वर", font=badge_font, fill=entry["text"])
        # badge top-right: n / 12
        idx = next(i for i, s in enumerate(SWAR) if s["roman"] == entry["roman"])
        draw.text((width - 40, 36), f"{idx + 1} / {len(SWAR)}", font=badge_font,
                  fill=entry["text"], anchor="ra")

    return img


def generate_card_pngs() -> None:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    for entry in SWAR:
        out = CARD_DIR / f"{entry['roman']}-card.png"
        img = render_card_image(entry, CARD_W, CARD_H)
        img.save(out, format="PNG")
        print(f"  [PNG] {out.name}")


def generate_audio(client, voice: str) -> list[Path]:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for entry in SWAR:
        out = AUDIO_DIR / f"{entry['roman']}.mp3"
        if out.exists():
            print(f"  [SKIP] {out.name}")
        else:
            # Say the letter 7 times with a natural pause between each
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
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s
    import tempfile

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    print("  Building atomic clips…")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        atoms: list[Path] = []
        for entry, af in zip(SWAR, audio_files):
            frame_png = tmp / f"{entry['roman']}.png"
            render_card_image(entry, VIDEO_W, VIDEO_H).save(str(frame_png))
            atom = tmp / f"{entry['roman']}.mp4"
            make_atomic_mp4(frame_png, af, atom, head_sil=0.3, tail_sil=0.6)
            atoms.append(atom)
        print(f"  Concatenating {len(atoms)} clips → {VIDEO_OUT}")
        concat_mp4s(atoms, VIDEO_OUT)
    print("  Done.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate swar letter card PNGs and video.")
    parser.add_argument("--cards-only", action="store_true",
                        help="Generate PNG cards only; skip TTS and video")
    parser.add_argument("--voice", default="nova",
                        help="OpenAI TTS voice (nova, shimmer, alloy, echo, fable, onyx)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_env()

    print("Generating swar letter card PNGs…")
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
