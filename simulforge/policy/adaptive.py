# -*- coding: utf-8 -*-
"""Confidence-adaptive policy: WRITE when confident, READ otherwise.

The model emits a confidence score for the current partial hypothesis. The
policy writes the next target word only when confidence exceeds a threshold;
otherwise it reads more source context. A higher ``skill`` model is confident
sooner, so it writes earlier -- lowering latency without sacrificing quality.
This is the mechanism behind Hy-SimulMT's near-3-second StreamLAAL.
"""
from .base import Policy, Decision, READ, WRITE


class AdaptivePolicy(Policy):
    name = "adaptive"

    def __init__(self, threshold=0.6, patience=6):
        self.threshold = threshold
        self.patience = max(1, int(patience))
        self._stuck = 0

    def decide(self, source_read, source_len, target_written, target_len,
               confidence):
        if target_written >= target_len:
            return Decision(READ)
        if source_read >= source_len:
            # no more source; must write out the rest
            return Decision(WRITE, confidence=confidence)
        if confidence >= self.threshold:
            self._stuck = 0
            return Decision(WRITE, confidence=confidence)
        # avoid livelock: force a write if we have read too long without emitting
        self._stuck += 1
        if self._stuck >= self.patience:
            self._stuck = 0
            return Decision(WRITE, confidence=confidence)
        return Decision(READ, confidence=confidence)

    def describe(self):
        return "adaptive(thr=%.2f)" % self.threshold
