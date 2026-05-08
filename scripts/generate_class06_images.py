"""
Generate 12 Class 6 lesson hero images using DALL-E 3.
Run:  .venv/bin/python scripts/generate_class06_images.py

- Reads OPENAI_API_KEY from .env
- Saves images to content/assets/students/class-06/
- Skips files that already exist (safe to re-run)
- Logs cost estimate at the end
- After generation, upload with: scripts/upload_class06_images.sh
"""
import os
import time
import urllib.request
from pathlib import Path

from openai import OpenAI

# ── load .env ─────────────────────────────────────────────────────────────────
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

# ── output folder ─────────────────────────────────────────────────────────────
OUT = Path(__file__).resolve().parents[1] / "content" / "assets" / "students" / "class-06"
OUT.mkdir(parents=True, exist_ok=True)

# ── style appended to every prompt ────────────────────────────────────────────
STYLE = (
    "Vibrant cartoon illustration style, Indian cultural setting, bold black outlines, "
    "warm bright sky-blue colour palette, comic book aesthetic, expressive faces, "
    "clean flat design, family-friendly, appropriate for 10–11 year olds, 2D art. "
    "No text, no letters, no numbers inside the image."
)

# ── 12 lesson hero images (filename, size, prompt) ────────────────────────────
IMAGES = [
    (
        "lesson-01-hero.jpg",
        "1792x1024",
        "Curious Indian 11-year-old boy at a school desk holding a glowing smartphone. "
        "A friendly small glowing blue AI robot floats beside him with big curious eyes. "
        "Thought bubbles above his head show gears, lightbulbs, and question marks. "
        "Bright Indian classroom background with colourful charts on the walls.",
    ),
    (
        "lesson-02-hero.jpg",
        "1792x1024",
        "Cheerful Indian female teacher at a colourful classroom blackboard holding large picture "
        "flashcards — apple, dog, ball. A small cute glowing blue robot student sits at a tiny desk "
        "looking at the cards with wide learning eyes. Stacks of colourful textbooks on the desk.",
    ),
    (
        "lesson-03-hero.jpg",
        "1792x1024",
        "Split scene showing AI in Indian daily life. Left side: Indian family morning — mother checking "
        "weather app, child asking homework question on phone. Right side: autorickshaw with GPS screen, "
        "kirana shop owner using inventory app, student with study-help tablet. "
        "All connected by glowing blue lines. Warm morning Indian home interior.",
    ),
    (
        "lesson-04-hero.jpg",
        "1792x1024",
        "Indian child sitting cross-legged with a tablet showing speech bubbles in Telugu, Hindi, and "
        "English with AI translation arrows between them. Colourful Indian language script symbols float "
        "around — Devanagari, Telugu, Tamil letters glowing. Small blue AI robot acts as friendly "
        "interpreter. Bright bookshelf background with Indian language books.",
    ),
    (
        "lesson-05-hero.jpg",
        "1792x1024",
        "Indian girl holding a tablet showing a split screen — left side is a photograph of a Chennai "
        "street scene, right side shows an AI-generated cartoon version. She looks amazed. "
        "Floating around her are small AI-generated artwork frames with Indian motifs, animals, and "
        "landscapes. Art supplies — pencils, paintbrush — nearby. Bright creative studio setting.",
    ),
    (
        "lesson-06-hero.jpg",
        "1792x1024",
        "Indian school student at a desk surrounded by colourful graphs, charts, and data visualisations. "
        "One chart shows cricket match scores as a bar chart, another shows exam results, a third shows "
        "rainfall data for Indian states. A glowing blue AI robot points at a pie chart helpfully. "
        "Calculator and notebook on the desk. Bright school setting.",
    ),
    (
        "lesson-07-hero.jpg",
        "1792x1024",
        "Indian child looking at a phone with a confused, doubtful expression. The phone screen shows "
        "a clearly wrong AI answer with a big red X symbol above it. Around the child float "
        "fact-check symbols, a magnifying glass, and an open encyclopaedia. "
        "Cartoon question marks around the child's head. Textbook and encyclopaedia open on the table.",
    ),
    (
        "lesson-08-hero.jpg",
        "1792x1024",
        "A large cartoon balance scale in the centre. On one pan: diverse group of cheerful Indian "
        "children of different skin tones, genders, and regions. On the other pan: a glowing AI tablet. "
        "The scale is perfectly balanced. Heart symbols and fairness stars float around. "
        "Colourful Indian community background with people of different states.",
    ),
    (
        "lesson-09-hero.jpg",
        "1792x1024",
        "Indian family — parents and two children — gathered around a phone or laptop together. "
        "A large glowing blue protective shield surrounds the device and family. "
        "Around the shield: lock icons, privacy signs, safe-browsing symbols. "
        "Warm Indian home living room, evening lighting. Family looks confident and informed.",
    ),
    (
        "lesson-10-hero.jpg",
        "1792x1024",
        "Illustrated cartoon map of India with five glowing city dots — Bengaluru, Hyderabad, Mumbai, "
        "Chennai, Pune. Radiating connection lines linking the cities with small icons: a farmer using "
        "a phone, a doctor with a tablet, a rocket (space programme), a student at a laptop, a market "
        "vendor with an app. Sense of innovation spreading across the country. Sky-blue and saffron colours.",
    ),
    (
        "lesson-11-hero.jpg",
        "1792x1024",
        "Indian school Career Day scene in a bright auditorium. On stage: adults in professional roles — "
        "a doctor in white coat, a software engineer with a laptop, an AI researcher beside a small robot. "
        "In the audience: excited Indian children age 10–12 with notebooks, wide eyes, thought bubbles "
        "showing future career dreams. Sky-blue banners. Positive inspiring energy.",
    ),
    (
        "lesson-12-hero.jpg",
        "1792x1024",
        "Indian boy happily writing in a colourful journal or diary at a desk. Around him float 12 small "
        "illustrated thought bubbles showing scenes from the Class 6 year — a robot, a map, a balance "
        "scale, a data chart, a brain, a shield, a career scene, a language bubble, an image frame. "
        "A small graduation cap sits on his desk. Stars and sparkles. Warm Indian home setting.",
    ),
]


def generate(filename: str, size: str, prompt: str) -> None:
    out_path = OUT / filename
    if out_path.exists():
        print(f"  SKIP  {filename}  (already exists)")
        return

    full_prompt = f"{prompt}  {STYLE}"
    print(f"  GEN   {filename} ...", end="", flush=True)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size=size,
            quality="standard",
            n=1,
        )
        url = response.data[0].url
        urllib.request.urlretrieve(url, out_path)
        print(f" saved ({out_path.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f" ERROR: {exc}")

    # DALL-E 3 rate limit: ~5 images/min on tier 1
    time.sleep(13)


if __name__ == "__main__":
    print(f"\nGenerating {len(IMAGES)} Class 6 hero images → {OUT}\n")
    for filename, size, prompt in IMAGES:
        generate(filename, size, prompt)

    cost_usd = len(IMAGES) * 0.04   # DALL-E 3 standard 1792x1024 = $0.04 each
    print(f"\nDone. Estimated cost: ~${cost_usd:.2f} USD ({len(IMAGES)} × $0.04)")
    print(f"Images saved to: {OUT}")
    print(f"\nNext: run  bash scripts/upload_class06_images.sh  to push to S3.")
