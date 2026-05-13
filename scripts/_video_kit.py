"""
_video_kit.py — bit-exact A/V sync helper for Hindi tuition videos.

Why this exists
---------------
The original pipeline built each "show the form / play the narration" segment
with moviepy and stitched them with `concatenate_videoclips(method="compose")`.
That introduced two visible defects:

  1. The TTS model emits a variable amount of leading silence (anywhere from
     ~0 to ~600 ms). With a fixed 0.3 s visual-first prefix added on top, the
     speech sometimes started 1+ seconds after the visual appeared.

  2. Moviepy's audio re-mixing during concatenation accumulates a few ms of
     drift per clip. Over 400 segments (barakhadi-sync.mp4) that drift grows
     into seconds — the audio for one form ends up under the visual of the
     next.

Strategy
--------
For each (frame, narration) pair we render an atomic, self-contained MP4 with
exactly the same codec parameters. The atomic clip is built so that:

  - The voiced portion of the TTS starts exactly `head_sil` seconds into the
    clip — leading silence the model emitted is trimmed first.
  - The clip ends `tail_sil` seconds after speech finishes (room for the
    child to say it back).
  - Video duration and audio duration are equal to the millisecond.

We then concatenate the atomic MP4s with `ffmpeg -f concat -c copy`. No
re-encoding, no drift, just file-level stitching.

Public API
----------
  detect_speech_onset(audio_path)   -> seconds of leading silence to trim
  audio_duration(audio_path)        -> seconds (float)
  make_atomic_mp4(...)              -> writes one self-contained mp4
  concat_mp4s(mp4_paths, out_mp4)   -> lossless concat
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np


# ── Audio analysis ────────────────────────────────────────────────────────────


def detect_speech_onset(audio_path: Path, threshold_db: float = -40.0,
                        frame_ms: int = 20) -> float:
    """Return seconds of leading silence in `audio_path`.

    Uses framewise RMS in dBFS. Anything below `threshold_db` is treated as
    silence. -40 dBFS is conservative enough that quiet aspirated consonants
    still register, but typical TTS room-tone is treated as silent.

    Returns 0.0 if the file is shorter than one frame or never crosses the
    threshold (in which case there is nothing useful to trim).
    """
    import soundfile as sf

    data, sr = sf.read(str(audio_path))
    if data.ndim > 1:
        data = data.mean(axis=1)
    if len(data) == 0:
        return 0.0

    frame_len = max(1, int(sr * frame_ms / 1000))
    n_frames = len(data) // frame_len
    if n_frames == 0:
        return 0.0

    frames = data[:n_frames * frame_len].reshape(n_frames, frame_len).astype(np.float32)
    rms = np.sqrt((frames ** 2).mean(axis=1) + 1e-12)
    db = 20.0 * np.log10(rms + 1e-12)

    above = np.where(db > threshold_db)[0]
    if len(above) == 0:
        return 0.0
    # Step back one frame so we don't clip the consonant's attack
    onset_frame = max(0, int(above[0]) - 1)
    return onset_frame * frame_ms / 1000.0


def audio_duration(audio_path: Path) -> float:
    """Return precise duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(audio_path),
    ]
    out = subprocess.check_output(cmd).decode()
    return float(json.loads(out)["format"]["duration"])


# ── Atomic clip rendering ─────────────────────────────────────────────────────


# Codec params kept identical across all atomic clips so concat -c copy works.
ATOMIC_FPS         = 24
ATOMIC_VIDEO_CODEC = "libx264"
ATOMIC_PIX_FMT     = "yuv420p"
ATOMIC_AUDIO_CODEC = "aac"
ATOMIC_AUDIO_RATE  = 44100
ATOMIC_AUDIO_BR    = "128k"
ATOMIC_AUDIO_CH    = 2


def make_atomic_mp4(
    frame_path: Path,
    audio_path: Path,
    out_path: Path,
    head_sil: float = 0.3,
    tail_sil: float = 0.6,
    trim_lead_silence: bool = True,
) -> None:
    """Render one self-contained MP4 from a static frame and a TTS audio file.

    Timeline inside the resulting clip:
        0.0 ......... frame appears
        head_sil .... voiced TTS begins (leading model-silence stripped)
        head_sil + spoken_dur .... voiced TTS ends
        head_sil + spoken_dur + tail_sil .... clip ends, frame still showing
    """
    frame_path = Path(frame_path)
    audio_path = Path(audio_path)
    out_path   = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lead = detect_speech_onset(audio_path) if trim_lead_silence else 0.0
    raw_dur = audio_duration(audio_path)
    spoken_dur = max(0.05, raw_dur - lead)
    total = head_sil + spoken_dur + tail_sil

    # Audio filtergraph: trim leading silence, then prepend head_sil silence,
    # then pad to `total` seconds (this also covers the tail silence).
    head_ms = int(round(head_sil * 1000))
    af = (
        f"atrim=start={lead:.4f},asetpts=PTS-STARTPTS,"
        f"adelay={head_ms}|{head_ms},"
        f"apad=whole_dur={total:.4f},"
        f"aresample={ATOMIC_AUDIO_RATE},aformat=channel_layouts=stereo"
    )

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-loop", "1", "-r", str(ATOMIC_FPS), "-i", str(frame_path),
        "-i", str(audio_path),
        "-filter_complex", f"[1:a]{af}[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-t", f"{total:.4f}",
        "-c:v", ATOMIC_VIDEO_CODEC, "-pix_fmt", ATOMIC_PIX_FMT, "-r", str(ATOMIC_FPS),
        "-c:a", ATOMIC_AUDIO_CODEC, "-b:a", ATOMIC_AUDIO_BR,
        "-ar", str(ATOMIC_AUDIO_RATE), "-ac", str(ATOMIC_AUDIO_CH),
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stderr=subprocess.PIPE)


# ── Lossless concat ───────────────────────────────────────────────────────────


def concat_mp4s(mp4_paths: list[Path], out_path: Path) -> None:
    """Concatenate atomic MP4s into one file using ffmpeg's concat demuxer.

    Uses `-c copy` so no re-encoding happens — sync is preserved bit-for-bit.
    All inputs must share codec parameters (use the constants in this module).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    list_file = out_path.parent / f".concat_{out_path.stem}.txt"
    list_file.write_text(
        "\n".join(f"file '{Path(p).resolve()}'" for p in mp4_paths),
        encoding="utf-8",
    )
    try:
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            "-movflags", "+faststart",
            str(out_path),
        ]
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    finally:
        try:
            list_file.unlink()
        except FileNotFoundError:
            pass
