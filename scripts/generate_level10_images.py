"""
Level 10 Scene Image Generator — AI Safety & Society
Generates 8 DALL-E 3 images for level-10-ai-safety
Saves to content/assets/scenes/ (gitignored, deployed to S3 via deploy_s3.py)

Run: .venv/bin/python scripts/generate_level10_images.py
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
        "img-l10-s01-hero.jpg",
        "Wide cinematic hero shot: five young Indian adults — two women and three men — "
        "gathered closely together outdoors at dusk in Hyderabad, all looking at a shared "
        "phone screen with concern but confidence and determination. Deep indigo and violet "
        "sky behind them with city lights. A soft purple glow emanates from the screen. "
        "Mood: empowered, thoughtful, united. Tagline mood: Use AI Wisely. Stay Safe. "
        "No text overlays. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s02-deepfake.jpg",
        "Young Indian woman in her mid-20s (Kavya) holding her phone at arm's length, "
        "looking at a video on screen with a suspicious, sceptical expression. "
        "The phone screen shows a blurry political video with visible visual artifacts — "
        "slightly warped face edges, unnatural skin texture — subtle signs of a deepfake. "
        "Kavya's expression is thoughtful, not panicked. Indigo and violet accent lighting. "
        "Photorealistic, documentary style. No celebrities or real political figures.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s03-fact-check.jpg",
        "Indian man in his late 30s (Srinivas) at a laptop in a home office in Hyderabad, "
        "focused and determined. Browser has multiple tabs open — a news article, a fact-check "
        "website, a Wikipedia page. He has a notepad with handwritten notes. "
        "Purple and indigo accent colours in the room decor. "
        "Expression: careful, investigative, professional. Photorealistic, warm desk lamp light.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s04-voice-clone-scam.jpg",
        "Indian homemaker in her mid-40s (Padma) at home in Vijayawada, holding a phone to her "
        "ear with a worried expression. In the background, her adult daughter is clearly visible "
        "in the kitchen — safe and unbothered. The contrast shows the voice on the phone is NOT "
        "her daughter. Soft dramatic lighting, split composition: left side tense phone call, "
        "right side calm daughter. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s05-consent-privacy.jpg",
        "Young Indian man in his late 20s (Raju) at a small photo studio in Nizamabad, "
        "showing a printed poster to a client. In the background, a third person — the subject "
        "of the poster — stands with arms crossed looking uncomfortable and unhappy. "
        "Raju's expression shifts from proud to apologetic as he realises the problem. "
        "The scene conveys the concept of consent and privacy without being confrontational. "
        "Soft studio lighting. Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s06-meera-integrity.jpg",
        "Young Indian woman in her late teens (Meera, college student) sitting across a desk "
        "from a kind, middle-aged Indian female teacher in a college classroom in Hyderabad. "
        "The teacher returns an essay paper gently. Meera's expression is thoughtful and "
        "remorseful but not crushed — it is clearly a learning conversation, not punishment. "
        "Afternoon sunlight through classroom windows. Warm, mentoring atmosphere. "
        "Photorealistic.",
        "vivid",
        "1792x1024",
    ),
    (
        "img-l10-s07-5-rules.jpg",
        "Clean bright infographic illustration: a colourful pledge card with 5 rules of "
        "responsible AI use. Five rows, each with a simple icon and short text: "
        "1) shield icon — Verify Before You Share, "
        "2) speech bubble icon — Declare AI Help, "
        "3) heart icon — Never Harm or Deceive, "
        "4) lock icon — Protect Personal Data, "
        "5) people icon — Teach Someone Else. "
        "Deep purple and indigo palette with gold accents. Indian design aesthetic. "
        "Friendly, shareable visual. No photographs — pure illustration.",
        "natural",
        "1792x1024",
    ),
    (
        "img-l10-s08-celebration.jpg",
        "Joyful outdoor celebration in a Hyderabad street setting: all five Indian characters "
        "together — Kavya (young woman, 24), Srinivas (professional man, 38), Padma (homemaker, 45), "
        "Raju (studio owner, 27), and Meera (college student, 19). They hold certificates or phones "
        "showing level completion. Purple and gold confetti falls around them. "
        "Wide smiles, arms around each other, golden evening light. "
        "Mood: proud, accomplished, hopeful. Photorealistic, vibrant.",
        "vivid",
        "1792x1024",
    ),
]

print(f"Generating {len(IMAGES)} images for Level 10: AI Safety & Society\n")

for i, (filename, prompt, style, size) in enumerate(IMAGES, start=1):
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
            style=style,   # "vivid" or "natural"
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

print(f"\nDone! All Level 10 images saved to {DEST}")
print("Next: run .venv/bin/python scripts/deploy_s3.py to upload to S3")
