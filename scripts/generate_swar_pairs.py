#!/usr/bin/env python3
"""
generate_swar_pairs.py  —  Swar pair cards + "Say it with me" MP4

Renders 6 wide cards (one per vowel pair) and assembles a narrated video
where the voice models each letter 3 times then says them together.
Designed for a 5–6-year-old Hindi beginner.

Usage:
  python scripts/generate_swar_pairs.py --cards-only
  python scripts/generate_swar_pairs.py --voice nova
"""

import argparse, pathlib, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT      = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR   = ROOT / "content/assets/images/swar"
VID_DIR   = ROOT / "content/assets/videos/hindi-h1"
OUT_VIDEO = VID_DIR / "swar-repeat.mp4"
FONT_DEV  = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT  = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

PAIRS = [
    {
        "name": "a-aa",
        "l1": "अ",  "r1": "a",   "p1": "a (as in 'about')",
        "l2": "आ", "r2": "aa",   "p2": "aa (as in 'father')",
        "narration": "मेरे साथ बोलिए। अ। अ। अ। अब आ। आ। आ। बहुत अच्छा! अ और आ।",
        "col_a": "#c94b4b", "col_b": "#4b134f",
    },
    {
        "name": "i-ee",
        "l1": "इ",  "r1": "i",   "p1": "i (short, as in 'it')",
        "l2": "ई",  "r2": "ee",  "p2": "ee (long, as in 'see')",
        "narration": "मेरे साथ बोलिए। इ। इ। इ। अब ई। ई। ई। बहुत अच्छा! इ और ई।",
        "col_a": "#134e5e", "col_b": "#71b280",
    },
    {
        "name": "u-oo",
        "l1": "उ",  "r1": "u",   "p1": "u (short, as in 'put')",
        "l2": "ऊ",  "r2": "oo",  "p2": "oo (long, as in 'food')",
        "narration": "मेरे साथ बोलिए। उ। उ। उ। अब ऊ। ऊ। ऊ। बहुत अच्छा! उ और ऊ।",
        "col_a": "#1a1a2e", "col_b": "#4286f4",
    },
    {
        "name": "e-ai",
        "l1": "ए",  "r1": "e",   "p1": "e (as in 'play')",
        "l2": "ऐ",  "r2": "ai",  "p2": "ai (as in 'cat')",
        "narration": "मेरे साथ बोलिए। ए। ए। ए। अब ऐ। ऐ। ऐ। बहुत अच्छा! ए और ऐ।",
        "col_a": "#870000", "col_b": "#c33764",
    },
    {
        "name": "o-au",
        "l1": "ओ", "r1": "o",    "p1": "o (as in 'go')",
        "l2": "औ", "r2": "au",   "p2": "au (as in 'caught')",
        "narration": "मेरे साथ बोलिए। ओ। ओ। ओ। अब औ। औ। औ। बहुत अच्छा! ओ और औ।",
        "col_a": "#005c97", "col_b": "#363795",
    },
    {
        "name": "an-ah",
        "l1": "अं", "r1": "an",  "p1": "an (nasal hum)",
        "l2": "अः", "r2": "ah",  "p2": "ah (soft breath)",
        "narration": "मेरे साथ बोलिए। अं। अं। अं। अब अः। अः। अः। बहुत अच्छा! अं और अः।",
        "col_a": "#0f9b58", "col_b": "#00bf8f",
    },
]

CARD_W, CARD_H = 1080, 480


def _hex(h: str) -> tuple:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def _blend(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _load_fonts():
    try:
        big   = ImageFont.truetype(FONT_DEV, 180)
        label = ImageFont.truetype(FONT_LAT, 40)
        pron  = ImageFont.truetype(FONT_LAT, 26)
        badge = ImageFont.truetype(FONT_LAT, 26)
    except Exception:
        big = label = pron = badge = ImageFont.load_default()
    return big, label, pron, badge


def render_pair_card(p: dict, active: str | None = None) -> Image.Image:
    col_a = _hex(p["col_a"])
    col_b = _hex(p["col_b"])

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    # Horizontal gradient
    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    big, lbl, pron_f, badge_f = _load_fonts()

    # Badge centred at top
    badge = "Say it with me  ·  मेरे साथ बोलिए"
    bw    = draw.textlength(badge, font=badge_f)
    bx    = (CARD_W - bw) / 2
    draw.rounded_rectangle([bx - 12, 10, bx + bw + 12, 44], radius=8, fill=(255, 255, 255))
    draw.text((bx, 14), badge, font=badge_f, fill="#222222")

    # Soft vertical divider
    mid = CARD_W // 2
    draw.line([(mid, 60), (mid, CARD_H - 30)], fill=(255, 255, 255), width=2)

    # Left and right cells
    half = CARD_W // 2
    cells = [
        ("left",  p["l1"], p["r1"], p.get("p1", ""), half // 2),
        ("right", p["l2"], p["r2"], p.get("p2", ""), half + half // 2),
    ]
    for side, letter, roman, pron_text, cx_mid in cells:
        if active in (side, "both"):
            left = 24 if side == "left" else half + 24
            right = half - 24 if side == "left" else CARD_W - 24
            draw.rounded_rectangle([left, 58, right, CARD_H - 32], radius=24, fill=(255, 248, 205))
            text_fill  = (24, 24, 24)
            label_fill = (60, 60, 60)
            pron_fill  = (180, 90, 0)
        else:
            text_fill  = "white"
            label_fill = "#f1f1f1"
            pron_fill  = (255, 240, 120)
        # Devanagari letter (large)
        lw  = draw.textlength(letter, font=big)
        lx  = cx_mid - lw / 2
        ly  = 55
        draw.text((lx, ly), letter, font=big, fill=text_fill)

        # Pronunciation hint (e.g. "i (short, as in 'it')")
        if pron_text:
            pw = draw.textlength(pron_text, font=pron_f)
            px = cx_mid - pw / 2
            py = CARD_H - 100
            draw.text((px, py), pron_text, font=pron_f, fill=pron_fill)

        # Roman label (a / aa)
        rw  = draw.textlength(roman, font=lbl)
        rx  = cx_mid - rw / 2
        ry  = CARD_H - 60
        draw.text((rx, ry), roman, font=lbl, fill=label_fill)

    return img


def generate_cards() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in PAIRS:
        out = IMG_DIR / f"pair-{p['name']}-card.png"
        render_pair_card(p).save(str(out))
        print(f"  [PNG] {out.name}")
    print("Cards done. Run without --cards-only to build video.")


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def _tts_text(text: str, voice: str) -> bytes:
    import openai
    client = openai.OpenAI()
    print(f"  [TTS] {text[:45]}…")
    return client.audio.speech.create(
        model="tts-1", voice=voice, speed=0.72, input=text
    ).content


def generate_video(voice: str) -> None:
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _av_sync import padded_audio
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

    clips = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for p in PAIRS:
            png = IMG_DIR / f"pair-{p['name']}-card.png"
            if not png.exists():
                render_pair_card(p).save(str(png))

            segments = [
                ("left", "मेरे साथ बोलिए। " + ". ".join([p["l1"]] * 3) + "."),
                ("right", "अब " + ". ".join([p["l2"]] * 3) + "."),
                ("both", f"बहुत अच्छा! {p['l1']} और {p['l2']}।"),
            ]
            for idx, (active, text) in enumerate(segments):
                frame = tmp / f"{p['name']}-{idx}.png"
                render_pair_card(p, active=active).save(str(frame))
                ap = tmp / f"{p['name']}-{idx}.mp3"
                ap.write_bytes(_tts_text(text, voice))
                aud = AudioFileClip(str(ap))
                padded = padded_audio(aud, head=0.3, tail=0.6)
                clips.append(ImageClip(str(frame)).with_duration(padded.duration).with_audio(padded))

        print("Assembling video…")
        final = concatenate_videoclips(clips, method="compose")
        print(f"  Writing {OUT_VIDEO}")
        final.write_videofile(
            str(OUT_VIDEO), fps=24, codec="libx264",
            audio_codec="aac", logger=None,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
        )
    print("  Done.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate swar pair cards and repeat-after-me video")
    ap.add_argument("--cards-only", action="store_true")
    ap.add_argument("--voice", default="nova")
    args = ap.parse_args()
    if args.cards_only:
        generate_cards()
    else:
        generate_cards()
        generate_video(args.voice)


if __name__ == "__main__":
    main()
