"""
Generate Level 9 English narrated intro video.
Topic: AI for Income — Your AI Skills = Real Income.
8 scenes, ~120s, voice: nova, speed: 0.95
Output: content/assets/videos/level-09-intro.mp4
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

ROOT      = Path(__file__).parent.parent
SCENES    = ROOT / "content/assets/scenes"
AUDIO_DIR = ROOT / "content/assets/videos/audio_tmp_l9"
OUT       = ROOT / "content/assets/videos/level-09-intro.mp4"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24

SCENES_DATA = [
    {
        "image": "img-l9-s01-hero.jpg",
        "text": (
            "Welcome to Level 9 — AI for Income. "
            "Your AI skills are now worth real money. "
            "Freelance with AI. Create content for pay. Add AI services to what you already do. "
            "No office. No boss. Just your phone, your skills, and real earnings."
        ),
    },
    {
        "image": "img-l9-s02-kavya-gig.jpg",
        "text": (
            "Kavya is a homemaker in Vijayawada. "
            "She started offering AI-written content for small businesses on freelance platforms. "
            "She earns ten to fifteen thousand rupees a month from her phone — in her spare time. "
            "Her only investment was learning how to write good prompts."
        ),
    },
    {
        "image": "img-l9-s03-srinivas-clients.jpg",
        "text": (
            "Srinivas is a retired government employee. "
            "He uses AI to help local businesses create proposals and formal letters. "
            "He charges five hundred to a thousand rupees per document. "
            "His clients trust him because the quality is professional and fast."
        ),
    },
    {
        "image": "img-l9-s04-padma-youtube.jpg",
        "text": (
            "Padma runs a small YouTube channel on cooking. "
            "She uses AI to write video scripts, titles, and descriptions. "
            "Her upload frequency doubled, her views tripled, and her channel started earning from ads. "
            "AI did not replace her voice — it freed her time to cook and record more."
        ),
    },
    {
        "image": "img-l9-s05-raju-studio.jpg",
        "text": (
            "Raju is a photographer in Hyderabad. "
            "He added AI-generated social media content as a new service for his studio clients. "
            "Now every photography package includes AI posts and captions. "
            "His average order value went up by forty percent."
        ),
    },
    {
        "image": "img-l9-s06-pricing.jpg",
        "text": (
            "The key to earning with AI is packaging your skills. "
            "You do not sell AI — you sell results. "
            "A WhatsApp promotion, a business proposal, a social media post, a YouTube script — "
            "these are services people pay for. You are the expert who delivers them, powered by AI."
        ),
    },
    {
        "image": "img-l9-s07-practice.jpg",
        "text": (
            "In this level, you will build your income plan: "
            "choose one AI service you can offer, set your price, create a sample to show clients, "
            "and practise delivering it. "
            "By the end, you will have a real service ready to sell."
        ),
    },
    {
        "image": "img-l9-s08-celebration.jpg",
        "text": (
            "That is Level 9. You have turned your AI skills into income. "
            "Your service, your price, your first sample — all ready. "
            "Scroll down to build your income plan. "
            "See you in Level 10, the final level, where you take AI into the future."
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
    print(f"  source .env && aws s3 cp {OUT} s3://mitra-ai-life-assets/videos/level-09-intro.mp4 --content-type 'video/mp4' --cache-control 'public, max-age=86400'")

if __name__ == "__main__":
    generate_audio()
    build_video()
