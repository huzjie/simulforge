# -*- coding: utf-8 -*-
"""GEMBA-style quality scoring.

GEMBA (GPT Estimation Metric Based Assessment) scores translation quality with a
model instead of surface n-gram overlap. Here the "model" is deterministic and
skill-monotonic: quality = boost * gold + (1-boost) * noise, where gold is the
per-sentence ceiling and noise is the per-sentence random baseline.
"""
from ..utils.random import stable_float


class GembaScorer:
    def __init__(self):
        pass

    def gold(self, audio_id):
        """Deterministic per-sentence quality ceiling in [0.85, 0.95]."""
        return 0.85 + 0.10 * stable_float("gemba-gold:" + str(audio_id), 0.0, 1.0)

    def noise(self, audio_id):
        """Deterministic per-sentence random baseline in [0.15, 0.35]."""
        return 0.15 + 0.20 * stable_float("gemba-noise:" + str(audio_id), 0.0, 1.0)

    def score(self, audio_id, boost):
        """Quality in [0,1] that is monotonically increasing in ``boost``."""
        return boost * self.gold(audio_id) + (1.0 - boost) * self.noise(audio_id)
