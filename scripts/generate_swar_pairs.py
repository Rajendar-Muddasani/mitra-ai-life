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
        "l1": "ए",  "r1": "e",   "p1": "e (like 'a' in 'make')",
        "l2": "ऐ",  "r2": "ai",  "p2": "ai (like 'i' in 'sky')",
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

CARD_W, CARD_H = 1080, 560   # taller so roman labels + pron hints are never cut


def _hex(h: str) -> tuple:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def _blend(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


CELL_TOP = 58           # y where white cells start
CELL_BOT = CARD_H - 50  # y where white cells end (50px bottom margin)
LETTER_Y = 64           # top of Devanagari letter inside cell
PRON_Y   = CARD_H - 120 # y of pronunciation hint
LABEL_Y  = CARD_H - 72  # y of roman label (e.g. "a", "aa")


def _load_fonts():
    try:
        big   = ImageFont.truetype(FONT_DEV, 200)
        label = ImageFont.truetype(FONT_LAT, 46)
        pron  = ImageFont.truetype(FONT_LAT, 28)
        badge = ImageFont.truetype(FONT_LAT, 28)
    except Exception:
        big = label = pron = badge = ImageFont.load_default()
    return big, label, pron, badge


def render_pair_card(p: dict, highlight: str | None = None) -> Image.Image:
    """Render a swar pair card.

    `highlight` can be "left", "right", "both", or None (no highlight).
    """
    col_a = _hex(p["col_a"])
    col_b = _hex(p["col_b"])

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    big, lbl, pron_f, badge_f = _load_fonts()

    # Badge centred at top
    badge = "मेरे साथ बोलिए  ·  Say it with me"
    bw    = draw.textlength(badge, font=badge_f)
    bx    = (CARD_W - bw) / 2
    draw.rounded_rectangle([bx - 14, 10, bx + bw + 14, 48], radius=8, fill=(255, 255, 255))
    draw.text((bx, 14), badge, font=badge_f, fill="#222222")

    # Vertical divider between the two halves
    mid = CARD_W // 2
    draw.line([(mid, 62), (mid, CARD_H - 54)], fill=(255, 255, 255), width=2)

    half = CARD_W // 2
    cells = [
        ("left",  p["l1"], p["r1"], p.get("p1", ""), half // 2),
        ("right", p["l2"], p["r2"], p.get("p2", ""), half + half // 2),
    ]
    for side, letter, roman, pron_text, cx_mid in cells:
        hi = highlight in (side, "both")
        left  = 20           if side == "left" else half + 20
        right = half - 20    if side == "left" else CARD_W - 20
        if hi:
            draw.rounded_rectangle([left, CELL_TOP, right, CELL_BOT],
                                    radius=24, fill=(255, 248, 205))
            text_fill  = (24, 24, 24)
            label_fill = (50, 50, 50)
            pron_fill  = (160, 80, 0)
        else:
            text_fill  = "white"
            label_fill = (240, 240, 240)
            pron_fill  = (255, 235, 100)

        # Large Devanagari letter
        lw = draw.textlength(letter, font=big)
        draw.text((cx_mid - lw / 2, LETTER_Y), letter, font=big, fill=text_fill)

        # Pronunciation hint
        if pron_text:
            pw = draw.textlength(pron_text, font=pron_f)
            draw.text((cx_mid - pw / 2, PRON_Y), pron_text, font=pron_f, fill=pron_fill)

        # Roman label — well above the card bottom
        rw = draw.textlength(roman, font=lbl)
        draw.text((cx_mid - rw / 2, LABEL_Y), roman, font=lbl, fill=label_fill)

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


def _tts_text(text: str, _voice: str = "nova", speed: float = 0.72) -> bytes:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _google_tts import tts_to_bytes
    print(f"  [gTTS] {text[:50]}…")
    return tts_to_bytes(text, speed=speed)


def generate_video(voice: str) -> None:
    """Swar pair repeat-after-me video.

    For each pair the sequence is:
      [l1 said once] +700ms → [l2 said once] +700ms
      → ["मेरे साथ बोलिए / Say it with me"] +5000ms (child repeats)

    No "बहुत अच्छा" — cleaner pacing, child focuses on saying not evaluating.
    Card always shows both letters at full brightness.
    """
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s

    # Regenerate pair card PNGs with the new taller layout
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in PAIRS:
        render_pair_card(p).save(str(IMG_DIR / f"pair-{p['name']}-card.png"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        atoms: list[pathlib.Path] = []

        for p in PAIRS:
            frame = tmp / f"{p['name']}.png"
            render_pair_card(p).save(str(frame))   # no highlight — full card

            # 3 clips — prompt FIRST so child knows to listen, then each letter,
            # then 5 s silence for the child to say both back
            for idx, (text, tail, spd) in enumerate([
                ("मेरे साथ बोलिए। Say it with me.", 0.8, 0.72),
                (p["l1"],                            0.7, 0.65),
                (p["l2"],                            5.0, 0.65),
            ]):
                mp3  = tmp / f"{p['name']}-{idx}.mp3"
                atom = tmp / f"{p['name']}-{idx}.mp4"
                mp3.write_bytes(_tts_text(text, voice, speed=spd))
                make_atomic_mp4(frame, mp3, atom, head_sil=0.3, tail_sil=tail)
                atoms.append(atom)

        print(f"  Concatenating {len(atoms)} clips → {OUT_VIDEO}")
        concat_mp4s(atoms, OUT_VIDEO)
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
