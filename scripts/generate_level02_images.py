"""
Generate DALL-E 3 images for Level 2: Daily Help
Run: .venv/bin/python scripts/generate_level02_images.py

Images are saved to content/assets/scenes/  (same folder as Level 1)
Script skips files that already exist — safe to re-run.
Rate limit: 5 images/min for Tier 1 → 13-second sleep between requests.
"""

import os, time, pathlib, urllib.request, json

# ─── load .env manually (no dotenv dependency) ──────────────────────────────
def load_env(path=".env"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No .env file found at {path}")
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ─── output dirs ────────────────────────────────────────────────────────────
SCENES_DIR = pathlib.Path("content/assets/scenes")
SCENES_DIR.mkdir(parents=True, exist_ok=True)

# ─── image definitions ──────────────────────────────────────────────────────
# Format: (filename, size, prompt)
IMAGES = [
    # ── wide hero ─────────────────────────────────────────────────────────
    (
        "img-l2-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic illustration of daily Indian life transformed by AI assistance. "
        "Three vignettes side by side: left — a middle-aged Indian shopkeeper typing a WhatsApp message on his smartphone at a small mobile accessories shop, "
        "center — an Indian homemaker holding a handwritten grocery list with a phone showing a budget table, "
        "right — a teenage Indian student sitting at a desk with textbooks and practice questions on his phone screen. "
        "Each person looks satisfied and confident. Warm lighting, vibrant Indian colours, flat-illustration style with depth, "
        "soft teal and amber colour palette. No text overlays."
    ),

    # ── ravi at shop counter on phone ─────────────────────────────────────
    (
        "img-l2-s02-ravi-phone.jpg",
        "1024x1024",
        "Close-up illustration of a middle-aged Indian man, shopkeeper, sitting behind a cluttered mobile shop counter "
        "in Hyderabad. He is typing on a basic Android smartphone, frowning slightly in concentration. "
        "Glass display cases with phones behind him. A few unsold vegetables in a bag on the counter suggesting he also sells produce. "
        "Natural morning light, warm tones. Flat digital illustration with Indian market atmosphere. No text on screen."
    ),

    # ── whatsapp result on phone ──────────────────────────────────────────
    (
        "img-l2-s03-supplier-reply.jpg",
        "1024x1024",
        "Illustration of a happy middle-aged Indian shopkeeper (Ravi) at his small shop counter, "
        "holding up his Android smartphone with a satisfied expression. He is smiling and giving a thumbs up. "
        "The phone screen shows a WhatsApp chat with a green background — the conversation is brief and professional-looking. "
        "Warm shop lighting, colourful Indian shop background with mobile accessories on the wall. "
        "Flat digital illustration, celebratory feel. No readable text on phone screen."
    ),

    # ── priya with grocery list ───────────────────────────────────────────
    (
        "img-l2-s04-priya-grocery.jpg",
        "1024x1024",
        "Illustration of a cheerful Indian homemaker (Priya) sitting at a kitchen table, "
        "holding a handwritten grocery list notepad and a smartphone. "
        "On the phone screen, a neat table/spreadsheet is visible showing grocery items and prices in Indian rupees. "
        "Kitchen background with spice jars, steel vessels, and a cloth calendar on the wall. "
        "Natural daylight, warm yellows and greens, flat digital illustration. No readable text on phone."
    ),

    # ── busy Indian market / grocery shopping ─────────────────────────────
    (
        "img-l2-s05-market-scene.jpg",
        "1792x1024",
        "Wide illustration of a vibrant Indian vegetable market — sabzi mandi — with colourful stalls displaying "
        "tomatoes, onions, spinach, brinjal, bananas, and fresh coriander. "
        "An Indian woman shopper (Priya) walks through the market holding her phone showing a list, confidently picking vegetables. "
        "Market vendors in the background. Bright mid-morning sunlight, rich greens and oranges, "
        "lively Indian market atmosphere. Flat-illustration style with depth and warmth. No text overlays."
    ),

    # ── rahul studying with practice questions ────────────────────────────
    (
        "img-l2-s06-rahul-exam.jpg",
        "1024x1024",
        "Illustration of a teenage Indian student (Rahul, 14-15 years old) studying late at night at a wooden desk. "
        "Books open in front of him — Science textbook with atom diagrams visible. "
        "He is reading from his smartphone which shows a list of practice questions in a clean chat interface. "
        "Small desk lamp, wall with a periodic table poster, notes and pencils scattered. "
        "Slightly tired but focused expression. Warm lamplight, flat digital illustration. No readable text on phone."
    ),

    # ── prompt tips illustration ──────────────────────────────────────────
    (
        "img-l2-s07-prompt-tips.jpg",
        "1792x1024",
        "Wide flat-design infographic illustration showing the concept of 'better prompts = better answers'. "
        "Two smartphone screens side by side: left phone has a vague short message bubble (labelled 'vague prompt'), "
        "right phone has a longer detailed message with bullet points (labelled 'specific prompt'). "
        "Between them an arrow and a star/sparkle symbol. Surrounding icons: a lightbulb, a speech bubble, a format list icon, and a refresh/iterate icon. "
        "Clean blue and teal colour palette on a light cream background. No actual text words — purely visual icons and symbols."
    ),

    # ── person at desk writing formal letter ─────────────────────────────
    (
        "img-l2-s08-complaint-letter.jpg",
        "1024x1024",
        "Illustration of an Indian adult (male, 35-40 years old) sitting at a home desk, holding a printed formal letter. "
        "His smartphone on the desk shows an AI chat interface where the letter was generated. "
        "He looks relieved and satisfied. Home office setting — simple wooden desk, one framed family photo, "
        "a cup of tea. An official-looking envelope on the desk addressed to an electricity board. "
        "Warm afternoon light, flat digital illustration. No readable text on letter or phone."
    ),

    # ── person practising AI on phone in daily life ───────────────────────
    (
        "img-l2-s09-practice-arena.jpg",
        "1024x1024",
        "Illustration of a young Indian adult (25-30 years old) sitting on a home sofa, enthusiastically typing on their smartphone. "
        "They look excited and curious, leaning forward. The phone screen shows a chat interface — a clean AI assistant conversation. "
        "Casual home environment with a colourful Indian cushion, a small plant, and afternoon sunlight from a window. "
        "Flat digital illustration, energetic and encouraging mood. No readable text on phone screen."
    ),

    # ── level 2 completion celebration ───────────────────────────────────
    (
        "img-l2-s10-celebration.jpg",
        "1792x1024",
        "Wide celebratory illustration showing the three main characters — a middle-aged Indian shopkeeper (Ravi), "
        "an Indian homemaker (Priya), and a teenage Indian student (Rahul) — standing together and celebrating with raised arms and big smiles. "
        "Each holds their smartphone. Digital confetti, stars, and certificate/badge icons float around them. "
        "A blue glowing AI companion sphere floats above them. "
        "Bright, joyful, colourful Indian celebration scene with firework sparkles. "
        "Flat digital illustration, warm and triumphant mood. No text overlays."
    ),
]

# ─── generate ────────────────────────────────────────────────────────────────
RATE_LIMIT_SLEEP = 13  # seconds — Tier 1: 5 images/min

def download(url, dest):
    urllib.request.urlretrieve(url, dest)

def generate():
    total = len(IMAGES)
    generated = 0
    skipped   = 0

    print(f"\n🎨  Level 2 image generation — {total} images\n{'─'*50}")

    for i, (filename, size, prompt) in enumerate(IMAGES, 1):
        dest = SCENES_DIR / filename
        if dest.exists():
            print(f"[{i}/{total}]  SKIP  {filename}  (already exists)")
            skipped += 1
            continue

        print(f"[{i}/{total}]  GEN   {filename}  ({size}) ...", end="", flush=True)
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            url = response.data[0].url
            download(url, dest)
            size_kb = dest.stat().st_size // 1024
            print(f"  ✅  {size_kb} KB")
            generated += 1
        except Exception as e:
            print(f"  ❌  ERROR: {e}")

        if i < total:
            print(f"    ⏱  Waiting {RATE_LIMIT_SLEEP}s (rate limit) …")
            time.sleep(RATE_LIMIT_SLEEP)

    print(f"\n{'─'*50}")
    print(f"✅  Done.  Generated: {generated}  |  Skipped: {skipped}  |  Total: {total}\n")

if __name__ == "__main__":
    generate()
