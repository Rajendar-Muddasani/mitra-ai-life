#!/usr/bin/env python3
"""
generate_word_cards.py  —  Word + image cards using DALL-E 3 + PIL

Two sets:
  1. Swar (vowel) words  → content/assets/images/word-cards/swar/
  2. Ka barakhadi words  → content/assets/images/word-cards/ka-bara/

Each card: large Hindi letter form at top, realistic object image in the middle,
Hindi word + English pronunciation + English meaning at the bottom.

Usage:
  python scripts/generate_word_cards.py --set swar
  python scripts/generate_word_cards.py --set ka
  python scripts/generate_word_cards.py --set all
"""

import argparse, pathlib, io
from PIL import Image, ImageDraw, ImageFont

ROOT      = pathlib.Path(__file__).resolve().parent.parent
OUT_SWAR  = ROOT / "content/assets/images/word-cards/swar"
OUT_KA    = ROOT / "content/assets/images/word-cards/ka-bara"
OUT_KHA   = ROOT / "content/assets/images/word-cards/kha-bara"
OUT_GA    = ROOT / "content/assets/images/word-cards/ga-bara"
OUT_GHA   = ROOT / "content/assets/images/word-cards/gha-bara"
OUT_NGA   = ROOT / "content/assets/images/word-cards/nga-bara"
FONT_DEV  = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"
FONT_LAT  = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

CARD_W, CARD_H = 900, 1120

REALISTIC_STYLE = (
    "DSLR photograph, Canon 5D, studio lighting, sharp focus, hyperrealistic, "
    "photorealistic product photo on a pure white seamless background. "
    "The subject fills most of the frame, large and immediately recognisable to a 5-year-old Indian child. "
    "ABSOLUTELY NO: cartoon, illustration, vector art, 3-D render, digital painting, watercolour, "
    "anime, flat design, clip art, text, labels, watermarks, borders, frames."
)

# ── Word lists ─────────────────────────────────────────────────────────────────

SWAR_WORDS = [
    {"form": "अ",  "slug": "a",  "word": "अनार", "pron": "anaar", "meaning": "pomegranate",
     "col_a": "#c0392b", "col_b": "#8e44ad",
     "prompt": "one ripe red pomegranate cut open with bright red seeds visible"},
    {"form": "आ", "slug": "aa", "word": "आम", "pron": "aam", "meaning": "mango",
     "col_a": "#f39c12", "col_b": "#e67e22",
     "prompt": "one ripe yellow mango with a small green leaf"},
    {"form": "इ",  "slug": "i",  "word": "इमली", "pron": "imli", "meaning": "tamarind",
     "col_a": "#27ae60", "col_b": "#16a085",
     "prompt": "real tamarind pods, some brown pods opened to show sticky tamarind pulp and seeds"},
    {"form": "ई",  "slug": "ee", "word": "ईंट", "pron": "eent", "meaning": "brick",
     "col_a": "#e74c3c", "col_b": "#c0392b",
     "prompt": "one red clay brick"},
    {"form": "उ",  "slug": "u",  "word": "उल्लू", "pron": "ullu", "meaning": "owl",
     "col_a": "#2c3e50", "col_b": "#8e44ad",
     "prompt": "one real owl sitting clearly on a small branch, absolutely no text or writing anywhere in the image"},
    {"form": "ऊ",  "slug": "oo", "word": "ऊँट", "pron": "oont", "meaning": "camel",
     "col_a": "#f39c12", "col_b": "#d35400",
     "prompt": "one camel standing sideways, full body visible, absolutely no text or writing or labels anywhere in the image"},
    {"form": "ए",  "slug": "e",  "word": "एक", "pron": "ek", "meaning": "one",
     "col_a": "#1abc9c", "col_b": "#3498db",
     "pil_one": True, "prompt": ""},
    # NOTE: ए uses PIL-generated numeral '1' — no DALL-E needed
    {"form": "ऐ",  "slug": "ai", "word": "ऐनक", "pron": "ainak", "meaning": "glasses",
     "col_a": "#9b59b6", "col_b": "#3498db",
     "prompt": "one pair of clear round eyeglasses"},
    {"form": "ओ", "slug": "o",  "word": "ओस", "pron": "os", "meaning": "dew drops",
     "col_a": "#2980b9", "col_b": "#27ae60",
     "prompt": "large clear dew drops on a fresh green leaf"},
    {"form": "औ", "slug": "au", "word": "औरत", "pron": "aurat", "meaning": "woman",
     "col_a": "#e91e63", "col_b": "#9c27b0",
     "prompt": "one smiling Indian woman in a simple colorful saree, friendly portrait"},
    {"form": "अं", "slug": "an", "word": "अंगूर", "pron": "angoor", "meaning": "grapes",
     "col_a": "#6a1b9a", "col_b": "#4527a0",
     "prompt": "one bunch of purple grapes"},
    {"form": "अः", "slug": "ah", "word": "अहा!", "pron": "aha", "meaning": "wow / aha!",
     "col_a": "#ff6f00", "col_b": "#e65100",
     "prompt": "a happy surprised Indian child smiling with wide eyes, expressive wow reaction"},
]

KA_WORDS = [
    {"form": "क",  "slug": "ka-word",  "word": "कमल", "pron": "kamal", "meaning": "lotus",
     "col_a": "#c0392b", "col_b": "#8e44ad",
     "prompt": "one pink lotus flower floating on water"},
    {"form": "का", "slug": "kaa-word", "word": "काका", "pron": "kaaka", "meaning": "uncle",
     "col_a": "#1a237e", "col_b": "#283593",
     "prompt": "one friendly middle aged Indian uncle smiling"},
    {"form": "कि", "slug": "ki-word",  "word": "किताब", "pron": "kitaab", "meaning": "book",
     "col_a": "#1b5e20", "col_b": "#2e7d32",
     "prompt": "one colorful closed children's book, no text visible"},
    {"form": "की", "slug": "kee-word", "word": "कीड़ा", "pron": "keeda", "meaning": "insect",
     "col_a": "#33691e", "col_b": "#558b2f",
     "prompt": "one clearly visible harmless insect on a green leaf, large enough for a child to recognize"},
    {"form": "कु", "slug": "ku-word",  "word": "कुत्ता", "pron": "kutta", "meaning": "dog",
     "col_a": "#bf360c", "col_b": "#d84315",
     "prompt": "one friendly dog sitting, full body visible"},
    {"form": "कू", "slug": "koo-word", "word": "कूलर", "pron": "cooler", "meaning": "air cooler",
     "col_a": "#006064", "col_b": "#00838f",
     "prompt": "one Indian room air cooler appliance, front view"},
    {"form": "के", "slug": "ke-word",  "word": "केला", "pron": "kela", "meaning": "banana",
     "col_a": "#f9a825", "col_b": "#f57f17",
     "prompt": "one bunch of yellow bananas"},
    {"form": "कै", "slug": "kai-word", "word": "कैंची", "pron": "kainchi", "meaning": "scissors",
     "col_a": "#37474f", "col_b": "#546e7a",
     "prompt": "one pair of child-safe scissors with red handle"},
    {"form": "को", "slug": "ko-word",  "word": "कोयल", "pron": "koyal", "meaning": "cuckoo bird",
     "col_a": "#1a237e", "col_b": "#4527a0",
     "prompt": "one black cuckoo bird sitting clearly on a branch"},
    {"form": "कौ", "slug": "kau-word", "word": "कौवा", "pron": "kauwa", "meaning": "crow",
     "col_a": "#212121", "col_b": "#424242",
     "prompt": "one black crow sitting clearly on a wall"},
    {"form": "कं", "slug": "kan-word", "word": "कंघी", "pron": "kanghi", "meaning": "comb",
     "col_a": "#880e4f", "col_b": "#ad1457",
     "prompt": "one simple colorful hair comb"},
    {"form": "कः", "slug": "kah-word", "word": "कहानी", "pron": "kahaani", "meaning": "story",
     "col_a": "#4a148c", "col_b": "#6a1b9a",
     "prompt": "one child reading a picture storybook, book has no readable text"},
]

KHA_WORDS = [
    {"form": "ख",  "slug": "kha-word",  "word": "खरगोश", "pron": "khargosh", "meaning": "rabbit",
     "col_a": "#c0392b", "col_b": "#4527a0",
     "prompt": "one white fluffy rabbit sitting clearly, full body visible"},
    {"form": "खा", "slug": "khaa-word", "word": "खाना", "pron": "khaana", "meaning": "food / meal",
     "col_a": "#e67e22", "col_b": "#c0392b",
     "prompt": "one Indian thali plate with simple home food: rice, dal, roti, sabzi"},
    {"form": "खि", "slug": "khi-word",  "word": "खिड़की", "pron": "khidki", "meaning": "window",
     "col_a": "#0d6efd", "col_b": "#1a237e",
     "prompt": "one wooden window with open shutters on a simple wall"},
    {"form": "खी", "slug": "khee-word", "word": "खीर", "pron": "kheer", "meaning": "rice pudding",
     "col_a": "#f9a825", "col_b": "#bf360c",
     "prompt": "one small bowl of Indian kheer rice pudding garnished with raisins"},
    {"form": "खु", "slug": "khu-word",  "word": "खुशी", "pron": "khushi", "meaning": "happiness",
     "col_a": "#ff6f00", "col_b": "#e65100",
     "prompt": "one happy smiling Indian child face, joyful expression, head and shoulders"},
    {"form": "खू", "slug": "khoo-word", "word": "खूंटी", "pron": "khoonti", "meaning": "wall hook",
     "col_a": "#37474f", "col_b": "#1a237e",
     "prompt": "one simple metal wall hook with a single coat hanging on it"},
    {"form": "खे", "slug": "khe-word",  "word": "खेल", "pron": "khel", "meaning": "game / play",
     "col_a": "#1b5e20", "col_b": "#2e7d32",
     "prompt": "one cricket bat and ball lying on grass, Indian style"},
    {"form": "खै", "slug": "khai-word", "word": "खैर", "pron": "khair", "meaning": "well-being",
     "col_a": "#006064", "col_b": "#00838f",
     "prompt": "one bunch of green leaves and a small clay diya symbolising blessing"},
    {"form": "खो", "slug": "kho-word",  "word": "खोपड़ा", "pron": "khopra", "meaning": "coconut",
     "col_a": "#4e342e", "col_b": "#6d4c41",
     "prompt": "one brown coconut, half cut showing white kernel inside"},
    {"form": "खौ", "slug": "khau-word", "word": "खौलना", "pron": "khaulna", "meaning": "boiling water",
     "col_a": "#b71c1c", "col_b": "#d84315",
     "prompt": "one steel pot on a stove with water boiling and steam rising clearly"},
    {"form": "खं", "slug": "khan-word", "word": "खंभा", "pron": "khambha", "meaning": "pillar / pole",
     "col_a": "#37474f", "col_b": "#546e7a",
     "prompt": "one tall stone pillar standing alone on a flat ground"},
    {"form": "खः", "slug": "khah-word", "word": "खटाई", "pron": "khataai", "meaning": "sour pickle",
     "col_a": "#827717", "col_b": "#9e9d24",
     "prompt": "one small bowl of Indian mango pickle, achaar, with oil visible"},
]

GA_WORDS = [
    {"form": "ग",  "slug": "ga-word",  "word": "गमला", "pron": "gamla", "meaning": "flower pot",
     "col_a": "#1b5e20", "col_b": "#2e7d32",
     "prompt": "one terracotta flower pot with a small green plant"},
    {"form": "गा", "slug": "gaa-word", "word": "गाय", "pron": "gaay", "meaning": "cow",
     "col_a": "#ff6f00", "col_b": "#bf360c",
     "prompt": "one Indian cow standing sideways, full body visible, brown and white"},
    {"form": "गि", "slug": "gi-word",  "word": "गिलहरी", "pron": "gilahri", "meaning": "squirrel",
     "col_a": "#4e342e", "col_b": "#6d4c41",
     "prompt": "one small Indian striped squirrel sitting on a branch, full body visible"},
    {"form": "गी", "slug": "gee-word", "word": "गीत", "pron": "geet", "meaning": "song",
     "col_a": "#6a1b9a", "col_b": "#4527a0",
     "prompt": "one simple acoustic music note symbol on a soft background, no text"},
    {"form": "गु", "slug": "gu-word",  "word": "गुड़", "pron": "gud", "meaning": "jaggery",
     "col_a": "#bf360c", "col_b": "#8d6e63",
     "prompt": "one block of brown Indian jaggery, gud, on a wooden surface"},
    {"form": "गू", "slug": "goo-word", "word": "गूलर", "pron": "goolar", "meaning": "fig fruit",
     "col_a": "#2e7d32", "col_b": "#1b5e20",
     "prompt": "one cluster of small green and reddish gular figs hanging from a tree branch"},
    {"form": "गे", "slug": "ge-word",  "word": "गेंद", "pron": "gend", "meaning": "ball",
     "col_a": "#d84315", "col_b": "#e65100",
     "prompt": "one bright red rubber ball sitting on a plain surface"},
    {"form": "गै", "slug": "gai-word", "word": "गैस", "pron": "gais", "meaning": "cooking gas",
     "col_a": "#01579b", "col_b": "#0277bd",
     "prompt": "one Indian red LPG cooking gas cylinder, simple front view"},
    {"form": "गो", "slug": "go-word",  "word": "गोलगप्पा", "pron": "golgappa", "meaning": "puchka",
     "col_a": "#f9a825", "col_b": "#bf360c",
     "prompt": "a small plate of round golgappa puris, Indian street food"},
    {"form": "गौ", "slug": "gau-word", "word": "गौरैया", "pron": "gauraiya", "meaning": "sparrow",
     "col_a": "#4e342e", "col_b": "#8d6e63",
     "prompt": "one small Indian sparrow sitting on a branch, brown and grey"},
    {"form": "गं", "slug": "gan-word", "word": "गंगा", "pron": "ganga", "meaning": "Ganga river",
     "col_a": "#0277bd", "col_b": "#01579b",
     "prompt": "one calm wide river flowing between green banks, simple peaceful scene"},
    {"form": "गः", "slug": "gah-word", "word": "गहना", "pron": "gehna", "meaning": "jewellery",
     "col_a": "#b8860b", "col_b": "#996515",
     "prompt": "one gold Indian bangle on a soft cloth"},
]

GHA_WORDS = [
    {"form": "घ",  "slug": "gha-word",  "word": "घड़ी", "pron": "ghadi", "meaning": "clock / watch",
     "col_a": "#1a237e", "col_b": "#283593",
     "prompt": "one round wall clock with classic 12-hour face, no text"},
    {"form": "घा", "slug": "ghaa-word", "word": "घास", "pron": "ghaas", "meaning": "grass",
     "col_a": "#1b5e20", "col_b": "#2e7d32",
     "prompt": "a small patch of green fresh grass on the ground"},
    {"form": "घि", "slug": "ghi-word",  "word": "घिसना", "pron": "ghisna", "meaning": "rubbing / sharpening",
     "col_a": "#4e342e", "col_b": "#3e2723",
     "prompt": "one hand rubbing a stone on a plain surface, simple educational image"},
    {"form": "घी", "slug": "ghee-word", "word": "घी", "pron": "ghee", "meaning": "ghee / clarified butter",
     "col_a": "#f9a825", "col_b": "#bf360c",
     "prompt": "one small glass jar of golden Indian ghee, lid open"},
    {"form": "घु", "slug": "ghu-word",  "word": "घुटना", "pron": "ghutna", "meaning": "knee",
     "col_a": "#bf360c", "col_b": "#d84315",
     "prompt": "one Indian child's bent knee close-up, simple plain background"},
    {"form": "घू", "slug": "ghoo-word", "word": "घूमना", "pron": "ghoomna", "meaning": "to roam / spin",
     "col_a": "#6a1b9a", "col_b": "#4527a0",
     "prompt": "one colourful spinning top toy mid-spin on a plain surface"},
    {"form": "घे", "slug": "ghe-word",  "word": "घेरा", "pron": "ghera", "meaning": "circle / ring",
     "col_a": "#d84315", "col_b": "#bf360c",
     "prompt": "one simple hand-drawn red circle ring on a white sheet of paper"},
    {"form": "घै", "slug": "ghai-word", "word": "घैल", "pron": "ghail", "meaning": "wound",
     "col_a": "#b71c1c", "col_b": "#c62828",
     "prompt": "one child's arm with a small bandage plaster on it, friendly safe image"},
    {"form": "घो", "slug": "gho-word",  "word": "घोड़ा", "pron": "ghoda", "meaning": "horse",
     "col_a": "#4e342e", "col_b": "#6d4c41",
     "prompt": "one brown horse standing sideways, full body visible"},
    {"form": "घौ", "slug": "ghau-word", "word": "घौंसला", "pron": "ghaunsla", "meaning": "nest",
     "col_a": "#8d6e63", "col_b": "#5d4037",
     "prompt": "one small bird's nest with three small eggs inside, sitting on a tree branch"},
    {"form": "घं", "slug": "ghan-word", "word": "घंटी", "pron": "ghanti", "meaning": "bell",
     "col_a": "#b8860b", "col_b": "#996515",
     "prompt": "one small brass Indian temple bell hanging from a chain"},
    {"form": "घः", "slug": "ghah-word", "word": "घर", "pron": "ghar", "meaning": "house / home",
     "col_a": "#283593", "col_b": "#1a237e",
     "prompt": "one simple Indian house with a sloping red roof, two windows, and one door"},
]

NGA_WORDS = [
    # ङ is rarely used in word-initial position; words shown are common ones containing ङ
    {"form": "ङ",  "slug": "nga-word",  "word": "ङ", "pron": "nga", "meaning": "rare nasal sound",
     "col_a": "#37474f", "col_b": "#546e7a",
     "prompt": "one large clear Devanagari letter ङ painted in black on a plain white wall, photograph style"},
    {"form": "ंक", "slug": "nga-anka-word",  "word": "अंक", "pron": "ank", "meaning": "number",
     "col_a": "#1a237e", "col_b": "#283593",
     "prompt": "the numeral 5 written large on a small chalkboard, no other text"},
    {"form": "ंग", "slug": "nga-anga-word",  "word": "अंगूठा", "pron": "angootha", "meaning": "thumb",
     "col_a": "#bf360c", "col_b": "#d84315",
     "prompt": "one Indian child showing a thumbs-up gesture, hand close-up, plain background"},
    {"form": "ंघ", "slug": "nga-singh-word", "word": "सिंह", "pron": "singh", "meaning": "lion",
     "col_a": "#e65100", "col_b": "#bf360c",
     "prompt": "one Indian lion sitting upright, mane visible, full body, plain background"},
    {"form": "ंक", "slug": "nga-pankha-word", "word": "पंखा", "pron": "pankha", "meaning": "fan",
     "col_a": "#0277bd", "col_b": "#01579b",
     "prompt": "one Indian ceiling fan with three blades, front view, white background"},
]


# ── Helpers ────────────────────────────────────────────────────────────────────
def _hex(h: str) -> tuple:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def _blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _make_numeral_one(col: tuple) -> Image.Image:
    """Render a large coloured '1' on a light background (for एक / one card)."""
    img  = Image.new("RGB", (1024, 1024), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype(FONT_LAT, 900)
    except Exception:
        f = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), "1", font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (1024 - tw) // 2 - bbox[0]   # subtract left bearing for true horizontal centre
    ty = (1024 - th) // 2 - bbox[1]   # subtract top bearing for true vertical centre
    draw.text((tx, ty), "1", font=f, fill=col)
    return img


def _load_fonts(big_size=134):
    try:
        big   = ImageFont.truetype(FONT_DEV, big_size)
        word  = ImageFont.truetype(FONT_DEV, 78)
        pron  = ImageFont.truetype(FONT_LAT, 50)   # pronunciation in Latin script
        mean  = ImageFont.truetype(FONT_LAT, 42)
    except Exception:
        big = word = pron = mean = ImageFont.load_default()
    return big, word, pron, mean


def _dalle_image(prompt: str, client) -> Image.Image:
    """Generate a realistic image using gpt-image-1 (dall-e-3 is retired)."""
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=f"{REALISTIC_STYLE} Subject: {prompt}.",
        n=1,
        size="1024x1024",
        quality="high",
    )
    import base64
    data = base64.b64decode(resp.data[0].b64_json)
    return Image.open(io.BytesIO(data)).convert("RGB")


def render_word_card(entry: dict, illus: Image.Image) -> Image.Image:
    col_a = _hex(entry["col_a"])
    col_b = _hex(entry["col_b"])

    TOP_H    = 162    # colored band at top (letter)
    BOT_H    = 340    # colored band at bottom (word + pron + meaning)
    IMG_H    = CARD_H - TOP_H - BOT_H  # ~618px image zone

    card = Image.new("RGB", (CARD_W, CARD_H), color=(255, 255, 255))
    draw = ImageDraw.Draw(card)

    # Gradient top band
    for y in range(TOP_H):
        draw.line([(0, y), (CARD_W, y)], fill=_blend(col_a, col_b, y / TOP_H))

    # Gradient bottom band
    for y in range(CARD_H - BOT_H, CARD_H):
        t = (y - (CARD_H - BOT_H)) / BOT_H
        draw.line([(0, y), (CARD_W, y)], fill=_blend(col_a, col_b, t))

    # Image zone: light neutral background
    draw.rectangle([0, TOP_H, CARD_W, CARD_H - BOT_H], fill=(248, 248, 252))

    big, word_f, pron_f, mean_f = _load_fonts(big_size=118)

    # Letter form — top band, vertically centered
    fw = draw.textlength(entry["form"], font=big)
    fx = (CARD_W - fw) / 2
    fy = (TOP_H - 118) / 2
    draw.text((fx, max(4, fy)), entry["form"], font=big, fill="white")

    # DALL-E / PIL illustration — fills the image zone
    img_size = min(IMG_H - 8, CARD_W - 8)
    illus_sq = illus.resize((img_size, img_size), Image.LANCZOS)
    ix = (CARD_W - img_size) // 2
    iy = TOP_H + (IMG_H - img_size) // 2
    card.paste(illus_sq, (ix, iy))

    # ── 3-row footer (Hindi word / pronunciation / English meaning) ────────
    bot_y = CARD_H - BOT_H          # top of footer band

    # Row 1: Hindi word — centered
    ww  = draw.textlength(entry["word"], font=word_f)
    wx  = (CARD_W - ww) / 2
    wy  = bot_y + 28
    draw.text((wx, wy), entry["word"], font=word_f, fill="white")

    # Row 2: Pronunciation — centered, bright yellow so kids can read easily
    pron_text = entry.get("pron", "")
    if pron_text:
        pw  = draw.textlength(pron_text, font=pron_f)
        px  = (CARD_W - pw) / 2
        py  = wy + 96
        draw.text((px, py), pron_text, font=pron_f, fill=(255, 240, 120))

    # Row 3: English meaning — centered, light mint
    mw  = draw.textlength(entry["meaning"], font=mean_f)
    mx  = (CARD_W - mw) / 2
    my  = wy + 96 + 66
    draw.text((mx, my), entry["meaning"], font=mean_f, fill=(200, 240, 210))

    return card


# ── Main ───────────────────────────────────────────────────────────────────────
def _load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def generate_set(words: list, out_dir: pathlib.Path, force: bool = False) -> None:
    import openai
    _load_env()
    client = openai.OpenAI()
    out_dir.mkdir(parents=True, exist_ok=True)

    for entry in words:
        out_path = out_dir / f"{entry['slug']}.png"
        if out_path.exists() and not force:
            print(f"  [SKIP] {out_path.name} already exists")
            continue
        try:
            if entry.get("pil_one"):
                print(f"  [PIL-1] {entry['form']}  →  {entry['word']}  (numeral 1)")
                illus = _make_numeral_one(_hex(entry["col_a"]))
            else:
                print(f"  [DALL-E] {entry['form']}  →  {entry['word']}  ({entry['meaning']})")
                illus = _dalle_image(entry["prompt"], client)
        except Exception as e:
            print(f"    ERROR: {e}")
            illus = Image.new("RGB", (1024, 1024), color=(200, 200, 200))
        card = render_word_card(entry, illus)
        card.save(str(out_path))
        print(f"    → saved {out_path.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set",
                    choices=["swar", "ka", "kha", "ga", "gha", "nga",
                             "ka-varga", "all"],
                    default="all")
    ap.add_argument("--force", action="store_true", help="Regenerate existing cards")
    args = ap.parse_args()

    sel = args.set
    if sel in ("swar", "all"):
        print("Generating swar word cards…")
        generate_set(SWAR_WORDS, OUT_SWAR, force=args.force)
    if sel in ("ka", "ka-varga", "all"):
        print("Generating ka barakhadi word cards…")
        generate_set(KA_WORDS, OUT_KA, force=args.force)
    if sel in ("kha", "ka-varga", "all"):
        print("Generating kha barakhadi word cards…")
        generate_set(KHA_WORDS, OUT_KHA, force=args.force)
    if sel in ("ga", "ka-varga", "all"):
        print("Generating ga barakhadi word cards…")
        generate_set(GA_WORDS, OUT_GA, force=args.force)
    if sel in ("gha", "ka-varga", "all"):
        print("Generating gha barakhadi word cards…")
        generate_set(GHA_WORDS, OUT_GHA, force=args.force)
    if sel in ("nga", "ka-varga", "all"):
        print("Generating nga barakhadi word cards…")
        generate_set(NGA_WORDS, OUT_NGA, force=args.force)

    print("Done.")


if __name__ == "__main__":
    main()
