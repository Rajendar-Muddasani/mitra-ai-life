"""
Shared A/V sync helper for Hindi tuition video scripts.

Adds a short head-silence before TTS audio so the visible card/frame has time to
register before the narrator speaks. Also adds tail silence so the child has a
moment to say it back before the next clip cuts in.

Usage:
    from _av_sync import padded_audio
    audio = AudioFileClip(path)
    padded = padded_audio(audio, head=0.3, tail=0.6)
    clip = ImageClip(frame, duration=padded.duration).with_audio(padded)
"""

from __future__ import annotations

import numpy as np


def silence_clip(duration: float, fps: int = 44100, nchannels: int = 2):
    from moviepy import AudioArrayClip
    n_samples = max(1, int(duration * fps))
    arr = np.zeros((n_samples, nchannels), dtype=np.float32)
    return AudioArrayClip(arr, fps=fps)


def padded_audio(audio, head: float = 0.3, tail: float = 0.6):
    """Return `audio` with `head` seconds of silence prepended and `tail` appended."""
    from moviepy import concatenate_audioclips
    fps = getattr(audio, "fps", None) or 44100
    nchannels = getattr(audio, "nchannels", None) or 2
    parts = []
    if head > 0:
        parts.append(silence_clip(head, fps=fps, nchannels=nchannels))
    parts.append(audio)
    if tail > 0:
        parts.append(silence_clip(tail, fps=fps, nchannels=nchannels))
    return concatenate_audioclips(parts)
