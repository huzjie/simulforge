# -*- coding: utf-8 -*-
"""Small DSP helpers shared across the audio stack (pure Python, no numpy)."""
import math


def db_from_rms(rms, floor=1e-9):
    if rms <= floor:
        return -120.0
    return 20.0 * math.log10(rms)


def rms(samples):
    if not samples:
        return 0.0
    return math.sqrt(sum(x * x for x in samples) / len(samples))


def peak(samples):
    if not samples:
        return 0.0
    return max(abs(x) for x in samples)


def energy(samples):
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


def hamming_window(n):
    return [0.54 - 0.46 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]


def dft(x):
    """Naive DFT returning (real, imag) per bin (fine for short frames)."""
    n = len(x)
    out = []
    for k in range(n // 2 + 1):
        re = im = 0.0
        for t in range(n):
            ang = -2 * math.pi * k * t / n
            re += x[t] * math.cos(ang)
            im += x[t] * math.sin(ang)
        out.append((re, im))
    return out


def hz_to_mel(hz):
    return 2595.0 * math.log10(1.0 + hz / 700.0)


def mel_to_hz(mel):
    return 700.0 * (10 ** (mel / 2595.0) - 1.0)


def mel_filterbank(n_mels, n_fft, sample_rate):
    """Triangular mel filterbank -> list of (start_bin, center_bin, end_bin)."""
    n_bins = n_fft // 2 + 1
    f_min, f_max = 0.0, sample_rate / 2.0
    m_min, m_max = hz_to_mel(f_min), hz_to_mel(f_max)
    mel_points = [m_min + (m_max - m_min) * i / (n_mels + 1) for i in range(n_mels + 2)]
    hz_points = [mel_to_hz(m) for m in mel_points]
    bins = [int(math.floor((n_fft + 1) * hz / sample_rate)) for hz in hz_points]
    banks = []
    for i in range(n_mels):
        banks.append((bins[i], bins[i + 1], bins[i + 2]))
    return banks
