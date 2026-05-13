#!/usr/bin/env python3
"""
generate_synced_learning_videos.py — frame-by-frame synced Hindi learning videos.

Outputs:
  content/assets/videos/hindi-h1/swar-word-sync.mp4
  content/assets/videos/hindi-h1/barakhadi-sync.mp4

Swar video: one wide teaching board per letter; audio says the exact visible
letter seven times, then the word, pronunciation, and English meaning.

Barakhadi video: one highlighted barakhadi cell per audio clip; audio says the
visible form slowly. Every displayed form is synced to its own TTS audio.
"""

import argparse
import os
import pathlib
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
VID_DIR = ROOT / "content/assets/videos/hindi-h1"
SWAR_CARD_DIR = ROOT / "content/assets/images/word-cards/swar"
FONT_DEV = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

SWAR = [
    {"form": "अ", "slug": "a", "word": "अनार", "pron": "anaar", "meaning": "pomegranate", "colors": ((192, 57, 43), (142, 68, 173))},
    {"form": "आ", "slug": "aa", "word": "आम", "pron": "aam", "meaning": "mango", "colors": ((243, 156, 18), (230, 126, 34))},
    {"form": "इ", "slug": "i", "word": "इमली", "pron": "imli", "meaning": "tamarind", "colors": ((39, 174, 96), (22, 160, 133))},
    {"form": "ई", "slug": "ee", "word": "ईंट", "pron": "eent", "meaning": "brick", "colors": ((231, 76, 60), (192, 57, 43))},
    {"form": "उ", "slug": "u", "word": "उल्लू", "pron": "ullu", "meaning": "owl", "colors": ((44, 62, 80), (142, 68, 173))},
    {"form": "ऊ", "slug": "oo", "word": "ऊँट", "pron": "oont", "meaning": "camel", "colors": ((243, 156, 18), (211, 84, 0))},
    {"form": "ए", "slug": "e", "word": "एक", "pron": "ek", "meaning": "one", "colors": ((26, 188, 156), (52, 152, 219))},
    {"form": "ऐ", "slug": "ai", "word": "ऐनक", "pron": "ainak", "meaning": "glasses", "colors": ((155, 89, 182), (52, 152, 219))},
    {"form": "ओ", "slug": "o", "word": "ओस", "pron": "os", "meaning": "dew drops", "colors": ((41, 128, 185), (39, 174, 96))},
    {"form": "औ", "slug": "au", "word": "औरत", "pron": "aurat", "meaning": "woman", "colors": ((233, 30, 99), (156, 39, 176))},
    {"form": "अं", "slug": "an", "word": "अंगूर", "pron": "angoor", "meaning": "grapes", "colors": ((106, 27, 154), (69, 39, 160))},
    {"form": "अः", "slug": "ah", "word": "अहा!", "pron": "aha", "meaning": "wow", "colors": ((255, 111, 0), (230, 81, 0))},
]

MATRAS = [
    {"matra": "", "label": "a"},
    {"matra": "\u093E", "label": "aa"},
    {"matra": "\u093F", "label": "i"},
    {"matra": "\u0940", "label": "ee"},
    {"matra": "\u0941", "label": "u"},
    {"matra": "\u0942", "label": "oo"},
    {"matra": "\u0947", "label": "e"},
    {"matra": "\u0948", "label": "ai"},
    {"matra": "\u094B", "label": "o"},
    {"matra": "\u094C", "label": "au"},
    {"matra": "\u0902", "label": "an"},
    {"matra": "\u0903", "label": "ah"},
]

VYANJAN = [
    {"letter": "क", "roman": "ka", "label": "ka", "varga": "ka"},
    {"letter": "ख", "roman": "kha", "label": "kha", "varga": "ka"},
    {"letter": "ग", "roman": "ga", "label": "ga", "varga": "ka"},
    {"letter": "घ", "roman": "gha", "label": "gha", "varga": "ka"},
    {"letter": "ङ", "roman": "nga", "label": "nga", "varga": "ka"},
    {"letter": "च", "roman": "cha", "label": "cha", "varga": "cha"},
    {"letter": "छ", "roman": "chha", "label": "chha", "varga": "cha"},
    {"letter": "ज", "roman": "ja", "label": "ja", "varga": "cha"},
    {"letter": "झ", "roman": "jha", "label": "jha", "varga": "cha"},
    {"letter": "ञ", "roman": "nya", "label": "nya", "varga": "cha"},
    {"letter": "ट", "roman": "tta", "label": "Ta", "varga": "Ta"},
    {"letter": "ठ", "roman": "ttha", "label": "Tha", "varga": "Ta"},
    {"letter": "ड", "roman": "dda", "label": "Da", "varga": "Ta"},
    {"letter": "ढ", "roman": "ddha", "label": "Dha", "varga": "Ta"},
    {"letter": "ण", "roman": "nna", "label": "Na", "varga": "Ta"},
    {"letter": "त", "roman": "ta", "label": "ta", "varga": "ta"},
    {"letter": "थ", "roman": "tha", "label": "tha", "varga": "ta"},
    {"letter": "द", "roman": "da", "label": "da", "varga": "ta"},
    {"letter": "ध", "roman": "dha", "label": "dha", "varga": "ta"},
    {"letter": "न", "roman": "na", "label": "na", "varga": "ta"},
    {"letter": "प", "roman": "pa", "label": "pa", "varga": "pa"},
    {"letter": "फ", "roman": "pha", "label": "pha", "varga": "pa"},
    {"letter": "ब", "roman": "ba", "label": "ba", "varga": "pa"},
    {"letter": "भ", "roman": "bha", "label": "bha", "varga": "pa"},
    {"letter": "म", "roman": "ma", "label": "ma", "varga": "pa"},
    {"letter": "य", "roman": "ya", "label": "ya", "varga": "semi"},
    {"letter": "र", "roman": "ra", "label": "ra", "varga": "semi"},
    {"letter": "ल", "roman": "la", "label": "la", "varga": "semi"},
    {"letter": "व", "roman": "va", "label": "va", "varga": "semi"},
    {"letter": "श", "roman": "sha", "label": "sha", "varga": "ush"},
    {"letter": "ष", "roman": "ssha", "label": "Sha", "varga": "ush"},
    {"letter": "स", "roman": "sa", "label": "sa", "varga": "ush"},
    {"letter": "ह", "roman": "ha", "label": "ha", "varga": "ush"},
]

PALETTES = {
    "ka": ((26, 42, 108), (178, 31, 31)),
    "cha": ((19, 78, 94), (113, 178, 128)),
    "Ta": ((75, 18, 72), (241, 7, 17)),
    "ta": ((0, 92, 151), (54, 55, 149)),
    "pa": ((26, 26, 46), (22, 33, 62)),
    "semi": ((55, 59, 68), (66, 134, 244)),
    "ush": ((15, 12, 41), (48, 43, 99)),
}

CARD_W, CARD_H = 1440, 810
COLS, ROWS = 6, 2
GRID_TOP = 128


def _load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def _blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _text_width(draw: ImageDraw.ImageDraw, text: str, font) -> float:
    return draw.textlength(text, font=font)


def _centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font, fill) -> None:
    left, top, right, bottom = box
    width = _text_width(draw, text, font)
    bbox = draw.textbbox((0, 0), text, font=font)
    height = bbox[3] - bbox[1]
    draw.text((left + (right - left - width) / 2, top + (bottom - top - height) / 2 - bbox[1]), text, font=font, fill=fill)


def _tts(text: str, _voice: str = "nova", speed: float = 0.72) -> bytes:
    """Google Cloud TTS — voice arg kept for API compat but voice is set in _google_tts.py."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _google_tts import tts_to_bytes
    return tts_to_bytes(text, speed=speed)


def render_swar_teaching_frame(item: dict, source_card: pathlib.Path) -> Image.Image:
    """Two-panel teaching card: object image (left) + letter/word/meaning (right).

    Left panel shows the realistic DALL-E image — cropped to include the full
    object without cutting heads/tops (word card image zone: y 166-776, x 145-755).
    Right panel shows: large letter form, Hindi word, English meaning.
    No 'Swar sound x7' or 'Say along with Mitra' labels — they add clutter.
    """
    col_a, col_b = item["colors"]
    img = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    dev_mega = _font(FONT_DEV, 200)
    dev_word = _font(FONT_DEV, 90)
    latin_big = _font(FONT_LAT, 62)
    latin_mid = _font(FONT_LAT, 46)

    # Left: object image — use the full DALL-E image bounds from the word card
    # Word card DALL-E image occupies (145, 166) to (755, 776) in the 900×1120 card
    card = Image.open(source_card).convert("RGB")
    object_crop = card.crop((145, 166, 755, 776)).resize((560, 560), Image.LANCZOS)
    draw.rounded_rectangle([50, 110, 658, 718], radius=28, fill=(255, 255, 255))
    img.paste(object_crop, (70, 130))

    # Right: letter + word + meaning panel
    panel = [710, 110, 1400, 718]
    draw.rounded_rectangle(panel, radius=30, fill=(255, 255, 255))
    _centered_text(draw, (panel[0], 125, panel[2], 330), item["form"], dev_mega, (24, 24, 24))
    _centered_text(draw, (panel[0], 340, panel[2], 455), item["word"],  dev_word, (42, 42, 42))
    _centered_text(draw, (panel[0], 480, panel[2], 570), item["pron"],  latin_big, (200, 90, 0))
    _centered_text(draw, (panel[0], 590, panel[2], 660), item["meaning"], latin_mid, (70, 70, 70))
    return img


def render_barakhadi_highlight(entry: dict, hi_idx: int) -> Image.Image:
    col_a, col_b = PALETTES[entry["varga"]]
    img = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    dev_big = _font(FONT_DEV, 104)
    dev_hi = _font(FONT_DEV, 128)
    hdr = _font(FONT_DEV, 56)
    label_f = _font(FONT_LAT, 36)
    badge_f = _font(FONT_LAT, 28)

    badge = "Hindi Barakhadi  ·  बाराखड़ी"
    bw = draw.textlength(badge, font=badge_f)
    bx = CARD_W - bw - 32
    draw.rounded_rectangle([bx - 14, 18, bx + bw + 14, 60], radius=10, fill=(255, 255, 255))
    draw.text((bx, 22), badge, font=badge_f, fill="#222222")

    current = entry["letter"] + MATRAS[hi_idx]["matra"]
    draw.text((32, 18), f"{entry['letter']} की बाराखड़ी  -  {current}", font=hdr, fill="white")

    cell_w = CARD_W // COLS
    cell_h = (CARD_H - GRID_TOP) // ROWS
    for idx, matra in enumerate(MATRAS):
        ci = idx % COLS
        ri = idx // COLS
        cx = ci * cell_w
        cy = GRID_TOP + ri * cell_h
        form = entry["letter"] + matra["matra"]
        highlighted = idx == hi_idx
        if highlighted:
            fill = (255, 248, 205)
            text = (20, 20, 20)
            label = (80, 80, 80)
            font = dev_hi
            outline = (255, 198, 0)
            width = 5
        else:
            fill = tuple(max(0, int(v * 0.48)) for v in _blend(col_a, col_b, (cx + cell_w / 2) / CARD_W))
            text = (190, 190, 190)
            label = (145, 145, 145)
            font = dev_big
            outline = None
            width = 1
        box = [cx + 9, cy + 9, cx + cell_w - 9, cy + cell_h - 9]
        draw.rounded_rectangle(box, radius=16, fill=fill, outline=outline, width=width)
        fw = draw.textlength(form, font=font)
        draw.text((cx + (cell_w - fw) / 2, cy + 24), form, font=font, fill=text)
        lw = draw.textlength(matra["label"], font=label_f)
        draw.text((cx + (cell_w - lw) / 2, cy + cell_h - 58), matra["label"], font=label_f, fill=label)
    return img


def generate_swar_video(voice: str, reps: int = 1) -> None:
    """Swar word-sync video.

    For each swar the sequence is (repeated `reps` times):
      [letter sound] +700ms → [Hindi word] +700ms → [English meaning] +700ms
    Between rounds: +2 s gap after the meaning clip.
    Audio files are generated once and reused across reps (same TTS cost).
    """
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s
    out = VID_DIR / "swar-word-sync.mp4"
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        atoms: list[pathlib.Path] = []
        for item in SWAR:
            png = SWAR_CARD_DIR / f"{item['slug']}.png"
            if not png.exists():
                raise FileNotFoundError(png)
            frame = tmp / f"swar-{item['slug']}.png"
            render_swar_teaching_frame(item, png).save(str(frame))

            # Generate 3 TTS files once — letter, Hindi word, English meaning
            print(f"  [SWAR] {item['form']} → {item['word']} → {item['meaning']}")
            letter_mp3 = tmp / f"{item['slug']}-letter.mp3"
            word_mp3   = tmp / f"{item['slug']}-word.mp3"
            mean_mp3   = tmp / f"{item['slug']}-mean.mp3"
            letter_mp3.write_bytes(_tts(item["form"],    voice, speed=0.72))
            word_mp3.write_bytes(  _tts(item["word"],    voice, speed=0.68))
            mean_mp3.write_bytes(  _tts(item["meaning"], voice, speed=0.78))

            # Build clips: reuse the same MP3 files each rep
            for rep in range(reps):
                is_last = (rep == reps - 1)
                inter_gap = 0.7 + 2.0   # 2 s breathing room between rounds
                final_gap = 0.7         # no extra gap after last round

                # Clip 1: letter
                a = tmp / f"{item['slug']}-r{rep}-l.mp4"
                make_atomic_mp4(frame, letter_mp3, a, head_sil=0.3, tail_sil=0.7)
                atoms.append(a)
                # Clip 2: Hindi word
                a = tmp / f"{item['slug']}-r{rep}-w.mp4"
                make_atomic_mp4(frame, word_mp3, a, head_sil=0.3, tail_sil=0.7)
                atoms.append(a)
                # Clip 3: English meaning (longer tail between rounds)
                tail = final_gap if is_last else inter_gap
                a = tmp / f"{item['slug']}-r{rep}-m.mp4"
                make_atomic_mp4(frame, mean_mp3, a, head_sil=0.3, tail_sil=tail)
                atoms.append(a)

        print(f"  Concatenating {len(atoms)} clips → {out}")
        concat_mp4s(atoms, out)


def generate_barakhadi_video(voice: str) -> None:
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s
    out = VID_DIR / "barakhadi-sync.mp4"
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        atoms: list[pathlib.Path] = []
        for entry in VYANJAN:
            print(f"  [ROW] {entry['letter']} की बाराखड़ी")
            for idx, matra in enumerate(MATRAS):
                form = entry["letter"] + matra["matra"]
                frame = tmp / f"{entry['roman']}-{idx:02d}.png"
                render_barakhadi_highlight(entry, idx).save(str(frame))
                mp3 = tmp / f"{entry['roman']}-{idx:02d}.mp3"
                mp3.write_bytes(_tts(form, voice, speed=0.65))
                atom = tmp / f"{entry['roman']}-{idx:02d}.mp4"
                make_atomic_mp4(frame, mp3, atom, head_sil=0.3, tail_sil=0.7)
                atoms.append(atom)
        print(f"  Concatenating {len(atoms)} clips → {out}")
        concat_mp4s(atoms, out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["swar", "barakhadi", "all"], default="all")
    parser.add_argument("--voice", default="nova")
    parser.add_argument("--reps", type=int, default=1,
                        help="Repetitions per swar (1 to verify, 3 for final)")
    args = parser.parse_args()
    if args.kind in ("swar", "all"):
        generate_swar_video(args.voice, reps=args.reps)
    if args.kind in ("barakhadi", "all"):
        generate_barakhadi_video(args.voice)


if __name__ == "__main__":
    main()
