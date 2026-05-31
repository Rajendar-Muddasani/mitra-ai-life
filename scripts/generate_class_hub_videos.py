"""
Generate class hub intro videos for Classes 7–12.
Each video: 5 scenes, ~90 seconds, voice: en-US-Chirp3-HD-Charon
Uses existing lesson hero images as scene backdrops.

Usage:
  python scripts/generate_class_hub_videos.py            # all 6 classes
  python scripts/generate_class_hub_videos.py --class 08 # single class
  python scripts/generate_class_hub_videos.py --class 07,10,12

Output: content/assets/students/class-NN/class-NN-intro-charon.mp4
Upload: s3://mitra-ai-life-assets/students/class-NN/class-NN-intro-charon.mp4
"""

import os, sys, argparse, base64
from pathlib import Path
import numpy as np
from PIL import Image
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

W, H, FPS = 1280, 720, 24
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0

# ---------------------------------------------------------------------------
# Scene data: 5 scenes per class.
# "image" is a relative path under content/assets/students/class-NN/
# ---------------------------------------------------------------------------
CLASS_DATA = {
    "07": {
        "title": "Class 7 — Prompting and Study Help",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 7 — Prompting and Study Help. "
                    "You already know AI can chat. In this class you learn to talk to AI like a pro. "
                    "A good prompt gets you a great answer. A vague prompt gets you nothing useful."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "Meet Priya. She was stuck on a history essay. "
                    "She typed 'write my essay' and got something boring and wrong. "
                    "Then she learned to prompt properly — give context, set the goal, ask for a format. "
                    "Same AI, ten times better answer."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "In Class 7 you will master prompting for homework, exam prep, science projects, and creative writing. "
                    "You will also learn why AI sometimes makes mistakes — and how to catch them before they catch you."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will use AI to summarise long chapters, create practice quiz questions, "
                    "and explain tough concepts in simple words. "
                    "Your study time will become more efficient every week."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "That is Class 7. Twelve lessons, all free, no sign-in needed. "
                    "By the end you will have a personal AI study toolkit you can use for every subject. "
                    "Scroll down and start Lesson 1 right now."
                ),
            },
        ],
    },
    "08": {
        "title": "Class 8 — Understanding AI Deeply",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 8 — Understanding AI Deeply. "
                    "You used AI in Class 7. Now it is time to understand what is happening inside it — "
                    "how it learns from data, and why it sometimes gets things completely wrong."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "Meet Arjun. He noticed AI gave different answers to the same question. Why? "
                    "In Class 8 you will find out — training data, patterns, bias, and confidence scores. "
                    "Understanding the machine makes you a far better user of it."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "You will write your very first Python code in this class. "
                    "Nothing scary — simple steps using Google Colab, which runs entirely in your browser. "
                    "No installation, no setup. Just open and start."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will train your first machine learning model, explore how AI makes decisions, "
                    "and learn what AI can and cannot do. "
                    "Real experiments, real data, real results — not just theory."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "Class 8 — twelve lessons, all free. "
                    "By the end you will know how AI learns, what bias means, "
                    "and how to run your own machine learning experiment from scratch. "
                    "Scroll down and start Lesson 1."
                ),
            },
        ],
    },
    "09": {
        "title": "Class 9 — Building with AI",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 9 — Building with AI. "
                    "You understood how AI works in Class 8. Now you start building with it. "
                    "A working classifier, a recommendation engine, a natural language app — all built by you."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "Meet Sneha. She built a spam detector for her school email system in two hours "
                    "using Python and scikit-learn. "
                    "No advanced degree. Just the right tools and a clear problem to solve."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "In Class 9 you will work with real datasets — customer reviews, product data, images, and text. "
                    "You will clean data, train models, and measure exactly how well they perform."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will call real AI APIs, build a simple web interface, "
                    "and deploy your first working model so other people can actually use it. "
                    "Everything runs in Google Colab — free and ready in your browser."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "Class 9 — twelve lessons, all free. "
                    "By the end you will have built three real AI applications "
                    "and have the skills to tackle any beginner AI project. "
                    "Scroll down and start Lesson 1."
                ),
            },
        ],
    },
    "10": {
        "title": "Class 10 — Advanced AI Projects",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 10 — Advanced AI Projects. "
                    "You can build AI apps. Now you go deeper — "
                    "convolutional neural networks, transformers, RAG chatbots, "
                    "and your own deployed AI product that the world can use."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "CNNs taught computers to recognise faces, read X-rays, and spot defects on a factory line. "
                    "In Class 10 you will build one yourself — "
                    "using transfer learning to fine-tune a model in under an hour."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "Transformers are behind ChatGPT, Google Search, and translation apps. "
                    "You will understand self-attention and fine-tune a small language model "
                    "for Indian text using Hugging Face — in Colab, for free."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will build a RAG chatbot that answers questions from your own documents, "
                    "create a REST API with FastAPI, "
                    "and deploy a web app on Streamlit Cloud for the world to see and use."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "Class 10 — twelve lessons, all free. "
                    "Your capstone is a complete end-to-end AI product: "
                    "dataset, model, API, web app, and a public GitHub link. "
                    "Scroll down and start Lesson 1."
                ),
            },
        ],
    },
    "11": {
        "title": "Class 11 — AI for Competitive Success",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 11 — AI for Competitive Success. "
                    "You have built real AI. Now you sharpen for competitive exams, olympiads, "
                    "and university applications — with AI as your training partner."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "AI can generate practice problems at exactly the difficulty you need. "
                    "It can explain why you got something wrong, suggest the next topic to study, "
                    "and simulate an oral interview. "
                    "You will set up this personalised system for yourself."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "In Class 11 you will use advanced NLP, build recommendation systems, "
                    "work with time-series data, and create explainable AI models that show their reasoning. "
                    "These are skills valued in every entrance exam and internship interview."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will also build your first public technical project — "
                    "documented, tested, and posted on GitHub. "
                    "Recruiters and universities look for exactly this kind of evidence."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "Class 11 — twelve lessons, all free. "
                    "By the end you will have a study system powered by AI "
                    "and a GitHub profile that makes you stand out. "
                    "Scroll down and start Lesson 1."
                ),
            },
        ],
    },
    "12": {
        "title": "Class 12 — AI Career Launch",
        "scenes": [
            {
                "image": "lesson-01-hero.jpg",
                "text": (
                    "Welcome to Class 12 — AI Career Launch. "
                    "This is your final class and your launch pad. "
                    "Portfolio projects, open-source contributions, internship applications, "
                    "and your own AI startup idea — it all comes together here."
                ),
            },
            {
                "image": "lesson-02-hero.jpg",
                "text": (
                    "Employers and universities now expect students to show projects, not just marks. "
                    "In Class 12 you will build three flagship projects — "
                    "each with a live demo URL, a clean GitHub repo, and a one-minute video walkthrough."
                ),
            },
            {
                "image": "lesson-03-hero.jpg",
                "text": (
                    "You will study large language models, responsible AI, AI regulation in India, "
                    "and how to navigate the ethical questions every AI builder faces in the real world."
                ),
            },
            {
                "image": "lesson-04-hero.jpg",
                "text": (
                    "You will write your first open-source pull request, "
                    "contribute to a real project, "
                    "and prepare for technical interviews at top companies and research programs."
                ),
            },
            {
                "image": "lesson-05-hero.jpg",
                "text": (
                    "Class 12 — twelve lessons, all free. "
                    "After this class you are not just an AI student — "
                    "you are an AI builder with a portfolio, a GitHub profile, and a career plan. "
                    "Scroll down and start Lesson 1."
                ),
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_paths(cls: str):
    asset_dir = ROOT / "content" / "assets" / "students" / f"class-{cls}"
    audio_dir = ROOT / "content" / "assets" / "students" / f"class-{cls}" / f"audio_tmp{VERSION_SUFFIX}"
    out_file  = ROOT / "content" / "assets" / "students" / f"class-{cls}" / f"class-{cls}-intro{VERSION_SUFFIX}.mp4"
    return asset_dir, audio_dir, out_file


def generate_audio(cls: str):
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    asset_dir, audio_dir, _ = get_paths(cls)
    audio_dir.mkdir(parents=True, exist_ok=True)
    scenes = CLASS_DATA[cls]["scenes"]
    print(f"  [{cls}] Generating TTS for {len(scenes)} scenes...")
    for i, sc in enumerate(scenes, 1):
        path = audio_dir / f"scene-{i:02d}.mp3"
        if path.exists():
            print(f"    Scene {i}: skip (exists)")
            continue
        preview = sc["text"][:55].replace("\n", " ")
        print(f"    Scene {i}: {preview}...")
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=sc["text"]),
            voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANGUAGE_CODE, name=TTS_VOICE),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=TTS_SPEAKING_RATE,
            ),
            timeout=45,
        )
        path.write_bytes(response.audio_content)
    print(f"  [{cls}] Audio done.\n")


def make_zoom_clip(img_path: Path, duration: float):
    from moviepy import ImageClip
    img = Image.open(img_path).convert("RGB")
    iw, ih = img.size
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (15, 23, 42))   # dark navy bg
    canvas.paste(img, ((W - nw) // 2, (H - nh) // 2))
    frame0 = np.array(canvas)

    def zoom_frame(get_frame, t):
        f = get_frame(t)
        s = 1.0 + 0.04 * (float(t) / duration)
        h, w = f.shape[:2]
        nw2, nh2 = int(w * s), int(h * s)
        zoomed = Image.fromarray(f).resize((nw2, nh2), Image.LANCZOS)
        ox, oy = (nw2 - w) // 2, (nh2 - h) // 2
        return np.array(zoomed.crop((ox, oy, ox + w, oy + h)))

    clip = ImageClip(frame0, duration=duration)
    return clip.transform(zoom_frame, apply_to="video")


def build_video(cls: str):
    from moviepy import AudioFileClip, concatenate_videoclips
    asset_dir, audio_dir, out_file = get_paths(cls)
    scenes = CLASS_DATA[cls]["scenes"]
    print(f"  [{cls}] Building video clips...")
    clips = []
    for i, sc in enumerate(scenes, 1):
        img_path = asset_dir / sc["image"]
        audio    = AudioFileClip(str(audio_dir / f"scene-{i:02d}.mp3"))
        dur      = audio.duration + 0.4
        clip     = make_zoom_clip(img_path, dur).with_audio(audio)
        clips.append(clip)
        print(f"    Scene {i}: {dur:.1f}s  ({sc['image']})")

    final = concatenate_videoclips(clips, method="compose")
    print(f"\n  [{cls}] Writing → {out_file.name}  ({int(final.duration)}s)")
    final.write_videofile(
        str(out_file), fps=FPS, codec="libx264", audio_codec="aac",
        temp_audiofile=str(audio_dir / "final_audio.m4a"),
        remove_temp=True, logger="bar",
    )
    print(f"  [{cls}] ✅  {out_file}\n")
    return out_file


def process_class(cls: str):
    print(f"\n{'='*60}")
    print(f"  CLASS {cls}: {CLASS_DATA[cls]['title']}")
    print(f"{'='*60}")
    generate_audio(cls)
    out = build_video(cls)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--class", dest="classes", default="",
                        help="Comma-separated class numbers, e.g. 07,10 (default: all)")
    args = parser.parse_args()

    if args.classes:
        targets = [c.strip().zfill(2) for c in args.classes.split(",")]
    else:
        targets = ["07", "08", "09", "10", "11", "12"]

    for cls in targets:
        if cls not in CLASS_DATA:
            print(f"Unknown class: {cls}")
            sys.exit(1)

    outputs = []
    for cls in targets:
        out = process_class(cls)
        outputs.append((cls, out))

    print("\n" + "="*60)
    print("ALL DONE")
    print("="*60)
    for cls, out in outputs:
        size_mb = out.stat().st_size / 1_000_000 if out.exists() else 0
        print(f"  class-{cls}: {out.name}  ({size_mb:.1f} MB)")

    print("\nUpload to S3:")
    for cls, out in outputs:
        print(f"  aws s3 cp {out} s3://mitra-ai-life-assets/students/class-{cls}/class-{cls}-intro{VERSION_SUFFIX}.mp4 \\")
        print(f"    --content-type 'video/mp4' --cache-control 'public, max-age=86400'")
