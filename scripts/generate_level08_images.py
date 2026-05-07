"""
Level 8 Scene Image Generator — AI for Small Business
Generates 8 DALL-E 3 images for level-08-ai-for-business
Saves to content/assets/scenes/ (gitignored, deployed to S3 via deploy_s3.py)

Run: .venv/bin/python scripts/generate_level08_images.py
"""

import os
import time
import urllib.request
from pathlib import Path

# ── Load .env ────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

DEST = Path(__file__).parent.parent / "content" / "assets" / "scenes"
DEST.mkdir(parents=True, exist_ok=True)

IMAGES = [
    (
        "img-l8-s01-hero.jpg",
        "Wide cinematic hero shot of a busy Indian mobile accessories shop in Hyderabad. "
        "A shopkeeper in his 30s stands proudly behind a glass counter filled with phone cases, "
        "earphones, and chargers. Colourful shop signage in Telugu and English. Warm evening light, "
        "street visible through open shutters. Vibrant, photorealistic, warm amber and orange tones. "
        "No text overlays.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s02-ravi-whatsapp.jpg",
        "Indian shopkeeper in his 30s sitting at a small desk in his mobile accessories shop in Hyderabad, "
        "typing on his smartphone. He is composing a WhatsApp promotional message. AI chat interface "
        "visible on a laptop screen beside him showing a professional Diwali offer message. "
        "Warm shop lighting, phone cases and accessories visible in background. "
        "Focused, optimistic expression. Photorealistic, warm tones.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s03-meena-tiffin.jpg",
        "Indian woman in her 40s in a home kitchen in a small town in Telangana. "
        "She is packaging tiffin boxes — idli, sambar, chutney visible. "
        "She looks at her phone screen with curiosity where an AI-generated menu with tagline is shown. "
        "Bright kitchen, steel containers, natural morning light. Hopeful expression. "
        "Photorealistic, warm domestic setting.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s04-suresh-complaint.jpg",
        "Indian tailor in his 40s in a small tailoring shop in Karimnagar. "
        "Fabric rolls and sewing machines in background. He holds his phone showing an angry WhatsApp message "
        "from a customer. He looks stressed but then looks at laptop screen where AI has drafted a calm, "
        "polite professional reply. Split-panel feeling — stress vs. relief. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s05-divya-instagram.jpg",
        "Young Indian woman in her mid-20s in Warangal, sitting cross-legged on a colourful durrie "
        "surrounded by neatly folded Pochampally silk sarees in orange, gold, and teal. "
        "She is typing on a laptop, Instagram feed visible on screen with saree photos and AI-generated captions. "
        "Cheerful, entrepreneurial energy. Natural daylight from window. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s06-ravi-calendar.jpg",
        "Same Indian shopkeeper from image 2, now at a small table with a notebook and laptop. "
        "Laptop screen shows a 4-week WhatsApp marketing calendar created by AI — weekly themes, "
        "festival offers, message timing. Shopkeeper looks impressed, making notes. "
        "Evening shop setting, warm light, organised and optimistic mood. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s07-practice.jpg",
        "Illustrated practice arena scene: four Indian small business owners — a shopkeeper, "
        "a home cook with tiffin boxes, a tailor, and a young woman with sarees — each at their "
        "own workstation with phones and laptops, all typing AI prompts. Connected by glowing "
        "digital lines suggesting a learning community. Warm amber and orange palette. "
        "Semi-realistic illustration style.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l8-s08-celebration.jpg",
        "Celebration scene: four happy Indian small business owners standing together outside "
        "their respective small businesses — a mobile shop, a tiffin kitchen door, a tailoring shop, "
        "an Instagram saree stall. Each holds their phone showing success — new customers, good reviews, "
        "more orders. Confetti, warm sunlight, joyful expressions. Photorealistic, vibrant.",
        "vivid",
        "1792x1024",
    ),
]

print(f"Generating {len(IMAGES)} images for Level 8: AI for Small Business\n")

for i, (filename, prompt, quality, size) in enumerate(IMAGES, start=1):
    dest_path = DEST / filename
    if dest_path.exists():
        print(f"[SKIP] {filename} already exists")
        continue

    print(f"[{i}/{len(IMAGES)}] Generating: {filename} ({size}) ...")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            style=quality,   # "vivid" or "natural"
            n=1,
        )
        url = response.data[0].url
        urllib.request.urlretrieve(url, dest_path)
        print(f"         Saved to {dest_path}")
    except Exception as e:
        print(f"         ERROR: {e}")

    if i < len(IMAGES):
        print(f"         Sleeping 13s (rate limit) ...")
        time.sleep(13)

print(f"\nDone! All Level 8 images saved to {DEST}")
print("Next: run .venv/bin/python scripts/deploy_s3.py to upload to S3")
