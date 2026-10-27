# -*- coding: utf-8 -*-
"""LatencyManager: turn a read/write trace into lag metrics.

A policy's sequence of READ/WRITE decisions determines ``read_times`` (how many
source words were read when each target word was committed). The manager folds
that trace into AL / LAAL / StreamLAAL and a seconds value.
"""


class LatencyManager:
    def __init__(self, word_seconds=0.5):
        self.word_seconds = word_seconds

    def build_read_times(self, source_len, target_len, policy, confidence_fn):
        """Simulate the policy and return read_times, translation_out.

        ``confidence_fn(source_read, target_written) -> float`` supplies the
        model confidence at each step. Returns ``(read_times, translation)``
        where translation is a list of target word indices.
        """
        read_times = []
        translation = []
        source_read = 0
        target_written = 0
        # translation is the reference translation by index (quality scored later)
        for _ in range(10 * max(source_len, target_len) + 10):
            if target_written >= target_len:
                break
            conf = confidence_fn(source_read, target_written)
            from ..policy.base import READ, WRITE
            decision = policy.decide(source_read, source_len,
                                     target_written, target_len, conf)
            if decision.action == WRITE:
                read_times.append(source_read)
                translation.append(target_written)  # positional marker
                target_written += 1
            else:
                source_read = min(source_len, source_read + 1)
                if source_read >= source_len:
                    # drain remaining target words
                    while target_written < target_len:
                        read_times.append(source_read)
                        translation.append(target_written)
                        target_written += 1
                    break
        return read_times, translation

    def measure(self, read_times, target_len, source_len):
        from .lag import average_lagging, length_adaptive_lagging, streamlaal
        return {
            "al_words": average_lagging(read_times, target_len, source_len),
            "laal": length_adaptive_lagging(read_times, target_len, source_len),
            "streamlaal_s": streamlaal(read_times, target_len, source_len,
                                       self.word_seconds),
        }
