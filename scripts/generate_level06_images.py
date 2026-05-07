"""
Generate DALL-E 3 images for Level 6: Power User
Run: .venv/bin/python scripts/generate_level06_images.py

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

    # -- wide hero -- all 5 L6 characters: power user skills -----------------
    (
        "img-l6-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic flat illustration representing 'Indian professionals as AI power users'. "
        "Five warm vignettes side by side: "
        "left -- Indian male HR manager (Pradeep) at a corporate desk in Hyderabad, laptop showing a structured context block on screen, efficient focused expression; "
        "center-left -- Indian woman project coordinator (Ananya) in Vijayawada, laptop showing a structured table and checklist summary, organised and satisfied look; "
        "center -- Indian male stationery shop owner (Venkat) in Tirupati, laptop showing a bar chart and sales insight panel, surprised and delighted expression; "
        "center-right -- Indian woman freelance writer (Divya) in Guntur, desk with proposal template on laptop screen with [PLACEHOLDER] fields visible, productive look; "
        "right -- Indian male civil engineer (Rajan) in Vizag, reviewing a printed structural document with a red checklist pen, careful and confident expression. "
        "Rose, crimson, dark red and amber colour palette. Deep dark backgrounds. "
        "Modern flat illustration style with depth. Professional, high-performance, Indian urban workplace mood. No text overlays."
    ),

    # -- Pradeep -- HR manager building daily AI routine ---------------------
    (
        "img-l6-s02-pradeep-routine.jpg",
        "1024x1024",
        "Illustration of an Indian male HR professional (Pradeep, early 30s, business casual) "
        "at a corporate desk in Hyderabad. "
        "He is typing on a laptop; the screen shows a structured AI context block with labelled sections -- text not readable but structured layout visible. "
        "A sticky note on his monitor reads a short bullet list (not readable). "
        "Coffee mug and employee files on the desk. Open-plan office background -- desks, a whiteboard, warm office lighting. "
        "He has a confident, efficient expression -- like he has a system that works. "
        "Rose-crimson and warm white tones, flat digital illustration. Organised, professional, time-saving workflow mood. No readable text."
    ),

    # -- Ananya -- project coordinator with structured AI outputs ------------
    (
        "img-l6-s03-ananya-structure.jpg",
        "1024x1024",
        "Illustration of an Indian woman project coordinator (Ananya, late 20s, professional appearance) "
        "at a desk in Vijayawada. "
        "Her laptop screen shows two neat tables -- one a priority action checklist with columns, one a risk table -- and a short paragraph summary above them. Text not readable. "
        "A printed 15-page report is stacked on the corner of her desk -- marked 'INPUT'. "
        "She has a relieved, satisfied expression -- the complex report is now a clean one-pager. "
        "She is wearing a formal kurta in teal. "
        "Teal, rose, and warm white tones, flat illustration. Organised, analytical, professional efficiency mood. No readable text."
    ),

    # -- Venkat -- shop owner doing AI sales analysis ------------------------
    (
        "img-l6-s04-venkat-sheets.jpg",
        "1024x1024",
        "Illustration of an Indian male stationery and gift shop owner (Venkat, mid-30s, informal business wear) "
        "sitting behind his shop counter in Tirupati. "
        "A laptop on the counter shows a colourful bar chart with top product categories and a short bullet-point insight list -- text not readable. "
        "An Excel spreadsheet printed on paper is open beside the laptop. "
        "Shop shelves visible behind him with notebooks, pens, and gift wrap. "
        "He has a surprised, excited expression -- like data revealed something he didn't know. "
        "Warm amber, rose, and gold tones, flat digital illustration. Data-driven, small business discovery, positive surprise mood. No readable text."
    ),

    # -- Divya -- writer with reusable prompt template -----------------------
    (
        "img-l6-s05-divya-templates.jpg",
        "1024x1024",
        "Illustration of an Indian woman freelance writer (Divya, late 20s, creative professional look) "
        "at a home desk in Guntur. "
        "Her laptop screen shows a document with clear sections and [PLACEHOLDER] labels in square brackets -- the placeholder format is visible but text not readable. "
        "A handwritten note on the desk shows a small checklist with 3 items checked. "
        "She is holding a pen and smiling -- looking productive and in control. "
        "She is wearing a casual salwar in warm pink. "
        "Rose, warm pink, and cream tones, flat digital illustration. Creative, efficient, template-driven productivity mood. No readable text."
    ),

    # -- Rajan -- civil engineer with verification checklist -----------------
    (
        "img-l6-s06-rajan-limits.jpg",
        "1024x1024",
        "Illustration of an Indian male civil engineer (Rajan, early 40s, wearing a hard hat on the desk, collared shirt) "
        "at a desk in Vizag. "
        "He is reading a printed structural specification document and has a red pen in hand, ticking items on a physical checklist beside it. "
        "A laptop screen in the background shows AI-generated text -- part of the same document in draft form. "
        "His expression is serious, careful, and methodical -- not anxious, but rigorous. "
        "Construction blueprints are rolled up in the background. A calculator and engineering handbook are on the desk. "
        "Deep teal, crimson red, and warm white tones, flat illustration. High-stakes, careful verification, professional responsibility mood. No readable text."
    ),

    # -- practice arena -- person practicing all 5 power user skills ---------
    (
        "img-l6-s07-practice.jpg",
        "1024x1024",
        "Illustration of an Indian professional (gender-neutral, 25-35 years old) "
        "sitting at a desk with a laptop. "
        "Around the person float five skill-icon panels in a soft arc: "
        "panel 1 -- a clock with a circular arrow (routine); "
        "panel 2 -- a table grid with columns (structured output); "
        "panel 3 -- a bar chart with a magnifying glass (spreadsheet analysis); "
        "panel 4 -- a document with [  ] placeholder brackets (templates); "
        "panel 5 -- a red shield with a checkmark (verification). "
        "The person looks focused and capable -- a power user at work. "
        "Rose, crimson, amber, and deep navy tones, flat digital illustration. Empowered, systematic, high-performance mood. No readable text."
    ),

    # -- celebration -- all 5 L6 characters celebrating as power users -------
    (
        "img-l6-s08-celebration.jpg",
        "1792x1024",
        "Wide cinematic flat illustration of five Indian professionals celebrating together as AI power users. "
        "Left to right: Pradeep (HR manager, Hyderabad), Ananya (project coordinator, Vijayawada), Venkat (shop owner, Tirupati), Divya (writer, Guntur), Rajan (civil engineer, Vizag). "
        "They are in a bright shared workspace -- some holding laptops, some giving thumbs-up, one showing a phone screen. "
        "Digital confetti and glowing achievement stars float around them. "
        "Each character has a small glowing icon above them matching their skill (context block, table, chart, template, shield). "
        "Rose, amber, crimson, teal, and deep navy colour palette. Warm celebratory lighting. "
        "Energetic, triumphant, diverse Indian professionals flat illustration. No text overlays."
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
