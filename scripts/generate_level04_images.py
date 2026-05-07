"""
Generate DALL-E 3 images for Level 4: Work Smart
Run: .venv/bin/python scripts/generate_level04_images.py

Images are saved to content/assets/scenes/
Script skips files that already exist — safe to re-run.
Rate limit: 5 images/min for Tier 1 → 13-second sleep between requests.
"""

import os, time, pathlib, urllib.request

# ─── load .env manually (no dotenv dependency) ──────────────────────────────
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

# ─── output dir ─────────────────────────────────────────────────────────────
SCENES_DIR = pathlib.Path("content/assets/scenes")
SCENES_DIR.mkdir(parents=True, exist_ok=True)

# ─── image definitions ──────────────────────────────────────────────────────
# Format: (filename, size, prompt)
IMAGES = [

    # ── wide hero — work smart with AI ───────────────────────────────────
    (
        "img-l4-s01-hero.jpg",
        "1792x1024",
        "Wide cinematic flat illustration representing 'working smarter with AI in India'. "
        "Four vignettes side by side: "
        "left — a young Indian professional woman (Deepa) in Hyderabad at a desk quickly typing an email on her laptop with a satisfied expression; "
        "center-left — an Indian female HR manager (Sunitha) in Guntur holding tidy meeting notes, looking organised; "
        "center-right — a young Indian male graduate (Anand) in Nellore reviewing a polished resume on a laptop with confidence; "
        "right — an Indian engineering student (Vikram) in Tirupati with a structured study plan and presentation slides open. "
        "Violet purple and warm amber colour palette, deep indigo backgrounds. "
        "Modern flat illustration style with depth. Professional, confident and energetic mood. No text overlays."
    ),

    # ── deepa — email drafting at laptop ─────────────────────────────────
    (
        "img-l4-s02-deepa-email.jpg",
        "1024x1024",
        "Illustration of a professional Indian woman (Deepa, late 20s) sitting at a tidy office desk in Hyderabad, "
        "typing on a laptop with a focused and confident expression. "
        "The laptop screen shows an email compose window with the AI chat panel beside it — text not readable. "
        "She is wearing a formal kurta in dark violet. "
        "The desk has a coffee cup, a small notepad, and soft office lighting. "
        "Modern open-plan office background, warm purple and amber tones. "
        "Flat digital illustration style. She looks productive and in control. No readable text."
    ),

    # ── sunitha — meeting notes to summary ───────────────────────────────
    (
        "img-l4-s03-sunitha-report.jpg",
        "1024x1024",
        "Illustration of an Indian female HR manager (Sunitha, mid-30s) sitting at a conference table in Guntur, "
        "looking at her smartphone with a neat, organised expression. "
        "She has a small open notebook with rough bullet-point scribbles, and her phone screen shows a clean formatted document — not readable. "
        "The conference room behind her has a whiteboard with blurred writing. "
        "She looks satisfied and efficient, as if she just transformed messy notes into a polished summary. "
        "Teal and warm white tones, flat illustration, professional setting. No readable text."
    ),

    # ── anand — improving resume on laptop ───────────────────────────────
    (
        "img-l4-s04-anand-resume.jpg",
        "1024x1024",
        "Illustration of a young Indian male fresh graduate (Anand, early 20s) sitting at a study desk in Nellore, "
        "looking at a laptop screen showing a before-and-after resume comparison — text not readable. "
        "He has a hopeful and focused expression. "
        "The desk has a printed resume, a pen, and a glass of water. "
        "Simple home study room setting with a small bookshelf in the background. "
        "Sky blue and white tones with violet accents, flat illustration style. "
        "He looks determined and hopeful about his job search. No readable text."
    ),

    # ── anand — mock interview practice with phone ───────────────────────
    (
        "img-l4-s05-anand-interview.jpg",
        "1024x1024",
        "Illustration of a young Indian male graduate (Anand, early 20s) practising a job interview alone in his room in Nellore. "
        "He is sitting upright at his desk, speaking confidently, looking at his smartphone propped against a book. "
        "The phone screen shows an AI chat interface acting as a mock interviewer — text not readable. "
        "He is dressed smartly in a button-up shirt, as if ready for an interview. "
        "The room has a small desk, family photo on wall, motivational note pinned above. "
        "Sky blue and amber tones, flat illustration. Focused, confident, self-improving atmosphere. No readable text."
    ),

    # ── vikram — study plan and presentation ─────────────────────────────
    (
        "img-l4-s06-vikram-study.jpg",
        "1024x1024",
        "Illustration of an Indian male engineering student (Vikram, early 20s) sitting at a hostel room desk in Tirupati. "
        "His laptop screen shows a structured weekly study plan with subject labels — not readable. "
        "On the side, a separate window shows a presentation outline with slide titles — not readable. "
        "Textbooks are stacked beside him, some with coloured sticky notes. "
        "He looks organised and relieved, as if the chaos has been sorted. "
        "Amber and violet tones, warm desk lamp light, flat illustration style. "
        "Student hostel room with a single bed and a motivational poster in the background. No readable text."
    ),

    # ── practice arena — all 5 tasks ─────────────────────────────────────
    (
        "img-l4-s07-practice.jpg",
        "1024x1024",
        "Illustration of a young Indian professional (gender-neutral, mid-20s) sitting at a clean modern desk, "
        "working on a laptop with five small floating UI panels around the screen — representing email, meeting notes, resume, interview chat, and a calendar plan. "
        "Each panel is a soft pastel card with a simple icon: envelope, clipboard, document, speech bubble, calendar — no text readable. "
        "The person looks energised, focused, and in command. "
        "Violet and amber colour palette, minimal home office setting with a plant and a mug on the desk. "
        "Flat illustration style with gentle shadow depth. Productive and empowered mood. No readable text."
    ),

    # ── wide celebration — all L4 characters ─────────────────────────────
    (
        "img-l4-s08-celebration.jpg",
        "1792x1024",
        "Wide celebratory flat illustration showing all four Level 4 characters together in a vibrant group scene. "
        "Left to right: "
        "Deepa — Indian professional woman in violet kurta, holding a laptop, smiling proudly; "
        "Sunitha — Indian female HR manager in a saree, holding neat meeting notes, looking accomplished; "
        "Anand — young Indian male graduate in a smart shirt, holding a polished resume, looking confident and happy; "
        "Vikram — Indian male engineering student in casual clothes, holding a study planner, looking relieved and joyful. "
        "They are standing together in a bright, cheerful space — confetti falling, a golden glow behind them. "
        "Violet purple, amber, sky blue and teal colour palette. "
        "Modern flat illustration style. Celebratory, warm, triumphant mood. No text overlays."
    ),
]

# ─── main ────────────────────────────────────────────────────────────────────
def main():
    total = len(IMAGES)
    for idx, (fname, size, prompt) in enumerate(IMAGES, 1):
        dest = SCENES_DIR / fname
        if dest.exists():
            print(f"[{idx}/{total}] SKIP (exists) {fname}")
            continue

        print(f"[{idx}/{total}] Generating {fname} ({size}) …", flush=True)
        try:
            resp = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            url = resp.data[0].url
            urllib.request.urlretrieve(url, dest)
            kb = dest.stat().st_size // 1024
            print(f"  ✅ Saved {fname} ({kb} KB)")
        except Exception as e:
            print(f"  ❌ ERROR on {fname}: {e}")

        if idx < total:
            print(f"  Waiting 13 s …")
            time.sleep(13)

    print("\nDone.")

if __name__ == "__main__":
    main()
