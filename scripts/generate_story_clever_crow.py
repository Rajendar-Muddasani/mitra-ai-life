#!/usr/bin/env python3
"""
generate_story_clever_crow.py
Bedtime story: The Clever Crow
DALL-E 3 images + Google Cloud TTS + ffmpeg → YouTube-ready MP4

Usage:
    source .venv/bin/activate
    python scripts/generate_story_clever_crow.py
    python scripts/generate_story_clever_crow.py --force   # re-generate all

Output:
    output/stories/clever-crow/final_clever_crow.mp4  (~8 min)
"""

import argparse
import os
import subprocess
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

# ── Environment ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_CREDS   = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
if not OPENAI_API_KEY:
    raise SystemExit("❌  OPENAI_API_KEY not found in .env")
if not GOOGLE_CREDS:
    raise SystemExit("❌  GOOGLE_APPLICATION_CREDENTIALS not found in .env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDS

# ── Paths ─────────────────────────────────────────────────────────────────────
OUT_DIR    = ROOT / "output" / "stories" / "clever-crow"
FONT_HEADING = str(ROOT / "scripts/_fonts/NotoSansTelugu-Bold.ttf")
FONT_BODY    = str(ROOT / "scripts/_fonts/NotoSansTelugu-Regular.ttf")
FINAL_MP4    = OUT_DIR / "final_clever_crow.mp4"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Story data ────────────────────────────────────────────────────────────────
# Each slide: (eyebrow, title_overlay, dall_e_scene_prompt, narration_text)
ART_STYLE = (
    "Soft watercolor children's book illustration, warm pastel colours, "
    "gentle brushstrokes, cozy magical Indian forest setting, "
    "golden and moonlit lighting, dreamlike and safe for children, "
    "no text or letters in the image. "
)

SLIDES = [
    (
        "",
        "The Clever Crow",
        "A majestic black crow perched on a moonlit banyan branch, glowing "
        "full moon behind, silver stars, warm golden light, title card feel",
        "Once upon a time, in a beautiful green forest in India, there lived "
        "a very clever crow. He was known for his bright eyes and quick mind. "
        "Tonight, we follow the crow on a very special day...",
    ),
    (
        "Part 1",
        "A Hot Summer Day",
        "A lush Indian forest under a blazing summer sun, dust on the path, "
        "wilting flowers, a small dry riverbed, warm amber and yellow tones",
        "It was the hottest day of summer. The sun blazed down on the forest "
        "like a great fire in the sky. The leaves drooped. The river had dried up. "
        "Every creature was searching for water. The crow was very, very thirsty.",
    ),
    (
        "Part 2",
        "The Thirsty Crow",
        "A tired crow with drooping wings flying over a dry Indian village, "
        "searching, looking down with worried bright eyes, golden sky",
        "The crow flew here and there, searching everywhere. He checked the "
        "riverbed — dry. He checked the old pond — empty. His wings grew heavy "
        "and his throat burned. But the clever crow did not give up.",
    ),
    (
        "Part 3",
        "Water! But So Far Down",
        "A crow peering into a tall clay pot sitting on dry ground, "
        "beak reaching in but too short to touch the water far below, "
        "late afternoon light, a few clouds",
        "At last! Near an old cottage, the crow spotted a tall clay pot. "
        "He flew down and looked inside. There was water — cool, beautiful water! "
        "But it was deep, deep at the bottom. No matter how far the crow stretched, "
        "he could not reach it. What would he do?",
    ),
    (
        "Part 4",
        "Think, Crow, Think",
        "A crow sitting quietly beside a clay pot, eyes closed in thought, "
        "a contemplative expression, soft evening light, pebbles nearby on the ground",
        "The crow sat very still. He did not panic. He thought carefully. "
        "He looked at the pot. He looked at his wings. He looked around him. "
        "And then — he looked down at the ground. Pebbles! Small round pebbles "
        "were scattered all around. An idea began to shine in his clever mind.",
    ),
    (
        "Part 5",
        "One Pebble at a Time",
        "A crow carefully picking up a small pebble with its beak, "
        "a clay pot nearby, water level very low inside, "
        "gentle determination in the crow's eyes, warm evening light",
        "The crow picked up one pebble with his beak. He walked to the pot "
        "and dropped it in. Plop. The water barely moved. He picked up another. "
        "Plop. And another. Plop plop plop. It was slow work. But the crow "
        "kept going, one pebble at a time, never stopping.",
    ),
    (
        "Part 6",
        "The Water is Rising!",
        "A crow excitedly dropping pebbles into a clay pot, "
        "the water level noticeably higher now, joy and hope on the crow's face, "
        "golden hour light, beautiful Indian forest background",
        "After many, many pebbles, something wonderful happened. The water began "
        "to rise! Slowly, slowly, it crept up toward the top. The crow worked "
        "faster now, his heart beating with excitement. Higher and higher the "
        "cool water climbed. The crow's clever plan was working.",
    ),
    (
        "Part 7",
        "One Last Pebble",
        "A crow holding the final pebble, looking at a nearly full clay pot, "
        "water very close to the top, a magical glowing light around the pot, "
        "triumphant but tender expression",
        "The crow picked up one last pebble. He held it for a moment, looking "
        "at the pot. The water was almost — almost — at the top. He took a deep "
        "breath. He dropped the pebble in. Plop. And the cool, clear water "
        "rose right up to the very brim.",
    ),
    (
        "Part 8",
        "Sweet Water, Sweet Victory",
        "A happy crow drinking water from a full clay pot, "
        "eyes closed with joy, evening sunlight, forest glowing warmly, "
        "relief and happiness, fireflies appearing in background",
        "The crow dipped his beak into the cool water and drank. Oh, how sweet "
        "it was! He drank and drank until his thirst was completely gone. "
        "He looked up at the golden sky, and felt very proud — not because he "
        "was strong, but because he had been patient and clever.",
    ),
    (
        "",
        "Goodnight, Little One",
        "A crow sleeping peacefully on a moonlit branch, "
        "bright stars, a soft glowing moon, fireflies, "
        "a cozy peaceful forest at night, gentle and dreamy",
        "And so, dear child, the clever crow taught us something important. "
        "When a problem feels too hard, sit quietly and think. Look around you. "
        "The answer is often right there, waiting. Now close your eyes, "
        "dream of cool water and kind forests. Goodnight.",
    ),
]

# ── Voice config ──────────────────────────────────────────────────────────────
VOICE = {
    "language_code": "en-US",
    "name": "en-US-Chirp3-HD-Aoede",   # warm, soothing feminine voice
    "fallback": "en-US-Neural2-F",
    "speaking_rate": 0.85,
    "pitch": -2.0,
}

# ── DALL-E 3 ──────────────────────────────────────────────────────────────────
def generate_image(scene_prompt: str, out_path: Path, force: bool) -> None:
    if out_path.exists() and not force:
        print(f"  [img] skip (cached) {out_path.name}")
        return
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    print(f"  [img] generating {out_path.name} …")
    resp = client.images.generate(
        model="dall-e-3",
        prompt=ART_STYLE + scene_prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    urllib.request.urlretrieve(resp.data[0].url, out_path)
    print(f"       ✓ saved {out_path.name}")


# ── PIL text overlay ──────────────────────────────────────────────────────────
def add_text_overlay(raw_img: Path, title: str, eyebrow: str,
                     out_path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(raw_img).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    W, H = 1920, 1080
    d = ImageDraw.Draw(img)

    # semi-transparent gradient bar at bottom
    bar = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    bd  = ImageDraw.Draw(bar)
    for y in range(220):
        alpha = int(180 * (y / 220))
        bd.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img.paste(bar, (0, H - 220), bar)

    try:
        f_body   = ImageFont.truetype(FONT_BODY,    28)
        f_eye    = ImageFont.truetype(FONT_BODY,    34)
        f_title  = ImageFont.truetype(FONT_HEADING, 68)
    except Exception:
        f_body = f_eye = f_title = ImageFont.load_default()

    # channel name top-right
    d.text((W - 28, 28), "Mitra AI Stories",
           fill=(255, 255, 255, 200), font=f_body, anchor="ra")

    # eyebrow (e.g. "PART 1")
    if eyebrow:
        d.text((48, H - 205), eyebrow.upper(),
               fill=(245, 158, 11), font=f_eye)

    # title — word-wrap, centred, bottom
    words, lines, current = title.split(), [], ""
    for w in words:
        t = f"{current} {w}".strip()
        if d.textbbox((0, 0), t, font=f_title)[2] < W - 120:
            current = t
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    y = H - 150
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=f_title)
        x  = (W - (bb[2] - bb[0])) / 2
        d.text((x + 2, y + 2), ln, fill=(0, 0, 0, 220), font=f_title)   # shadow
        d.text((x,     y),     ln, fill=(255, 255, 255), font=f_title)
        y += int(f_title.size * 1.2)

    img.save(out_path, "JPEG", quality=95)


# ── Google TTS ────────────────────────────────────────────────────────────────
def tts_to_file(text: str, out_path: Path, force: bool) -> None:
    if out_path.exists() and not force:
        print(f"  [tts] skip (cached) {out_path.name}")
        return
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    for voice_name in [VOICE["name"], VOICE["fallback"]]:
        try:
            resp = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=VOICE["language_code"],
                    name=voice_name,
                ),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=VOICE["speaking_rate"],
                    pitch=VOICE["pitch"],
                ),
            )
            out_path.write_bytes(resp.audio_content)
            print(f"  [tts] {out_path.name}  ({voice_name})")
            return
        except Exception as e:
            print(f"  [WARN] {voice_name} failed: {e}")
    raise RuntimeError("All TTS voices failed")


# ── ffmpeg helpers ────────────────────────────────────────────────────────────
def audio_duration(p: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(p),
    ])
    return float(out.strip())


def make_segment(img: Path, audio: Path, out: Path,
                 head_sil: float = 0.6, tail_sil: float = 1.8) -> None:
    """Longer tail silence for comfortable bedtime pacing."""
    if out.exists():
        print(f"  [seg] skip (cached) {out.name}")
        return
    a_dur = audio_duration(audio)
    total = head_sil + a_dur + tail_sil
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{total:.3f}", "-i", str(img),
        "-i", str(audio),
        "-f", "lavfi", "-t", f"{head_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-f", "lavfi", "-t", f"{tail_sil:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex", "[2:a][1:a][3:a]concat=n=3:v=0:a=1[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", str(out),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode()[-600:])
    print(f"  [seg] ✓ {out.name}")


def concat_segments(mp4s: list, out_mp4: Path) -> None:
    listfile = OUT_DIR / "_concat.txt"
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in mp4s))
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(listfile),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    listfile.unlink(missing_ok=True)
    dur = audio_duration(out_mp4)
    sz  = out_mp4.stat().st_size / (1024 * 1024)
    print(f"\n  ✅  {out_mp4.name}  {dur:.0f}s ({dur/60:.1f} min)  {sz:.1f} MB")
    print(f"  📁  {out_mp4.resolve()}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true",
                        help="Re-generate all images and audio (ignore cache)")
    args = parser.parse_args()

    segments: list[Path] = []

    for i, (eyebrow, title, scene_prompt, narration) in enumerate(SLIDES, 1):
        tag   = f"slide{i:02d}"
        print(f"\n── Slide {i:02d} / {len(SLIDES)}: {title or 'Title card'}")

        raw_img  = OUT_DIR / f"{tag}_raw.jpg"
        over_img = OUT_DIR / f"{tag}_overlay.jpg"
        audio    = OUT_DIR / f"{tag}.mp3"
        seg_mp4  = OUT_DIR / f"{tag}.mp4"

        # 1. DALL-E 3 image
        generate_image(scene_prompt, raw_img, args.force)

        # 2. PIL text overlay
        if not over_img.exists() or args.force:
            add_text_overlay(raw_img, title, eyebrow, over_img)
            print(f"  [ovr] ✓ {over_img.name}")
        else:
            print(f"  [ovr] skip (cached) {over_img.name}")

        # 3. TTS narration
        tts_to_file(narration, audio, args.force)

        # 4. ffmpeg segment
        make_segment(over_img, audio, seg_mp4)
        segments.append(seg_mp4)

    # 5. Concatenate all segments
    print(f"\n── Concatenating {len(segments)} segments …")
    concat_segments(segments, FINAL_MP4)

    # 6. YouTube metadata hint
    yt_meta = OUT_DIR / "youtube_metadata.txt"
    yt_meta.write_text(
        "TITLE: The Clever Crow | Bedtime Story for Kids | Mitra AI Stories\n\n"
        "DESCRIPTION:\n"
        "A thirsty crow finds a pot of water — but the water is too deep to reach.\n"
        "Watch how clever thinking and patience save the day in this beautiful classic fable.\n\n"
        "This gentle bedtime story teaches children that calm thinking and persistence\n"
        "always find a way — even when a problem seems impossible.\n\n"
        "🌙 New story every day. Subscribe to Mitra AI Stories.\n\n"
        "TAGS: bedtime story, clever crow story, crow and pitcher, moral story for kids,\n"
        "animated story, story in English, Mitra AI Stories, fable for children,\n"
        "Aesop fable, bedtime stories for toddlers, short story with moral\n\n"
        "CATEGORY: Education\n"
        "THUMBNAIL: use slide01_overlay.jpg or slide09_overlay.jpg\n"
    )
    print(f"  📝  YouTube metadata → {yt_meta.name}")


if __name__ == "__main__":
    main()
