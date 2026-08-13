from __future__ import annotations

import json
import math
import statistics
import struct
import wave
from itertools import pairwise
from pathlib import Path

from .models import HeartbeatSignature
from .provenance import canonical_json, sha256_bytes, sha256_file


def _decode_pcm(raw: bytes, sample_width: int) -> list[float]:
    if sample_width == 1:
        return [(value - 128) / 128.0 for value in raw]
    if sample_width == 2:
        count = len(raw) // 2
        return [value / 32768.0 for value in struct.unpack(f"<{count}h", raw)]
    if sample_width == 3:
        values: list[float] = []
        for i in range(0, len(raw), 3):
            chunk = raw[i : i + 3]
            if len(chunk) < 3:
                break
            value = int.from_bytes(chunk, "little", signed=True)
            values.append(value / 8388608.0)
        return values
    if sample_width == 4:
        count = len(raw) // 4
        return [value / 2147483648.0 for value in struct.unpack(f"<{count}i", raw)]
    raise ValueError(f"Unsupported PCM sample width: {sample_width} bytes")


def _mono(samples: list[float], channels: int) -> list[float]:
    if channels == 1:
        return samples
    if channels < 1:
        raise ValueError("WAV file reports no audio channels")
    mono: list[float] = []
    usable = len(samples) - (len(samples) % channels)
    for index in range(0, usable, channels):
        frame = samples[index : index + channels]
        mono.append(sum(frame) / channels)
    return mono


def _window_envelope(samples: list[float], sample_rate: int, window_ms: float) -> tuple[list[float], int]:
    window = max(1, int(sample_rate * window_ms / 1000.0))
    envelope: list[float] = []
    for start in range(0, len(samples), window):
        chunk = samples[start : start + window]
        if not chunk:
            continue
        rms = math.sqrt(sum(value * value for value in chunk) / len(chunk))
        envelope.append(rms)
    return envelope, window


def _detect_peaks(envelope: list[float], seconds_per_window: float, min_interval: float) -> list[int]:
    if len(envelope) < 3 or max(envelope, default=0.0) <= 0.0:
        return []

    median = statistics.median(envelope)
    mad = statistics.median(abs(value - median) for value in envelope)
    threshold = max(median + 3.0 * mad, max(envelope) * 0.15)

    candidates: list[int] = []
    for index in range(1, len(envelope) - 1):
        value = envelope[index]
        if value < threshold:
            continue
        left = envelope[index - 1]
        right = envelope[index + 1]
        if value >= left and value >= right and (value > left or value > right):
            candidates.append(index)

    min_windows = max(1, round(min_interval / seconds_per_window))
    chosen: list[int] = []
    for candidate in sorted(candidates, key=lambda i: envelope[i], reverse=True):
        if all(abs(candidate - existing) >= min_windows for existing in chosen):
            chosen.append(candidate)
    return sorted(chosen)


def analyze_wav(path: str | Path, *, window_ms: float = 25.0, min_interval: float = 0.30) -> HeartbeatSignature:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)

    with wave.open(str(source), "rb") as wav:
        if wav.getcomptype() != "NONE":
            raise ValueError("Only uncompressed PCM WAV files are supported")
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frame_count = wav.getnframes()
        raw = wav.readframes(frame_count)

    samples = _mono(_decode_pcm(raw, sample_width), channels)
    if sample_rate <= 0 or len(samples) < sample_rate // 2:
        raise ValueError("Heartbeat sample must contain at least 0.5 seconds of audio")

    envelope, window_size = _window_envelope(samples, sample_rate, window_ms)
    seconds_per_window = window_size / sample_rate
    peak_indices = _detect_peaks(envelope, seconds_per_window, min_interval)
    beat_times = [round((index + 0.5) * seconds_per_window, 6) for index in peak_indices]
    intervals = [round(b - a, 6) for a, b in pairwise(beat_times)]
    bpm = round(60.0 / statistics.median(intervals), 3) if intervals else None
    duration = round(len(samples) / sample_rate, 6)

    digest_payload = {
        "algorithm": "heartlight-envelope-peaks-v1",
        "source_sha256": sha256_file(source),
        "sample_rate": sample_rate,
        "duration_seconds": duration,
        "beat_times_seconds": beat_times,
        "intervals_seconds": intervals,
        "estimated_bpm": bpm,
    }
    rhythm_digest = sha256_bytes(canonical_json(digest_payload).encode("utf-8"))

    return HeartbeatSignature(
        source_sha256=digest_payload["source_sha256"],
        sample_rate=sample_rate,
        duration_seconds=duration,
        beat_times_seconds=beat_times,
        intervals_seconds=intervals,
        estimated_bpm=bpm,
        rhythm_digest=rhythm_digest,
    )


def signature_json(path: str | Path) -> str:
    return json.dumps(analyze_wav(path).to_dict(), indent=2, sort_keys=True)
