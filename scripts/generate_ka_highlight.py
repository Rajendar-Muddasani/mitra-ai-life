#!/usr/bin/env python3
"""
generate_ka_highlight.py  —  Per-cell highlight barakhadi videos.

For a chosen consonant (default क), each of the 12 matra forms is:
  1. Shown on screen with that cell highlighted (bright, others dimmed)
  2. Said 4 times slowly by the TTS voice

A 0.3s visual-first gap is added at the start of every clip so the highlighted
cell is on screen before the narrator speaks. A 0.5s tail silence is added so
the child has time to say it back.

Usage:
  python scripts/generate_ka_highlight.py --voice nova                    # ka only
  python scripts/generate_ka_highlight.py --letters ka,kha,ga,gha,nga     # several
  python scripts/generate_ka_highlight.py --letters all-ka-varga          # convenience
"""

import argparse, pathlib, tempfile, sys
from PIL import Image, ImageDraw, ImageFont

ROOT      = pathlib.Path(__file__).resolve().parent.parent
VID_DIR   = ROOT / "content/assets/videos/hindi-h1"
FONT_DEV  = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT  = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

MATRAS = [
    {"matra": "",       "label": "a"},
    {"matra": "ा", "label": "aa"},
    {"matra": "ि", "label": "i"},
    {"matra": "ी", "label": "ee"},
    {"matra": "ु", "label": "u"},
    {"matra": "ू", "label": "oo"},
    {"matra": "े", "label": "e"},
    {"matra": "ै", "label": "ai"},
    {"matra": "ो", "label": "o"},
    {"matra": "ौ", "label": "au"},
    {"matra": "ं", "label": "an"},
    {"matra": "ः", "label": "ah"},
]

# Letter catalog: roman → (devanagari, gradient_a, gradient_b)
LETTERS = {
    # ka-varga (deep blue → red)
    "ka":  ("क",  (26, 42, 108),  (178, 31, 31)),
    "kha": ("ख",  (26, 42, 108),  (178, 31, 31)),
    "ga":  ("ग",  (26, 42, 108),  (178, 31, 31)),
    "gha": ("घ",  (26, 42, 108),  (178, 31, 31)),
    "nga": ("ङ",  (26, 42, 108),  (178, 31, 31)),
    # cha-varga (teal → sage)
    "cha":  ("च",  (19, 78, 94),   (113, 178, 128)),
    "chha": ("छ",  (19, 78, 94),   (113, 178, 128)),
    "ja":   ("ज",  (19, 78, 94),   (113, 178, 128)),
    "jha":  ("झ",  (19, 78, 94),   (113, 178, 128)),
    "nya":  ("ञ",  (19, 78, 94),   (113, 178, 128)),
    # Ta-varga (deep purple → vivid red)
    "tta":  ("ट",  (75, 18, 72),   (241, 7, 17)),
    "ttha": ("ठ",  (75, 18, 72),   (241, 7, 17)),
    "dda":  ("ड",  (75, 18, 72),   (241, 7, 17)),
    "ddha": ("ढ",  (75, 18, 72),   (241, 7, 17)),
    "nna":  ("ण",  (75, 18, 72),   (241, 7, 17)),
    # ta-varga (blue → indigo)
    "ta":   ("त",  (0, 92, 151),   (54, 55, 149)),
    "tha":  ("थ",  (0, 92, 151),   (54, 55, 149)),
    "da":   ("द",  (0, 92, 151),   (54, 55, 149)),
    "dha":  ("ध",  (0, 92, 151),   (54, 55, 149)),
    "na":   ("न",  (0, 92, 151),   (54, 55, 149)),
    # pa-varga (dark navy)
    "pa":   ("प",  (26, 26, 46),   (22, 33, 62)),
    "pha":  ("फ",  (26, 26, 46),   (22, 33, 62)),
    "ba":   ("ब",  (26, 26, 46),   (22, 33, 62)),
    "bha":  ("भ",  (26, 26, 46),   (22, 33, 62)),
    "ma":   ("म",  (26, 26, 46),   (22, 33, 62)),
    # antastha
    "ya":   ("य",  (55, 59, 68),   (66, 134, 244)),
    "ra":   ("र",  (55, 59, 68),   (66, 134, 244)),
    "la":   ("ल",  (55, 59, 68),   (66, 134, 244)),
    "va":   ("व",  (55, 59, 68),   (66, 134, 244)),
    # ushma
    "sha":  ("श",  (15, 12, 41),   (48, 43, 99)),
    "ssha": ("ष",  (15, 12, 41),   (48, 43, 99)),
    "sa":   ("स",  (15, 12, 41),   (48, 43, 99)),
    "ha":   ("ह",  (15, 12, 41),   (48, 43, 99)),
}

GROUP_PRESETS = {
    "all-ka-varga": ["ka", "kha", "ga", "gha", "nga"],
    "all-cha-varga": ["cha", "chha", "ja", "jha", "nya"],
    "all-ta-varga": ["tta", "ttha", "dda", "ddha", "nna"],
    "all-dental-varga": ["ta", "tha", "da", "dha", "na"],
    "all-pa-varga": ["pa", "pha", "ba", "bha", "ma"],
    "all-antastha": ["ya", "ra", "la", "va"],
    "all-ushma": ["sha", "ssha", "sa", "ha"],
}

CARD_W   = 1080
CARD_H   = 480
COLS     = 6
ROWS_G   = 2
GRID_TOP = 72


# ── Helpers ──────────────────────────────────────────────────────────────────
def _blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _dim(c, factor=0.45):
    return tuple(int(v * factor) for v in c)


def _load_fonts():
    try:
        f_big   = ImageFont.truetype(FONT_DEV, 56)
        f_label = ImageFont.truetype(FONT_LAT, 22)
        f_hdr   = ImageFont.truetype(FONT_DEV, 32)
        f_badge = ImageFont.truetype(FONT_LAT, 17)
        f_hi    = ImageFont.truetype(FONT_DEV, 68)
    except Exception:
        f_big = f_label = f_hdr = f_badge = f_hi = ImageFont.load_default()
    return f_big, f_label, f_hdr, f_badge, f_hi


def render_highlight_frame(letter: str, col_a, col_b, label: str, hi_idx: int) -> Image.Image:
    """Render a barakhadi card for `letter` with cell hi_idx highlighted."""
    cell_w = CARD_W // COLS
    cell_h = (CARD_H - GRID_TOP) // ROWS_G

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    f_big, f_label, f_hdr, f_badge, f_hi = _load_fonts()

    badge = "Hindi Barakhadi  ·  बाराखड़ी"
    bw    = draw.textlength(badge, font=f_badge)
    bx    = CARD_W - bw - 24
    draw.rounded_rectangle([bx - 8, 10, bx + bw + 8, 34], radius=6, fill=(255, 255, 255))
    draw.text((bx, 12), badge, font=f_badge, fill="#222222")

    draw.text((20, 10), f"{letter}  ·  {label}", font=f_hdr, fill="white")

    for idx, mt in enumerate(MATRAS):
        ci = idx % COLS
        ri = idx // COLS
        cx = ci * cell_w
        cy = GRID_TOP + ri * cell_h

        form    = letter + mt["matra"]
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
            fy = cy + 8
            draw.text((fx, fy), form, font=f_hi, fill="#1a1a1a")
            lw = draw.textlength(mt["label"], font=f_label)
            lx = cx + (cell_w - lw) / 2
            ly = cy + cell_h - 32
            draw.text((lx, ly), mt["label"], font=f_label, fill="#555555")
        else:
            dim_bg = _dim(base_bg, 0.45)
            draw.rounded_rectangle(
                [cx + 5, cy + 5, cx + cell_w - 5, cy + cell_h - 5],
                radius=10, fill=dim_bg,
            )
            fw = draw.textlength(form, font=f_big)
            fx = cx + (cell_w - fw) / 2
            fy = cy + 10
            draw.text((fx, fy), form, font=f_big, fill=(180, 180, 180))
            lw = draw.textlength(mt["label"], font=f_label)
            lx = cx + (cell_w - lw) / 2
            ly = cy + cell_h - 32
            draw.text((lx, ly), mt["label"], font=f_label, fill=(120, 120, 120))

    return img


def _load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def _tts_form(form: str, voice: str, reps: int = 4) -> bytes:
    import openai
    client = openai.OpenAI()
    narration = ". ".join([form] * reps) + "."
    print(f"  [TTS] {form}  ×{reps}")
    return client.audio.speech.create(
        model="tts-1", voice=voice, speed=0.72, input=narration
    ).content


def generate_video_for_letter(roman: str, voice: str) -> None:
    if roman not in LETTERS:
        raise SystemExit(f"Unknown letter: {roman}. Known: {sorted(LETTERS)}")
    letter, col_a, col_b = LETTERS[roman]
    label = roman

    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _av_sync import padded_audio
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

    out_video = VID_DIR / f"{roman}-barakhadi-detailed.mp4"
    print(f"\n=== {letter} ({roman})  →  {out_video.name} ===")

    import openai
    client = openai.OpenAI()
    print("  [TTS] intro")
    intro_audio = client.audio.speech.create(
        model="tts-1", voice=voice, speed=0.75,
        input=f"चलो, {letter} की बाराखड़ी सीखते हैं। मेरे साथ बोलिए।"
    ).content

    clips = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        intro_img = render_highlight_frame(letter, col_a, col_b, label, 0)
        intro_png = tmp / "intro.png"
        intro_img.save(str(intro_png))
        ap = tmp / "intro.mp3"
        ap.write_bytes(intro_audio)
        aud = AudioFileClip(str(ap))
        padded = padded_audio(aud, head=0.3, tail=0.4)
        clips.append(ImageClip(str(intro_png)).with_duration(padded.duration).with_audio(padded))

        for idx, m in enumerate(MATRAS):
            form  = letter + m["matra"]
            frame = render_highlight_frame(letter, col_a, col_b, label, idx)
            frame_path = tmp / f"frame_{idx:02d}.png"
            frame.save(str(frame_path))

            audio_bytes = _tts_form(form, voice, reps=4)
            mp = tmp / f"form_{idx:02d}.mp3"
            mp.write_bytes(audio_bytes)

            aud = AudioFileClip(str(mp))
            padded = padded_audio(aud, head=0.3, tail=0.6)
            clip = ImageClip(str(frame_path)).with_duration(padded.duration).with_audio(padded)
            clips.append(clip)

        print("  Assembling…")
        final = concatenate_videoclips(clips, method="compose")
        print(f"  Writing {out_video}")
        final.write_videofile(
            str(out_video), fps=24, codec="libx264",
            audio_codec="aac", logger=None,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
        )
    print(f"  Done: {out_video}")


def _resolve_letters(arg: str) -> list[str]:
    if arg in GROUP_PRESETS:
        return GROUP_PRESETS[arg]
    return [p.strip() for p in arg.split(",") if p.strip()]


def main():
    ap = argparse.ArgumentParser(description="Generate per-cell barakhadi highlight videos")
    ap.add_argument("--voice", default="nova")
    ap.add_argument("--letters", default="ka",
                    help="comma-separated roman labels (default: ka). "
                         "Use 'all-ka-varga' / 'all-cha-varga' etc. for groups.")
    args = ap.parse_args()
    for roman in _resolve_letters(args.letters):
        generate_video_for_letter(roman, args.voice)


if __name__ == "__main__":
    main()
