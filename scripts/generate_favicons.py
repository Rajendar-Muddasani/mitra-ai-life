#!/usr/bin/env python3
"""Generate favicon and app icon assets for the public site.

Draws the Mitra AI logo (option 6: no lines) programmatically using Pillow.
Outputs: site/favicon.ico, favicon PNG sizes, apple-touch-icon, android-chrome icons.
"""

from __future__ import annotations

import json
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
    """Draw the Mitra AI option-6 logo at the requested pixel size."""
    s = size / 320.0  # scale factor from SVG viewBox 320x320

    canvas = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(canvas)

    # orbit ring (simplified single circle)
    if size >= 48:
        ring_r = 104 * s
        cx = cy = size / 2
        draw.ellipse(
            [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
            outline=(42, 52, 71, 92),
            width=max(1, round(2.4 * s)),
        )

    # 7 VIBGYOR dots
    DOTS = [
        (118.8, 75.5,  "#7c3aed"),
        (190.6, 71.1,  "#4f46e5"),
        (244.5, 118.8, "#2563eb"),
        (248.9, 190.6, "#22c55e"),
        (201.2, 244.5, "#facc15"),
        (129.4, 248.9, "#fb923c"),
        (75.5,  201.2, "#ef4444"),
    ]
    dot_r = 17.6 * s
    for dx, dy, color in DOTS:
        x, y = dx * s, dy * s
        draw.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=hex_to_rgba(color))

    # black dot cluster with white outline
    CLUSTER = [
        (71.1, 129.4, 16.7, 2.2),
        (40.1, 113.4, 8.8,  1.6),
        (40.1, 145.4, 8.8,  1.6),
    ]
    white_outline = hex_to_rgba("#f8fbff", 200)
    black_fill = hex_to_rgba("#111111")
    for dx, dy, r, sw in CLUSTER:
        x, y = dx * s, dy * s
        r_s = r * s
        sw_s = max(1, sw * s)
        draw.ellipse(
            [x - r_s - sw_s, y - r_s - sw_s, x + r_s + sw_s, y + r_s + sw_s],
            fill=white_outline,
        )
        draw.ellipse([x - r_s, y - r_s, x + r_s, y + r_s], fill=black_fill)

    # white AI oval
    ex, ey, erx, ery = 160 * s, 160 * s, 78 * s, 48 * s
    sw_oval = max(1, round(3 * s))
    draw.ellipse(
        [ex - erx - sw_oval, ey - ery - sw_oval, ex + erx + sw_oval, ey + ery + sw_oval],
        fill=hex_to_rgba("#d6deea"),
    )
    draw.ellipse([ex - erx, ey - ery, ex + erx, ey + ery], fill=(255, 255, 255, 255))

    # "AI" text (only at sizes >= 48)
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
        draw.text(
            (160 * s, 174 * s),
            "AI",
            fill=hex_to_rgba("#0f172a"),
            font=font,
            anchor="mm",
        )

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
