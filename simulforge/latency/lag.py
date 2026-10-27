# -*- coding: utf-8 -*-
"""Latency metrics for simultaneous translation.

Average Lagging (AL) and Length-Adaptive Average Lagging (LAAL) are the standard
metrics from the SimulMT literature (Ma et al. 2019; Cherry & Foster 2019).
StreamLAAL (used by the RealSI long-audio benchmark that Hy-SimulMT reports) is
the length-adaptive lag expressed in *seconds* by multiplying by the nominal
seconds-per-word rate.
"""


def average_lagging(read_times, target_len, source_len):
    """AL = (1/tau) sum_i (g_i - (i-1)/gamma).

    ``read_times`` is a list where ``read_times[i]`` is the number of source
    words read when the (i+1)-th target word was committed. ``gamma`` is the
    target/source length ratio. Lower is better.
    """
    tau = len(read_times)
    if tau == 0:
        return 0.0
    gamma = (target_len / source_len) if source_len else 1.0
    total = 0.0
    for i, g in enumerate(read_times):
        total += max(0.0, g - (i / gamma))
    return total / tau


def length_adaptive_lagging(read_times, target_len, source_len):
    """LAAL normalizes AL so different target lengths are comparable."""
    al = average_lagging(read_times, target_len, source_len)
    if target_len <= 1:
        return al
    return al / target_len


def streamlaal(read_times, target_len, source_len, word_seconds=0.5):
    """StreamLAAL in seconds: length-adaptive lag * seconds-per-word."""
    return length_adaptive_lagging(read_times, target_len, source_len) * word_seconds
