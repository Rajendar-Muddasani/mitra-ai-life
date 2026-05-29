#!/usr/bin/env python3
"""
Generate overview videos for the main track pages that do not already have a
live overview video.

Outputs:
    content/assets/videos/track-overviews/{slug}-overview-{lang}.mp4
    content/assets/videos/track-overviews/{slug}-overview-{lang}-poster.jpg

Usage:
  source .venv/bin/activate
  python scripts/generate_track_overview_videos.py --track daily-life
    python scripts/generate_track_overview_videos.py --track daily-life --lang te
  python scripts/generate_track_overview_videos.py
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content" / "assets" / "videos" / "track-overviews"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VERSION_SUFFIX_BY_LANG = {"en": "", "te": "-v2"}

WIDTH, HEIGHT = 1920, 1080
TEXT = (248, 251, 255)
MUTED = (184, 199, 218)
NAVY = (6, 17, 31)


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()


def find_font(candidates: list[str]) -> str:
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise SystemExit(f"No font found among: {candidates}")


FONT_HEADING = find_font([
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
FONT_BODY = find_font([
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
])
FONT_TE_HEADING = find_font([
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Bold.ttf"),
    "/System/Library/Fonts/KohinoorTelugu.ttc",
    "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc",
])
FONT_TE_BODY = find_font([
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Regular.ttf"),
    str(ROOT / "scripts" / "_fonts" / "NotoSansTelugu-Bold.ttf"),
    "/System/Library/Fonts/KohinoorTelugu.ttc",
    "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc",
])


TRACKS = {
    "daily-life": {
        "title": "AI for Daily Life",
        "accent": (104, 225, 255),
        "warm": (245, 158, 11),
        "slides": [
            ("MITRA AI LIFE", "AI for Daily Life", "Free beginner lessons for everyday Indian life"),
            ("START SIMPLE", "Use AI for real daily tasks", "Messages, letters, summaries, budgets, planning, and family help."),
            ("STAY SAFE", "Learn what not to trust", "Scams, fake news, deepfakes, privacy, and AI mistakes are explained simply."),
            ("LEARN VISUALLY", "Ten free levels are live", "Short lessons, practical examples, and no technical background needed."),
            ("START FREE", "Begin with Level 1 today", "Open AI for Daily Life and build one useful habit at a time."),
        ],
        "narration": [
            "Mitra AI Life presents AI for Daily Life. Free beginner lessons for everyday Indian life.",
            "Start simple. Use AI for real daily tasks. Messages, letters, summaries, family planning, budgets, and helpful daily routines.",
            "Stay safe. Learn what not to trust. Scams, fake news, deepfakes, privacy, and AI mistakes are explained in simple words.",
            "Learn visually. Ten free levels are live now. The lessons use practical examples and do not require any technical background.",
            "Start free today. Begin with Level 1 and build one useful AI habit at a time.",
        ],
    },
    "students": {
        "title": "AI for Students",
        "accent": (125, 211, 252),
        "warm": (250, 204, 21),
        "slides": [
            ("CLASS 6 TO JC +2", "AI for Students", "School-safe AI literacy, class by class"),
            ("USE AI HONESTLY", "Study help, not cheating", "Prompting, research, revision, coding, and project skills with responsibility."),
            ("CLASS BY CLASS", "Start from your level", "Every class has its own free hub, written lessons, and age-appropriate examples."),
            ("BUILD SKILLS", "From awareness to AI projects", "Older classes move into Python, machine learning, apps, and portfolio projects."),
            ("START NOW", "Choose your class", "Open the student track, pick your class, and begin the first free lesson."),
        ],
        "narration": [
            "Mitra AI Life presents AI for Students. A school-safe AI learning path from Class 6 to Junior College plus 2.",
            "Use AI honestly. This track is for study help, not cheating. Students learn prompting, research, revision, coding, and project skills with responsibility.",
            "Start from your level. Every class has its own free hub, written lessons, and examples that match the learner's age.",
            "Build skills step by step. Older classes move into Python, machine learning, AI apps, and portfolio projects.",
            "Start now. Open the student track, choose your class, and begin the first free lesson.",
        ],
    },
    "tuition": {
        "title": "AI Tuition",
        "accent": (134, 239, 172),
        "warm": (251, 191, 36),
        "slides": [
            ("HINDI FOUNDATION", "AI Tuition", "Letters, sounds, reading, writing, and confidence"),
            ("ZERO TO STRONG", "Start with sounds", "Swar, vyanjan, barakhadi, numbers, words, grammar, reading, and speaking."),
            ("WATCH AND REPEAT", "Short visual practice", "Learners hear each sound clearly, repeat it, and connect letters with words."),
            ("PARENT FRIENDLY", "Simple learning path", "Choose a topic, watch the video, read the examples, and practice slowly."),
            ("START TODAY", "Begin with Letters and Sounds", "AI Tuition is built for steady practice, not pressure."),
        ],
        "narration": [
            "Mitra AI Life presents AI Tuition. A Hindi foundation path for letters, sounds, reading, writing, and confidence.",
            "Go from zero to strong. Start with sounds, then move through swar, vyanjan, barakhadi, numbers, words, grammar, reading, and speaking.",
            "Watch and repeat. Learners hear each sound clearly, repeat it slowly, and connect letters with real words.",
            "The path is parent friendly. Choose a topic, watch the video, read the examples, and practice one step at a time.",
            "Start today with Letters and Sounds. AI Tuition is built for steady practice, not pressure.",
        ],
    },
    "spoken-english": {
        "title": "Spoken English",
        "accent": (196, 181, 253),
        "warm": (251, 113, 133),
        "slides": [
            ("SPEAK WITH CONFIDENCE", "Spoken English", "Listen, repeat, roleplay, and use real conversations"),
            ("NO GRAMMAR FEAR", "Start with useful sentences", "Introduce yourself, ask for help, speak at shops, offices, and interviews."),
            ("PRACTICE SAFELY", "Use AI before real conversations", "Try, repeat, correct, and build confidence without embarrassment."),
            ("REAL LIFE FIRST", "Indian daily situations", "Students, job seekers, parents, and workers practice words they actually need."),
            ("START SMALL", "One conversation at a time", "Open the Spoken English track and begin with the first practical roleplay."),
        ],
        "narration": [
            "Mitra AI Life presents Spoken English. Learn through listening, repeating, roleplay, and real conversations.",
            "No grammar fear. Start with useful sentences for introducing yourself, asking for help, speaking at shops, offices, and interviews.",
            "Practice safely with AI before real conversations. Try, repeat, correct, and build confidence without embarrassment.",
            "Real life first. Students, job seekers, parents, and workers practice the words they actually need.",
            "Start small. Open the Spoken English track and begin with one practical roleplay at a time.",
        ],
    },
    "projects": {
        "title": "AI Project Kits",
        "accent": (0, 212, 170),
        "warm": (240, 180, 41),
        "slides": [
            ("PREMIUM BUILD TRACK", "AI Project Kits", "Thesis-ready, portfolio-ready, and viva-ready AI projects"),
            ("NOT TOY DEMOS", "Build serious systems", "RAG assistants, dashboards, support bots, forecasting, and computer vision demos."),
            ("CLEAR DELIVERY", "Everything has a path", "Problem brief, milestones, architecture, code, deployment, report, PPT, and viva help."),
            ("FOR COLLEGE AND JOBS", "Show real proof", "Create a GitHub repo, a demo URL, and a clear project story for interviews."),
            ("START WITH PROJECT 01", "Document Q and A Assistant", "Open the first public kit and see how a serious AI project is structured."),
        ],
        "narration": [
            "Mitra AI Life presents AI Project Kits. Thesis-ready, portfolio-ready, and viva-ready AI projects.",
            "These are not toy demos. Build serious systems like RAG assistants, dashboards, support bots, forecasting tools, and computer vision demos.",
            "Every kit has a delivery path. Problem brief, milestones, architecture, code, deployment, report, presentation, and viva preparation.",
            "For college and jobs, show real proof. Create a GitHub repo, a demo URL, and a clear project story for interviews.",
            "Start with Project 01, the Document Q and A Assistant. Open the first public kit and see how a serious AI project is structured.",
        ],
    },
    "small-business": {
        "title": "AI for Small Business",
        "accent": (253, 186, 116),
        "warm": (34, 197, 94),
        "slides": [
            ("LOCAL BUSINESS FIRST", "AI for Small Business", "Practical AI help for shops, services, tutors, and home businesses"),
            ("CUSTOMER MESSAGES", "Write faster, reply calmly", "WhatsApp offers, customer replies, complaint responses, and product descriptions."),
            ("PROMOTION HELP", "Plan your month", "Festival offers, Instagram captions, posters, and simple campaign ideas."),
            ("STAY IN CONTROL", "AI assists, owner decides", "You review every message and never paste private customer data into AI tools."),
            ("START SIMPLE", "One useful workflow", "Open the Small Business track and begin with communication and promotion basics."),
        ],
        "narration": [
            "Mitra AI Life presents AI for Small Business. Practical AI help for shops, local services, tutors, and home businesses.",
            "Write faster and reply calmly. Use AI for WhatsApp offers, customer replies, complaint responses, and product descriptions.",
            "Get promotion help. Plan festival offers, Instagram captions, posters, and simple campaign ideas for the month.",
            "Stay in control. AI assists, the owner decides. Review every message and never paste private customer data into AI tools.",
            "Start simple. Open the Small Business track and begin with communication and promotion basics.",
        ],
    },
}


TRACKS_TE = {
    "daily-life": {
        "title": "రోజువారీ జీవితానికి AI",
        "accent": (104, 225, 255),
        "warm": (245, 158, 11),
        "slides": [
            ("MITRA AI LIFE", "రోజువారీ జీవితానికి AI", "Indian daily life కోసం simple AI skills"),
            ("సింపుల్ గా మొదలు", "Real daily పనులకు AI", "Message. Letter. Summary. Budget. Family plan."),
            ("సేఫ్టీ ముఖ్యం", "ఏది నమ్మకూడదో నేర్చుకోండి", "Scam check. Fake news check. Privacy check."),
            ("విజువల్ లెర్నింగ్", "10 beginner levels సిద్ధంగా ఉన్నాయి", "Short lessons. Practical examples. Simple practice."),
            ("ఇవాళే మొదలు", "Level 1 తో ఒక habit build చేయండి", "చిన్న practical task తో AI confidence పెంచుకోండి."),
        ],
        "narration": [
            "మిత్ర ఏ ఐ లైఫ్ లో రోజువారీ జీవితానికి ఏ ఐ ట్రాక్. ఇది beginners కోసం. Indian daily life లో ఉపయోగపడే simple skills ఇక్కడ నేర్చుకుంటారు.",
            "సింపుల్ గా మొదలు పెడదాం. ముందు message రాయడం. తర్వాత formal letter. తర్వాత short summary. తర్వాత family plan. ఒక్కో పని separately practice చేస్తారు.",
            "Safety part కూడా ఉంటుంది. Scam message ని check చేస్తారు. Fake news ని verify చేస్తారు. Privacy protect చేస్తారు. AI mistake ని cross check చేస్తారు.",
            "ఈ track visual గా ఉంటుంది. పది beginner levels సిద్ధంగా ఉన్నాయి. ఒక్క page ఒకసారి. Practical example ఒకసారి. Simple practice ఒకసారి.",
            "ఇవాళే Level 1 తో మొదలు పెట్టండి. చిన్న task తో start చేయండి. Daily life లో confidence step by step పెరుగుతుంది.",
        ],
    },
    "spoken-english": {
        "title": "Spoken English with AI",
        "accent": (196, 181, 253),
        "warm": (251, 113, 133),
        "slides": [
            ("SPEAK WITH CONFIDENCE", "Spoken English with AI", "Listen, repeat, roleplay, real conversations."),
            ("GRAMMAR భయం వద్దు", "Useful sentences తో start చేయండి", "Introduce. Ask for help. Speak at shops. Practice interviews."),
            ("SAFE PRACTICE", "Real conversation ముందు AI తో practice", "Try. Repeat. Correct. Build confidence."),
            ("REAL LIFE FIRST", "Indian situations కోసం English", "Student practice. Job practice. Parent practice. Work practice."),
            ("చిన్నగా మొదలు", "ఒక conversation ఒకసారి", "First practical roleplay తో speaking confidence పెంచుకోండి."),
        ],
        "narration": [
            "మిత్ర ఏ ఐ లైఫ్ లో Spoken English with AI track. ముందుగా వినండి. తర్వాత repeat చేయండి. తర్వాత roleplay చేయండి. తర్వాత real conversation కి prepare అవ్వండి.",
            "Grammar భయం అవసరం లేదు. ముందు self introduction. తర్వాత help అడగడం. తర్వాత shop లో మాట్లాడటం. తర్వాత interview answer practice.",
            "Real person తో మాట్లాడే ముందు AI తో practice చేయవచ్చు. ఒక sentence try చేయండి. అదే sentence repeat చేయండి. Mistake ఉంటే correct చేసుకోండి.",
            "ఈ track Indian situations కోసం. Students కి practice. Job seekers కి practice. Parents కి practice. Workers కి practice.",
            "చిన్నగా మొదలు పెట్టండి. ఒక్క conversation ఒకసారి. First roleplay తో speaking confidence పెంచుకోండి.",
        ],
    },
    "small-business": {
        "title": "Small Business కోసం AI",
        "accent": (253, 186, 116),
        "warm": (34, 197, 94),
        "slides": [
            ("LOCAL BUSINESS FIRST", "Small Business కోసం AI", "Shops, services, tutors, home businesses కోసం practical help."),
            ("CUSTOMER MESSAGES", "వేగంగా, calm గా reply చేయండి", "Offer message. Customer reply. Complaint response."),
            ("PROMOTION HELP", "మీ month plan చేయండి", "Festival offer. Caption. Poster idea. Campaign plan."),
            ("మీ control లో ఉంటుంది", "AI assist చేస్తుంది. Owner decide చేస్తారు.", "Private customer data ని AI tools లో paste చేయవద్దు."),
            ("సింపుల్ గా మొదలు", "ఒక useful workflow", "Communication మరియు promotion basics తో business confidence పెంచుకోండి."),
        ],
        "narration": [
            "మిత్ర ఏ ఐ లైఫ్ లో Small Business కోసం ఏ ఐ track. Shops కోసం help. Local services కోసం help. Tutors కోసం help. Home business కోసం help.",
            "Customer messages calm గా రాయండి. ముందుగా WhatsApp offer. తర్వాత customer reply. తర్వాత complaint response. తర్వాత product description.",
            "Promotion planning లో కూడా AI ఉపయోగపడుతుంది. ముందు festival offer. తర్వాత caption. తర్వాత poster idea. తర్వాత simple campaign plan.",
            "ఇది మీ control లో ఉంటుంది. AI assist చేస్తుంది. Owner final decision తీసుకుంటారు. Private customer data ని AI tools లో paste చేయకూడదు.",
            "సింపుల్ గా మొదలు పెట్టండి. ఒక useful workflow తో start చేయండి. Communication basics. Promotion basics. Business confidence step by step.",
        ],
    },
}


TRACKS_BY_LANG = {"en": TRACKS, "te": TRACKS_TE}


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def blend(color_a: tuple[int, int, int], color_b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(int(color_a[channel] * (1 - ratio) + color_b[channel] * ratio) for channel in range(3))


def render_slide(eyebrow: str, title: str, subline: str, path: Path, accent: tuple[int, int, int], warm: tuple[int, int, int], lang: str) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)

    for y_pos in range(HEIGHT):
        ratio = y_pos / HEIGHT
        draw.line([(0, y_pos), (WIDTH, y_pos)], fill=blend(NAVY, (12, 24, 44), ratio))

    for x_pos in range(0, WIDTH, 96):
        draw.line([(x_pos, 0), (x_pos, HEIGHT)], fill=(255, 255, 255, 10))
    for y_pos in range(0, HEIGHT, 96):
        draw.line([(0, y_pos), (WIDTH, y_pos)], fill=(255, 255, 255, 10))

    draw.rectangle([0, 0, WIDTH, 16], fill=warm)
    draw.rectangle([0, HEIGHT - 16, WIDTH, HEIGHT], fill=accent)
    draw.ellipse([WIDTH - 480, -180, WIDTH + 180, 480], outline=accent, width=10)
    draw.ellipse([-220, HEIGHT - 420, 380, HEIGHT + 180], outline=warm, width=8)

    font_body_path = FONT_TE_BODY if lang == "te" else FONT_BODY
    font_heading_path = FONT_TE_HEADING if lang == "te" else FONT_HEADING
    font_eyebrow = ImageFont.truetype(font_body_path, 38)
    font_title = ImageFont.truetype(font_heading_path, 104)
    font_sub = ImageFont.truetype(font_body_path, 48)
    font_brand = ImageFont.truetype(FONT_BODY, 30)

    eyebrow_width = draw.textbbox((0, 0), eyebrow, font=font_eyebrow)[2]
    eye_left = (WIDTH - eyebrow_width) / 2 - 30
    eye_right = (WIDTH + eyebrow_width) / 2 + 30
    draw.rounded_rectangle([eye_left, 108, eye_right, 180], radius=22, outline=accent, width=3)
    draw.text(((WIDTH - eyebrow_width) / 2, 122), eyebrow, fill=accent, font=font_eyebrow)

    title_lines = wrap_text(title, font_title, int(WIDTH * 0.82), draw)
    line_height = font_title.size + 18
    title_height = line_height * len(title_lines)
    title_y = (HEIGHT - title_height) / 2 - 60
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width) / 2 + 4, title_y + 4), line, fill=(0, 0, 0), font=font_title)
        draw.text(((WIDTH - line_width) / 2, title_y), line, fill=TEXT, font=font_title)
        title_y += line_height

    sub_lines = wrap_text(subline, font_sub, int(WIDTH * 0.78), draw)
    sub_y = title_y + 44
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width) / 2, sub_y), line, fill=MUTED, font=font_sub)
        sub_y += font_sub.size + 12

    brand = "mitraailife.com"
    brand_width = draw.textbbox((0, 0), brand, font=font_brand)[2]
    draw.text((WIDTH - brand_width - 64, HEIGHT - 72), brand, fill=MUTED, font=font_brand)
    image.save(path, "JPEG", quality=92)


def tts_to_file(text: str, out_path: Path, lang: str) -> None:
    if out_path.exists():
        return
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=text,
        speed=0.88 if lang == "te" else 0.95,
    ) as response:
        response.stream_to_file(str(out_path))
    print(f"  [tts] {out_path.name}")


def audio_duration(path: Path) -> float:
    output = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(output.strip())


def make_segment(image_path: Path, audio_path: Path, output_path: Path) -> None:
    if output_path.exists():
        return
    lead_silence = 0.25
    tail_silence = 0.45
    total_duration = lead_silence + audio_duration(audio_path) + tail_silence
    command = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{total_duration:.3f}", "-i", str(image_path),
        "-i", str(audio_path),
        "-f", "lavfi", "-t", f"{lead_silence:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-f", "lavfi", "-t", f"{tail_silence:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex", "[2:a][1:a][3:a]concat=n=3:v=0:a=1[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", str(output_path),
    ]
    subprocess.run(command, check=True, capture_output=True)
    print(f"  [seg] {output_path.name}")


def concat_segments(segment_paths: list[Path], output_path: Path) -> None:
    list_file = output_path.parent / f"_concat_{output_path.stem}.txt"
    list_file.write_text("".join(f"file '{segment_path.resolve()}'\n" for segment_path in segment_paths))
    command = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart", str(output_path),
    ]
    subprocess.run(command, check=True, capture_output=True)
    list_file.unlink()


def build_track(slug: str, lang: str, force: bool = False) -> Path:
    config = TRACKS_BY_LANG[lang][slug]
    work_dir = OUT_DIR / f"{slug}-{lang}"
    if force and work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    suffix = VERSION_SUFFIX_BY_LANG[lang]
    output_path = OUT_DIR / f"{slug}-overview-{lang}{suffix}.mp4"
    poster_path = OUT_DIR / f"{slug}-overview-{lang}{suffix}-poster.jpg"
    if force and output_path.exists():
        output_path.unlink()
    if output_path.exists() and not force:
        print(f"\n[{slug}] skip final exists: {output_path.name}")
        return output_path

    print(f"\n===== {config['title']} ({lang}) =====")
    segments: list[Path] = []
    slides = config["slides"]
    narration = config["narration"]
    for slide_number, ((eyebrow, title, subline), voiceover) in enumerate(zip(slides, narration), 1):
        slide_id = f"{slide_number:02d}"
        image_path = work_dir / f"slide-{slide_id}.jpg"
        audio_path = work_dir / f"narr-{slide_id}.mp3"
        segment_path = work_dir / f"seg-{slide_id}.mp4"
        print(f"[{slug}:{slide_id}] {title}")
        render_slide(eyebrow, title, subline, image_path, config["accent"], config["warm"], lang)
        if slide_number == 1:
            shutil.copyfile(image_path, poster_path)
        tts_to_file(voiceover, audio_path, lang)
        make_segment(image_path, audio_path, segment_path)
        segments.append(segment_path)

    print(f"[{slug}] concat -> {output_path.name}")
    concat_segments(segments, output_path)
    duration = audio_duration(output_path)
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[{slug}] done duration={duration:.1f}s size={size_mb:.2f} MB")
    return output_path


def parse_targets(raw_targets: str, lang: str) -> list[str]:
    available_tracks = TRACKS_BY_LANG[lang]
    if raw_targets == "all":
        return list(available_tracks.keys())
    targets = [target.strip() for target in raw_targets.split(",") if target.strip()]
    unknown = [target for target in targets if target not in available_tracks]
    if unknown:
        raise SystemExit(f"Unknown {lang} track(s): {', '.join(unknown)}")
    return targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", default="all", help="Track slug, comma list, or all")
    parser.add_argument("--lang", choices=["en", "te"], default="en")
    parser.add_argument("--force", action="store_true", help="Regenerate cached segments and final MP4")
    args = parser.parse_args()

    outputs = []
    for slug in parse_targets(args.track, args.lang):
        outputs.append((slug, build_track(slug, args.lang, force=args.force)))

    print("\nAll requested videos are ready:")
    for slug, output_path in outputs:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  {slug}: {output_path} ({size_mb:.2f} MB)")

    print("\nUpload commands:")
    for slug, output_path in outputs:
        print(
            "  aws s3 cp "
            f"{output_path} s3://mitra-ai-life-assets/videos/track-overviews/{output_path.name} "
            "--content-type 'video/mp4' --cache-control 'public, max-age=86400'"
        )
        poster_path = OUT_DIR / f"{output_path.stem}-poster.jpg"
        print(
            "  aws s3 cp "
            f"{poster_path} s3://mitra-ai-life-assets/videos/track-overviews/{poster_path.name} "
            "--content-type 'image/jpeg' --cache-control 'public, max-age=86400'"
        )


if __name__ == "__main__":
    main()