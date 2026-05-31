#!/usr/bin/env python3
"""Generate favicon and app icon assets for the public site.

Draws the selected Mitra AI linked-circle logo programmatically using Pillow.
Outputs: site/favicon.ico, favicon PNG sizes, apple-touch-icon, android-chrome icons.
"""

from __future__ import annotations

import json
from math import cos, pi, sin
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

BG = (6, 17, 31, 255)

OUTPUTS = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
}


def hex_to_rgba(h: str, a: int = 255) -> Tuple[int, int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def draw_logo(size: int) -> Image.Image:
    """Draw the selected Mitra AI linked-circle logo at the requested pixel size."""
    s = size / 320.0
    canvas = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(canvas)

    cx = cy = size / 2
    orbit_radius = 112 * s
    head_r = 15 * s
    oval_rx, oval_ry = 82 * s, 50 * s
    torso_len = 38 * s
    neck_gap = 10 * s
    shoulder_span = 8 * s
    hand_span = 18 * s
    leg_spread = 7 * s
    stroke_width = max(1, round(5.2 * s))
    line_color = hex_to_rgba("#0f172a", 235)
    head_colors = [
        "#7c3aed", "#4f46e5", "#2563eb", "#0f766e",
        "#16a34a", "#f59e0b", "#f97316", "#dc2626",
    ]

    def point(radius: float, angle_deg: float) -> tuple[float, float]:
        angle = angle_deg * pi / 180.0
        return cx + radius * cos(angle), cy + radius * sin(angle)

    def ellipse_point(rx: float, ry: float, angle_deg: float) -> tuple[float, float]:
        angle = angle_deg * pi / 180.0
        return cx + rx * cos(angle), cy + ry * sin(angle)

    def add(p: tuple[float, float], v: tuple[float, float]) -> tuple[float, float]:
        return p[0] + v[0], p[1] + v[1]

    def scale(v: tuple[float, float], amount: float) -> tuple[float, float]:
        return v[0] * amount, v[1] * amount

    def radial_and_tangent(angle_deg: float) -> tuple[tuple[float, float], tuple[float, float]]:
        angle = angle_deg * pi / 180.0
        return (cos(angle), sin(angle)), (-sin(angle), cos(angle))

    if size >= 48:
        guide_r = 94 * s
        draw.ellipse(
            [cx - guide_r, cy - guide_r, cx + guide_r, cy + guide_r],
            outline=(203, 213, 225, 46),
            width=max(1, round(1.8 * s)),
        )

    angles = [-90 + index * 45 for index in range(8)]
    people: list[dict[str, tuple[float, float] | float]] = []
    for angle_deg in angles:
        radial, tangent = radial_and_tangent(angle_deg)
        head = point(orbit_radius, angle_deg)
        neck = add(head, scale(radial, -(head_r + 2 * s)))
        shoulder_center = add(head, scale(radial, -(head_r + neck_gap)))
        hip = add(head, scale(radial, -(head_r + torso_len)))
        foot_center = ellipse_point(oval_rx, oval_ry, angle_deg)
        people.append(
            {
                "head": head,
                "neck": neck,
                "hip": hip,
                "shoulder_left": add(shoulder_center, scale(tangent, -shoulder_span)),
                "shoulder_right": add(shoulder_center, scale(tangent, shoulder_span)),
                "hand_left": add(shoulder_center, scale(tangent, -hand_span)),
                "hand_right": add(shoulder_center, scale(tangent, hand_span)),
                "left_foot": add(foot_center, scale(tangent, -leg_spread)),
                "right_foot": add(foot_center, scale(tangent, leg_spread)),
                "angle_deg": angle_deg,
            }
        )

    for index, person in enumerate(people):
        next_person = people[(index + 1) % len(people)]
        start = person["hand_right"]
        end = next_person["hand_left"]
        draw.line([start, end], fill=line_color, width=stroke_width)

    oval_outline = max(1, round(3.2 * s))
    draw.ellipse(
        [cx - oval_rx - oval_outline, cy - oval_ry - oval_outline,
         cx + oval_rx + oval_outline, cy + oval_ry + oval_outline],
        fill=hex_to_rgba("#d6deea"),
    )
    draw.ellipse([cx - oval_rx, cy - oval_ry, cx + oval_rx, cy + oval_ry], fill=(255, 255, 255, 255))

    body_width = stroke_width
    leg_width = max(1, round(4.8 * s))
    for index, person in enumerate(people):
        draw.line([person["shoulder_left"], person["shoulder_right"]], fill=line_color, width=body_width)
        draw.line([person["neck"], person["hip"]], fill=line_color, width=body_width)
        draw.line([person["hip"], person["left_foot"]], fill=line_color, width=leg_width)
        draw.line([person["hip"], person["right_foot"]], fill=line_color, width=leg_width)

        head_x, head_y = person["head"]
        outline = max(1, round(2 * s))
        draw.ellipse(
            [head_x - head_r - outline, head_y - head_r - outline,
             head_x + head_r + outline, head_y + head_r + outline],
            fill=hex_to_rgba("#f8fbff"),
        )
        draw.ellipse(
            [head_x - head_r, head_y - head_r, head_x + head_r, head_y + head_r],
            fill=hex_to_rgba(head_colors[index]),
        )

    if size >= 48:
        font_size = max(10, round(42 * s))
        font = None
        for fpath in (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
        ):
            try:
                font = ImageFont.truetype(fpath, font_size)
                break
            except OSError:
                pass
        if font is None:
            font = ImageFont.load_default()
        draw.text((160 * s, 174 * s), "AI", fill=hex_to_rgba("#0f172a"), font=font, anchor="mm")

    return canvas


def main() -> None:
    for name, size in OUTPUTS.items():
        img = draw_logo(size)
        img.save(SITE / name, format="PNG")
        print(f"wrote site/{name}")

    favicon_frames = [draw_logo(sz).convert("RGB") for sz in (16, 32, 48)]
    favicon_frames[0].save(
        SITE / "favicon.ico",
        format="ICO",
        append_images=favicon_frames[1:],
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print("wrote site/favicon.ico")

    manifest = {
        "name": "Mitra AI Life",
        "short_name": "Mitra AI",
        "start_url": "./",
        "display": "standalone",
        "background_color": "#06111f",
        "theme_color": "#06111f",
        "icons": [
            {"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    (SITE / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("wrote site/site.webmanifest")


if __name__ == "__main__":
    main()
