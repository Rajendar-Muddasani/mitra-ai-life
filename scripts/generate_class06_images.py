"""
Generate Class 6 student lesson images using DALL-E 3.
Run:  source .env && .venv/bin/python scripts/generate_class06_images.py

- Reads OPENAI_API_KEY from .env
- Saves 3 scene images to content/assets/scenes/
- Skips files that already exist (safe to re-run)
- Logs cost estimate at the end
"""
import os
import time
import urllib.request
from pathlib import Path

from openai import OpenAI

# ── load .env manually ────────────────────────────────────────────────────
def load_env(path=".env"):
    env_path = Path(__file__).resolve().parents[1] / path
    if not env_path.exists():
        raise FileNotFoundError(f".env not found at {env_path}")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

load_env()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SCENES = Path(__file__).resolve().parents[1] / "content" / "assets" / "scenes"
SCENES.mkdir(parents=True, exist_ok=True)

# Style consistent with rest of site — vibrant Indian cartoon
STYLE = (
    "Vibrant cartoon illustration style, Indian school setting, bold black outlines, "
    "warm and bright colours, flat 2D art, expressive faces, family-friendly, clean."
)

IMAGES = [
    (
        "img-c6-01-computer-learning.jpg",
        "A friendly cartoon computer on a school desk surrounded by thousands of tiny floating images — "
        "photos of cats, dogs, fruits, cars, and faces — all being absorbed into the screen with small glowing arrows. "
        "A speech bubble from the computer says 'I am learning!'. "
        "Bright Indian classroom background with colourful charts on the walls.",
    ),
    (
        "img-c6-02-student-checking.jpg",
        "An Indian girl student, age 11, in school uniform, sitting at a desk. "
        "She is looking at her phone screen showing an AI chatbot answer, "
        "and at the same time checking the same information in her open science textbook beside the phone. "
        "Her expression is thoughtful and careful. Pencil in her hand, ready to write. "
        "Warm Indian home study table, afternoon light from window.",
    ),
    (
        "img-c6-03-student-ai-tablet.jpg",
        "An Indian boy student, age 11, in school uniform sitting at a wooden study table. "
        "He is holding a tablet and chatting with an AI assistant. "
        "His science notebook is open beside him with handwritten notes. "
        "He looks curious and happy. A small backpack hangs on the chair. "
        "Colourful Indian home background.",
    ),
]


def generate(filename: str, prompt: str):
    out_path = SCENES / filename
    if out_path.exists():
        print(f"  SKIP  {filename}  (already exists)")
        return

    full_prompt = f"{prompt}  {STYLE}"
    print(f"  GEN   {filename} ...", end="", flush=True)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        url = response.data[0].url
        urllib.request.urlretrieve(url, out_path)
        print(f" saved ({out_path.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f" ERROR: {exc}")

    # DALL-E 3 rate limit: 5 images/min on tier 1
    time.sleep(13)


if __name__ == "__main__":
    print(f"Generating {len(IMAGES)} Class 6 scene images...\n")
    for fname, prompt in IMAGES:
        generate(fname, prompt)
    print(f"\nDone. Estimated cost: ~${len(IMAGES) * 0.04:.2f} USD")
    print(f"Files saved to: {SCENES}")
