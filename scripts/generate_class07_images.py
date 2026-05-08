"""
Generate 12 Class 7 lesson hero images using DALL-E 3.
Run:  .venv/bin/python scripts/generate_class07_images.py

- Reads OPENAI_API_KEY from .env
- Saves images to content/assets/students/class-07/
- Skips files that already exist (safe to re-run)
- Logs cost estimate at the end
- After generation, upload with: bash scripts/upload_class07_images.sh
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
OUT = Path(__file__).resolve().parents[1] / "content" / "assets" / "students" / "class-07"
OUT.mkdir(parents=True, exist_ok=True)

# ── style appended to every prompt ────────────────────────────────────────────
STYLE = (
    "Vibrant cartoon illustration style, Indian cultural setting, bold black outlines, "
    "warm bright purple colour palette, comic book aesthetic, expressive faces, "
    "clean flat design, family-friendly, appropriate for 11–12 year olds, 2D art. "
    "No text, no letters, no numbers inside the image."
)

# ── 12 lesson hero images (filename, size, prompt) ────────────────────────────
IMAGES = [
    (
        "lesson-01-hero.jpg",
        "1792x1024",
        "Indian boy age 12, sitting at a school desk in Warangal, typing a question on a tablet. "
        "Large glowing purple speech bubbles float above the tablet — one small vague question, "
        "one large detailed question with arrows showing improvement. A friendly purple AI robot "
        "stands beside the desk giving an approving thumbs up. Bright Indian classroom background "
        "with colourful motivational posters. Warm purple and gold tones.",
    ),
    (
        "lesson-02-hero.jpg",
        "1792x1024",
        "Indian girl age 12 seated at a study table surrounded by six colourful subject textbooks "
        "spread open — Science, Maths, History, English, Geography, and Hindi. Each book has a small "
        "glowing chat bubble floating above it showing a helpful AI answer symbol. "
        "The girl looks happy and organised. Bright Bengaluru home study room, afternoon light, "
        "purple and yellow colour palette.",
    ),
    (
        "lesson-03-hero.jpg",
        "1792x1024",
        "Indian child at a desk building a colourful stack of large paper flashcards. "
        "Each flashcard has a bold drawing — a planet, a Mughal fort, a Maths formula symbol, "
        "a leaf. A glowing purple tablet beside the cards shows an AI chatbot screen. "
        "Scissors, coloured pens, and a notebook on the desk. "
        "Cheerful Indian bedroom study corner, warm afternoon light.",
    ),
    (
        "lesson-04-hero.jpg",
        "1792x1024",
        "Indian child holding an open notebook with a short creative story written inside, "
        "surrounded by floating colourful story elements — a rocket, a magical forest, a talking "
        "parrot, a brave Indian girl character. A glowing purple AI robot holds a pencil nearby "
        "like a creative collaborator. Large open book as background. Imaginative artistic scene.",
    ),
    (
        "lesson-05-hero.jpg",
        "1792x1024",
        "Indian boy at a blackboard working through a Maths equation step by step, with each step "
        "numbered in colourful chalk. A glowing purple AI tutor robot beside the board points at "
        "each step with a chalk pointer, teaching the method. Bright Indian classroom, "
        "equations and geometry diagrams on the board. Encouraging atmosphere.",
    ),
    (
        "lesson-06-hero.jpg",
        "1792x1024",
        "Indian student at a library desk with several open reference books and a glowing tablet. "
        "Above the tablet floats a magnifying glass icon and a checklist with tick marks "
        "symbolising source verification. Book spines visible in the background. "
        "Warm library setting, afternoon light through windows. Purple and cream tones.",
    ),
    (
        "lesson-07-hero.jpg",
        "1792x1024",
        "Cartoon cross-section of a friendly cartoon robot brain. Inside the brain: colourful small "
        "text tokens floating like puzzle pieces, a glowing context window frame, a memory storage "
        "box that is half-empty showing the concept of forgetting. "
        "An Indian child peeks in through a large magnifying glass with a curious expression. "
        "Purple and teal tones, clean flat design.",
    ),
    (
        "lesson-08-hero.jpg",
        "1792x1024",
        "Indian child looking at a tablet showing a stunning AI-generated artwork — a colourful "
        "landscape with a peacock and Indian palace. Around the child float small AI art frame "
        "previews of different styles. A camera and paintbrush float nearby. "
        "Warm creative studio setting, purple and gold colour palette. Sense of wonder and creativity.",
    ),
    (
        "lesson-09-hero.jpg",
        "1792x1024",
        "Illustrated cartoon map of India with school building icons across different states — "
        "Andhra Pradesh, Telangana, Maharashtra, Tamil Nadu, UP, Rajasthan. Glowing purple tablet "
        "screens show DIKSHA-style educational apps. Indian students in school uniforms use tablets "
        "and phones. Sense of digital education spreading across the country.",
    ),
    (
        "lesson-10-hero.jpg",
        "1792x1024",
        "Indian student at a desk with a chain of glowing purple prompt cards arranged in a row "
        "on the table — first card leads to second leads to third, each building on the last. "
        "A small AI robot at the end of the chain gives a helpful answer. "
        "Arrows showing the iterative prompting process. Bright study room setting.",
    ),
    (
        "lesson-11-hero.jpg",
        "1792x1024",
        "Split scene of two Indian teenagers side by side. Left side: teen sharing true, helpful "
        "information on a phone — green checkmark floating above. Right side: teen pausing before "
        "sharing a suspicious message, holding up a stop-hand gesture — magnifying glass and "
        "question mark floating. Digital safety and responsibility theme. "
        "Purple and green vs. amber tones. Friendly, not scary.",
    ),
    (
        "lesson-12-hero.jpg",
        "1792x1024",
        "Indian student proudly holding up a colourful project portfolio folder labelled with "
        "a star. Around the student float 12 small illustrated icons representing each Class 7 "
        "lesson — a prompt card, a subject book, a flashcard, a story, a Maths equation, a library "
        "book, a robot brain, an AI artwork, a school map, a prompt chain, a safety shield, "
        "a portfolio. Graduation cap and sparkles. Warm celebratory scene. Purple and gold.",
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
    time.sleep(1)  # rate-limit pause


def main():
    print(f"Output folder: {OUT}")
    print(f"Total images : {len(IMAGES)}\n")
    for filename, size, prompt in IMAGES:
        generate(filename, size, prompt)
    cost = len(IMAGES) * 0.040
    print(f"\nDone. Estimated cost: ${cost:.2f} USD (standard quality 1792×1024)")


if __name__ == "__main__":
    main()
