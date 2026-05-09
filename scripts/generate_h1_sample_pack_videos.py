"""
Generate narrated H1 Hindi sample-pack videos from the lesson manifest.

Inputs:
- content/tuition/hindi-foundation/manifests/h1-sample-pack.json
- content/assets/scenes/hindi-h1/h1-01-s01.jpg ...

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
SCENES_DIR = ROOT / "content" / "assets" / "scenes" / "hindi-h1"
VIDEO_DIR = ROOT / "content" / "assets" / "videos" / "hindi-h1"
VIDEO_W = 1280
VIDEO_H = 720
FPS = 24


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

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


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


def ensure_scene_images(job: dict) -> None:
    missing: list[str] = []
    for scene in job["lesson"]["videoScenes"]:
        path = image_path(job["slug"], int(scene["scene"]))
        if not path.exists():
            missing.append(str(path))

    if missing:
        joined = "\n".join(missing)
        raise FileNotFoundError(
            f"Missing scene images for {job['lesson']['id']}. Generate images first:\n{joined}"
        )


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
            response = client.audio.speech.create(
                model=tts_model,
                voice=voice,
                input=scene["narration"],
                speed=0.95,
            )
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
    clips = []
    for scene, audio_file in zip(job["lesson"]["videoScenes"], audio_files):
        scene_number = int(scene["scene"])
        clips.append(make_scene_clip(image_path(job["slug"], scene_number), audio_file))

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
                print(f"  scene {scene_number:02d}: {image_path(job['slug'], scene_number)}")
        print(f"\nDry run only. Planned lesson videos: {len(jobs)}")
        return

    load_env()
    client = get_openai_client()

    for job in jobs:
        print(f"\nBuilding {job['lesson']['id']} — {job['lesson']['title']}")
        ensure_scene_images(job)
        audio_files = generate_audio(job, client, voice=args.voice, tts_model=args.tts_model)
        render_video(job, audio_files)


if __name__ == "__main__":
    main()