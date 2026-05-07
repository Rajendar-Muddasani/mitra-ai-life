"""
Generate DALL-E 3 images for Level 7: Build With AI
Run: .venv/bin/python scripts/generate_level07_images.py

Images are saved to content/assets/scenes/
Script skips files that already exist -- safe to re-run.
Rate limit: 5 images/min for Tier 1 -> 13-second sleep between requests.
"""

import os, time, pathlib, urllib.request

# --- load .env manually (no dotenv dependency) ------------------------------
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

# --- output dir -------------------------------------------------------------
SCENES_DIR = pathlib.Path("content/assets/scenes")
SCENES_DIR.mkdir(parents=True, exist_ok=True)

# --- image definitions ------------------------------------------------------
# Format: (filename, size, prompt)
IMAGES = [

    # -- wide hero -- all 4 L7 characters: AI builders -----------------------
    (
        "img-l7-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic flat illustration representing 'Indian professionals building real things with AI as co-builder'. "
        "Four warm vignettes side by side: "
        "left -- Indian woman school teacher (Nandini) in Nellore, sitting at a home desk, laptop screen showing a clean website with class schedule and WhatsApp button, pleased and surprised expression; "
        "center-left -- Indian male medical shop owner (Suresh) at a pharmacy counter in Karimnagar, phone showing a chat UI with FAQ bubbles, medicine shelves visible behind him, relieved expression; "
        "center-right -- Indian woman graphic designer (Pooja) in Hyderabad, at a Canva design workspace, colorful poster visible on screen with bold headline text, creative and confident expression; "
        "right -- Indian male CS engineering student (Kiran) in Guntur, laptop showing a Streamlit app with a data table and AI suggestion panel, GitHub page visible on second tab, proud and focused expression. "
        "Indigo, deep purple, midnight blue, and amber colour palette. Dark atmospheric backgrounds with glowing screen light. "
        "Modern flat illustration style with depth. Builder, creator, real output mood. No text overlays."
    ),

    # -- Nandini -- teacher reviewing her AI-built website -------------------
    (
        "img-l7-s02-nandini-website.jpg",
        "1024x1024",
        "Illustration of an Indian woman school teacher (Nandini, early 30s, traditional salwar in warm blue) "
        "sitting at a home desk in Nellore. "
        "Her laptop screen shows a clean, mobile-friendly one-page website with sections visible -- an About section, a class schedule table, and a green WhatsApp button at the top. Text not readable but layout clear. "
        "A printed handwritten note with her tuition details is beside the laptop -- her source content. "
        "She has a delighted, disbelieving expression -- like she can't believe she made something this good. "
        "A family photo and a small plant on the desk. Modest home study background, warm evening light. "
        "Indigo, teal, and warm cream tones, flat digital illustration. First-time creator, proud achievement, warm home setting mood. No readable text."
    ),

    # -- Suresh -- medical shop owner with FAQ chatbot on phone -------------
    (
        "img-l7-s03-suresh-chatbot.jpg",
        "1024x1024",
        "Illustration of an Indian male medical shop owner (Suresh, mid-30s, wearing a white pharmacy coat) "
        "standing at his shop counter in Karimnagar. "
        "He is holding a smartphone; the phone screen shows a simple chat UI -- green bubbles on the right (customer questions) and white bubbles on the left (automated FAQ answers). Layout visible, text not readable. "
        "Medicine shelves with labelled bottles and packets are visible behind him. "
        "A counter with a cash register and a few medicine boxes. "
        "He has a calm, relieved expression -- like the phone is now doing the work for him. "
        "Teal, indigo, and warm white tones, flat digital illustration. Small business efficiency, automation relief, medical shop setting mood. No readable text."
    ),

    # -- Pooja -- graphic designer building AI-assisted poster ---------------
    (
        "img-l7-s04-pooja-poster.jpg",
        "1024x1024",
        "Illustration of an Indian woman freelance graphic designer (Pooja, late 20s, creative professional look, colourful dupatta) "
        "at a bright design desk in Hyderabad. "
        "Her laptop screen shows a colourful social media promotional poster in Canva -- bold headline text visible but not readable, brand colour palette swatches, strong CTA button visible on the poster design. "
        "A sticky note beside the laptop shows bullet points -- her content notes, not readable. "
        "She has a confident, satisfied expression -- the hardest part (copy) is done. "
        "Design books, a colour palette card, and a coffee mug on the desk. Urban Hyderabad skyline softly visible through a window. "
        "Rose, indigo, amber, and bright creative tones, flat digital illustration. Freelancer flow state, creative confidence, design productivity mood. No readable text."
    ),

    # -- Kiran -- CS student with portfolio project on laptop ----------------
    (
        "img-l7-s05-kiran-portfolio.jpg",
        "1024x1024",
        "Illustration of an Indian male final-year computer science student (Kiran, early 20s, casual t-shirt and jeans) "
        "at a college study desk in Guntur. "
        "His laptop shows a split view: left tab -- a Streamlit web app with a data upload section and a results panel with AI-generated menu suggestions (layout visible, text not readable); right tab -- a GitHub repository page with commit history visible. "
        "Engineering textbooks stacked on one side. A printed resume on the desk with a few lines visible but not readable. "
        "He has a proud, focused expression -- someone who shipped something real. "
        "College hostel or study room background, late evening with desk lamp light. "
        "Indigo, deep blue, amber, and cool white tones, flat digital illustration. Student builder, portfolio pride, late-night focus mood. No readable text."
    ),

    # -- practice arena -- person with 4 floating project panels -------------
    (
        "img-l7-s06-practice.jpg",
        "1024x1024",
        "Illustration of an Indian professional (gender-neutral, 25-35 years old) "
        "sitting at a clean desk with a laptop, in a focused but energised pose. "
        "Around the person float four glowing project-icon panels in a soft arc: "
        "panel 1 -- a browser window icon with a page layout (website); "
        "panel 2 -- a chat bubble with a robot face (chatbot); "
        "panel 3 -- a colourful poster frame with a bold headline shape (poster); "
        "panel 4 -- a laptop with a GitHub octocat and code icon (portfolio project). "
        "The person looks capable and ready to build -- hands on keyboard. "
        "Indigo, midnight blue, amber, and teal tones, flat digital illustration. Builder mindset, creative empowerment, making things mood. No readable text."
    ),

    # -- celebration -- all 4 L7 characters celebrating completion -----------
    (
        "img-l7-s07-celebration.jpg",
        "1792x1024",
        "Wide cinematic flat illustration of four Indian professionals celebrating together after completing real AI-built projects. "
        "Left to right: Nandini (teacher in Nellore, warm blue salwar), Suresh (medical shop owner in Karimnagar, white pharmacy coat), Pooja (graphic designer in Hyderabad, colourful dupatta), Kiran (CS student in Guntur, casual t-shirt). "
        "They are in a bright warm space -- some holding laptops showing their projects, some giving thumbs-up, Pooja holding a printed poster, Kiran showing his phone with a live app. "
        "Digital confetti and glowing star sparks float around them. "
        "Each character has a small glowing icon above them: website icon, chat bubble, poster frame, GitHub octocat. "
        "Indigo, deep purple, amber, teal, and warm cream colour palette. Celebratory warm lighting. "
        "Energetic, triumphant, diverse Indian builders flat illustration. No text overlays."
    ),

]

# --- generate ---------------------------------------------------------------
SLEEP_SECONDS = 13  # Tier 1: 5 images/min -> 12s gap, 13s to be safe

total = len(IMAGES)
for i, (filename, size, prompt) in enumerate(IMAGES, start=1):
    dest = SCENES_DIR / filename
    if dest.exists():
        print(f"[{i}/{total}] SKIP (exists): {filename}")
        continue

    print(f"[{i}/{total}] Generating: {filename} ({size}) ...")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        url = response.data[0].url
        urllib.request.urlretrieve(url, dest)
        print(f"         Saved to {dest}")
    except Exception as e:
        print(f"         ERROR: {e}")

    if i < total:
        print(f"         Sleeping {SLEEP_SECONDS}s (rate limit) ...")
        time.sleep(SLEEP_SECONDS)

print("\nDone! Check content/assets/scenes/ for new files.")
