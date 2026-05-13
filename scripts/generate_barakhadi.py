#!/usr/bin/env python3
"""
generate_barakhadi.py  —  Hindi Barakhadi row cards + narrated MP4

For each of the 33 vyanjan, renders a landscape PNG showing all 12 matra
forms (the barakhadi row for that consonant) and assembles them into a
single narrated video with OpenAI TTS.

Usage:
  python scripts/generate_barakhadi.py --cards-only
  python scripts/generate_barakhadi.py --voice nova
"""

import argparse, pathlib, tempfile
from PIL import Image, ImageDraw, ImageFont

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT      = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR   = ROOT / "content/assets/images/barakhadi"
VID_DIR   = ROOT / "content/assets/videos/hindi-h1"
OUT_VIDEO = VID_DIR / "barakhadi.mp4"
FONT_DEV  = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT  = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# ── Matra sequence (12 standard forms) ────────────────────────────────────────
MATRAS = [
    {"matra": "",       "label": "a"},
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

# ── Consonants ─────────────────────────────────────────────────────────────────
VYANJAN = [
    # ka-varga
    {"letter": "क", "roman": "ka",   "label": "ka",   "varga": "ka"},
    {"letter": "ख", "roman": "kha",  "label": "kha",  "varga": "ka"},
    {"letter": "ग", "roman": "ga",   "label": "ga",   "varga": "ka"},
    {"letter": "घ", "roman": "gha",  "label": "gha",  "varga": "ka"},
    {"letter": "ङ", "roman": "nga",  "label": "nga",  "varga": "ka"},
    # cha-varga
    {"letter": "च", "roman": "cha",  "label": "cha",  "varga": "cha"},
    {"letter": "छ", "roman": "chha", "label": "chha", "varga": "cha"},
    {"letter": "ज", "roman": "ja",   "label": "ja",   "varga": "cha"},
    {"letter": "झ", "roman": "jha",  "label": "jha",  "varga": "cha"},
    {"letter": "ञ", "roman": "nya",  "label": "nya",  "varga": "cha"},
    # Ta-varga (retroflex — double prefix to avoid macOS case collision)
    {"letter": "ट", "roman": "tta",  "label": "Ta",   "varga": "Ta"},
    {"letter": "ठ", "roman": "ttha", "label": "Tha",  "varga": "Ta"},
    {"letter": "ड", "roman": "dda",  "label": "Da",   "varga": "Ta"},
    {"letter": "ढ", "roman": "ddha", "label": "Dha",  "varga": "Ta"},
    {"letter": "ण", "roman": "nna",  "label": "Na",   "varga": "Ta"},
    # ta-varga (dental)
    {"letter": "त", "roman": "ta",   "label": "ta",   "varga": "ta"},
    {"letter": "थ", "roman": "tha",  "label": "tha",  "varga": "ta"},
    {"letter": "द", "roman": "da",   "label": "da",   "varga": "ta"},
    {"letter": "ध", "roman": "dha",  "label": "dha",  "varga": "ta"},
    {"letter": "न", "roman": "na",   "label": "na",   "varga": "ta"},
    # pa-varga
    {"letter": "प", "roman": "pa",   "label": "pa",   "varga": "pa"},
    {"letter": "फ", "roman": "pha",  "label": "pha",  "varga": "pa"},
    {"letter": "ब", "roman": "ba",   "label": "ba",   "varga": "pa"},
    {"letter": "भ", "roman": "bha",  "label": "bha",  "varga": "pa"},
    {"letter": "म", "roman": "ma",   "label": "ma",   "varga": "pa"},
    # antastha
    {"letter": "य", "roman": "ya",   "label": "ya",   "varga": "semi"},
    {"letter": "र", "roman": "ra",   "label": "ra",   "varga": "semi"},
    {"letter": "ल", "roman": "la",   "label": "la",   "varga": "semi"},
    {"letter": "व", "roman": "va",   "label": "va",   "varga": "semi"},
    # ushma
    {"letter": "श", "roman": "sha",  "label": "sha",  "varga": "ush"},
    {"letter": "ष", "roman": "ssha", "label": "Sha",  "varga": "ush"},
    {"letter": "स", "roman": "sa",   "label": "sa",   "varga": "ush"},
    {"letter": "ह", "roman": "ha",   "label": "ha",   "varga": "ush"},
]

# Gradient palettes per varga (match vyanjan card colours)
PALETTES = {
    "ka":   ("#1a2a6c", "#b21f1f"),
    "cha":  ("#134e5e", "#71b280"),
    "Ta":   ("#4b1248", "#f10711"),
    "ta":   ("#005c97", "#363795"),
    "pa":   ("#1a1a2e", "#16213e"),
    "semi": ("#373b44", "#4286f4"),
    "ush":  ("#0f0c29", "#302b63"),
}

CARD_W, CARD_H = 1920, 420
COLS, ROWS_G   = 12, 1      # single row of 12
GRID_TOP       = 96


# ── Helpers ────────────────────────────────────────────────────────────────────
def _hex(h: str) -> tuple:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def _blend(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _lighten(c: tuple, amt: int = 40) -> tuple:
    return tuple(min(255, v + amt) for v in c)


def _load_fonts():
    try:
        f_big   = ImageFont.truetype(FONT_DEV, 92)
        f_label = ImageFont.truetype(FONT_LAT, 34)
        f_hdr   = ImageFont.truetype(FONT_DEV, 50)
        f_badge = ImageFont.truetype(FONT_LAT, 26)
    except Exception:
        f_big = f_label = f_hdr = f_badge = ImageFont.load_default()
    return f_big, f_label, f_hdr, f_badge


# ── Card renderer ──────────────────────────────────────────────────────────────
def render_card(entry: dict) -> Image.Image:
    col_a = _hex(PALETTES[entry["varga"]][0])
    col_b = _hex(PALETTES[entry["varga"]][1])

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    # Horizontal gradient background
    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    f_big, f_label, f_hdr, f_badge = _load_fonts()

    # Badge — top right
    badge = "Hindi Barakhadi  ·  बाराखड़ी"
    bw    = draw.textlength(badge, font=f_badge)
    bx    = CARD_W - bw - 24
    draw.rounded_rectangle([bx - 14, 16, bx + bw + 14, 58], radius=10, fill=(255, 255, 255))
    draw.text((bx, 20), badge, font=f_badge, fill="#222222")

    # Header — top left: consonant + label
    draw.text((28, 16), f"{entry['letter']}  -  {entry['label']}", font=f_hdr, fill="white")

    # 12×1 cell grid
    grid_top = GRID_TOP
    cell_w   = CARD_W // COLS
    cell_h   = (CARD_H - grid_top) // ROWS_G

    for idx, m in enumerate(MATRAS):
        ci = idx % COLS
        ri = idx // COLS
        cx = ci * cell_w
        cy = grid_top + ri * cell_h

        # Cell background: slightly lighter gradient colour
        mid_t  = (cx + cell_w / 2) / CARD_W
        bg     = _lighten(_blend(col_a, col_b, mid_t), 38)
        draw.rounded_rectangle([cx + 8, cy + 8, cx + cell_w - 8, cy + cell_h - 8],
                                radius=10, fill=bg)

        # Devanagari form
        form = entry["letter"] + m["matra"]
        fw   = draw.textlength(form, font=f_big)
        fx   = cx + (cell_w - fw) / 2
        fy   = cy + 24
        draw.text((fx, fy), form, font=f_big, fill="white")

        # Roman label
        lw = draw.textlength(m["label"], font=f_label)
        lx = cx + (cell_w - lw) / 2
        ly = cy + cell_h - 48
        draw.text((lx, ly), m["label"], font=f_label, fill="white")

    return img


# ── Highlight renderer (per-cell sync) ────────────────────────────────────────
def render_highlight_frame(entry: dict, hi_idx: int) -> Image.Image:
    """Render the barakhadi card for `entry` with cell hi_idx highlighted."""
    col_a   = _hex(PALETTES[entry["varga"]][0])
    col_b   = _hex(PALETTES[entry["varga"]][1])
    cell_w  = CARD_W // COLS
    cell_h  = (CARD_H - GRID_TOP) // ROWS_G

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    f_big, f_label, f_hdr, f_badge = _load_fonts()
    try:
        f_hi = ImageFont.truetype(FONT_DEV, 80)
    except Exception:
        f_hi = f_big

    badge = "Hindi Barakhadi  ·  बाराखड़ी"
    bw    = draw.textlength(badge, font=f_badge)
    bx    = CARD_W - bw - 24
    draw.rounded_rectangle([bx - 12, 12, bx + bw + 12, 48], radius=8, fill=(255, 255, 255))
    draw.text((bx, 16), badge, font=f_badge, fill="#222222")
    draw.text((28, 12), f"{entry['letter']}  -  {entry['label']}", font=f_hdr, fill="white")

    for idx, m in enumerate(MATRAS):
        ci      = idx % COLS
        ri      = idx // COLS
        cx      = ci * cell_w
        cy      = GRID_TOP + ri * cell_h
        form    = entry["letter"] + m["matra"]
        mid_t   = (cx + cell_w / 2) / CARD_W
        base_bg = _blend(col_a, col_b, mid_t)

        if idx == hi_idx:
            draw.rounded_rectangle(
                [cx + 4, cy + 4, cx + cell_w - 4, cy + cell_h - 4],
                radius=12, fill=(255, 248, 200),
            )
            draw.rounded_rectangle(
                [cx + 4, cy + 4, cx + cell_w - 4, cy + cell_h - 4],
                radius=12, outline=(255, 200, 0), width=3,
            )
            fw = draw.textlength(form, font=f_hi)
            fx = cx + (cell_w - fw) / 2
            draw.text((fx, cy + 8), form, font=f_hi, fill="#1a1a1a")
            lw = draw.textlength(m["label"], font=f_label)
            lx = cx + (cell_w - lw) / 2
            draw.text((lx, cy + cell_h - 32), m["label"], font=f_label, fill="#555555")
        else:
            dim_bg = tuple(int(v * 0.35) for v in base_bg)
            draw.rounded_rectangle(
                [cx + 5, cy + 5, cx + cell_w - 5, cy + cell_h - 5],
                radius=10, fill=dim_bg,
            )
            fw = draw.textlength(form, font=f_big)
            fx = cx + (cell_w - fw) / 2
            draw.text((fx, cy + 16), form, font=f_big, fill=(160, 160, 160))
            lw = draw.textlength(m["label"], font=f_label)
            lx = cx + (cell_w - lw) / 2
            draw.text((lx, cy + cell_h - 32), m["label"], font=f_label, fill=(140, 140, 140))

    return img


def _tts_form_single(form: str, voice: str, reps: int = 2) -> bytes:
    import openai
    client    = openai.OpenAI()
    narration = ". ".join([form] * reps) + "."
    return client.audio.speech.create(
        model="tts-1", voice=voice, speed=0.65, input=narration
    ).content


def generate_highlight_video(voice: str) -> None:
    """Per-cell highlighted barakhadi video — every form is synced with its cell."""
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _av_sync import padded_audio
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
    import openai
    client = openai.OpenAI()

    clips = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)

        for v_idx, v in enumerate(VYANJAN):
            print(f"[{v_idx + 1:02d}/33]  {v['letter']}  ({v['roman']})")

            # Consonant intro clip
            intro_text  = f"{v['letter']} की बाराखड़ी।"
            intro_bytes = client.audio.speech.create(
                model="tts-1", voice=voice, speed=0.72, input=intro_text
            ).content
            intro_img = render_highlight_frame(v, 0)
            ip = tmp / f"v{v_idx:02d}_intro.png"
            intro_img.save(str(ip))
            ap = tmp / f"v{v_idx:02d}_intro.mp3"
            ap.write_bytes(intro_bytes)
            aud = AudioFileClip(str(ap))
            padded = padded_audio(aud, head=0.3, tail=0.4)
            clips.append(ImageClip(str(ip)).with_duration(padded.duration).with_audio(padded))

            # One clip per matra form (2 reps each)
            for m_idx, m in enumerate(MATRAS):
                form        = v["letter"] + m["matra"]
                frame       = render_highlight_frame(v, m_idx)
                fp          = tmp / f"v{v_idx:02d}_m{m_idx:02d}.png"
                frame.save(str(fp))
                audio_bytes = _tts_form_single(form, voice, reps=2)
                ap          = tmp / f"v{v_idx:02d}_m{m_idx:02d}.mp3"
                ap.write_bytes(audio_bytes)
                aud  = AudioFileClip(str(ap))
                padded = padded_audio(aud, head=0.3, tail=0.5)
                clip = ImageClip(str(fp)).with_duration(padded.duration).with_audio(padded)
                clips.append(clip)

    print("Assembling highlight video…")
    final = concatenate_videoclips(clips, method="compose")
    print(f"  Writing {OUT_VIDEO}")
    final.write_videofile(
        str(OUT_VIDEO), fps=24, codec="libx264",
        audio_codec="aac", logger=None,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )
    print("  Done.")


# ── Public API ─────────────────────────────────────────────────────────────────
def generate_cards() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for v in VYANJAN:
        out = IMG_DIR / f"{v['roman']}-bara.png"
        render_card(v).save(str(out))
        print(f"  [PNG] {out.name}")
    print(f"Cards done. Run without --cards-only to generate TTS audio and video.")


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def _tts(entry: dict, _voice: str = "nova") -> bytes:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _google_tts import tts_to_bytes
    forms     = [entry["letter"] + m["matra"] for m in MATRAS]
    doubled   = ". ".join(f"{f}. {f}" for f in forms)
    narration = f"{entry['letter']} की बाराखड़ी। {doubled}."
    print(f"  [gTTS] {entry['roman']}  →  {narration[:55]}…")
    return tts_to_bytes(narration, speed=0.65)


def generate_video(voice: str) -> None:
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        atoms: list[pathlib.Path] = []
        for v in VYANJAN:
            png = IMG_DIR / f"{v['roman']}-bara.png"
            if not png.exists():
                render_card(v).save(str(png))
            ap = tmp / f"{v['roman']}.mp3"
            ap.write_bytes(_tts(v, voice))
            atom = tmp / f"{v['roman']}.mp4"
            make_atomic_mp4(png, ap, atom, head_sil=0.3, tail_sil=0.7)
            atoms.append(atom)
        print(f"  Concatenating {len(atoms)} clips → {OUT_VIDEO}")
        concat_mp4s(atoms, OUT_VIDEO)
    print("  Done.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate Hindi barakhadi cards and video")
    ap.add_argument("--cards-only", action="store_true", help="Only generate PNG cards, skip video")
    ap.add_argument("--highlight",  action="store_true", help="Per-cell sync highlight video (replaces barakhadi.mp4)")
    ap.add_argument("--voice", default="nova", help="OpenAI TTS voice (default: nova)")
    args = ap.parse_args()

    if args.cards_only:
        generate_cards()
    elif args.highlight:
        generate_cards()
        generate_highlight_video(args.voice)
    else:
        generate_cards()
        generate_video(args.voice)


if __name__ == "__main__":
    main()
