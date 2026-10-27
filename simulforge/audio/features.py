# -*- coding: utf-8 -*-
"""Frame-level audio features: energy, zero-crossing rate, mel spectrogram.

All implemented in pure Python so the managed runtime stays dependency-free.
The mel filterbank + DFT is a genuine (if unoptimized) feature front-end; with a
trained model these frames would feed the streaming ASR encoder.
"""
import math

from ..utils.audio import hamming_window, dft, mel_filterbank


def frame_energy(samples):
    if not samples:
        return 0.0
    return sum(x * x for x in samples) / len(samples)


def zero_crossing_rate(samples):
    if len(samples) < 2:
        return 0.0
    n = 0
    for i in range(1, len(samples)):
        if (samples[i - 1] >= 0) != (samples[i] >= 0):
            n += 1
    return n / (len(samples) - 1)


def mel_spectrogram(samples, sample_rate=16000, n_fft=512, n_mels=40):
    """Compute a mel spectrogram (list of frames, each a list of mel energies).

    Returns a list of frames; each frame is a list of ``n_mels`` float energies.
    """
    if not samples:
        return []
    win = hamming_window(n_fft)
    banks = mel_filterbank(n_mels, n_fft, sample_rate)
    hop = n_fft // 2
    frames = []
    for start in range(0, len(samples) - n_fft + 1, hop):
        x = [samples[start + i] * win[i] for i in range(n_fft)]
        spec = dft(x)
        powers = [(re * re + im * im) for re, im in spec]
        mel = []
        for (a, b, c) in banks:
            val = 0.0
            for k in range(a, min(c + 1, len(powers))):
                if k <= b:
                    w = (k - a) / max(1, (b - a))
                else:
                    w = (c - k) / max(1, (c - b))
                val += powers[k] * w
            mel.append(math.log(val + 1e-9))
        frames.append(mel)
    return frames
