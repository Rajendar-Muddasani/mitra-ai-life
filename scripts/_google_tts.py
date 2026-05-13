"""
_google_tts.py — Google Cloud TTS wrapper for Hindi tuition scripts.

Replaces OpenAI tts-1 for all Hindi content.
Uses hi-IN-Chirp3-HD voices (highest quality) by default.

API pricing: ~$0.000016 per character for Chirp3-HD (~10× cheaper than OpenAI tts-1).

Usage:
    from _google_tts import tts_to_bytes, tts_to_file, DEFAULT_VOICE

    data = tts_to_bytes("कमल", speed=0.70)
    tts_to_file("कमल", Path("kamal.mp3"), speed=0.70)
"""

from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Default: Chirp3-HD Kore — clear, natural Hindi, preferred by user review
DEFAULT_VOICE = "hi-IN-Chirp3-HD-Kore"

# Speaking rate mapping from the old OpenAI "speed" scale (0.65–0.82)
# to Google's speaking_rate (0.25–4.0, where 1.0 = normal).
# We keep the same relative slowness.
def _grate(openai_speed: float) -> float:
    """Convert OpenAI speed (0.65-0.82) to Google speaking_rate."""
    return openai_speed


def _client():
    env_path = ROOT / ".env"
    if env_path.exists() and not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    from google.cloud import texttospeech
    return texttospeech.TextToSpeechClient()


def tts_to_bytes(text: str, speed: float = 0.70,
                 voice: str = DEFAULT_VOICE) -> bytes:
    """Synthesise `text` in Hindi and return raw MP3 bytes."""
    from google.cloud import texttospeech
    client = _client()
    resp = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(
            language_code="hi-IN", name=voice
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=_grate(speed),
        ),
    )
    return resp.audio_content


def tts_to_file(text: str, out_path: Path, speed: float = 0.70,
                voice: str = DEFAULT_VOICE, skip_existing: bool = True) -> None:
    """Synthesise `text` and stream to `out_path` (MP3)."""
    out_path = Path(out_path)
    if skip_existing and out_path.exists():
        print(f"  [SKIP] {out_path.name}")
        return
    print(f"  [gTTS] {repr(text[:40])}  →  {out_path.name}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(tts_to_bytes(text, speed=speed, voice=voice))
