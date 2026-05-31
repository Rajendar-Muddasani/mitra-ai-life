"""
Generate narrated H1 Hindi sample-pack videos from the lesson manifest.

Inputs:
- content/tuition/hindi-foundation/manifests/h1-sample-pack.json
- local deterministic frame cards rendered at runtime from lesson data

Outputs:
- content/assets/videos/hindi-h1/h1-01-intro.mp4

Run:
- /Users/rajendarmuddasani/Mitra_AI_Life/.venv/bin/python scripts/generate_h1_sample_pack_videos.py --lesson H1-01
- /Users/rajendarmuddasani/Mitra_AI_Life/.venv/bin/python scripts/generate_h1_sample_pack_videos.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path


ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "content" / "tuition" / "hindi-foundation" / "manifests" / "h1-sample-pack.json"
SHARED_CONTENT = ROOT / "content" / "tuition" / "hindi-foundation" / "manifests" / "h1-shared-content.json"
SCENES_DIR = ROOT / "content" / "assets" / "scenes" / "hindi-h1"
VIDEO_DIR = ROOT / "content" / "assets" / "videos" / "hindi-h1"
VIDEO_W = 1280
VIDEO_H = 720
FPS = 24
FRAME_DIR = VIDEO_DIR / "frame_cards"
DEVANAGARI_FONT = Path("/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc")
LATIN_FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

THEME_COLORS = {
    "sunrise": {"bg_a": "#fff7d3", "bg_b": "#ffca66", "text": "#1f1609", "muted": "#5d4824", "chip_bg": "#fff9e6"},
    "ocean": {"bg_a": "#dff7ff", "bg_b": "#5cc8ff", "text": "#122039", "muted": "#1f4160", "chip_bg": "#eefcff"},
    "berry": {"bg_a": "#ffe0ef", "bg_b": "#ff8cbc", "text": "#3d1830", "muted": "#6b3656", "chip_bg": "#fff0f7"},
    "mint": {"bg_a": "#e8ffe9", "bg_b": "#8ce99a", "text": "#14301b", "muted": "#32543c", "chip_bg": "#f3fff4"},
    "midnight": {"bg_a": "#10224a", "bg_b": "#244a8f", "text": "#f8fbff", "muted": "#d6e6ff", "chip_bg": "#365eaa"},
}


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        raise FileNotFoundError(f"No .env file found at {env_path}")

    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_shared_content() -> dict:
    return json.loads(SHARED_CONTENT.read_text(encoding="utf-8"))


def normalize_lesson_id(lesson_id: str) -> str:
    return lesson_id.lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Hindi H1 narrated videos.")
    parser.add_argument("--lesson", nargs="*", help="Optional lesson IDs, for example H1-01 H1-02")
    parser.add_argument("--dry-run", action="store_true", help="Print planned video jobs without TTS or rendering")
    parser.add_argument("--voice", default="nova", help="OpenAI TTS voice")
    parser.add_argument("--tts-model", default="tts-1", help="OpenAI TTS model")
    return parser.parse_args()


def get_openai_client():
    from openai import OpenAI

    if api_key := os.environ.get("OPENAI_API_KEY"):
        return OpenAI(api_key=api_key)
    raise RuntimeError("OPENAI_API_KEY is not set")


def lesson_jobs(manifest: dict, selected_lessons: set[str] | None) -> list[dict]:
    jobs: list[dict] = []
    for lesson in manifest["lessons"]:
        lesson_id = lesson["id"]
        if selected_lessons and lesson_id not in selected_lessons:
            continue

        jobs.append(
            {
                "lesson": lesson,
                "slug": normalize_lesson_id(lesson_id),
                "audio_dir": VIDEO_DIR / "audio_tmp" / normalize_lesson_id(lesson_id),
                "video_out": VIDEO_DIR / f"{normalize_lesson_id(lesson_id)}-intro.mp4",
            }
        )
    return jobs


def image_path(slug: str, scene_number: int) -> Path:
    return SCENES_DIR / f"{slug}-s{scene_number:02d}.jpg"


def frame_card_path(slug: str, scene_number: int) -> Path:
    return FRAME_DIR / f"{slug}-s{scene_number:02d}.png"


def font_path(path: Path) -> str:
    if path.exists():
        return str(path)
    raise FileNotFoundError(f"Font file not found: {path}")


def rounded_rect(draw, bounds: tuple[int, int, int, int], radius: int, fill: str) -> None:
    draw.rounded_rectangle(bounds, radius=radius, fill=fill)


def render_frame_cards(job: dict) -> list[Path]:
    from PIL import Image, ImageDraw, ImageFont

    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    devanagari_font = ImageFont.truetype(font_path(DEVANAGARI_FONT), 72)
    devanagari_small = ImageFont.truetype(font_path(DEVANAGARI_FONT), 34)
    latin_title = ImageFont.truetype(font_path(LATIN_FONT), 30)
    latin_body = ImageFont.truetype(font_path(LATIN_FONT), 24)
    latin_chip = ImageFont.truetype(font_path(LATIN_FONT), 24)

    card_paths: list[Path] = []
    lesson_id = job["lesson"]["id"]
    shared = load_shared_content()[lesson_id]
    frames = {int(board["sceneNumber"]): board for board in shared["scenes"]["boards"] if "sceneNumber" in board}

    for scene in job["lesson"]["videoScenes"]:
        scene_number = int(scene["scene"])
        layout = frames[scene_number]
        colors = THEME_COLORS[layout["theme"]]
        out_path = frame_card_path(job["slug"], scene_number)

        image = Image.new("RGB", (VIDEO_W, VIDEO_H), colors["bg_a"])
        draw = ImageDraw.Draw(image)

        for y in range(VIDEO_H):
            ratio = y / max(VIDEO_H - 1, 1)
            start = tuple(int(colors["bg_a"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            end = tuple(int(colors["bg_b"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            blended = tuple(int(start[i] * (1 - ratio) + end[i] * ratio) for i in range(3))
            draw.line((0, y, VIDEO_W, y), fill=blended)

        rounded_rect(draw, (56, 40, 290, 92), 26, colors["chip_bg"])
        rounded_rect(draw, (998, 40, 1224, 92), 26, colors["chip_bg"])
        draw.text((84, 54), layout["label"], font=latin_chip, fill=colors["text"])
        draw.text((1016, 54), layout["badge"], font=latin_chip, fill=colors["text"])

        draw.text((86, 170), layout["title"], font=latin_title, fill=colors["text"])
        draw.text((86, 250), layout["hindi"], font=devanagari_font, fill=colors["text"])
        draw.multiline_text((86, 360), layout["caption"], font=latin_body, fill=colors["muted"], spacing=8)

        chip_x = 86
        chip_y = 585
        for chip in layout["chips"]:
            chip_font = devanagari_small if any("\u0900" <= char <= "\u097F" for char in chip) else latin_chip
            bbox = draw.textbbox((0, 0), chip, font=chip_font)
            chip_w = (bbox[2] - bbox[0]) + 34
            rounded_rect(draw, (chip_x, chip_y, chip_x + chip_w, chip_y + 48), 22, colors["chip_bg"])
            draw.text((chip_x + 17, chip_y + 9), chip, font=chip_font, fill=colors["text"])
            chip_x += chip_w + 14

        image.save(out_path, format="PNG")
        card_paths.append(out_path)

    return card_paths


def generate_audio(job: dict, client, voice: str, tts_model: str) -> list[Path]:
    audio_files: list[Path] = []
    audio_dir = job["audio_dir"]
    audio_dir.mkdir(parents=True, exist_ok=True)

    for scene in job["lesson"]["videoScenes"]:
        scene_number = int(scene["scene"])
        audio_path = audio_dir / f"scene-{scene_number:02d}.mp3"
        if audio_path.exists():
            print(f"  [SKIP] {job['lesson']['id']} scene {scene_number:02d} audio")
        else:
            print(f"  [TTS] {job['lesson']['id']} scene {scene_number:02d}")
            with client.audio.speech.with_streaming_response.create(
                model=tts_model,
                voice=voice,
                input=scene["narration"],
                speed=0.95,
            ) as response:
                response.stream_to_file(str(audio_path))
            time.sleep(1)
        audio_files.append(audio_path)

    return audio_files


def make_scene_clip(image_file: Path, audio_file: Path):
    from moviepy import AudioFileClip, ImageClip
    from PIL import Image
    import numpy as np

    source = Image.open(image_file).convert("RGB")
    input_width, input_height = source.size
    scale = max(VIDEO_W / input_width, VIDEO_H / input_height)
    source = source.resize((int(input_width * scale), int(input_height * scale)), Image.LANCZOS)

    left = (source.width - VIDEO_W) // 2
    top = (source.height - VIDEO_H) // 2
    source = source.crop((left, top, left + VIDEO_W, top + VIDEO_H))
    frame = np.array(source)

    audio = AudioFileClip(str(audio_file))
    duration = audio.duration + 0.4
    clip = ImageClip(frame, duration=duration)

    def zoom_frame(get_frame, current_time):
        frame_data = get_frame(current_time)
        scale_factor = 1.0 + 0.04 * (float(current_time) / duration)
        height, width = frame_data.shape[:2]
        zoomed_width = int(width * scale_factor)
        zoomed_height = int(height * scale_factor)
        zoomed = Image.fromarray(frame_data).resize((zoomed_width, zoomed_height), Image.LANCZOS)
        offset_x = (zoomed_width - width) // 2
        offset_y = (zoomed_height - height) // 2
        return np.array(zoomed.crop((offset_x, offset_y, offset_x + width, offset_y + height)))

    return clip.transform(zoom_frame, apply_to="video").with_audio(audio)


def render_video(job: dict, audio_files: list[Path]) -> None:
    import imageio_ffmpeg
    from moviepy import concatenate_videoclips

    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_bin

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    frame_cards = render_frame_cards(job)
    clips = [make_scene_clip(frame_card, audio_file) for frame_card, audio_file in zip(frame_cards, audio_files)]

    final = concatenate_videoclips(clips, method="compose")
    temp_audio = job["audio_dir"] / "final_audio.m4a"
    print(f"  Writing {job['video_out']}")
    final.write_videofile(
        str(job["video_out"]),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(temp_audio),
        remove_temp=True,
        logger="bar",
    )


def main() -> None:
    args = parse_args()
    manifest = load_manifest()
    selected_lessons = set(args.lesson) if args.lesson else None
    jobs = lesson_jobs(manifest, selected_lessons)

    if not jobs:
        raise SystemExit("No video jobs matched the requested lessons.")

    if args.dry_run:
        for job in jobs:
            print(f"{job['lesson']['id']} -> {job['video_out']}")
            for scene in job["lesson"]["videoScenes"]:
                scene_number = int(scene["scene"])
                print(f"  scene {scene_number:02d}: {frame_card_path(job['slug'], scene_number)}")
        print(f"\nDry run only. Planned lesson videos: {len(jobs)}")
        return

    load_env()
    client = get_openai_client()

    for job in jobs:
        print(f"\nBuilding {job['lesson']['id']} — {job['lesson']['title']}")
        audio_files = generate_audio(job, client, voice=args.voice, tts_model=args.tts_model)
        render_video(job, audio_files)


if __name__ == "__main__":
    main()