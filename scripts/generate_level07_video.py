"""
Generate Level 7 English narrated intro video.
Topic: Build With AI — Stop Using AI. Start Building With It.
7 scenes, ~120s, voice: nova, speed: 0.95
Output: content/assets/videos/level-07-intro.mp4
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

ROOT      = Path(__file__).parent.parent
SCENES    = ROOT / "content/assets/scenes"
AUDIO_DIR = ROOT / "content/assets/videos/audio_tmp_l7"
OUT       = ROOT / "content/assets/videos/level-07-intro.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l7-s01-hero.jpg",
        "text": (
            "Welcome to Level 7 — Build With AI. "
            "This is where you stop using AI for small tasks and start building real things. "
            "A website, a chatbot, a business poster, and a real portfolio project — AI is your co-builder. "
            "You bring the idea. AI helps you ship it."
        ),
    },
    {
        "image": "img-l7-s02-nandini-website.jpg",
        "text": (
            "Nandini wanted a website for her home bakery. "
            "She described her business to AI, picked a style, and got a ready-to-use website draft. "
            "No coding, no design skills — just her idea and AI's help. "
            "Now her bakery is online and getting new orders every week."
        ),
    },
    {
        "image": "img-l7-s03-suresh-chatbot.jpg",
        "text": (
            "Suresh runs a coaching centre. "
            "He used AI to build a simple chatbot that answers parents' questions about timings, fees, and courses. "
            "The bot works 24/7 and saves him hours every week. "
            "AI is not just for chatting — it's for building tools that work for you."
        ),
    },
    {
        "image": "img-l7-s04-pooja-poster.jpg",
        "text": (
            "Pooja is a freelance designer. "
            "She used AI to create a business poster for a local event. "
            "She gave the details, picked a theme, and AI generated a poster ready to print. "
            "Now she offers poster design as a service — powered by AI."
        ),
    },
    {
        "image": "img-l7-s05-kiran-portfolio.jpg",
        "text": (
            "Kiran wanted to apply for jobs. "
            "He used AI to build a portfolio site with his projects, resume, and a contact form. "
            "He got interview calls within a week. "
            "Building with AI means you can launch faster and stand out."
        ),
    },
    {
        "image": "img-l7-s06-practice.jpg",
        "text": (
            "In this level, you will build four real projects: a website, a chatbot, a business poster, and your own portfolio. "
            "You will learn how to turn your ideas into reality with AI as your co-builder. "
            "No experience needed — just follow the steps and build."
        ),
    },
    {
        "image": "img-l7-s07-celebration.jpg",
        "text": (
            "That is Level 7. You have built real things with AI. "
            "Your website, your chatbot, your poster, your portfolio — all live and working. "
            "Scroll down to start your projects. "
            "See you in Level 8, where you will learn to automate and scale."
        ),
    },
]

def generate_audio():
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    print("Step 1: Generating TTS narration audio...")
    for i, sc in enumerate(SCENES_DATA, 1):
        path = AUDIO_DIR / f"scene-{i:02d}.mp3"
        if path.exists():
            print(f"  [{i}/{len(SCENES_DATA)}] Skipping (exists): {path.name}")
            continue
        preview = sc["text"][:60].replace("\n", " ")
        print(f"  [{i}/{len(SCENES_DATA)}] TTS: {preview}...")
        response = client.audio.speech.create(
            model="tts-1", voice="nova", input=sc["text"], speed=0.95,
        )
        response.stream_to_file(str(path))
        print(f"    Saved: {path.name}")
    print(f"  Audio ready: {len(SCENES_DATA)} files\n")

def make_zoom_clip(img_path: Path, duration: float):
    img = Image.open(img_path).convert("RGB")
    iw, ih = img.size
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(img, ((W - nw) // 2, (H - nh) // 2))
    frame0 = np.array(canvas)

    def zoom_frame(get_frame, t):
        f = get_frame(t)
        s = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw2, nh2 = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw2, nh2), Image.LANCZOS)
        ox2, oy2 = (nw2 - w) // 2, (nh2 - h) // 2
        return np.array(zoomed.crop((ox2, oy2, ox2 + w, oy2 + h)))

    clip = ImageClip(frame0, duration=duration)
    return clip.transform(zoom_frame, apply_to="video")

def build_video():
    import moviepy
    print("Step 2: Building video...")
    print(f"  Using ffmpeg: {moviepy.config.FFMPEG_BINARY}")
    print("  Building clips...")
    clips = []
    for i, sc in enumerate(SCENES_DATA, 1):
        print(f"  [{i}/{len(SCENES_DATA)}] {sc['image']}")
        audio = AudioFileClip(str(AUDIO_DIR / f"scene-{i:02d}.mp3"))
        dur   = audio.duration + 0.4
        clip  = make_zoom_clip(SCENES / sc["image"], dur).with_audio(audio)
        clips.append(clip)

    print("\n  Concatenating clips...")
    final = concatenate_videoclips(clips, method="compose")
    print(f"  Writing: {OUT}")
    final.write_videofile(
        str(OUT), fps=FPS, codec="libx264", audio_codec="aac",
        temp_audiofile=str(AUDIO_DIR / "final_audio.m4a"),
        remove_temp=True, logger="bar",
    )
    dur_s = int(final.duration)
    print(f"\n✅ Video ready: {OUT}")
    print(f"   Duration: ~{dur_s}s")
    print(f"\nNext — upload to S3:")
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-07-intro.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
