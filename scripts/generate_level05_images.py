"""
Generate DALL-E 3 images for Level 5: Life Upgrade
Run: .venv/bin/python scripts/generate_level05_images.py

Images are saved to content/assets/scenes/
Script skips files that already exist — safe to re-run.
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

    # -- wide hero -- Indian family using AI for everyday life decisions ------
    (
        "img-l5-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic flat illustration representing 'AI for everyday Indian life upgrade'. "
        "Five warm vignettes side by side: "
        "left -- Indian homemaker woman (Lakshmi) at a kitchen table reviewing a budget spreadsheet on her phone, relieved expression; "
        "center-left -- Indian father and teenage son studying together at a table, son pointing at a science diagram on a phone; "
        "center -- Indian woman teacher (Kavitha) planning a family trip, phone showing a 3-day itinerary, map visible; "
        "center-right -- young Indian male professional (Srinivas) at a laptop comparing two phone plan cards side by side; "
        "right -- Indian working woman (Meera) doing light morning exercise at home, phone showing a habit tracker. "
        "Warm orange, burnt sienna, and golden amber colour palette. Deep dark orange and navy backgrounds. "
        "Modern flat illustration style with depth. Energetic, hopeful, everyday Indian household mood. No text overlays."
    ),

    # -- Lakshmi -- homemaker with household budget on phone -----------------
    (
        "img-l5-s02-lakshmi-budget.jpg",
        "1024x1024",
        "Illustration of an Indian homemaker woman (Lakshmi, mid-30s) sitting at a kitchen table in Visakhapatnam. "
        "She is holding a smartphone showing a neat budget table with category rows and numbers -- text not readable. "
        "A small notebook with handwritten expense notes is open on the table beside her. "
        "She has a calm, satisfied expression, as if things finally make sense. "
        "Kitchen background: steel vessels on shelf, gas stove, a small plant on windowsill, morning light. "
        "She is wearing a cotton saree in warm orange tones. "
        "Warm amber and burnt orange palette, flat digital illustration style. Domestic, organised, reassuring mood. No readable text."
    ),

    # -- Ramaiah -- father helping son with homework --------------------------
    (
        "img-l5-s03-ramaiah-homework.jpg",
        "1024x1024",
        "Illustration of an Indian father (Ramaiah, mid-40s, government clerk look) and his teenage son (Arjun, 13 years old) "
        "sitting together at a study table in Warangal. "
        "The father is pointing at a phone screen showing a simple science explanation with a water-pipe diagram illustration -- text not readable. "
        "The son looks engaged and is writing in his notebook. "
        "The table has a open textbook, pencils, and a glass of water. "
        "A small bookshelf is visible in the background. Warm desk lamp lighting. "
        "The father looks proud and helpful. "
        "Warm amber and teal tones, flat digital illustration. Heartwarming, educational, family bonding atmosphere. No readable text."
    ),

    # -- Kavitha -- teacher planning family trip on phone --------------------
    (
        "img-l5-s04-kavitha-travel.jpg",
        "1024x1024",
        "Illustration of an Indian woman (Kavitha, early 30s, teacher appearance) sitting at a home desk in Kadapa, "
        "holding her smartphone showing a day-by-day travel itinerary with icons for temple, fort, and park -- text not readable. "
        "A small printed map of Andhra Pradesh is pinned to the wall beside her. "
        "On the desk: a notebook with trip notes, a pen, and a family photo. "
        "She has a happy, excited expression -- as if the trip is finally coming together. "
        "She is wearing a light cotton salwar in soft blue. "
        "Sky blue, amber, and warm white tones, flat illustration. Organised, cheerful, holiday planning mood. No readable text."
    ),

    # -- Srinivas -- young professional comparing phone plans ----------------
    (
        "img-l5-s05-srinivas-compare.jpg",
        "1024x1024",
        "Illustration of a young Indian male professional (Srinivas, mid-20s, bank officer appearance) "
        "sitting at a home desk in Rajahmundry, looking at a laptop screen. "
        "The laptop screen shows two side-by-side comparison cards for two mobile plans with price tags and icons -- text not readable. "
        "A speech bubble from the screen shows a small checkmark and a highlighted winner card. "
        "He has a confident, decisive expression -- like he just made a clear, informed choice. "
        "He is wearing a collared shirt. "
        "Modern home desk, clean and minimal. Sky blue and orange tones, flat illustration. Smart, analytical, satisfied mood. No readable text."
    ),

    # -- Meera -- working woman doing morning exercise at home ---------------
    (
        "img-l5-s06-meera-habits.jpg",
        "1024x1024",
        "Illustration of an Indian working woman (Meera, early 30s, professional appearance) "
        "doing light morning exercise at home in Vijayawada -- stretching or doing simple bodyweight movements on a yoga mat. "
        "A smartphone propped against a wall shows a simple weekly habit tracker with checkboxes -- text not readable. "
        "Morning sunlight through a window. "
        "She is wearing comfortable exercise clothes in teal. "
        "The room is tidy: a small plant, water bottle nearby, shoes by the door suggesting she just got up. "
        "She looks energised and motivated. "
        "Teal, warm morning gold, and white tones, flat digital illustration. Healthy, motivated, everyday wellness mood. No readable text."
    ),

    # -- practice arena -- person trying all 5 life skills -------------------
    (
        "img-l5-s07-practice.jpg",
        "1024x1024",
        "Illustration of a young Indian person (gender-neutral, mid-20s) sitting at a bright clean home desk, "
        "working on a phone and laptop simultaneously. "
        "Five small floating card panels surround the screens, each with a simple icon and soft orange background: "
        "a rupee coin icon (budget), a graduation cap icon (learning), an airplane icon (travel), a scale/compare icon (comparison), a running figure icon (health habit). "
        "No text readable on any panel. "
        "The person looks energised, curious, and fully in control. "
        "Warm orange, amber, and white tones, flat illustration. Empowered, everyday life mastery mood. No readable text."
    ),

    # -- wide celebration -- all 5 L5 characters together --------------------
    (
        "img-l5-s08-celebration.jpg",
        "1792x1024",
        "Wide cinematic flat illustration of five Indian characters celebrating together outdoors in a warm sunny setting. "
        "Left to right: "
        "Indian homemaker woman (Lakshmi) holding a phone showing a savings chart; "
        "Indian father and teenage son (Ramaiah and Arjun) giving each other a thumbs up; "
        "Indian woman teacher (Kavitha) holding a small travel itinerary card; "
        "Young Indian male professional (Srinivas) showing his phone screen confidently; "
        "Indian working woman (Meera) in exercise clothes looking fit and energised. "
        "All five look happy, proud, and accomplished. "
        "Warm golden orange and amber sky background, celebratory confetti in orange and yellow. "
        "Wide flat illustration, cinematic composition. Joyful, empowering, everyday life upgrade mood. No text overlays."
    ),
]

# --- generation loop --------------------------------------------------------
def generate_image(filename, size, prompt):
    dest = SCENES_DIR / filename
    if dest.exists():
        print(f"  [skip] {filename} already exists")
        return

    print(f"  [gen]  {filename} ({size}) ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    url = response.data[0].url
    urllib.request.urlretrieve(url, dest)
    size_kb = dest.stat().st_size // 1024
    print(f"  [ok]   {filename} saved ({size_kb} KB)")


if __name__ == "__main__":
    total = len(IMAGES)
    for i, (filename, size, prompt) in enumerate(IMAGES, 1):
        print(f"\n[{i}/{total}] {filename}")
        generate_image(filename, size, prompt)
        if i < total:
            print("  [wait] 13s rate-limit pause ...")
            time.sleep(13)

    print("\nDone.")
