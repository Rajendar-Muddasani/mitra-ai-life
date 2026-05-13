#!/usr/bin/env python3
"""
test_pronunciation.py — generate individual TTS MP3s and an HTML test page.

Open the HTML page in the browser to listen to each letter/form individually
and identify any that sound wrong.

Usage:
  python scripts/test_pronunciation.py --target vyanjan
  python scripts/test_pronunciation.py --target swar
  python scripts/test_pronunciation.py --target barakhadi --letter ka
  python scripts/test_pronunciation.py --voice shimmer --target all
"""

import argparse, os, pathlib, time

ROOT      = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR   = ROOT / "content/assets/audio/pronunciation-test"
HTML_OUT  = ROOT / "content/assets/audio/pronunciation-test/index.html"

SWAR = [
    ("अ", "a"), ("आ", "aa"), ("इ", "i"), ("ई", "ee"),
    ("उ", "u"), ("ऊ", "oo"), ("ए", "e"), ("ऐ", "ai"),
    ("ओ", "o"), ("औ", "au"), ("अं", "an"), ("अः", "ah"),
]

VYANJAN = [
    ("क", "ka"), ("ख", "kha"), ("ग", "ga"), ("घ", "gha"), ("ङ", "nga"),
    ("च", "cha"), ("छ", "chha"), ("ज", "ja"), ("झ", "jha"), ("ञ", "nya"),
    ("ट", "tta"), ("ठ", "ttha"), ("ड", "dda"), ("ढ", "ddha"), ("ण", "nna"),
    ("त", "ta"), ("थ", "tha"), ("द", "da"), ("ध", "dha"), ("न", "na"),
    ("प", "pa"), ("फ", "pha"), ("ब", "ba"), ("भ", "bha"), ("म", "ma"),
    ("य", "ya"), ("र", "ra"), ("ल", "la"), ("व", "va"),
    ("श", "sha"), ("ष", "ssha"), ("स", "sa"), ("ह", "ha"),
]

MATRAS = [
    ("", "a"), ("ा", "aa"), ("ि", "i"), ("ी", "ee"),
    ("ु", "u"), ("ू", "oo"), ("े", "e"), ("ै", "ai"),
    ("ो", "o"), ("ौ", "au"), ("ं", "an"), ("ः", "ah"),
]


def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def tts_to_file(text: str, out_path: pathlib.Path, voice: str = "hi-IN-Chirp3-HD-Aoede",
                speed: float = 0.70):
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from _google_tts import tts_to_file as g_tts
    g_tts(text, out_path, speed=speed, voice=voice, skip_existing=True)


def gen_group(entries: list[tuple], group_dir: pathlib.Path, voice: str):
    """Generate one test clip per letter — 3 reps at slow speed so it's clearly audible."""
    group_dir.mkdir(parents=True, exist_ok=True)
    for (letter, slug) in entries:
        # Repeat 3× so the sound is long enough to hear; add a comma pause between reps
        text = f"{letter}, {letter}, {letter}"
        tts_to_file(text, group_dir / f"{slug}.mp3", voice, speed=0.60)


def gen_barakhadi(letter: str, slug: str, bar_dir: pathlib.Path, voice: str):
    bar_dir.mkdir(parents=True, exist_ok=True)
    for (matra, mlabel) in MATRAS:
        form = letter + matra
        tts_to_file(form, bar_dir / f"{slug}-{mlabel}.mp3", voice)


def build_html(voice: str, target: str):
    """Build a clickable test page at content/assets/audio/pronunciation-test/index.html."""
    sections: list[str] = []

    def audio_row(label: str, mp3_rel: str) -> str:
        return (
            f'<div class="row">'
            f'<span class="lbl">{label}</span>'
            f'<audio controls src="{mp3_rel}"></audio>'
            f'</div>'
        )

    if target in ("swar", "all"):
        rows = "\n".join(
            audio_row(f"{l} ({s})", f"swar/{s}.mp3")
            for l, s in SWAR
            if (OUT_DIR / "swar" / f"{s}.mp3").exists()
        )
        sections.append(f"<h2>Swar / Vowels</h2><div class='group'>{rows}</div>")

    if target in ("vyanjan", "all"):
        rows = "\n".join(
            audio_row(f"{l} ({s})", f"vyanjan/{s}.mp3")
            for l, s in VYANJAN
            if (OUT_DIR / "vyanjan" / f"{s}.mp3").exists()
        )
        sections.append(f"<h2>Vyanjan / Consonants</h2><div class='group'>{rows}</div>")

    if target in ("barakhadi", "all"):
        for (letter, slug) in VYANJAN:
            bar_dir = OUT_DIR / f"bara-{slug}"
            if not bar_dir.exists():
                continue
            rows = "\n".join(
                audio_row(f"{letter}{matra} ({slug}-{ml})", f"bara-{slug}/{slug}-{ml}.mp3")
                for matra, ml in MATRAS
                if (bar_dir / f"{slug}-{ml}.mp3").exists()
            )
            if rows:
                sections.append(
                    f"<h3>{letter} barakhadi</h3><div class='group'>{rows}</div>"
                )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Pronunciation Test — {voice}</title>
<style>
  body {{ font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
  h2 {{ border-bottom: 2px solid #333; padding-bottom: 4px; margin-top: 2rem; }}
  h3 {{ margin-top: 1.5rem; color: #444; }}
  .group {{ display: grid; gap: 0.5rem; margin-top: 0.75rem; }}
  .row {{ display: flex; align-items: center; gap: 1rem; }}
  .lbl {{
    font-family: 'Noto Sans Devanagari', serif;
    font-size: 1.4rem;
    min-width: 160px;
    font-weight: 700;
  }}
  audio {{ height: 32px; }}
</style>
</head>
<body>
<h1>Pronunciation Test — voice: {voice}</h1>
<p>Play each clip. If a letter sounds wrong, note it and we fix the TTS input text.</p>
{"".join(sections)}
</body>
</html>"""

    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"\n  HTML: {HTML_OUT}")
    print(f"  Open: http://127.0.0.1:8080/content/assets/audio/pronunciation-test/index.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["swar", "vyanjan", "barakhadi", "all"],
                    default="vyanjan")
    ap.add_argument("--letter", default="ka",
                    help="Which consonant's barakhadi to test (roman, e.g. ka kha)")
    ap.add_argument("--voice",  default="nova")
    ap.add_argument("--speed",  type=float, default=0.70)
    args = ap.parse_args()

    load_env()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.target in ("swar", "all"):
        print("Generating swar test clips…")
        gen_group(SWAR, OUT_DIR / "swar", args.voice)

    if args.target in ("vyanjan", "all"):
        print("Generating vyanjan test clips…")
        gen_group(VYANJAN, OUT_DIR / "vyanjan", args.voice)

    if args.target in ("barakhadi", "all"):
        for letter_roman in args.letter.split(","):
            lr = letter_roman.strip()
            entry = next(((l, s) for l, s in VYANJAN if s == lr), None)
            if entry:
                print(f"Generating barakhadi test clips for {entry[0]} ({lr})…")
                gen_barakhadi(entry[0], lr, OUT_DIR / f"bara-{lr}", args.voice)

    build_html(args.voice, args.target)
    print("Done.")


if __name__ == "__main__":
    main()
