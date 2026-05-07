#!/usr/bin/env python3
"""Mitra AI Life · Open Graph PNG generator.

Generates one 1200x630 PNG card per public page using the brand
colours from track-page.css. Writes to site/og/<slug>.png.

Run: .venv/bin/python scripts/generate_og_images.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "site" / "og"

W, H = 1200, 630

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"


@dataclass
class Track:
    slug: str
    eyebrow: str
    title: str
    sub: str
    bg: str
    accent: str
    amber: str


TRACKS: list[Track] = [
    Track("home", "MITRA AI LIFE", "Practical AI for every Indian family",
          "Daily life, students, tuition, spoken English, business, teachers, projects",
          "#06111f", "#68e1ff", "#f59e0b"),
    Track("daily-life", "AI FOR DAILY LIFE", "Beginner-first AI for ordinary Indian life",
          "Levels 1-10  ·  safety  ·  writing  ·  planning  ·  family help",
          "#06111f", "#68e1ff", "#f59e0b"),
    Track("students", "AI FOR STUDENTS", "School-safe AI literacy for students",
          "Study support  ·  safety  ·  classroom habits",
          "#082033", "#7dd3fc", "#facc15"),
    Track("tuition", "AI TUITION", "Gentle Hindi catch-up for primary children",
          "Slow pronunciation  ·  barakhadi  ·  writing  ·  quizzes",
          "#102018", "#86efac", "#fbbf24"),
    Track("spoken-english", "SPOKEN ENGLISH", "Real-life English confidence for Indians",
          "Listen  ·  repeat  ·  roleplay  ·  speak",
          "#181126", "#c4b5fd", "#fb7185"),
    Track("projects", "AI PROJECT KITS", "Premium AI projects for college students",
          "Code  ·  documentation  ·  demo  ·  deployment",
          "#0d1117", "#00d4aa", "#f0b429"),
    Track("small-business", "AI FOR SMALL BUSINESS", "Practical AI for shopkeepers and freelancers",
          "WhatsApp offers  ·  captions  ·  replies  ·  promotions",
          "#171006", "#fdba74", "#22c55e"),
    Track("teachers", "AI FOR TEACHERS", "Save preparation time, keep classroom control",
          "Worksheets  ·  quizzes  ·  explanations  ·  parent notes",
          "#081a26", "#67e8f9", "#a3e635"),
    Track("contact", "CONTACT", "Talk to Mitra AI Life",
          "Parents  ·  students  ·  teachers  ·  business  ·  partnerships",
          "#111827", "#93c5fd", "#fbbf24"),
    Track("privacy", "PRIVACY POLICY", "How we handle your information",
          "Plain-English privacy practices",
          "#111827", "#93c5fd", "#fbbf24"),
    Track("payment-policy", "PAYMENTS", "What is free, what is paid, and refunds",
          "Clear pricing for premium tracks",
          "#171006", "#fdba74", "#22c55e"),
]


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_alpha(rgb: tuple[int, int, int], a: int) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], a)


def gradient_bg(bg_hex: str) -> Image.Image:
    bg = hex_rgb(bg_hex)
    black = (0, 0, 0)
    img = Image.new("RGB", (W, H), bg)
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = ((x / W) * 0.5 + (y / H) * 0.5)
            px[x, y] = lerp(bg, black, t * 0.7)
    return img


def wrap_lines(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_card(t: Track) -> Image.Image:
    img = gradient_bg(t.bg).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    accent = hex_rgb(t.accent)
    amber = hex_rgb(t.amber)

    # subtle grid
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=add_alpha(accent, 14), width=1)
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=add_alpha(accent, 14), width=1)

    # corner blobs
    draw.ellipse([1080 - 220, 560 - 220, 1080 + 220, 560 + 220],
                 fill=add_alpha(accent, 26))
    draw.ellipse([120 - 160, 80 - 160, 120 + 160, 80 + 160],
                 fill=add_alpha(amber, 20))

    # brand bar
    draw.rectangle([80, 80, 86, 136], fill=accent)

    # brand text
    f_brand = ImageFont.truetype(FONT_BLACK, 36)
    draw.text((110, 86), "Mitra ", font=f_brand, fill=(248, 251, 255))
    bb = draw.textbbox((0, 0), "Mitra ", font=f_brand)
    bw = bb[2] - bb[0]
    draw.text((110 + bw, 86), "AI", font=f_brand, fill=accent)
    bb2 = draw.textbbox((0, 0), "AI", font=f_brand)
    aw = bb2[2] - bb2[0]
    draw.text((110 + bw + aw, 86), " Life", font=f_brand, fill=(248, 251, 255))

    # eyebrow
    f_eye = ImageFont.truetype(FONT_BLACK, 28)
    draw.text((80, 220), t.eyebrow, font=f_eye, fill=accent, spacing=4)

    # title (wrap to ~24 chars/line max 3 lines)
    f_title = ImageFont.truetype(FONT_BLACK, 60)
    lines = wrap_lines(t.title, 28)[:3]
    y = 290
    for line in lines:
        draw.text((80, y), line, font=f_title, fill=(248, 251, 255))
        y += 74

    # sub
    f_sub = ImageFont.truetype(FONT_REGULAR, 26)
    sub_lines = wrap_lines(t.sub, 70)[:2]
    y_sub = max(y + 20, 470)
    for line in sub_lines:
        draw.text((80, y_sub), line, font=f_sub, fill=(184, 199, 218))
        y_sub += 34

    # url chip
    chip_w, chip_h = 320, 50
    chip_x, chip_y = 80, 540
    draw.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h],
                           radius=25, fill=amber)
    f_url = ImageFont.truetype(FONT_BLACK, 22)
    bb_url = draw.textbbox((0, 0), "mitraailife.com", font=f_url)
    uw = bb_url[2] - bb_url[0]
    uh = bb_url[3] - bb_url[1]
    draw.text((chip_x + (chip_w - uw) / 2, chip_y + (chip_h - uh) / 2 - 4),
              "mitraailife.com", font=f_url, fill=(32, 18, 0))

    return Image.alpha_composite(img, overlay).convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for t in TRACKS:
        out = OUT_DIR / f"{t.slug}.png"
        img = render_card(t)
        img.save(out, "PNG", optimize=True)
        print("wrote", out.relative_to(ROOT))
    print(f"Done: {len(TRACKS)} OG cards.")


if __name__ == "__main__":
    main()
