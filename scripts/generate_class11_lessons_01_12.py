#!/usr/bin/env python3
"""
Generate overview videos for Class 11 Lessons 01-12.
Usage:
    python3 scripts/generate_class11_lessons_01_12.py          # all lessons
    python3 scripts/generate_class11_lessons_01_12.py 01 02    # specific lessons
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import textwrap
from html import unescape
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from google.cloud import texttospeech
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips


env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT / "content" / "assets" / "students" / "class-11"
HTML_DIR = ROOT / "content" / "students" / "class-11"
S3_BUCKET = "mitra-ai-life-assets"
S3_PREFIX = "students/class-11"
VIDEO_W, VIDEO_H, FPS = 1280, 720, 24
TTS_LANG = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_RATE = 1.0
BADGE_COL = (217, 119, 6)
BULLET_COL = (251, 191, 36)
OUTLINE_COL = (245, 158, 11, 145)

ASCII_MAP = str.maketrans(
    {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "—": " - ",
        "–": " - ",
        "…": "...",
        "\u00a0": " ",
    }
)

try:
    FONT_TITLE = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52
    )
    FONT_BODY = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial.ttf", 28
    )
    FONT_BADGE = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18
    )
    FONT_FOOTER = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial.ttf", 20
    )
except OSError:
    FONT_TITLE = FONT_BODY = FONT_BADGE = FONT_FOOTER = ImageFont.load_default()


def _cover(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    scale = max(VIDEO_W / img.width, VIDEO_H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left = (img.width - VIDEO_W) // 2
    top = (img.height - VIDEO_H) // 2
    return img.crop((left, top, left + VIDEO_W, top + VIDEO_H))


def _wrap(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_w: int,
) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _put_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y: int,
    font: ImageFont.ImageFont,
    fill,
    gap: int,
) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + gap
    return y


def _make_frame(lesson_data: dict, scene: dict, idx: int, total: int) -> np.ndarray:
    base = _cover(ASSET_DIR / lesson_data["image"]).convert("RGBA")

    shade = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 70))
    base.alpha_composite(shade)

    grad = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for x in range(0, 690):
        alpha = int(170 * (1 - x / 690))
        gd.line([(x, 0), (x, VIDEO_H)], fill=(2, 6, 23, alpha))
    base.alpha_composite(grad)

    ov = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    drw = ImageDraw.Draw(ov)
    drw.rounded_rectangle(
        (56, 60, 642, 656),
        radius=28,
        fill=(69, 26, 3, 220),
        outline=OUTLINE_COL,
        width=2,
    )
    drw.rounded_rectangle((86, 90, 360, 132), radius=20, fill=(*BADGE_COL, 220))
    drw.text(
        (106, 99),
        lesson_data["badge"].upper(),
        font=FONT_BADGE,
        fill=(255, 251, 235, 255),
    )
    drw.text((86, 155), f"{idx:02d}/{total:02d}", font=FONT_FOOTER, fill=(253, 224, 71, 255))

    y = 195
    for line in _wrap(drw, scene["title"], FONT_TITLE, 500):
        drw.text((86, y), line, font=FONT_TITLE, fill=(255, 255, 255, 255))
        bbox = drw.textbbox((86, y), line, font=FONT_TITLE)
        y += (bbox[3] - bbox[1]) + 12
    y += 20

    for bullet in scene["bullets"]:
        lines = _wrap(drw, bullet, FONT_BODY, 455)
        drw.ellipse((90, y + 12, 108, y + 30), fill=(*BULLET_COL, 255))
        y = _put_lines(drw, lines, 126, y, FONT_BODY, (255, 247, 237, 255), 8)
        y += 14

    drw.text((86, 610), "Mitra AI Life", font=FONT_FOOTER, fill=(253, 224, 71, 255))
    base.alpha_composite(ov)
    return np.array(base.convert("RGB"))


def _find_div_block(html: str, marker: str, start: int = 0) -> tuple[str, int]:
    block_start = html.find(marker, start)
    if block_start == -1:
        return "", -1

    depth = 0
    i = block_start
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
        elif html.startswith("</div>", i):
            depth -= 1
            if depth == 0:
                return html[block_start : i + 6], i + 6
        i += 1
    raise ValueError(f"Could not find closing </div> for marker: {marker}")


def _extract_div_blocks(html: str, marker: str) -> list[str]:
    blocks: list[str] = []
    start = 0
    while True:
        block, start = _find_div_block(html, marker, start)
        if not block:
            return blocks
        blocks.append(block)


def _first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.S)
    return match.group(1) if match else ""


def _strip_html(text: str) -> str:
    text = text.translate(ASCII_MAP)
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clean_title(text: str) -> str:
    text = _strip_html(text)
    text = re.sub(r"^[^A-Za-z0-9]+", "", text)
    return text.strip()


def _extract_ordered_texts(block: str) -> list[str]:
    token_re = re.compile(
        r"<h3[^>]*>.*?</h3>|"
        r"<h4[^>]*>.*?</h4>|"
        r"<p[^>]*>.*?</p>|"
        r"<li[^>]*>.*?</li>|"
        r"<div class=\"callout[^\"]*\"[^>]*>.*?</div>",
        re.S,
    )
    texts: list[str] = []
    for match in token_re.finditer(block):
        text = _strip_html(match.group(0))
        if not text:
            continue
        texts.append(text)
    return texts


def _fallback_block_text(block: str, title: str) -> str:
    text = _strip_html(block)
    if title and text.startswith(title):
        text = text[len(title) :].strip()
    return text


def _sentence_candidates(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?])\s+", text)
    if len(pieces) == 1:
        pieces = re.split(r"\s+-\s+|;\s+|:\s+", text)
    cleaned: list[str] = []
    for piece in pieces:
        piece = piece.strip(" -")
        if len(piece.split()) < 3:
            continue
        cleaned.append(piece)
    return cleaned


def _build_scene_text(prefix: str, texts: list[str], max_chars: int = 460) -> str:
    candidates: list[str] = []
    if prefix:
        candidates.append(prefix)

    for text in texts:
        snippets = _sentence_candidates(text) or [text]
        for snippet in snippets:
            snippet = textwrap.shorten(snippet, width=150, placeholder="...")
            if snippet and snippet not in candidates:
                candidates.append(snippet)

    final: list[str] = []
    total = 0
    for snippet in candidates:
        sentence = snippet.rstrip(".?!") + "."
        if final and total + len(sentence) + 1 > max_chars:
            break
        final.append(sentence)
        total += len(sentence) + 1
    return " ".join(final)


def _build_bullets(title: str, texts: list[str]) -> list[str]:
    bullets: list[str] = []
    for text in texts:
        for snippet in _sentence_candidates(text) or [text]:
            bullet = textwrap.shorten(snippet, width=72, placeholder="...")
            if bullet and bullet not in bullets:
                bullets.append(bullet)
            if len(bullets) == 3:
                return bullets

    fallback = textwrap.shorten(title, width=72, placeholder="...")
    while len(bullets) < 3:
        bullets.append(fallback or "Understand the key idea step by step")
    return bullets[:3]


def _spread_indices(count: int, target: int) -> list[int]:
    if count <= target:
        return list(range(count))
    indices: list[int] = []
    for i in range(target):
        idx = round(i * (count - 1) / (target - 1))
        if idx not in indices:
            indices.append(idx)
    for idx in range(count):
        if len(indices) == target:
            break
        if idx not in indices:
            indices.append(idx)
    return sorted(indices)


def _parse_section(block: str) -> dict | None:
    title = _clean_title(
        _first_match(r'<div class="ls-title">(.*?)</div>', block)
        or _first_match(r"<h2>(.*?)</h2>", block)
    )
    if not title:
        return None

    texts = [text for text in _extract_ordered_texts(block) if text and text != title]
    fallback = _fallback_block_text(block, title)
    if len(" ".join(texts)) < 90 and fallback:
        texts.append(fallback)

    texts = [text for text in texts if text]
    if not texts:
        texts = [title]

    return {
        "title": title,
        "bullets": _build_bullets(title, texts),
        "text": _build_scene_text("", texts),
    }


def _build_intro_scene(
    lesson_id: str,
    title: str,
    description: str,
    section_blocks: list[str],
) -> tuple[dict, list[str]]:
    intro_prefix = f"Welcome to Class 11 Lesson {int(lesson_id)} - {title}"
    intro_texts = [description] if description else []
    remaining_blocks = section_blocks

    if section_blocks:
        first_block = section_blocks[0]
        section_label = _clean_title(_first_match(r'<div class="ls-label">(.*?)</div>', first_block))
        section_title = _clean_title(_first_match(r'<div class="ls-title">(.*?)</div>', first_block))
        first_texts = _extract_ordered_texts(first_block)
        fallback = _fallback_block_text(first_block, section_title)
        if len(" ".join(first_texts)) < 80 and fallback:
            first_texts.append(fallback)
        first_texts = [
            text for text in first_texts if text and text not in {section_label, section_title}
        ]

        if section_label:
            intro_texts.append(section_label)
        if section_title:
            intro_texts.append(section_title)
        intro_texts.extend(first_texts[:3])
        remaining_blocks = section_blocks[1:]

    intro_texts = [text for text in intro_texts if text]
    if not intro_texts:
        intro_texts = [title]

    return (
        {
            "title": title,
            "bullets": _build_bullets(title, intro_texts),
            "text": _build_scene_text(intro_prefix, intro_texts),
        },
        remaining_blocks,
    )


def load_lesson(lesson_id: str) -> dict:
    html_path = HTML_DIR / f"lesson-{lesson_id}.html"
    if not html_path.exists():
        raise FileNotFoundError(f"Missing lesson page: {html_path}")

    html = html_path.read_text(encoding="utf-8")
    title = _clean_title(_first_match(r"<h1>(.*?)</h1>", html))
    description = _strip_html(_first_match(r'<meta name="description" content="(.*?)"', html))
    image = _first_match(r'src="[^"]*/(lesson-\d{2}-hero\.jpg)"', html)
    if not image:
        raise ValueError(f"Could not find hero image in {html_path.name}")

    section_blocks = _extract_div_blocks(html, '<div class="lesson-section">')
    intro_scene, body_blocks = _build_intro_scene(lesson_id, title, description, section_blocks)

    parsed_sections = [section for block in body_blocks if (section := _parse_section(block))]
    chosen_sections = [
        parsed_sections[idx]
        for idx in _spread_indices(len(parsed_sections), min(4, len(parsed_sections)))
    ]

    return {
        "badge": f"CLASS 11 - LESSON {int(lesson_id)}",
        "title": title,
        "image": image,
        "scenes": [intro_scene, *chosen_sections],
    }


def generate(lesson_id: str) -> None:
    data = load_lesson(lesson_id)
    out = ASSET_DIR / f"lesson-{lesson_id}-overview-charon.mp4"
    aud_dir = ASSET_DIR / f"audio_tmp_lesson-{lesson_id}-charon"
    aud_dir.mkdir(parents=True, exist_ok=True)

    client = texttospeech.TextToSpeechClient()
    audio_files: list[Path] = []
    print(f"\n=== Lesson {lesson_id}: {data['title']} ===")
    print(f"Step 1: TTS ({len(data['scenes'])} scenes)...")
    for i, scene in enumerate(data["scenes"], 1):
        path = aud_dir / f"scene-{i:02d}.mp3"
        if path.exists():
            print(f"  [{i}] skip (cached): {path.name}")
        else:
            print(f"  [{i}] TTS: {scene['text'][:64]}...")
            resp = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=scene["text"]),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=TTS_LANG,
                    name=TTS_VOICE,
                ),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=TTS_RATE,
                ),
                timeout=45,
            )
            path.write_bytes(resp.audio_content)
            print(f"    saved: {path.name}")
        audio_files.append(path)

    print("Step 2: Building video...")
    total = len(data["scenes"])
    clips = []
    for i, (scene, aud) in enumerate(zip(data["scenes"], audio_files), 1):
        print(f"  [{i}/{total}] {scene['title']}")
        audio = AudioFileClip(str(aud))
        duration = audio.duration + 0.45
        frame = _make_frame(data, scene, i, total)
        clip = ImageClip(frame, duration=duration)

        def _zoom(get_frame, t, dur=duration):
            frame_img = get_frame(t)
            scale = 1.0 + 0.035 * (float(t) / dur)
            height, width = frame_img.shape[:2]
            zoomed = Image.fromarray(frame_img).resize(
                (int(width * scale), int(height * scale)),
                Image.LANCZOS,
            )
            ox, oy = (zoomed.width - width) // 2, (zoomed.height - height) // 2
            return np.array(zoomed.crop((ox, oy, ox + width, oy + height)))

        clips.append(clip.transform(_zoom, apply_to="video").with_audio(audio))

    final = concatenate_videoclips(clips, method="compose")
    print(f"Step 3: Writing {out.name} ...")
    final.write_videofile(
        str(out),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(aud_dir / "final_audio.m4a"),
        remove_temp=True,
        logger="bar",
    )
    print(f"Done: {out}  ({final.duration:.1f}s, {out.stat().st_size / 1024 / 1024:.1f} MB)")

    s3_key = f"{S3_PREFIX}/lesson-{lesson_id}-overview-charon.mp4"
    print(f"Step 4: Uploading to s3://{S3_BUCKET}/{s3_key} ...")
    result = subprocess.run(
        [
            "aws",
            "s3",
            "cp",
            str(out),
            f"s3://{S3_BUCKET}/{s3_key}",
            "--content-type",
            "video/mp4",
            "--cache-control",
            "public, max-age=86400",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  Uploaded OK: {s3_key}")
    else:
        print(f"  ERROR uploading: {result.stderr.strip()}")
        return

    embed_video_in_html(lesson_id, data["title"])


def embed_video_in_html(lesson_id: str, lesson_title: str) -> None:
    html_path = HTML_DIR / f"lesson-{lesson_id}.html"
    if not html_path.exists():
        print(f"  HTML not found: {html_path}")
        return

    html = html_path.read_text(encoding="utf-8")
    if "<video" in html:
        print(f"  HTML already has <video>: {html_path.name}")
        return

    s3_url = (
        f"https://{S3_BUCKET}.s3.us-west-2.amazonaws.com/"
        f"{S3_PREFIX}/lesson-{lesson_id}-overview-charon.mp4"
    )
    poster_url = (
        f"https://{S3_BUCKET}.s3.us-west-2.amazonaws.com/"
        f"{S3_PREFIX}/lesson-{lesson_id}-hero.jpg"
    )
    video_box = (
        '<div class="video-box">\n'
        f'      <video controls preload="none" poster="{poster_url}">\n'
        f'        <source src="{s3_url}" type="video/mp4">\n'
        '        Your browser does not support the video tag.\n'
        '      </video>\n'
        '    </div>'
    )
    section_html = (
        '\n<section class="lesson-video">\n'
        '  <div style="width:90%;max-width:760px;margin:0 auto;">\n'
        '    <div class="sec-label">Watch first - 2-3 minutes</div>\n'
        f'    <h2>Class 11 Lesson {int(lesson_id)} - {lesson_title}</h2>\n'
        f'    {video_box}\n'
        '    <p class="video-caption">No sign-in needed - English narration - Safe for all school ages</p>\n'
        '  </div>\n'
        '</section>\n'
    )

    video_css = (
        ".lesson-video{background:#78350f;padding:2.5rem 1rem;color:#fff;margin:0;}\n"
        ".lesson-video .sec-label{font-size:.72rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#fbbf24;margin-bottom:.5rem;text-align:center}\n"
        ".lesson-video h2{color:#fff;font-family:'Baloo 2',cursive;font-size:1.4rem;text-align:center;margin-bottom:1.2rem}\n"
        ".video-caption{color:rgba(255,255,255,.62);font-size:.78rem;text-align:center;margin-top:.7rem}\n"
        ".video-box{position:relative;width:100%;max-width:820px;margin:0 auto;padding-top:56.25%;border-radius:14px;overflow:hidden;background:#020617;border:2px solid rgba(245,158,11,.45)}\n"
        ".video-box video{position:absolute;inset:0;width:100%;height:100%;display:block;background:#020617}\n"
    )

    if ".lesson-video{" not in html:
        if ".content-wrap{" in html:
            html = html.replace(".content-wrap{", video_css + ".content-wrap{", 1)
        else:
            html = html.replace("</style>", video_css + "</style>", 1)

    hero_match = re.search(r'(<img[^>]*class="hero-img"[^>]*>\s*)', html)
    if not hero_match:
        print(f"  WARNING: Could not find hero image insertion point in {html_path.name}")
        return

    insert_at = hero_match.end(1)
    html = html[:insert_at] + section_html + html[insert_at:]
    html_path.write_text(html, encoding="utf-8")
    print(f"  Embedded video in: {html_path.name}")


def main() -> None:
    ids = sys.argv[1:] if len(sys.argv) > 1 else [f"{i:02d}" for i in range(1, 13)]
    for lesson_id in ids:
        generate(lesson_id)
    print("\nAll done.")


if __name__ == "__main__":
    main()