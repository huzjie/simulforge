# -*- coding: utf-8 -*-
"""Monotonic multihead attention policy (MMA).

MMA (Arivazhagan et al. 2019; Ma et al. 2020) learns a hard-monotonic alignment
between source and target positions, so a target word is emitted only after the
attention energy for the next source word exceeds a learned threshold. Here the
"energy" is a deterministic function of (source position, target position,
skill); a higher skill concentrates energy earlier, yielding lower lag.
"""
from .base import Policy, Decision, READ, WRITE


class MonotonicAlignmentPolicy(Policy):
    name = "mma"

    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def decide(self, source_read, source_len, target_written, target_len,
               confidence):
        if target_written >= target_len:
            return Decision(READ)
        if source_read >= source_len:
            return Decision(WRITE, confidence=confidence)
        # deterministic energy at the current alignment point
        energy = _energy(source_read, target_written)
        if energy >= self.threshold:
            return Decision(WRITE, confidence=confidence)
        return Decision(READ, confidence=confidence)

    def describe(self):
        return "mma(thr=%.2f)" % self.threshold


def _energy(src_pos, tgt_pos):
    """Deterministic, monotonically increasing-in-src energy for a point."""
    # a simple logistic in (src - tgt) so energy rises as we read ahead
    z = (src_pos - tgt_pos) / 3.0
    e = 1.0 / (1.0 + 2.718281828459045 ** (-z))
    return e
