# -*- coding: utf-8 -*-
"""Streaming chunkers: split a live audio stream into fixed or adaptive windows.

Simultaneous interpretation feeds audio in small chunks so the ASR can emit
partial hypotheses as soon as speech starts, instead of waiting for the end of a
sentence. A fixed window is the simplest policy; an adaptive chunker grows the
window while speech is active (energy above threshold) so word boundaries are
less likely to be split mid-phoneme.
"""


class FixedWindowChunker:
    """Split samples into fixed-length chunks with a fixed hop."""

    def __init__(self, window_ms=100, hop_ms=100, sample_rate=16000):
        self.window_ms = window_ms
        self.hop_ms = hop_ms
        self.sample_rate = sample_rate

    def _n(self, ms):
        return max(1, int(self.sample_rate * ms / 1000))

    def iter_chunks(self, samples):
        win = self._n(self.window_ms)
        hop = self._n(self.hop_ms)
        pos = 0
        t = 0
        while pos < len(samples):
            chunk = samples[pos:pos + win]
            yield chunk, t, t + int(len(chunk) * 1000 / self.sample_rate)
            pos += hop
            t += int(hop * 1000 / self.sample_rate)


class AdaptiveChunker:
    """Grow the window while speech is active, shrink it during silence.

    Uses a coarse energy threshold to decide whether to extend the current
    window (more context while speaking) or cut it (commit the chunk during a
    pause). This mirrors how a human interpreter waits for a natural pause.
    """

    def __init__(self, base_ms=60, max_ms=300, hop_ms=30, sample_rate=16000,
                 energy_threshold=0.02):
        self.base_ms = base_ms
        self.max_ms = max_ms
        self.hop_ms = hop_ms
        self.sample_rate = sample_rate
        self.energy_threshold = energy_threshold

    def _n(self, ms):
        return max(1, int(self.sample_rate * ms / 1000))

    @staticmethod
    def _energy(x):
        return sum(v * v for v in x) / len(x) if x else 0.0

    def iter_chunks(self, samples):
        pos = 0
        t = 0
        base = self._n(self.base_ms)
        maxn = self._n(self.max_ms)
        hop = self._n(self.hop_ms)
        while pos < len(samples):
            win = base
            # extend while the trailing window still has speech energy
            while win < maxn and pos + win + hop <= len(samples):
                tail = samples[pos + win:pos + win + hop]
                if self._energy(tail) < self.energy_threshold:
                    break
                win += hop
            chunk = samples[pos:pos + win]
            yield chunk, t, t + int(len(chunk) * 1000 / self.sample_rate)
            pos += win
            t += int(win * 1000 / self.sample_rate)
