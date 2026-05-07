"""
Generate 7 Mitra character icon variations using DALL-E 3.
Icons are saved to content/assets/mitra-icons/
The user will select one preferred icon for the chatbot widget.
"""

import os
import time
import urllib.request
from pathlib import Path
from openai import OpenAI

# ── Load .env manually ────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = Path(__file__).parent.parent / "content" / "assets" / "mitra-icons"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ICONS = [
    {
        "filename": "mitra-icon-v1-kawaii.png",
        "size": "1024x1024",
        "style": "vivid",
        "prompt": (
            "A cute friendly AI mascot character named Mitra. Round glowing blue planet body "
            "with a cheerful face, big sparkly eyes, small white gloves, tiny legs. "
            "Surrounded by stars and sparkles. Kawaii cartoon style, clean white background, "
            "vibrant blue and teal colors. Suitable as a chatbot avatar icon."
        ),
    },
    {
        "filename": "mitra-icon-v2-professional.png",
        "size": "1024x1024",
        "style": "vivid",
        "prompt": (
            "A friendly but professional AI assistant mascot. Round glowing indigo-blue orb "
            "with a calm smiling face, soft gradient, subtle glow effect. Clean modern design, "
            "not childish. Looks like a trustworthy AI companion. White background. "
            "Suitable for a floating chatbot icon on an education website."
        ),
    },
    {
        "filename": "mitra-icon-v3-modern-flat.png",
        "size": "1024x1024",
        "style": "natural",
        "prompt": (
            "A modern flat-design AI mascot icon. Simple circle face with minimal features: "
            "small dot eyes, slight smile. Gradient from deep blue to cyan. Clean geometric "
            "design inspired by modern mobile app icons. No heavy outlines, smooth shapes. "
            "White background. Minimalist and professional, suitable as a website chatbot button."
        ),
    },
    {
        "filename": "mitra-icon-v4-indian-warmth.png",
        "size": "1024x1024",
        "style": "vivid",
        "prompt": (
            "A warm, inviting AI mascot character with Indian cultural warmth. Round friendly "
            "face, gentle smile, soft saffron and blue color palette inspired by Indian design. "
            "Approachable, not cartoonish. Looks like a kind helpful guide. "
            "Clean white background. Suitable as a floating chatbot avatar on an Indian education platform."
        ),
    },
    {
        "filename": "mitra-icon-v5-3d-bubble.png",
        "size": "1024x1024",
        "style": "vivid",
        "prompt": (
            "A glossy 3D rendered AI mascot bubble icon. Smooth glass-like sphere with a happy "
            "face reflection. Deep blue to electric cyan gradient. Subtle light reflection on top. "
            "Looks like a premium app icon. White background with soft shadow. "
            "Modern, clean, could work as a mobile app icon or chatbot avatar."
        ),
    },
    {
        "filename": "mitra-icon-v6-geometric-tech.png",
        "size": "1024x1024",
        "style": "natural",
        "prompt": (
            "A geometric tech-style AI mascot icon. Hexagonal or polygonal design with circuit "
            "patterns, a central glowing blue core with a simple friendly face. "
            "Dark background with neon blue and teal accents. Feels futuristic and intelligent. "
            "Suitable for a tech-forward education chatbot. Clean, sharp edges."
        ),
    },
    {
        "filename": "mitra-icon-v7-illustrated-mentor.png",
        "size": "1024x1024",
        "style": "vivid",
        "prompt": (
            "An illustrated friendly AI mentor mascot. Small round character with a graduation-cap "
            "style glow around the head, holding a tiny glowing book or light bulb. "
            "Warm blue and gold color palette. Looks knowledgeable and friendly, not childish. "
            "Suitable for an education platform chatbot. Clean white background. "
            "Illustration style, slightly editorial, charming and trustworthy."
        ),
    },
]

SLEEP_SECONDS = 13  # Tier 1 rate limit: 5 images/min

for i, icon in enumerate(ICONS, 1):
    dest = OUTPUT_DIR / icon["filename"]
    if dest.exists():
        print(f"[{i}/{len(ICONS)}] SKIP (exists): {icon['filename']}")
        continue

    print(f"[{i}/{len(ICONS)}] Generating: {icon['filename']} ({icon['size']}) ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=icon["prompt"],
        size=icon["size"],
        quality="standard",
        style=icon["style"],
        n=1,
    )
    url = response.data[0].url
    urllib.request.urlretrieve(url, dest)
    print(f"         Saved to {dest}")

    if i < len(ICONS):
        print(f"         Sleeping {SLEEP_SECONDS}s (rate limit) ...")
        time.sleep(SLEEP_SECONDS)

print("\nDone! All Mitra icon variations saved to content/assets/mitra-icons/")
print("Review all 7 and tell me which variation to use for the chatbot widget.")
