# -*- coding: utf-8 -*-
"""StreamLAAL latency metric (seconds), as reported by the RealSI benchmark."""


class StreamLAALMetric:
    def __init__(self, word_seconds=0.5):
        self.word_seconds = word_seconds

    def score(self, read_times, target_len, source_len):
        from ..latency.lag import streamlaal
        return streamlaal(read_times, target_len, source_len, self.word_seconds)
