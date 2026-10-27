# -*- coding: utf-8 -*-
"""Linear-interpolation resampler (pure Python)."""


def linear_resample(samples, src_rate, dst_rate):
    """Resample a list of samples from src_rate to dst_rate by linear interp."""
    if not samples or src_rate == dst_rate:
        return list(samples)
    ratio = src_rate / dst_rate
    out = []
    n_out = max(1, int(len(samples) / ratio))
    for i in range(n_out):
        pos = i * ratio
        lo = int(pos)
        hi = min(lo + 1, len(samples) - 1)
        frac = pos - lo
        out.append(samples[lo] * (1.0 - frac) + samples[hi] * frac)
    return out
