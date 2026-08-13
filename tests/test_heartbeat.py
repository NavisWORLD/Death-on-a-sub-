import math
import struct
import wave

from heartlight.heartbeat import analyze_wav


def _write_pulse_wav(path, sample_rate=8000, seconds=6.0, bpm=60):
    total = int(sample_rate * seconds)
    samples = [0.0] * total
    interval = 60.0 / bpm
    t = 0.5
    while t < seconds - 0.2:
        center = int(t * sample_rate)
        width = int(0.05 * sample_rate)
        for i in range(max(0, center - width), min(total, center + width)):
            phase = (i - center) / sample_rate
            samples[i] += 0.8 * math.exp(-abs(phase) * 45.0)
        t += interval
    pcm = b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)


def test_detects_regular_pulse(tmp_path):
    path = tmp_path / "pulse.wav"
    _write_pulse_wav(path)
    result = analyze_wav(path)
    assert len(result.beat_times_seconds) >= 4
    assert result.estimated_bpm is not None
    assert 55 <= result.estimated_bpm <= 65
    assert len(result.rhythm_digest) == 64
