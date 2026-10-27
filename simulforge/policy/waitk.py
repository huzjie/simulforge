# -*- coding: utf-8 -*-
"""The wait-k policy: read k source words, then alternate read/write.

wait-k is the canonical SimulMT baseline (Ma et al. 2019). It commits the i-th
target word after reading ``k + i - 1`` source words, which makes the average
lagging essentially equal to ``k``. Larger ``k`` -> higher latency but more
context -> higher quality. The whole policy is one integer.
"""
from .base import Policy, Decision, READ, WRITE


class WaitKPolicy(Policy):
    name = "waitk"

    def __init__(self, k=4):
        self.k = max(1, int(k))

    def decide(self, source_read, source_len, target_written, target_len,
               confidence):
        if target_written >= target_len:
            return Decision(READ)
        if source_read < min(self.k + target_written, source_len):
            return Decision(READ, confidence=0.0)
        return Decision(WRITE, confidence=1.0)

    def describe(self):
        return "wait-k(k=%d)" % self.k
