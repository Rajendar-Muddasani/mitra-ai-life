"""
Generate Class 6 lesson overview videos.

Produces:
- content/assets/students/class-06/lesson-02-overview-charon.mp4
- content/assets/students/class-06/lesson-03-overview-charon.mp4

Uses Google Cloud TTS en-US-Chirp3-HD-Charon and local Class 6 hero images.
"""

import os
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips


env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


ROOT = Path(__file__).parent.parent
ASSET_DIR = ROOT / "content" / "assets" / "students" / "class-06"
VERSION_SUFFIX = "-charon"
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_SPEAKING_RATE = 1.0
VIDEO_W, VIDEO_H = 1280, 720
FPS = 24

os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()


LESSONS = {
    "02": {
        "badge": "Class 6 - Lesson 2",
        "title": "AI Around You",
        "image": "lesson-02-hero.jpg",
        "audio_dir": ASSET_DIR / f"audio_tmp_lesson-02{VERSION_SUFFIX}",
        "output": ASSET_DIR / f"lesson-02-overview{VERSION_SUFFIX}.mp4",
        "s3_key": f"students/class-06/lesson-02-overview{VERSION_SUFFIX}.mp4",
        "scenes": [
            {
                "title": "AI is already around you",
                "bullets": ["Apps quietly learn from actions", "Spot AI before it guides you", "Use every tool with intention"],
                "text": (
                    "Welcome to Class 6 Lesson 2, AI Around You. In this short overview, Anu notices AI in the apps she uses every day. "
                    "You will learn to spot AI before it silently guides your choices."
                ),
            },
            {
                "title": "YouTube recommendations",
                "bullets": ["Watch time is a signal", "Similar viewers shape suggestions", "Rabbit holes need a timer"],
                "text": (
                    "YouTube recommends videos by studying watch time, clicks, and what similar viewers enjoyed. This can help you learn, but it can also pull you into a rabbit hole. "
                    "Before you open YouTube, decide what you came to watch."
                ),
            },
            {
                "title": "Search, maps, and routes",
                "bullets": ["Search reads meaning", "Maps predicts traffic", "Important answers need checking"],
                "text": (
                    "Google Search uses AI to understand meaning, not only keywords. Google Maps predicts traffic using GPS speed, history, and events. "
                    "These tools are useful, but important answers and routes should still be checked."
                ),
            },
            {
                "title": "Everyday smart helpers",
                "bullets": ["Face unlock recognises patterns", "Keyboards predict words", "Weather apps read sensor data"],
                "text": (
                    "Face unlock, predictive keyboards, and weather apps are also AI systems. They recognise patterns, make predictions, and help you act faster. "
                    "They are helpful, but they can still make mistakes."
                ),
            },
            {
                "title": "Privacy and filter bubbles",
                "bullets": ["Check app permissions", "Verify before forwarding", "Look for different viewpoints"],
                "text": (
                    "Recommendation AI can show one side again and again until you stop seeing other views. This is called a filter bubble. "
                    "Check privacy permissions, verify WhatsApp forwards, and deliberately look for different viewpoints."
                ),
            },
            {
                "title": "Your AI spy challenge",
                "bullets": ["List the app or tool", "Write what AI did", "Decide whether it helped"],
                "text": (
                    "Your challenge is to keep an AI spy list for one day. Write the app or tool, what the AI did, and whether it helped. "
                    "Smart users spot AI, use it with intention, and verify important information."
                ),
            },
        ],
    },
    "03": {
        "badge": "Class 6 - Lesson 3",
        "title": "How AI Learns",
        "image": "lesson-03-hero.jpg",
        "audio_dir": ASSET_DIR / f"audio_tmp_lesson-03{VERSION_SUFFIX}",
        "output": ASSET_DIR / f"lesson-03-overview{VERSION_SUFFIX}.mp4",
        "s3_key": f"students/class-06/lesson-03-overview{VERSION_SUFFIX}.mp4",
        "scenes": [
            {
                "title": "AI learns from examples",
                "bullets": ["No rule list for every case", "Examples reveal patterns", "This is machine learning"],
                "text": (
                    "Welcome to Class 6 Lesson 3, How AI Learns. You will see why AI can recognise faces, suggest videos, and predict rain without humans writing every rule. "
                    "The key idea is learning from examples."
                ),
            },
            {
                "title": "Machine learning in simple words",
                "bullets": ["Study many examples", "Find the pattern", "Try the pattern on new cases"],
                "text": (
                    "Machine learning means learning from examples. Like a child seeing many cat and dog pictures, AI studies labelled examples and finds patterns. "
                    "Then it tries to use those patterns on new examples it has never seen before."
                ),
            },
            {
                "title": "Training data and labels",
                "bullets": ["Data is the AI textbook", "Labels give the right answer", "Humans still teach the system"],
                "text": (
                    "Training data is the textbook the AI studies. Labels tell the AI the right answer for each example. "
                    "Humans tag photos, text, and audio so the AI can learn from them. Better data usually means better AI."
                ),
            },
            {
                "title": "Guess, check, adjust",
                "bullets": ["The model makes a guess", "Wrong answers adjust weights", "Repeating builds skill"],
                "text": (
                    "During training, the model makes a guess, checks the correct answer, and adjusts tiny internal weights. "
                    "It repeats this many times until the pattern works on new examples, not only on the examples it memorised."
                ),
            },
            {
                "title": "Testing and accuracy",
                "bullets": ["Keep a hidden test set", "Measure on new examples", "Ask what accuracy really means"],
                "text": (
                    "Testing is how engineers know whether the AI learned well. They keep a test set hidden during training, then measure performance on those unseen examples. "
                    "Accuracy numbers are useful, but you must ask what task and what data they describe."
                ),
            },
            {
                "title": "Bias and overfitting",
                "bullets": ["Incomplete data creates unfair results", "Memorising is not understanding", "Indian context data matters"],
                "text": (
                    "Bias happens when training data does not represent everyone fairly. Overfitting happens when a model memorises too much and fails on new examples. "
                    "For India, local language data and local context data matter a lot."
                ),
            },
            {
                "title": "Hands-on activity",
                "bullets": ["Sort shapes without rules", "Use examples to guess", "More examples improve accuracy"],
                "text": (
                    "In the hands-on activity, you sort shapes without knowing the rule. That is supervised machine learning in miniature. "
                    "You study examples, make a guess, test your guess, and learn why more examples usually improve accuracy."
                ),
            },
        ],
    },
}


def load_font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for font_path in candidates:
        if Path(font_path).exists():
            return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


FONT_BADGE = load_font(26, bold=True)
FONT_TITLE = load_font(54, bold=True)
FONT_BODY = load_font(34)
FONT_FOOTER = load_font(22, bold=True)


def cover_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image_w, image_h = image.size
    scale = max(VIDEO_W / image_w, VIDEO_H / image_h)
    resized = image.resize((int(image_w * scale), int(image_h * scale)), Image.LANCZOS)
    left = (resized.width - VIDEO_W) // 2
    top = (resized.height - VIDEO_H) // 2
    return resized.crop((left, top, left + VIDEO_W, top + VIDEO_H))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int, font: ImageFont.ImageFont, fill, line_gap: int) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def make_frame(lesson: dict, scene: dict, scene_index: int, total_scenes: int) -> np.ndarray:
    base = cover_image(ASSET_DIR / lesson["image"]).convert("RGBA")

    shade = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 70))
    base.alpha_composite(shade)

    gradient = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for x in range(0, 690):
        alpha = int(170 * (1 - x / 690))
        gradient_draw.line([(x, 0), (x, VIDEO_H)], fill=(2, 6, 23, alpha))
    base.alpha_composite(gradient)

    overlay = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((56, 60, 642, 656), radius=28, fill=(8, 20, 36, 220), outline=(56, 189, 248, 145), width=2)
    draw.rounded_rectangle((86, 90, 336, 132), radius=20, fill=(14, 165, 233, 220))
    draw.text((106, 99), lesson["badge"].upper(), font=FONT_BADGE, fill=(240, 249, 255, 255))
    draw.text((86, 155), f"{scene_index:02d}/{total_scenes:02d}", font=FONT_FOOTER, fill=(125, 211, 252, 255))

    y = 195
    title_lines = wrap_text(draw, scene["title"], FONT_TITLE, 500)
    y = draw_text_lines(draw, title_lines, 86, y, FONT_TITLE, (255, 255, 255, 255), 12)
    y += 20

    for bullet in scene["bullets"]:
        bullet_lines = wrap_text(draw, bullet, FONT_BODY, 455)
        draw.ellipse((90, y + 12, 108, y + 30), fill=(34, 197, 94, 255))
        y = draw_text_lines(draw, bullet_lines, 126, y, FONT_BODY, (226, 232, 240, 255), 8)
        y += 14

    draw.text((86, 610), "Mitra AI Life", font=FONT_FOOTER, fill=(186, 230, 253, 255))
    base.alpha_composite(overlay)
    return np.array(base.convert("RGB"))


def generate_audio(lesson_id: str, lesson: dict):
    from google.cloud import texttospeech

    audio_dir = lesson["audio_dir"]
    audio_dir.mkdir(parents=True, exist_ok=True)
    client = texttospeech.TextToSpeechClient()
    audio_files = []
    print(f"Step 1: Generating TTS for Lesson {lesson_id}...")
    for index, scene in enumerate(lesson["scenes"], 1):
        audio_path = audio_dir / f"scene-{index:02d}.mp3"
        if audio_path.exists():
            print(f"  [{index}/{len(lesson['scenes'])}] Skipping (exists): {audio_path.name}")
        else:
            preview = scene["text"][:68].replace("\n", " ")
            print(f"  [{index}/{len(lesson['scenes'])}] TTS: {preview}...")
            response = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=scene["text"]),
                voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANGUAGE_CODE, name=TTS_VOICE),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=TTS_SPEAKING_RATE,
                ),
                timeout=45,
            )
            audio_path.write_bytes(response.audio_content)
            print(f"    Saved: {audio_path.name}")
        audio_files.append(audio_path)
    return audio_files


def build_video(lesson_id: str, lesson: dict, audio_files: list[Path]):
    print(f"Step 2: Building Lesson {lesson_id} video...")
    clips = []
    for index, (scene, audio_path) in enumerate(zip(lesson["scenes"], audio_files), 1):
        print(f"  [{index}/{len(lesson['scenes'])}] {scene['title']}")
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration + 0.45
        frame = make_frame(lesson, scene, index, len(lesson["scenes"]))
        clip = ImageClip(frame, duration=duration)

        def zoom_frame(get_frame, t, clip_duration=duration):
            current_frame = get_frame(t)
            scale = 1.0 + 0.035 * (float(t) / clip_duration)
            height, width = current_frame.shape[:2]
            new_width, new_height = int(width * scale), int(height * scale)
            zoomed = Image.fromarray(current_frame).resize((new_width, new_height), Image.LANCZOS)
            x_offset = (new_width - width) // 2
            y_offset = (new_height - height) // 2
            return np.array(zoomed.crop((x_offset, y_offset, x_offset + width, y_offset + height)))

        clips.append(clip.transform(zoom_frame, apply_to="video").with_audio(audio))

    final = concatenate_videoclips(clips, method="compose")
    output = lesson["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Writing: {output}")
    final.write_videofile(
        str(output),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(lesson["audio_dir"] / "final_audio.m4a"),
        remove_temp=True,
        logger="bar",
    )
    print(f"Video ready: {output}")
    print(f"  Duration: {final.duration:.2f}s")
    print(f"  S3 key: s3://mitra-ai-life-assets/{lesson['s3_key']}")


def main():
    for lesson_id in sorted(LESSONS):
        lesson = LESSONS[lesson_id]
        audio_files = generate_audio(lesson_id, lesson)
        build_video(lesson_id, lesson, audio_files)


if __name__ == "__main__":
    main()