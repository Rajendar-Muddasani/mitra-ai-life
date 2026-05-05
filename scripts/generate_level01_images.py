"""
Generate all Level 1 character and scene images using DALL-E 3.
Run:  .venv/bin/python scripts/generate_level01_images.py

- Reads OPENAI_API_KEY from .env
- Saves images to content/assets/{characters,scenes}/
- Skips files that already exist (safe to re-run)
- Logs cost estimate at the end
"""
import os
import time
from pathlib import Path

from openai import OpenAI

# ── load .env manually (no dotenv dependency needed) ─────────────────────
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

# ── output folders ────────────────────────────────────────────────────────
BASE    = Path(__file__).resolve().parents[1] / "content" / "assets"
CHARS   = BASE / "characters"
SCENES  = BASE / "scenes"
for folder in [CHARS, SCENES]:
    folder.mkdir(parents=True, exist_ok=True)

# ── style modifier appended to every prompt ───────────────────────────────
STYLE = (
    "Vibrant cartoon illustration style, Indian cultural setting, bold black outlines, "
    "warm and bright colours, comic book aesthetic, expressive faces, clean flat design, "
    "family-friendly, 2D art."
)


def generate(prompt: str, out_path: Path, *, size="1024x1024"):
    """Generate one image and save it. Skips if file already exists."""
    if out_path.exists():
        print(f"  SKIP  {out_path.name}  (already exists)")
        return

    full_prompt = f"{prompt}  {STYLE}"
    print(f"  GEN   {out_path.name} ...", end="", flush=True)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size=size,
            quality="standard",
            n=1,
        )
        url = response.data[0].url

        # Download and save
        import urllib.request
        urllib.request.urlretrieve(url, out_path)
        print(f" saved ({out_path.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f" ERROR: {exc}")

    # Rate-limit: DALL-E 3 allows 5 images/min on tier 1
    time.sleep(13)


# ── asset definitions ─────────────────────────────────────────────────────

CHARACTER_SHEETS = [
    (
        "ravi-reference.png",
        "Character design sheet for an Indian male shopkeeper named Ravi, age 38-40, medium build, "
        "dark short hair, wearing a simple blue or white cotton kurta, warm brown skin, friendly face, "
        "slightly round face, expressive large eyes, default neutral-happy expression. "
        "Full body front view on the left, side view on the right. Consistent design. No text in the image.",
    ),
    (
        "priya-reference.png",
        "Character design sheet for an Indian woman named Priya, age 35, homemaker, wearing a simple "
        "cotton salwar kameez in green or yellow, bindi on forehead, warm brown skin, curly shoulder-length "
        "black hair, warm smile, expressive eyes. Full body front view on the left, side view on the right. "
        "Consistent design. No text in the image.",
    ),
    (
        "rahul-reference.png",
        "Character design sheet for an Indian teenage boy named Rahul, age 15, school student, wearing "
        "a school uniform with white shirt and dark trousers, school bag on shoulder, slightly curly hair, "
        "eager curious expression, holding a textbook. Full body front view on the left, side view on the right. "
        "Consistent design. No text in the image.",
    ),
    (
        "mitra-reference.png",
        "Character design for an AI guide named Mitra. A bright glowing blue sphere with a friendly face: "
        "large white eyes with blue pupils, a curved warm smile, two small rounded hands, no legs. "
        "Looks like a happy friendly emoji come to life. Glowing soft blue aura around it. "
        "NOT scary, NOT robotic, very approachable and cute. Four views: normal, waving, happy-dance, thinking. "
        "White background. No text in the image.",
    ),
]

SCENE_IMAGES = [
    (
        "img-s01-hero.jpg",
        "1792x1024",
        "Vibrant Indian-style festive illustration. The word AI in large colourful cartoon letters in the centre, "
        "surrounded by small cartoon icons of Indian daily life: a tiffin box, a smartphone, a school bag, a kirana "
        "shop, an autorickshaw, a recipe book, a WhatsApp notification bubble. Background is a warm orange-yellow "
        "gradient. Celebratory and welcoming energy. NO scary robots. Hand-drawn bold letters style.",
    ),
    (
        "img-s02-shop.jpg",
        "1792x1024",
        "Cartoon comic panel. Interior of an Indian kirana shop. A friendly shopkeeper (Indian male, age 38, "
        "dark hair, simple kurta) behind a counter with packed shelves of groceries and snacks behind him. "
        "Warm yellow evening lighting. A customer browsing. Happy neighbourhood feel. Hyderabad setting. "
        "Thick comic panel border. No text.",
    ),
    (
        "img-s03-frustrated.jpg",
        "1024x1024",
        "Cartoon comic panel. Indian male shopkeeper Ravi sitting at a home table looking frustrated. "
        "Three crumpled papers on the table and floor. A blank paper in front of him, pen in hand. "
        "Clock on wall shows 7:30 PM. Cartoon steam lines coming from his head indicating frustration. "
        "Question marks in a thought bubble above his head. Warm Indian home interior in the background. "
        "Comic book style with thick border. No text.",
    ),
    (
        "img-s04-priya-entering.jpg",
        "1024x1024",
        "Cartoon comic panel. Indian woman Priya walking into a living room holding a smartphone, "
        "cheerful expression, finger pointing at the phone with excitement. An Indian man visible in the "
        "background sitting at a table looking sceptical with one eyebrow raised. Indian home setting, "
        "evening light. Empty speech bubble outlines (no text inside). Comic book style with thick border.",
    ),
    (
        "img-s05-mitra-greeting.png",
        "1024x1024",
        "Friendly AI character Mitra: a bright glowing blue sphere with a big warm smile, large white eyes, "
        "waving one hand in greeting. Stars and sparkles around it. Very cute and welcoming. NOT scary. "
        "White background. Suitable for use as a website mascot sticker.",
    ),
    (
        "img-s06-library-analogy.jpg",
        "1792x1024",
        "Cartoon illustration of a magical glowing library with infinite tall shelves of colourful books "
        "stretching upward to the sky. A small cute blue robot at the bottom reading many books "
        "simultaneously, with speed lines and books flying around it. Warm golden magical light. "
        "Sense of wonder and knowledge. Fantasy-cartoon style. No text.",
    ),
    (
        "img-s07-typing-phone.jpg",
        "1024x1024",
        "Cartoon close-up illustration from above showing two hands with warm brown skin holding a smartphone, "
        "typing on a chat app. A colourful phone case. Simple chat interface visible. Clean background. "
        "Flat illustration style. No specific text visible on screen.",
    ),
    (
        "img-s08-ravi-amazed.jpg",
        "1024x1024",
        "Cartoon comic panel. Indian man Ravi staring at his smartphone with wide eyes and slightly open mouth "
        "in complete amazement. Stars and sparkles around his head. His wife Priya visible over his shoulder "
        "also looking impressed, pointing at the phone. Evening home setting with warm lamp light. "
        "Comic book style with thick border. Happy excited energy. No text.",
    ),
    (
        "img-s09-priya-kitchen.jpg",
        "1024x1024",
        "Cartoon comic panel. Indian kitchen setting. Indian woman Priya standing near a kitchen counter "
        "holding a phone, reading something with a smile. Traditional clay pots and modern appliances visible. "
        "Warm kitchen lighting. Her mother-in-law (elderly Indian woman) visible in background also smiling. "
        "Comic book style with thick border. No text.",
    ),
    (
        "img-s10-rahul-studying.jpg",
        "1024x1024",
        "Cartoon comic panel. Indian teenage boy Rahul at a wooden study desk. Open science textbook on the "
        "left. Smartphone on the right showing an AI chat response. Rahul looking at the phone with a bright "
        "lightbulb appearing above his head indicating a moment of understanding. Study lamp. Night time. "
        "Poster of the map of India on the wall. Comic book style with thick border. No text.",
    ),
    (
        "img-s11-safety-warning.jpg",
        "1792x1024",
        "Friendly cartoon illustration showing an Indian family gathered around a tablet learning about AI "
        "safety. A cheerful blue robot mascot is pointing to four glowing shield icons floating in the air, "
        "each with a small friendly symbol like a padlock, a magnifying glass, a lightbulb, and a heart. "
        "Warm cozy home setting. Bright cheerful colors, comic book style. No text.",
    ),
    (
        "img-s12-ai-wrong-answer.jpg",
        "1024x1024",
        "Funny cartoon comic panel. A cute confused robot character with question marks floating around its "
        "head showing text on a screen. An Indian man looking at the screen with one eyebrow raised and a "
        "question mark above his head. A wall calendar in the background with a wrong year circled in red. "
        "Light-hearted and funny tone, not scary. Comic book style with thick border.",
    ),
    (
        "img-s13-celebration.jpg",
        "1792x1024",
        "Vibrant celebration cartoon illustration. The Mitra blue sphere AI character doing a happy dance "
        "with confetti and stars exploding around it. Confetti in orange, white, and green (Indian flag colours) "
        "plus blue. Festive and joyful energy. Trophy icon visible. No specific text needed.",
    ),
    (
        "img-s14-level2-teaser.jpg",
        "1792x1024",
        "Futuristic Indian-style illustration with a dark blue and purple background and glowing neon elements. "
        "Small glowing preview windows floating in space showing: a formal letter, a WhatsApp chat window, "
        "a grocery list, a student's notes. The Mitra blue sphere AI character in the centre pointing at them "
        "with excitement. Stars and energy lines. Sense of adventure and possibility.",
    ),
    (
        "img-s15-ravi-types.jpg",
        "1024x1024",
        "Cartoon illustration of an Indian man's hands close up, typing on a smartphone keyboard. "
        "The phone screen shows a chat input box with text appearing letter by letter, animated feel. "
        "Warm brown skin hands. Expressive typing with slight motion blur on fingers. "
        "Clean simple background. Flat cartoon style.",
    ),
]


# ── main ──────────────────────────────────────────────────────────────────

def main():
    print("\n=== Mitra AI Life Education — DALL-E 3 Image Generator ===\n")

    # Count what needs generating
    chars_to_gen  = sum(1 for name, _ in CHARACTER_SHEETS   if not (CHARS / name).exists())
    scenes_to_gen = sum(1 for name, _, _ in SCENE_IMAGES    if not (SCENES / name).exists())
    total         = chars_to_gen + scenes_to_gen

    if total == 0:
        print("All images already generated. Nothing to do.")
        return

    # DALL-E 3 pricing (as of 2025): $0.04 per standard 1024×1024, $0.08 per 1792×1024
    cost_1024 = sum(0.04 for n, _ in CHARACTER_SHEETS if not (CHARS / n).exists())
    cost_1792 = sum(
        (0.08 if size == "1792x1024" else 0.04)
        for n, size, _ in SCENE_IMAGES
        if not (SCENES / n).exists()
    )
    est_cost = cost_1024 + cost_1792
    print(f"Images to generate:  {total}  (characters: {chars_to_gen}, scenes: {scenes_to_gen})")
    print(f"Estimated cost:      ~${est_cost:.2f} USD")
    print(f"Estimated time:      ~{total * 13 // 60 + 1} minutes (rate-limited)\n")

    print("── Character sheets ──────────────────────────────────────")
    for name, prompt in CHARACTER_SHEETS:
        generate(prompt, CHARS / name, size="1024x1024")

    print("\n── Scene images ──────────────────────────────────────────")
    for name, size, prompt in SCENE_IMAGES:
        generate(prompt, SCENES / name, size=size)

    print(f"\nDone! Images saved to {BASE.relative_to(Path.cwd())}")
    print("Next step: replace CSS art in level-01-comic.html with these image paths.")


if __name__ == "__main__":
    main()
