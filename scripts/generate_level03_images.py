"""
Generate DALL-E 3 images for Level 3: Smart Basics
Run: .venv/bin/python scripts/generate_level03_images.py

Images are saved to content/assets/scenes/
Script skips files that already exist — safe to re-run.
Rate limit: 5 images/min for Tier 1 → 13-second sleep between requests.
"""

import os, time, pathlib, urllib.request

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

# ─── output dir ─────────────────────────────────────────────────────────────
SCENES_DIR = pathlib.Path("content/assets/scenes")
SCENES_DIR.mkdir(parents=True, exist_ok=True)

# ─── image definitions ──────────────────────────────────────────────────────
# Format: (filename, size, prompt)
IMAGES = [

    # ── wide hero — critical AI thinking ─────────────────────────────────
    (
        "img-l3-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic flat illustration representing 'using AI wisely, not just often'. "
        "Three vignettes side by side: "
        "left — a young Indian male student in Hyderabad holding a phone with a fact-check checklist visible, "
        "center — an Indian teacher in Vizag pointing at a numbered step-by-step list on her phone with students behind her, "
        "right — a middle-aged Indian shop owner in Vijayawada holding two phone screens side by side comparing results. "
        "Emerald green and warm amber colour palette, deep forest green backgrounds, modern flat illustration style with depth. "
        "Confident and thoughtful mood. No text overlays."
    ),

    # ── arjun — the wrong trust mistake ──────────────────────────────────
    (
        "img-l3-s02-arjun-mistake.jpg",
        "1024x1024",
        "Illustration of a worried young Indian male student (Arjun, early 20s) in Hyderabad, sitting on a bed, "
        "looking at his smartphone with a concerned expression. "
        "He has just realised the AI health information he shared with his grandmother was wrong. "
        "A blurred elderly Indian woman is visible in the background. "
        "The phone screen shows an AI chat interface — not readable. "
        "Muted warm tones with a slightly anxious atmosphere. Flat digital illustration, "
        "simple home bedroom setting with a single bed, a poster on the wall, and books on a shelf. No readable text."
    ),

    # ── meena — teacher in classroom, fact-check moment ──────────────────
    (
        "img-l3-s03-meena-factcheck.jpg",
        "1024x1024",
        "Illustration of an Indian female teacher (Meena, mid-30s) standing in a school classroom in Vizag, "
        "holding a smartphone and looking thoughtful. "
        "She is showing the phone screen to a small group of students seated in front of her. "
        "The classroom has a blackboard behind her with chalked formulas, and simple wooden desks. "
        "The phone screen shows a web search interface — not readable. "
        "Afternoon classroom light, warm greens and ochre tones, flat illustration. "
        "She looks careful and responsible, demonstrating how to verify information. No readable text."
    ),

    # ── rahul — step-by-step prompt on phone ─────────────────────────────
    (
        "img-l3-s04-rahul-steps.jpg",
        "1024x1024",
        "Illustration of a young Indian engineering student (Rahul, early 20s) in Guntur, "
        "sitting at a hostel room desk, reading from his smartphone with a focused and relieved expression. "
        "The phone screen shows a numbered list — steps 1 through 5 are visible as blocks, not readable. "
        "Open textbooks and notes around him. A college pennant on the wall. "
        "Desk lamp light, flat digital illustration, academic setting. "
        "He is taking notes in a notebook, clearly following the step-by-step guidance. No readable text on screen."
    ),

    # ── priya — tone rewrite, HR office ──────────────────────────────────
    (
        "img-l3-s05-priya-tone.jpg",
        "1024x1024",
        "Illustration of a professional Indian woman (Priya, HR executive, late 20s) at a clean office desk in Hyderabad. "
        "She is holding her smartphone and smiling with satisfaction. "
        "Two versions of a message are visible on a split phone screen — left side has a red-tinted cold-looking text, "
        "right side has a warm green-tinted friendly-looking text. She is pointing to the right (warmer) version. "
        "Modern office environment with a laptop, a small plant, and corporate stationery. "
        "Bright professional lighting, emerald and amber tones, flat digital illustration. No readable text."
    ),

    # ── kiran — comparing two answers at his shop ────────────────────────
    (
        "img-l3-s06-kiran-compare.jpg",
        "1024x1024",
        "Illustration of a middle-aged Indian shop owner (Kiran) standing in his small electronics and payment services shop "
        "in Vijayawada. He is holding two smartphones side by side, one in each hand, comparing the screens. "
        "He looks thoughtful and analytical, weighing the options. "
        "Shop shelves behind him have mobile phone boxes and accessories. "
        "A PhonePe QR code sticker is visible near the counter. "
        "Warm shop lighting, flat digital illustration, confident decision-making mood. No readable text on phone screens."
    ),

    # ── prompt library — saving prompts concept ───────────────────────────
    (
        "img-l3-s07-prompt-library.jpg",
        "1792x1024",
        "Wide flat-design illustration representing the concept of a personal prompt library. "
        "Centre: an Indian person's hand holding a smartphone with a Notes app open showing 5 labeled entries "
        "(represented as coloured blocks, not readable text). "
        "Surrounding the phone: icons for copy-paste, a bookmark, a recycling/reuse symbol, a lightbulb, and a lock/save icon. "
        "To the left: a small illustration of someone typing a prompt. "
        "To the right: a small illustration of someone getting a great result with a gold star. "
        "Emerald green and amber colour palette on a cream background. Clean, minimal, instructional mood. No actual text words."
    ),

    # ── practice arena — person trying on phone ───────────────────────────
    (
        "img-l3-s08-practice.jpg",
        "1024x1024",
        "Illustration of a young Indian adult (25 years old, gender-neutral presentation) "
        "sitting cross-legged on a colourful floor cushion, enthusiastically using a smartphone. "
        "They are clearly practising something — leaning forward with a focused and curious expression. "
        "A small notebook beside them with doodles. "
        "Cozy Indian home environment — a window with afternoon sunlight, a rangoli pattern on the floor, "
        "plants in clay pots. The phone screen shows an active AI chat — icons visible, no readable text. "
        "Emerald greens and warm yellows, flat digital illustration, energetic and encouraging mood."
    ),

    # ── level 3 completion — 5 characters celebrating ────────────────────
    (
        "img-l3-s09-celebration.jpg",
        "1792x1024",
        "Wide celebratory illustration showing five Indian characters standing together and celebrating: "
        "a young male student (Arjun, Hyderabad), a female teacher (Meena, Vizag), "
        "a male engineering student (Rahul, Guntur), a professional woman (Priya, Hyderabad), "
        "and a middle-aged male shop owner (Kiran, Vijayawada). "
        "Each holds a smartphone showing a green certificate or badge. They have raised arms and big smiles. "
        "Digital confetti in emerald green and amber, sparkles, and small brain/lightbulb icons floating around them. "
        "A glowing AI companion orb in emerald green floats above. "
        "Bright, joyful, diverse South Indian crowd feel, flat digital illustration. No text overlays."
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

    print(f"\n🎨  Level 3 image generation — {total} images\n{'─'*50}")

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
