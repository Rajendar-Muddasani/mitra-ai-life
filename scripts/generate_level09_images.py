"""
Level 9 Scene Image Generator — AI for Income
Generates 8 DALL-E 3 images for level-09-ai-for-income
Saves to content/assets/scenes/ (gitignored, deployed to S3 via deploy_s3.py)

Run: .venv/bin/python scripts/generate_level09_images.py
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
        "img-l9-s01-hero.jpg",
        "Wide cinematic hero shot: a young Indian woman in her mid-20s sitting on a simple home "
        "desk in Warangal, Telangana. She types on her phone with confidence. A glowing teal and "
        "emerald green aura surrounds a floating UI showing income notifications — UPI payment alerts, "
        "client messages, rupee amounts. Modern, aspirational, photorealistic. "
        "Tagline mood: Your AI Skills = Real Income. No text overlays.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s02-kavya-gig.jpg",
        "Young Indian woman in her mid-20s (Kavya) sitting across a small shop counter "
        "from a middle-aged saree shop owner in Warangal. Kavya shows the shop owner "
        "AI-generated product descriptions on her phone screen. The shop owner looks impressed "
        "and pleased. Sarees visible on racks behind the counter. Natural daylight, warm tones. "
        "Photorealistic. Professional yet approachable atmosphere.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s03-srinivas-clients.jpg",
        "Indian man in his late 30s (Srinivas), professional demeanour, sitting at a home desk "
        "on a weekend morning in Hyderabad. Laptop screen shows a content dashboard with three "
        "client tiles — a dental clinic, a restaurant, a tutoring centre — each with social media "
        "post drafts created by AI. Coffee cup nearby. Calm, organised, side-hustle energy. "
        "Teal accent colours. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s04-padma-youtube.jpg",
        "Indian homemaker in her mid-40s (Padma) in a bright Vijayawada kitchen. "
        "She stands at a counter with traditional Telugu food dishes laid out beautifully — "
        "pesarattu, gongura pickle, pulihora. A phone on a small tripod records her. "
        "On a second phone nearby, an AI-generated Telugu video script is visible. "
        "Warm kitchen light, authentic domestic setting. Joyful, confident expression. "
        "Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s05-raju-studio.jpg",
        "Young Indian man in his late 20s (Raju) in a small photo studio in Nizamabad. "
        "Photography backdrops and ring lights visible. He shows a client — a small business owner — "
        "a printed sheet with AI-written photo captions and a WhatsApp promotional message. "
        "Client looks happy and surprised at the added value. Professional yet friendly setting. "
        "Photorealistic, warm studio light.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s06-pricing.jpg",
        "Clean, bright infographic-style illustration of three pricing tiers for AI freelance work. "
        "Three stacked cards: bottom card shows per-piece pricing (₹50–₹200 per post), "
        "middle card shows monthly retainer (₹1,500–₹3,000/month), "
        "top card shows premium bundle (₹5,000+/month). "
        "Teal and emerald green palette, Indian rupee symbols, simple icons. "
        "Friendly, educational illustration. No client logos.",
        "natural",
        "1792x1024",
    ),
    (
        "img-l9-s07-practice.jpg",
        "A small group of young Indian adults — men and women — sitting together at a community "
        "learning space or co-working cafe in a Telangana town. Each person works on a phone or "
        "laptop, practising AI prompt writing for freelance work. Motivational energy. "
        "Teal and emerald colour accents in the space. Natural light, collaborative atmosphere. "
        "Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l9-s08-celebration.jpg",
        "Joyful celebration scene: four Indian characters — a young woman (Kavya), a professional "
        "man (Srinivas), a homemaker (Padma), and a studio owner (Raju) — standing together "
        "outdoors in a Telangana street. Each holds their phone showing UPI payment notifications "
        "with rupee amounts — their first freelance income earned with AI. "
        "Wide smiles, confetti, golden evening light. Photorealistic, vibrant.",
        "vivid",
        "1792x1024",
    ),
]

print(f"Generating {len(IMAGES)} images for Level 9: AI for Income\n")

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

print(f"\nDone! All Level 9 images saved to {DEST}")
print("Next: run .venv/bin/python scripts/deploy_s3.py to upload to S3")
