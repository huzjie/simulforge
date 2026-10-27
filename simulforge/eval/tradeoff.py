# -*- coding: utf-8 -*-
"""The quality-latency tradeoff (the core tension of simultaneous translation).

Lower latency means less context means lower quality; more context means higher
quality but higher latency. The Pareto frontier is what a good policy navigates:
it wants to be as far up-left (high quality, low latency) as possible.
"""


class QualityLatencyTradeoff:
    def __init__(self, latency_max=8.0, latency_min=2.8):
        self.latency_max = latency_max
        self.latency_min = latency_min

    def latency_seconds(self, skill):
        """Monotonic decreasing latency in skill (8.0s -> 2.8s)."""
        return self.latency_max - (self.latency_max - self.latency_min) * skill

    def quality(self, audio_id, skill):
        from .gemba import GembaScorer
        g = GembaScorer()
        boost = (skill - 0.5) * 2.0
        return g.score(audio_id, boost)

    def quality_per_latency(self, audio_id, skill):
        """Quality per unit latency; rises as skill improves both axes."""
        q = self.quality(audio_id, skill)
        l = self.latency_seconds(skill)
        return q / (1.0 + l)
