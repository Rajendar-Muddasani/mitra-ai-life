#!/usr/bin/env python3
"""Generate 7 Mitra AI logo SVG variants for review.

Requested direction:
- keep the white oval and AI word
- increase outer dots to ~1.5x size
- place dots on an almost-equal circular orbit
- replace straight saffron/green lines with eyelid-like arcs
- keep one black dot plus two smaller black dots as a cluster
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "logo-options"

COLORS = [
    "#7c3aed",  # violet
    "#4f46e5",  # indigo
    "#2563eb",  # blue
    "#22c55e",  # green
    "#facc15",  # yellow
    "#fb923c",  # orange
    "#ef4444",  # red
]


@dataclass
class Variant:
    slug: str
    title: str
    orbit_radius: float
    dot_r: float
    base_angle_deg: float
    line_mode: str
    connect_lids: bool
    lid_stroke: float
    oval_rx: float
    oval_ry: float
    black_big_scale: float
    black_small_offset_x: float
    black_small_offset_y: float
    show_small_black_dots: bool
    ring_opacity: float
    ring_dash: str


VARIANTS = [
    Variant("logo-01-lines-on-dots", "Lines On Dots", 101, 21, -122, "on_dots", False, 10, 80, 50, 1.00, 34, 17, True, 0.32, "3 10"),
    Variant("logo-02-lines-above-dots", "Lines Above Dots", 106, 21, -126, "above_dots", False, 11, 82, 49, 1.00, 36, 18, True, 0.28, "2 9"),
    Variant("logo-03-connected-above", "Connected Above Dots", 98, 22, -118, "above_dots", True, 9, 76, 52, 1.05, 32, 18, True, 0.34, "4 11"),
    Variant("logo-04-connected-on", "Connected On Dots", 100, 20, -120, "on_dots", True, 8, 79, 49, 1.00, 33, 16, True, 0.26, "2 12"),
    Variant("logo-05-connected-inside", "Connected Inside Dots", 104, 21, -124, "inside_dots", True, 13, 80, 50, 1.00, 36, 17, True, 0.30, "4 10"),
    Variant("logo-06-no-lines", "No Lines", 94, 22, -116, "none", False, 10, 78, 48, 0.95, 31, 16, True, 0.36, "3 9"),
    Variant("logo-07-no-lines-single-black", "No Lines, Single Black Dot", 109, 20, -128, "none", False, 10, 84, 50, 1.05, 38, 19, False, 0.24, "2 8"),
]


def polar(cx: float, cy: float, radius: float, angle_deg: float) -> tuple[float, float]:
    angle = angle_deg * pi / 180.0
    return cx + radius * cos(angle), cy + radius * sin(angle)


def lid_geometry(cy: float, orbit_radius: float, dot_r: float, line_mode: str) -> tuple[float, float, float]:
  if line_mode == "above_dots":
    top_y = cy - orbit_radius - dot_r - 12
    bottom_y = cy + orbit_radius + dot_r + 12
    ctrl_lift = 28
  elif line_mode == "on_dots":
    top_y = cy - orbit_radius + dot_r * 0.15
    bottom_y = cy + orbit_radius - dot_r * 0.15
    ctrl_lift = 22
  elif line_mode == "inside_dots":
    top_y = cy - orbit_radius + dot_r + 12
    bottom_y = cy + orbit_radius - dot_r - 12
    ctrl_lift = 18
  else:
    top_y = bottom_y = ctrl_lift = 0
  return top_y, bottom_y, ctrl_lift


def svg_for(variant: Variant) -> str:
    cx = cy = 160
    dot_r = variant.dot_r * 0.8
    ring_radius = variant.orbit_radius + 10
    points = [polar(cx, cy, variant.orbit_radius, variant.base_angle_deg + i * (360 / 8)) for i in range(7)]
    black_x, black_y = polar(cx, cy, variant.orbit_radius, variant.base_angle_deg + 7 * (360 / 8))
    black_big_r = dot_r * variant.black_big_scale
    small_1 = (black_x - variant.black_small_offset_x, black_y - variant.black_small_offset_y)
    small_2 = (black_x - variant.black_small_offset_x, black_y + variant.black_small_offset_y)
    small_r = dot_r * 0.5

    lid_svg = ""
    if variant.line_mode != "none":
      top_y, bottom_y, ctrl_lift = lid_geometry(cy, variant.orbit_radius, dot_r, variant.line_mode)
      top_start = (74, top_y)
      top_end = (246, top_y)
      bottom_start = (74, bottom_y)
      bottom_end = (246, bottom_y)
      top_ctrl = top_y - ctrl_lift
      bottom_ctrl = bottom_y + ctrl_lift
      lid_svg = (
        f'<path d="M {top_start[0]} {top_start[1]:.1f} Q 160 {top_ctrl:.1f} {top_end[0]} {top_end[1]:.1f}" fill="none" stroke="#ff8a1f" stroke-width="{variant.lid_stroke}" stroke-linecap="round" opacity="0.96"/>'
        f'<path d="M {bottom_start[0]} {bottom_start[1]:.1f} Q 160 {bottom_ctrl:.1f} {bottom_end[0]} {bottom_end[1]:.1f}" fill="none" stroke="#16a34a" stroke-width="{variant.lid_stroke}" stroke-linecap="round" opacity="0.96"/>'
      )
      if variant.connect_lids:
        left_ctrl_x = 42 if variant.line_mode == "above_dots" else 56
        right_ctrl_x = 278 if variant.line_mode == "above_dots" else 264
        lid_svg += (
          f'<path d="M {top_start[0]} {top_start[1]:.1f} Q {left_ctrl_x} 160 {bottom_start[0]} {bottom_start[1]:.1f}" fill="none" stroke="#ffb347" stroke-width="{max(variant.lid_stroke - 2, 5)}" stroke-linecap="round" opacity="0.88"/>'
          f'<path d="M {top_end[0]} {top_end[1]:.1f} Q {right_ctrl_x} 160 {bottom_end[0]} {bottom_end[1]:.1f}" fill="none" stroke="#4ade80" stroke-width="{max(variant.lid_stroke - 2, 5)}" stroke-linecap="round" opacity="0.88"/>'
        )

    black_small_svg = ""
    if variant.show_small_black_dots:
      black_small_svg = (
        f'<circle cx="{small_1[0]:.1f}" cy="{small_1[1]:.1f}" r="{small_r:.1f}" fill="#111111" stroke="#f8fbff" stroke-opacity="0.74" stroke-width="1.6"/>'
        f'<circle cx="{small_2[0]:.1f}" cy="{small_2[1]:.1f}" r="{small_r:.1f}" fill="#111111" stroke="#f8fbff" stroke-opacity="0.74" stroke-width="1.6"/>'
      )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" role="img" aria-labelledby="title desc">
  <title id="title">Mitra AI Life logo option: {variant.title}</title>
  <desc id="desc">AI oval with VIBGYOR orbit dots and black dot cluster.</desc>
  <defs>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <circle cx="160" cy="160" r="{ring_radius}" fill="none" stroke="#2a3447" stroke-width="2.4" stroke-dasharray="{variant.ring_dash}" opacity="{variant.ring_opacity}"/>

  {lid_svg}

  {''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dot_r:.1f}" fill="{color}" filter="url(#softGlow)"/>' for (x, y), color in zip(points, COLORS))}

  <circle cx="{black_x:.1f}" cy="{black_y:.1f}" r="{black_big_r:.1f}" fill="#111111" stroke="#f8fbff" stroke-opacity="0.78" stroke-width="2.2"/>
  {black_small_svg}

  <ellipse cx="160" cy="160" rx="{variant.oval_rx}" ry="{variant.oval_ry}" fill="#ffffff" stroke="#d6deea" stroke-width="3"/>
  <text x="160" y="174" text-anchor="middle" font-family="Syne, Nunito, Arial, sans-serif" font-size="42" font-weight="800" fill="#0f172a">AI</text>
</svg>
'''


def preview_html() -> str:
    cards = []
    for i, variant in enumerate(VARIANTS, start=1):
        cards.append(
            f'''<article class="card"><img src="logo-options/{variant.slug}.svg" alt="{variant.title}" /><h2>Option {i}</h2><p>{variant.title}</p><code>site/logo-options/{variant.slug}.svg</code></article>'''
        )
    joined = "\n      ".join(cards)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mitra AI Logo Options</title>
  <style>
    :root {{
      --bg: #07101d;
      --panel: rgba(255,255,255,0.06);
      --line: rgba(255,255,255,0.12);
      --text: #f8fbff;
      --muted: #afbdd0;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Nunito, Arial, sans-serif; background: radial-gradient(circle at top, #122036, #07101d 65%); color: var(--text); }}
    main {{ max-width: 1280px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ margin: 0 0 10px; font-size: clamp(2rem, 4vw, 3rem); }}
    p.lead {{ margin: 0 0 28px; color: var(--muted); font-size: 1rem; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 20px; padding: 20px; }}
    .card img {{ width: 100%; aspect-ratio: 1; object-fit: contain; border-radius: 16px; background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.07); padding: 16px; }}
    .card h2 {{ margin: 14px 0 4px; font-size: 1.05rem; }}
    .card p {{ margin: 0 0 8px; color: var(--muted); }}
    code {{ color: #d4def1; font-size: 0.82rem; word-break: break-all; }}
  </style>
</head>
<body>
  <main>
    <h1>Mitra AI Logo Options</h1>
    <p class="lead">Option 1 keeps lines on the dots. Option 2 keeps lines above the dots. Option 3 connects the outer lines above the dots. Option 4 connects them on the dots. Option 5 connects them inside the dots. Option 6 has no lines. Option 7 has no lines and only one black dot.</p>
    <section class="grid">
      {joined}
    </section>
  </main>
</body>
</html>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for variant in VARIANTS:
        path = OUT / f"{variant.slug}.svg"
        path.write_text(svg_for(variant), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    preview = ROOT / "site" / "logo-options.html"
    preview.write_text(preview_html(), encoding="utf-8")
    print(f"wrote {preview.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
