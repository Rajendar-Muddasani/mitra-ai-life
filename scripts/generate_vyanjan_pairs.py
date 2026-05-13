#!/usr/bin/env python3
"""
generate_vyanjan_pairs.py  —  Vyanjan pair / solo cards + "Say it with me" MP4

Pairs similar-sounding consonants across all 7 vargas.
Unpaired consonants (ङ, ञ, ण, न, म) get solo cards.
Designed for a 5–6-year-old Hindi beginner.

Usage:
  python scripts/generate_vyanjan_pairs.py --cards-only
  python scripts/generate_vyanjan_pairs.py --voice nova
"""

import argparse, pathlib, tempfile, time
from PIL import Image, ImageDraw, ImageFont

ROOT      = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR   = ROOT / "content/assets/images/vyanjan-pairs"
VID_DIR   = ROOT / "content/assets/videos/hindi-h1"
OUT_VIDEO = VID_DIR / "vyanjan-repeat.mp4"
FONT_DEV  = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT  = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# Pairs and solos across all 7 vargas.
# solo=True cards show one letter centered in the full card width.
PAIRS = [
    # क-वर्ग
    {
        "name": "ka-kha", "solo": False,
        "l1": "क", "r1": "ka",  "l2": "ख", "r2": "kha",
        "narration": "मेरे साथ बोलिए। क। क। क। अब ख। ख। ख। बहुत अच्छा! क और ख।",
        "col_a": "#c94b4b", "col_b": "#4b134f",
    },
    {
        "name": "ga-gha", "solo": False,
        "l1": "ग", "r1": "ga",  "l2": "घ", "r2": "gha",
        "narration": "मेरे साथ बोलिए। ग। ग। ग। अब घ। घ। घ। बहुत अच्छा! ग और घ।",
        "col_a": "#134e5e", "col_b": "#71b280",
    },
    {
        "name": "nga", "solo": True,
        "l1": "ङ", "r1": "nga", "l2": "", "r2": "",
        "narration": "सुनिए और बोलिए। ङ। ङ। ङ। बहुत अच्छा!",
        "col_a": "#1a1a2e", "col_b": "#4286f4",
    },
    # च-वर्ग
    {
        "name": "cha-chha", "solo": False,
        "l1": "च", "r1": "cha", "l2": "छ", "r2": "chha",
        "narration": "मेरे साथ बोलिए। च। च। च। अब छ। छ। छ। बहुत अच्छा! च और छ।",
        "col_a": "#870000", "col_b": "#c33764",
    },
    {
        "name": "ja-jha", "solo": False,
        "l1": "ज", "r1": "ja",  "l2": "झ", "r2": "jha",
        "narration": "मेरे साथ बोलिए। ज। ज। ज। अब झ। झ। झ। बहुत अच्छा! ज और झ।",
        "col_a": "#005c97", "col_b": "#363795",
    },
    {
        "name": "nya", "solo": True,
        "l1": "ञ", "r1": "nya", "l2": "", "r2": "",
        "narration": "सुनिए और बोलिए। ञ। ञ। ञ। बहुत अच्छा!",
        "col_a": "#0f9b58", "col_b": "#00bf8f",
    },
    # ट-वर्ग (retroflex)
    {
        "name": "tta-ttha", "solo": False,
        "l1": "ट", "r1": "Ta",  "l2": "ठ", "r2": "Tha",
        "narration": "मेरे साथ बोलिए। ट। ट। ट। अब ठ। ठ। ठ। बहुत अच्छा! ट और ठ।",
        "col_a": "#c94b4b", "col_b": "#1a1a2e",
    },
    {
        "name": "dda-ddha", "solo": False,
        "l1": "ड", "r1": "Da",  "l2": "ढ", "r2": "Dha",
        "narration": "मेरे साथ बोलिए। ड। ड। ड। अब ढ। ढ। ढ। बहुत अच्छा! ड और ढ।",
        "col_a": "#134e5e", "col_b": "#870000",
    },
    {
        "name": "nna", "solo": True,
        "l1": "ण", "r1": "Na",  "l2": "", "r2": "",
        "narration": "सुनिए और बोलिए। ण। ण। ण। बहुत अच्छा!",
        "col_a": "#005c97", "col_b": "#0f9b58",
    },
    # त-वर्ग (dental)
    {
        "name": "ta-tha", "solo": False,
        "l1": "त", "r1": "ta",  "l2": "थ", "r2": "tha",
        "narration": "मेरे साथ बोलिए। त। त। त। अब थ। थ। थ। बहुत अच्छा! त और थ।",
        "col_a": "#c33764", "col_b": "#363795",
    },
    {
        "name": "da-dha", "solo": False,
        "l1": "द", "r1": "da",  "l2": "ध", "r2": "dha",
        "narration": "मेरे साथ बोलिए। द। द। द। अब ध। ध। ध। बहुत अच्छा! द और ध।",
        "col_a": "#1a1a2e", "col_b": "#71b280",
    },
    {
        "name": "na", "solo": True,
        "l1": "न", "r1": "na",  "l2": "", "r2": "",
        "narration": "सुनिए और बोलिए। न। न। न। बहुत अच्छा!",
        "col_a": "#870000", "col_b": "#c94b4b",
    },
    # प-वर्ग
    {
        "name": "pa-pha", "solo": False,
        "l1": "प", "r1": "pa",  "l2": "फ", "r2": "pha",
        "narration": "मेरे साथ बोलिए। प। प। प। अब फ। फ। फ। बहुत अच्छा! प और फ।",
        "col_a": "#4b134f", "col_b": "#134e5e",
    },
    {
        "name": "ba-bha", "solo": False,
        "l1": "ब", "r1": "ba",  "l2": "भ", "r2": "bha",
        "narration": "मेरे साथ बोलिए। ब। ब। ब। अब भ। भ। भ। बहुत अच्छा! ब और भ।",
        "col_a": "#363795", "col_b": "#0f9b58",
    },
    {
        "name": "ma", "solo": True,
        "l1": "म", "r1": "ma",  "l2": "", "r2": "",
        "narration": "सुनिए और बोलिए। म। म। म। बहुत अच्छा!",
        "col_a": "#005c97", "col_b": "#c33764",
    },
    # अन्तःस्थ
    {
        "name": "ya-ra", "solo": False,
        "l1": "य", "r1": "ya",  "l2": "र", "r2": "ra",
        "narration": "मेरे साथ बोलिए। य। य। य। अब र। र। र। बहुत अच्छा! य और र।",
        "col_a": "#c94b4b", "col_b": "#4286f4",
    },
    {
        "name": "la-va", "solo": False,
        "l1": "ल", "r1": "la",  "l2": "व", "r2": "va",
        "narration": "मेरे साथ बोलिए। ल। ल। ल। अब व। व। व। बहुत अच्छा! ल और व।",
        "col_a": "#1a1a2e", "col_b": "#71b280",
    },
    # ऊष्म
    {
        "name": "sha-ssha", "solo": False,
        "l1": "श", "r1": "sha", "l2": "ष", "r2": "Sha",
        "narration": "मेरे साथ बोलिए। श। श। श। अब ष। ष। ष। बहुत अच्छा! श और ष।",
        "col_a": "#870000", "col_b": "#134e5e",
    },
    {
        "name": "sa-ha", "solo": False,
        "l1": "स", "r1": "sa",  "l2": "ह", "r2": "ha",
        "narration": "मेरे साथ बोलिए। स। स। स। अब ह। ह। ह। बहुत अच्छा! स और ह।",
        "col_a": "#0f9b58", "col_b": "#4b134f",
    },
]

CARD_W, CARD_H = 1080, 480


def _hex(h: str) -> tuple:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def _blend(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _load_fonts():
    try:
        big   = ImageFont.truetype(FONT_DEV, 200)
        label = ImageFont.truetype(FONT_LAT, 34)
        badge = ImageFont.truetype(FONT_LAT, 26)
    except Exception:
        big = label = badge = ImageFont.load_default()
    return big, label, badge


def render_pair_card(p: dict, active: str | None = None) -> Image.Image:
    col_a = _hex(p["col_a"])
    col_b = _hex(p["col_b"])

    img  = Image.new("RGB", (CARD_W, CARD_H))
    draw = ImageDraw.Draw(img)

    # Horizontal gradient
    for x in range(CARD_W):
        draw.line([(x, 0), (x, CARD_H)], fill=_blend(col_a, col_b, x / CARD_W))

    big, label, badge = _load_fonts()

    if p["solo"]:
        if active in ("left", "both"):
            draw.rounded_rectangle([42, 58, CARD_W - 42, CARD_H - 38], radius=28, fill=(255, 248, 205))
            text_fill = (24, 24, 24)
            label_fill = (80, 80, 80)
        else:
            text_fill = "white"
            label_fill = (220, 220, 220)
        # Single letter centered
        lw = draw.textlength(p["l1"], font=big)
        lx = (CARD_W - lw) / 2
        draw.text((lx, 40), p["l1"], font=big, fill=text_fill)
        rw = draw.textlength(p["r1"], font=label)
        draw.text(((CARD_W - rw) / 2, CARD_H - 70), p["r1"], font=label, fill=label_fill)
    else:
        if active in ("left", "both"):
            draw.rounded_rectangle([34, 58, CARD_W // 2 - 34, CARD_H - 38], radius=28, fill=(255, 248, 205))
            left_text = (24, 24, 24)
            left_label = (80, 80, 80)
        else:
            left_text = "white"
            left_label = (220, 220, 220)
        if active in ("right", "both"):
            draw.rounded_rectangle([CARD_W // 2 + 34, 58, CARD_W - 34, CARD_H - 38], radius=28, fill=(255, 248, 205))
            right_text = (24, 24, 24)
            right_label = (80, 80, 80)
        else:
            right_text = "white"
            right_label = (220, 220, 220)
        # Left letter
        lw = draw.textlength(p["l1"], font=big)
        lx = CARD_W // 4 - lw / 2
        draw.text((lx, 40), p["l1"], font=big, fill=left_text)
        rw_lbl = draw.textlength(p["r1"], font=label)
        draw.text((CARD_W // 4 - rw_lbl / 2, CARD_H - 70), p["r1"], font=label, fill=left_label)

        # Divider
        draw.line([(CARD_W // 2, 40), (CARD_W // 2, CARD_H - 40)],
                  fill=(255, 255, 255), width=3)

        # Right letter
        r2w = draw.textlength(p["l2"], font=big)
        r2x = 3 * CARD_W // 4 - r2w / 2
        draw.text((r2x, 40), p["l2"], font=big, fill=right_text)
        r2lw = draw.textlength(p["r2"], font=label)
        draw.text((3 * CARD_W // 4 - r2lw / 2, CARD_H - 70), p["r2"], font=label, fill=right_label)

    # Badge top-left
    badge_text = "Say it with me  ·  मेरे साथ बोलिए" if not p["solo"] else "Listen and say  ·  सुनिए और बोलिए"
    draw.text((28, 20), badge_text, font=badge, fill=(255, 255, 255))

    return img


def generate_cards() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in PAIRS:
        out = IMG_DIR / f"pair-{p['name']}-card.png"
        img = render_pair_card(p)
        img.save(str(out))
        print(f"  [PNG] {out.name}")


def _tts(client, narration: str, out_path: pathlib.Path, voice: str) -> None:
    if out_path.exists():
        print(f"  [SKIP] {out_path.name}")
        return
    print(f"  [TTS] {narration[:50]}")
    with client.audio.speech.with_streaming_response.create(
        model="tts-1", voice=voice, input=narration, speed=0.72,
    ) as resp:
        resp.stream_to_file(str(out_path))
    time.sleep(0.5)


def generate_video(voice: str) -> None:
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from _video_kit import make_atomic_mp4, concat_mp4s
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    import openai
    client = openai.OpenAI()

    VID_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        atoms: list[pathlib.Path] = []

        for p in PAIRS:
            card_path = IMG_DIR / f"pair-{p['name']}-card.png"
            if not card_path.exists():
                render_pair_card(p).save(str(card_path))

            if p["solo"]:
                segments = [("left", "सुनिए और बोलिए। " + ". ".join([p["l1"]] * 3) + ". बहुत अच्छा!")]
            else:
                segments = [
                    ("left",  "मेरे साथ बोलिए। " + ". ".join([p["l1"]] * 3) + "."),
                    ("right", "अब " + ". ".join([p["l2"]] * 3) + "."),
                    ("both",  f"बहुत अच्छा! {p['l1']} और {p['l2']}।"),
                ]

            for idx, (active, narration) in enumerate(segments):
                frame = tmp / f"{p['name']}-{idx}.png"
                render_pair_card(p, active=active).save(str(frame))
                mp3 = tmp / f"{p['name']}-{idx}.mp3"
                _tts(client, narration, mp3, voice)
                atom = tmp / f"{p['name']}-{idx}.mp4"
                make_atomic_mp4(frame, mp3, atom, head_sil=0.3, tail_sil=0.7)
                atoms.append(atom)

        print(f"  Concatenating {len(atoms)} clips → {OUT_VIDEO}")
        concat_mp4s(atoms, OUT_VIDEO)
    print("  Done.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-only", action="store_true")
    ap.add_argument("--voice", default="nova")
    args = ap.parse_args()

    print("Generating vyanjan pair card PNGs…")
    generate_cards()

    if not args.cards_only:
        print("Generating vyanjan-repeat.mp4…")
        generate_video(args.voice)


if __name__ == "__main__":
    main()
