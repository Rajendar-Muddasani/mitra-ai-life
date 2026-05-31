#!/usr/bin/env python3
"""Generate human-chain Mitra AI logo variants for review.

Requested direction:
- keep the white AI oval
- replace the outer dots with 8 human heads
- show them holding hands with simple connecting lines
- let their legs rest on the oval edge
- offer 3 readable style directions for selection
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "logo-options"

HEAD_COLORS = [
    "#7c3aed",
    "#4f46e5",
    "#2563eb",
    "#0f766e",
    "#16a34a",
    "#f59e0b",
    "#f97316",
    "#dc2626",
]


@dataclass
class Variant:
    slug: str
    title: str
    note: str
    orbit_radius: float
    head_r: float
    base_angle_deg: float
    oval_rx: float
    oval_ry: float
    torso_len: float
    neck_gap: float
    shoulder_span: float
    hand_span: float
    leg_spread: float
    stroke_width: float
    arm_style: str
    arm_lift: float
    line_color: str
    guide_opacity: float


VARIANTS = [
    Variant(
        "logo-human-01-linked-circle",
        "Linked Circle",
        "Straight hand links. Cleanest and most logo-like.",
        112,
        15,
        -90,
        82,
        50,
        38,
        10,
        8,
        18,
        7,
        5.2,
        "straight",
        0,
        "#0f172a",
        0.18,
    ),
    Variant(
        "logo-human-02-soft-embrace",
        "Soft Embrace",
        "Curved hand links. Feels warmer and more human.",
        114,
        15.5,
        -90,
        84,
        51,
        40,
        11,
        8.5,
        19,
        7.5,
        5.4,
        "arc",
        12,
        "#10233f",
        0.14,
    ),
    Variant(
        "logo-human-03-oval-stand",
        "Oval Stand",
        "Tighter chain with a stronger standing-on-the-oval feel.",
        108,
        14.5,
        -90,
        86,
        54,
        35,
        9,
        7.5,
        16,
        6,
        5.0,
        "scallop",
        16,
        "#162033",
        0.12,
    ),
]


def polar(cx: float, cy: float, radius: float, angle_deg: float) -> tuple[float, float]:
    angle = angle_deg * pi / 180.0
    return cx + radius * cos(angle), cy + radius * sin(angle)


def ellipse_point(cx: float, cy: float, rx: float, ry: float, angle_deg: float) -> tuple[float, float]:
    angle = angle_deg * pi / 180.0
    return cx + rx * cos(angle), cy + ry * sin(angle)


def add(point: tuple[float, float], vector: tuple[float, float]) -> tuple[float, float]:
    return point[0] + vector[0], point[1] + vector[1]


def scale(vector: tuple[float, float], amount: float) -> tuple[float, float]:
    return vector[0] * amount, vector[1] * amount


def radial_and_tangent(angle_deg: float) -> tuple[tuple[float, float], tuple[float, float]]:
    angle = angle_deg * pi / 180.0
    radial = (cos(angle), sin(angle))
    tangent = (-sin(angle), cos(angle))
    return radial, tangent


def curved_link(
    start: tuple[float, float],
    end: tuple[float, float],
    lift_vector: tuple[float, float],
    mode: str,
) -> str:
    midpoint = ((start[0] + end[0]) * 0.5, (start[1] + end[1]) * 0.5)
    if mode == "arc":
        control = add(midpoint, lift_vector)
        return f"M {start[0]:.1f} {start[1]:.1f} Q {control[0]:.1f} {control[1]:.1f} {end[0]:.1f} {end[1]:.1f}"

    control_1 = add(((start[0] * 2 + end[0]) / 3, (start[1] * 2 + end[1]) / 3), lift_vector)
    control_2 = add(((start[0] + end[0] * 2) / 3, (start[1] + end[1] * 2) / 3), lift_vector)
    return (
        f"M {start[0]:.1f} {start[1]:.1f} "
        f"C {control_1[0]:.1f} {control_1[1]:.1f} {control_2[0]:.1f} {control_2[1]:.1f} {end[0]:.1f} {end[1]:.1f}"
    )


def svg_for(variant: Variant) -> str:
    cx = cy = 160
    angles = [variant.base_angle_deg + index * 45 for index in range(8)]
    people: list[dict[str, tuple[float, float] | float]] = []

    for angle_deg in angles:
        radial, tangent = radial_and_tangent(angle_deg)
        head = polar(cx, cy, variant.orbit_radius, angle_deg)
        neck = add(head, scale(radial, -(variant.head_r + 2)))
        shoulder_center = add(head, scale(radial, -(variant.head_r + variant.neck_gap)))
        hip = add(head, scale(radial, -(variant.head_r + variant.torso_len)))
        shoulder_left = add(shoulder_center, scale(tangent, -variant.shoulder_span))
        shoulder_right = add(shoulder_center, scale(tangent, variant.shoulder_span))
        hand_left = add(shoulder_center, scale(tangent, -variant.hand_span))
        hand_right = add(shoulder_center, scale(tangent, variant.hand_span))
        foot_center = ellipse_point(cx, cy, variant.oval_rx, variant.oval_ry, angle_deg)
        left_foot = add(foot_center, scale(tangent, -variant.leg_spread))
        right_foot = add(foot_center, scale(tangent, variant.leg_spread))
        people.append(
            {
                "head": head,
                "neck": neck,
                "hip": hip,
                "shoulder_left": shoulder_left,
                "shoulder_right": shoulder_right,
                "hand_left": hand_left,
                "hand_right": hand_right,
                "left_foot": left_foot,
                "right_foot": right_foot,
                "angle_deg": angle_deg,
            }
        )

    guide_radius = variant.orbit_radius - 18
    guide_ring = (
        f'<circle cx="{cx}" cy="{cy}" r="{guide_radius:.1f}" fill="none" '
        f'stroke="#cbd5e1" stroke-width="1.8" stroke-dasharray="3 10" opacity="{variant.guide_opacity:.2f}"/>'
    )

    arm_links: list[str] = []
    for index, person in enumerate(people):
        next_person = people[(index + 1) % len(people)]
        start = person["hand_right"]
        end = next_person["hand_left"]
        angle_deg = (person["angle_deg"] + next_person["angle_deg"]) * 0.5
        radial, _ = radial_and_tangent(angle_deg)
        lift = scale(radial, 0 if variant.arm_style == "straight" else variant.arm_lift)
        if variant.arm_style == "straight":
            path_data = f"M {start[0]:.1f} {start[1]:.1f} L {end[0]:.1f} {end[1]:.1f}"
        else:
            path_data = curved_link(start, end, lift, variant.arm_style)
        arm_links.append(
            f'<path d="{path_data}" fill="none" stroke="{variant.line_color}" stroke-width="{variant.stroke_width:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>'
        )

    bodies: list[str] = []
    for index, person in enumerate(people):
        head_x, head_y = person["head"]
        neck_x, neck_y = person["neck"]
        hip_x, hip_y = person["hip"]
        shoulder_left_x, shoulder_left_y = person["shoulder_left"]
        shoulder_right_x, shoulder_right_y = person["shoulder_right"]
        left_foot_x, left_foot_y = person["left_foot"]
        right_foot_x, right_foot_y = person["right_foot"]

        bodies.append(
            f'<path d="M {shoulder_left_x:.1f} {shoulder_left_y:.1f} L {shoulder_right_x:.1f} {shoulder_right_y:.1f}" '
            f'fill="none" stroke="{variant.line_color}" stroke-width="{variant.stroke_width:.1f}" stroke-linecap="round"/>'
        )
        bodies.append(
            f'<path d="M {neck_x:.1f} {neck_y:.1f} L {hip_x:.1f} {hip_y:.1f}" '
            f'fill="none" stroke="{variant.line_color}" stroke-width="{variant.stroke_width:.1f}" stroke-linecap="round"/>'
        )
        bodies.append(
            f'<path d="M {hip_x:.1f} {hip_y:.1f} L {left_foot_x:.1f} {left_foot_y:.1f}" '
            f'fill="none" stroke="{variant.line_color}" stroke-width="{variant.stroke_width - 0.4:.1f}" stroke-linecap="round"/>'
        )
        bodies.append(
            f'<path d="M {hip_x:.1f} {hip_y:.1f} L {right_foot_x:.1f} {right_foot_y:.1f}" '
            f'fill="none" stroke="{variant.line_color}" stroke-width="{variant.stroke_width - 0.4:.1f}" stroke-linecap="round"/>'
        )
        bodies.append(
            f'<circle cx="{head_x:.1f}" cy="{head_y:.1f}" r="{variant.head_r:.1f}" fill="{HEAD_COLORS[index]}" stroke="#f8fbff" stroke-width="2"/>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" role="img" aria-labelledby="title desc">
  <title id="title">Mitra AI Life logo option: {variant.title}</title>
  <desc id="desc">Eight human figures holding hands around the AI oval.</desc>
  <defs>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  {guide_ring}
  {''.join(arm_links)}
  <ellipse cx="160" cy="160" rx="{variant.oval_rx}" ry="{variant.oval_ry}" fill="#ffffff" stroke="#d6deea" stroke-width="3.2"/>
  {''.join(bodies)}
  <text x="160" y="174" text-anchor="middle" font-family="Syne, Nunito, Arial, sans-serif" font-size="42" font-weight="800" fill="#0f172a">AI</text>
</svg>
'''


def preview_html() -> str:
    cards = []
    for index, variant in enumerate(VARIANTS, start=1):
        cards.append(
            f'''<article class="card"><img src="logo-options/{variant.slug}.svg" alt="{variant.title}" /><h2>Option {index}</h2><p>{variant.title}</p><p class="note">{variant.note}</p><code>site/logo-options/{variant.slug}.svg</code></article>'''
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
    p.lead {{ margin: 0 0 28px; color: var(--muted); font-size: 1rem; line-height: 1.6; max-width: 900px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 20px; padding: 20px; }}
    .card img {{ width: 100%; aspect-ratio: 1; object-fit: contain; border-radius: 16px; background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.07); padding: 16px; }}
    .card h2 {{ margin: 14px 0 4px; font-size: 1.05rem; }}
    .card p {{ margin: 0 0 8px; color: var(--muted); }}
    .card p.note {{ color: #d7e4f7; min-height: 46px; }}
    code {{ color: #d4def1; font-size: 0.82rem; word-break: break-all; }}
  </style>
</head>
<body>
  <main>
    <h1>Mitra AI Logo Options</h1>
    <p class="lead">Three human-chain concepts based on your direction: 8 heads around the oval, simple joined hand-lines between them, and legs standing on the AI oval. Option 1 is the cleanest. Option 2 is softer and more friendly. Option 3 makes the standing posture on the oval stronger.</p>
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
