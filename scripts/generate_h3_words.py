#!/usr/bin/env python3
"""
generate_h3_words.py  —  Words and Reading word+image cards for h3.html

Five topic groups, six words each (30 cards total):
  1. animals (जानवर)
  2. food (खाना)
  3. home objects (घर)
  4. body parts (शरीर)
  5. colours (रंग)

Each card uses the same render_word_card layout as `generate_word_cards.py`,
with a Devanagari letter form at the top, a realistic DALL-E image in the
middle, and a Hindi word + pronunciation + English meaning at the bottom.

Also assembles a single words-reading.mp4 with TTS narration grouped by topic.

Usage:
  python scripts/generate_h3_words.py --cards-only
  python scripts/generate_h3_words.py --topic animals
  python scripts/generate_h3_words.py
"""

import argparse, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_BASE = ROOT / "content/assets/images/word-cards"
VID_DIR  = ROOT / "content/assets/videos/hindi-h1"
OUT_VIDEO = VID_DIR / "words-reading.mp4"

sys.path.insert(0, str(ROOT / "scripts"))
from generate_word_cards import (
    render_word_card, _dalle_image, _hex, _make_numeral_one, _load_env,
)

TOPICS = {
    "animals": {
        "label": "Animals · जानवर",
        "intro_hi": "ये जानवर हैं। हर जानवर का नाम मेरे साथ बोलिए।",
        "words": [
            {"form": "श",  "slug": "sher",   "word": "शेर",   "pron": "sher",   "meaning": "lion",
             "col_a": "#e65100", "col_b": "#bf360c",
             "prompt": "one Indian lion sitting upright with full mane, plain background, full body visible"},
            {"form": "ब",  "slug": "billi",  "word": "बिल्ली", "pron": "billi",  "meaning": "cat",
             "col_a": "#37474f", "col_b": "#546e7a",
             "prompt": "one small house cat sitting upright, full body visible, plain background"},
            {"form": "क",  "slug": "kutta",  "word": "कुत्ता", "pron": "kutta",  "meaning": "dog",
             "col_a": "#bf360c", "col_b": "#d84315",
             "prompt": "one friendly Indian street dog sitting upright, full body visible, plain background"},
            {"form": "ह",  "slug": "haathi", "word": "हाथी",  "pron": "haathi", "meaning": "elephant",
             "col_a": "#4e342e", "col_b": "#6d4c41",
             "prompt": "one Indian elephant standing sideways with long trunk down, full body visible, plain background"},
            {"form": "ब",  "slug": "bandar", "word": "बंदर",  "pron": "bandar", "meaning": "monkey",
             "col_a": "#5d4037", "col_b": "#3e2723",
             "prompt": "one Indian rhesus monkey sitting on a tree branch, full body visible"},
            {"form": "च",  "slug": "chidiya","word": "चिड़िया","pron": "chidiya","meaning": "bird",
             "col_a": "#2e7d32", "col_b": "#1b5e20",
             "prompt": "one small Indian sparrow sitting on a small branch, brown and grey"},
        ],
    },
    "food": {
        "label": "Food · खाना",
        "intro_hi": "ये खाने की चीज़ें हैं। मेरे साथ बोलिए।",
        "words": [
            {"form": "र",  "slug": "roti",   "word": "रोटी",  "pron": "roti",   "meaning": "flatbread",
             "col_a": "#bf360c", "col_b": "#8d6e63",
             "prompt": "one round Indian wheat roti chapati on a plain steel plate, top-down view"},
            {"form": "च",  "slug": "chawal", "word": "चावल",  "pron": "chawal", "meaning": "rice",
             "col_a": "#f9a825", "col_b": "#bf360c",
             "prompt": "one small steel bowl filled with cooked white Indian basmati rice, top-down"},
            {"form": "द",  "slug": "dal",    "word": "दाल",   "pron": "dal",    "meaning": "lentils",
             "col_a": "#f9a825", "col_b": "#e65100",
             "prompt": "one small steel bowl filled with cooked yellow Indian dal lentils, top-down"},
            {"form": "स",  "slug": "sabzi",  "word": "सब्ज़ी", "pron": "sabzi",  "meaning": "vegetables",
             "col_a": "#1b5e20", "col_b": "#2e7d32",
             "prompt": "one small steel bowl of cooked Indian mixed vegetable sabzi with visible green vegetables"},
            {"form": "द",  "slug": "doodh",  "word": "दूध",   "pron": "doodh",  "meaning": "milk",
             "col_a": "#cfd8dc", "col_b": "#90a4ae",
             "prompt": "one clear glass of plain white milk on a plain surface, side view"},
            {"form": "फ",  "slug": "phal",   "word": "फल",    "pron": "phal",   "meaning": "fruit",
             "col_a": "#e65100", "col_b": "#bf360c",
             "prompt": "one small bowl of mixed fresh Indian fruits: banana, apple, orange, mango"},
        ],
    },
    "home": {
        "label": "Home Objects · घर की चीज़ें",
        "intro_hi": "ये घर की चीज़ें हैं। नाम बोलिए।",
        "words": [
            {"form": "क",  "slug": "kursi",  "word": "कुर्सी","pron": "kursi",  "meaning": "chair",
             "col_a": "#4e342e", "col_b": "#6d4c41",
             "prompt": "one simple wooden Indian household chair, single, plain background"},
            {"form": "म",  "slug": "mez",    "word": "मेज़",   "pron": "mez",    "meaning": "table",
             "col_a": "#5d4037", "col_b": "#3e2723",
             "prompt": "one simple wooden Indian household table, single, plain background"},
            {"form": "प",  "slug": "pankha", "word": "पंखा",  "pron": "pankha", "meaning": "fan",
             "col_a": "#0277bd", "col_b": "#01579b",
             "prompt": "one Indian ceiling fan with three blades, front view, plain background"},
            {"form": "ब",  "slug": "bistar", "word": "बिस्तर","pron": "bistar", "meaning": "bed",
             "col_a": "#283593", "col_b": "#1a237e",
             "prompt": "one simple Indian wooden bed with white sheet and pillow, single, plain background"},
            {"form": "द",  "slug": "darwaza","word": "दरवाज़ा","pron": "darwaza","meaning": "door",
             "col_a": "#4e342e", "col_b": "#3e2723",
             "prompt": "one simple wooden Indian house door, single, plain background"},
            {"form": "ख",  "slug": "khidki", "word": "खिड़की","pron": "khidki", "meaning": "window",
             "col_a": "#1565c0", "col_b": "#0d47a1",
             "prompt": "one simple wooden Indian house window with open shutters, plain wall"},
        ],
    },
    "body": {
        "label": "Body Parts · शरीर के अंग",
        "intro_hi": "ये शरीर के अंग हैं। मेरे साथ बोलिए।",
        "words": [
            {"form": "स",  "slug": "sir",     "word": "सिर",    "pron": "sir",     "meaning": "head",
             "col_a": "#ad1457", "col_b": "#880e4f",
             "prompt": "one friendly Indian child's head and face close-up, simple plain background"},
            {"form": "आ",  "slug": "aankh",   "word": "आँख",    "pron": "aankh",   "meaning": "eye",
             "col_a": "#1565c0", "col_b": "#0d47a1",
             "prompt": "close-up of one human eye, simple plain background, friendly"},
            {"form": "न",  "slug": "naak",    "word": "नाक",    "pron": "naak",    "meaning": "nose",
             "col_a": "#bf360c", "col_b": "#8d6e63",
             "prompt": "close-up of human nose and cheek area, simple plain background, friendly"},
            {"form": "क",  "slug": "kaan",    "word": "कान",    "pron": "kaan",    "meaning": "ear",
             "col_a": "#5d4037", "col_b": "#4e342e",
             "prompt": "close-up of one human ear from side, simple plain background"},
            {"form": "ह",  "slug": "haath",   "word": "हाथ",    "pron": "haath",   "meaning": "hand",
             "col_a": "#6d4c41", "col_b": "#5d4037",
             "prompt": "open palm of one Indian child's hand, simple plain background"},
            {"form": "प",  "slug": "pair",    "word": "पैर",    "pron": "pair",    "meaning": "foot / leg",
             "col_a": "#3e2723", "col_b": "#5d4037",
             "prompt": "one Indian child's bare foot on a plain floor, side view"},
        ],
    },
    "colours": {
        "label": "Colours · रंग",
        "intro_hi": "ये रंग हैं। हर रंग का नाम बोलिए।",
        "words": [
            {"form": "ल",  "slug": "lal",     "word": "लाल",    "pron": "laal",    "meaning": "red",
             "col_a": "#b71c1c", "col_b": "#7f0000",
             "prompt": "one solid bright red colour painted circle on a pure white background, simple"},
            {"form": "ह",  "slug": "hara",    "word": "हरा",    "pron": "hara",    "meaning": "green",
             "col_a": "#1b5e20", "col_b": "#0d4715",
             "prompt": "one solid bright green colour painted circle on a pure white background, simple"},
            {"form": "न",  "slug": "neela",   "word": "नीला",   "pron": "neela",   "meaning": "blue",
             "col_a": "#0d47a1", "col_b": "#082567",
             "prompt": "one solid bright blue colour painted circle on a pure white background, simple"},
            {"form": "प",  "slug": "peela",   "word": "पीला",   "pron": "peela",   "meaning": "yellow",
             "col_a": "#f9a825", "col_b": "#bf6c00",
             "prompt": "one solid bright yellow colour painted circle on a pure white background, simple"},
            {"form": "क",  "slug": "kaala",   "word": "काला",   "pron": "kaala",   "meaning": "black",
             "col_a": "#212121", "col_b": "#000000",
             "prompt": "one solid black colour painted circle on a pure white background, simple"},
            {"form": "स",  "slug": "safed",   "word": "सफ़ेद",  "pron": "safed",   "meaning": "white",
             "col_a": "#90a4ae", "col_b": "#546e7a",
             "prompt": "one solid white colour painted circle outlined in light grey, on a pure white background, simple"},
        ],
    },
}


def generate_topic_cards(topic: str, force: bool) -> None:
    import openai
    _load_env()
    client = openai.OpenAI()
    spec = TOPICS[topic]
    out_dir = OUT_BASE / f"h3-{topic}"
    out_dir.mkdir(parents=True, exist_ok=True)

    for entry in spec["words"]:
        out_path = out_dir / f"{entry['slug']}.png"
        if out_path.exists() and not force:
            print(f"  [SKIP] {topic}/{out_path.name}")
            continue
        try:
            print(f"  [DALL-E] {topic} · {entry['word']} ({entry['meaning']})")
            illus = _dalle_image(entry["prompt"], client)
        except Exception as e:
            print(f"    ERROR: {e}")
            from PIL import Image
            illus = Image.new("RGB", (1024, 1024), color=(200, 200, 200))
        card = render_word_card(entry, illus)
        card.save(str(out_path))
        print(f"    → saved {topic}/{out_path.name}")


def generate_video(voice: str) -> None:
    _load_env()
    VID_DIR.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _video_kit import make_atomic_mp4, concat_mp4s
    import openai, tempfile
    client = openai.OpenAI()

    def tts(text: str, speed: float = 0.68) -> bytes:
        return client.audio.speech.create(
            model="tts-1", voice=voice, speed=speed, input=text,
        ).content

    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        atoms: list[pathlib.Path] = []
        for topic, spec in TOPICS.items():
            for entry in spec["words"]:
                card_path = OUT_BASE / f"h3-{topic}" / f"{entry['slug']}.png"
                if not card_path.exists():
                    print(f"  [SKIP] missing card: {card_path.name}")
                    continue
                narration = (
                    f"{entry['word']}. {entry['word']}. "
                    f"{entry['pron']}. {entry['meaning']}."
                )
                print(f"  [TTS] {topic} · {entry['word']}")
                mp3 = tmp / f"{topic}-{entry['slug']}.mp3"
                mp3.write_bytes(tts(narration))
                atom = tmp / f"{topic}-{entry['slug']}.mp4"
                make_atomic_mp4(card_path, mp3, atom, head_sil=0.4, tail_sil=1.2)
                atoms.append(atom)

        if not atoms:
            print("No clips to assemble.")
            return
        print(f"  Concatenating {len(atoms)} clips → {OUT_VIDEO}")
        concat_mp4s(atoms, OUT_VIDEO)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", choices=list(TOPICS.keys()) + ["all"], default="all")
    ap.add_argument("--cards-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--voice", default="nova")
    args = ap.parse_args()

    topics = list(TOPICS.keys()) if args.topic == "all" else [args.topic]
    for t in topics:
        print(f"--- {t} ---")
        generate_topic_cards(t, force=args.force)

    if not args.cards_only:
        generate_video(args.voice)
    print("Done.")


if __name__ == "__main__":
    main()
