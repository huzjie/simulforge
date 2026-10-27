# -*- coding: utf-8 -*-
"""A chunk or segment of audio with timing metadata."""


class SpeechSegment:
    """A contiguous slice of the audio stream.

    Attributes
    ----------
    samples : list[float]
        The PCM samples in this segment.
    start_ms : int
        Start time in milliseconds (relative to stream start).
    end_ms : int
        End time in milliseconds.
    """

    def __init__(self, samples, start_ms, end_ms):
        self.samples = list(samples)
        self.start_ms = int(start_ms)
        self.end_ms = int(end_ms)

    @property
    def duration_ms(self):
        return self.end_ms - self.start_ms

    @property
    def n_samples(self):
        return len(self.samples)

    def __repr__(self):
        return "SpeechSegment(start=%dms, end=%dms, n=%d)" % (
            self.start_ms, self.end_ms, self.n_samples)
