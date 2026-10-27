# -*- coding: utf-8 -*-
"""Energy-based voice activity detection.

Splits a stream into voiced segments separated by silence. The hangover
(``min_silence_ms``) prevents a brief pause from splitting one word into two
segments, and ``min_speech_ms`` discards clicks/pops that are too short to be
speech.
"""
from .segment import SpeechSegment


class EnergyVAD:
    def __init__(self, sample_rate=16000, energy_threshold=0.02,
                 min_speech_ms=300, min_silence_ms=200, frame_ms=25):
        self.sample_rate = sample_rate
        self.energy_threshold = energy_threshold
        self.min_speech_ms = min_speech_ms
        self.min_silence_ms = min_silence_ms
        self.frame_ms = frame_ms

    def _frame_n(self):
        return max(1, int(self.sample_rate * self.frame_ms / 1000))

    def _energy(self, x):
        return sum(v * v for v in x) / len(x) if x else 0.0

    def segment(self, samples):
        """Return a list of SpeechSegment for voiced regions."""
        fn = self._frame_n()
        frames = [samples[i:i + fn] for i in range(0, len(samples), fn)]
        if not frames:
            return []

        voiced = [self._energy(f) >= self.energy_threshold for f in frames]
        frame_ms = self.frame_ms
        segments = []
        i = 0
        n = len(voiced)
        while i < n:
            if not voiced[i]:
                i += 1
                continue
            start = i
            j = i
            while j < n and voiced[j]:
                j += 1
            end = j  # first non-voiced frame (or n)
            # hangover: short silences are absorbed into the segment
            k = j
            while k < n and not voiced[k]:
                k += 1
            silence_ms = (k - j) * frame_ms
            if silence_ms < self.min_silence_ms:
                end = k
            start_ms = start * frame_ms
            end_ms = end * frame_ms
            if end_ms - start_ms >= self.min_speech_ms:
                s0 = start * fn
                s1 = min(len(samples), end * fn)
                segments.append(SpeechSegment(samples[s0:s1], start_ms, end_ms))
            i = max(end, i + 1)
        return segments
