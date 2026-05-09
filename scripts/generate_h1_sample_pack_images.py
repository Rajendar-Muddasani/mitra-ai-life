"""
Generate H1 Hindi sample-pack images from the lesson manifest.

Outputs:
- content/assets/scenes/hindi-h1/h1-01-hero.jpg
- content/assets/scenes/hindi-h1/h1-01-s01.jpg ...

Run:
- /Users/rajendarmuddasani/Mitra_AI_Life/.venv/bin/python scripts/generate_h1_sample_pack_images.py
- /Users/rajendarmuddasani/Mitra_AI_Life/.venv/bin/python scripts/generate_h1_sample_pack_images.py --lesson H1-01
- /Users/rajendarmuddasani/Mitra_AI_Life/.venv/bin/python scripts/generate_h1_sample_pack_images.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "content" / "tuition" / "hindi-foundation" / "manifests" / "h1-sample-pack.json"
SCENES_DIR = ROOT / "content" / "assets" / "scenes" / "hindi-h1"
RATE_LIMIT_SLEEP = 13


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


def build_image_jobs(manifest: dict, selected_lessons: set[str] | None) -> list[dict]:
    jobs: list[dict] = []

    for lesson in manifest["lessons"]:
        lesson_id = lesson["id"]
        if selected_lessons and lesson_id not in selected_lessons:
            continue

        slug = normalize_lesson_id(lesson_id)
        jobs.append(
            {
                "lesson_id": lesson_id,
                "filename": f"{slug}-hero.jpg",
                "size": "1792x1024",
                "kind": "hero",
                "prompt": (
                    f"Hindi H1 lesson hero illustration for '{lesson['title']}'. "
                    f"Learning outcome: {lesson['learningOutcome']} "
                    f"Visual direction: {lesson['heroPrompt']} "
                    "Bright beginner-friendly Indian classroom atmosphere, child-safe, uncluttered, "
                    "educational illustration, no text overlays, no watermark."
                ),
            }
        )

        for scene in lesson["videoScenes"]:
            scene_number = int(scene["scene"])
            jobs.append(
                {
                    "lesson_id": lesson_id,
                    "filename": f"{slug}-s{scene_number:02d}.jpg",
                    "size": "1792x1024",
                    "kind": f"scene-{scene_number:02d}",
                    "prompt": (
                        f"Hindi H1 lesson scene illustration for '{lesson['title']}', scene {scene_number}. "
                        f"Purpose: {scene['purpose']}. "
                        f"Narration context: {scene['narration']} "
                        f"Visual prompt: {scene['visualPrompt']} "
                        "Use a clean 16:9 educational composition, child-safe Indian learning context, "
                        "large readable Devanagari when needed, no Latin text overlays, no watermark."
                    ),
                }
            )

    return jobs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Hindi H1 sample-pack images.")
    parser.add_argument("--lesson", nargs="*", help="Optional lesson IDs, for example H1-01 H1-02")
    parser.add_argument("--force", action="store_true", help="Regenerate images even if files exist")
    parser.add_argument("--dry-run", action="store_true", help="Print planned image jobs without calling OpenAI")
    return parser.parse_args()


def ensure_openai_client():
    from openai import OpenAI

    if api_key := os.environ.get("OPENAI_API_KEY"):
        return OpenAI(api_key=api_key)
    raise RuntimeError("OPENAI_API_KEY is not set")


def download(url: str, destination: Path) -> None:
    urllib.request.urlretrieve(url, destination)


def generate_jobs(jobs: list[dict], force: bool) -> None:
    client = ensure_openai_client()
    SCENES_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0

    print(f"\nHindi H1 image generation — {len(jobs)} assets\n{'-' * 58}")
    for index, job in enumerate(jobs, start=1):
        destination = SCENES_DIR / job["filename"]
        if destination.exists() and not force:
            print(f"[{index}/{len(jobs)}] SKIP {job['filename']} ({job['lesson_id']} {job['kind']})")
            skipped += 1
            continue

        print(f"[{index}/{len(jobs)}] GEN  {job['filename']} ({job['size']}) ...", end="", flush=True)
        response = client.images.generate(
            model="dall-e-3",
            prompt=job["prompt"],
            size=job["size"],
            quality="standard",
            n=1,
        )
        download(response.data[0].url, destination)
        print(f" OK {destination.stat().st_size // 1024} KB")
        generated += 1

        if index < len(jobs):
            print(f"    waiting {RATE_LIMIT_SLEEP}s for rate limit")
            time.sleep(RATE_LIMIT_SLEEP)

    print(f"\nDone. Generated: {generated} | Skipped: {skipped} | Total: {len(jobs)}")
    print(f"Assets directory: {SCENES_DIR}")


def main() -> None:
    args = parse_args()
    manifest = load_manifest()
    selected_lessons = set(args.lesson) if args.lesson else None
    jobs = build_image_jobs(manifest, selected_lessons)

    if not jobs:
        raise SystemExit("No image jobs matched the requested lessons.")

    if args.dry_run:
        for job in jobs:
            print(f"{job['lesson_id']} {job['kind']}: {job['filename']}")
        print(f"\nDry run only. Planned assets: {len(jobs)}")
        return

    load_env()
    generate_jobs(jobs, force=args.force)


if __name__ == "__main__":
    main()