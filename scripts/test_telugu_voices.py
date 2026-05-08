"""
Telugu Voice Test Script
========================
Tests all available te-IN voices with:
  1. Plain text — "AI" as-is (current behaviour, wrong pronunciation)
  2. SSML fix — "AI" spelled out using <say-as interpret-as="characters">

Run:  source .env && .venv/bin/python scripts/test_telugu_voices.py

Output: voice_tests/ folder with MP3 files. Listen and pick the best voice.

Files produced:
  voice_tests/te-IN-Standard-A-plain.mp3   ← current voice, wrong AI sound
  voice_tests/te-IN-Standard-A-fixed.mp3   ← current voice, AI fixed
  voice_tests/te-IN-Standard-B-plain.mp3
  voice_tests/te-IN-Standard-B-fixed.mp3
  voice_tests/te-IN-Wavenet-A-plain.mp3    ← better quality female
  voice_tests/te-IN-Wavenet-A-fixed.mp3
  voice_tests/te-IN-Wavenet-B-plain.mp3    ← better quality male
  voice_tests/te-IN-Wavenet-B-fixed.mp3
"""

import os
import pathlib
from google.cloud import texttospeech

OUT_DIR = pathlib.Path("voice_tests")
OUT_DIR.mkdir(exist_ok=True)

client = texttospeech.TextToSpeechClient()

# Sample text that contains "AI" several times — similar to what's in the videos
PLAIN_TEXT = (
    "నమస్కారం! నేను మిత్ర. "
    "AI అంటే Artificial Intelligence. "
    "AI మీ రోజువారీ జీవితాన్ని చాలా సులభంగా చేస్తుంది. "
    "ChatGPT, Google Bard వంటి AI tools ఇప్పుడు అందరికీ అందుబాటులో ఉన్నాయి. "
    "మీరు AI ని phone లో కూడా వాడవచ్చు — text type చేయండి, answer వస్తుంది!"
)

# SSML version — AI is forced to say each letter: "Ay Eye"
SSML_TEXT = (
    "నమస్కారం! నేను మిత్ర. "
    '<say-as interpret-as="characters">AI</say-as> అంటే Artificial Intelligence. '
    '<say-as interpret-as="characters">AI</say-as> మీ రోజువారీ జీవితాన్ని చాలా సులభంగా చేస్తుంది. '
    "ChatGPT, Google Bard వంటి "
    '<say-as interpret-as="characters">AI</say-as> tools ఇప్పుడు అందరికీ అందుబాటులో ఉన్నాయి. '
    "మీరు "
    '<say-as interpret-as="characters">AI</say-as>'
    " ని phone లో కూడా వాడవచ్చు — text type చేయండి, answer వస్తుంది!"
)

VOICES = [
    "te-IN-Standard-A",   # female — current
    "te-IN-Standard-B",   # male
    "te-IN-Wavenet-A",    # female HQ
    "te-IN-Wavenet-B",    # male HQ
]

AUDIO_CFG = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.90,
)

def synthesize(input_obj, voice_name, out_path):
    voice = texttospeech.VoiceSelectionParams(
        language_code="te-IN",
        name=voice_name,
    )
    try:
        resp = client.synthesize_speech(input=input_obj, voice=voice, audio_config=AUDIO_CFG)
        out_path.write_bytes(resp.audio_content)
        size_kb = len(resp.audio_content) // 1024
        print(f"  ✅  {out_path.name}  ({size_kb} KB)")
    except Exception as e:
        print(f"  ❌  {voice_name}: {e}")

print("\n=== Telugu Voice Test ===\n")
for voice_name in VOICES:
    print(f"▶ {voice_name}")

    # Test 1: plain text (current approach — AI may sound wrong)
    plain_input = texttospeech.SynthesisInput(text=PLAIN_TEXT)
    synthesize(plain_input, voice_name, OUT_DIR / f"{voice_name}-plain.mp3")

    # Test 2: SSML with say-as fix
    ssml_input = texttospeech.SynthesisInput(ssml=f"<speak>{SSML_TEXT}</speak>")
    synthesize(ssml_input, voice_name, OUT_DIR / f"{voice_name}-fixed.mp3")

print(f"\nDone! Open the 'voice_tests/' folder and listen to all files.")
print("Pick the voice you like and tell me — I'll update all 10 video scripts.")
print("\nNaming guide:")
print("  Standard-A/B = normal quality  |  Wavenet-A/B = higher quality (costs more)")
print("  -plain.mp3  = current AI sound |  -fixed.mp3  = AI fixed (Ay + Eye)\n")
