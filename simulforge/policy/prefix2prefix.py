# -*- coding: utf-8 -*-
"""Prefix-to-prefix policy: keep the source/target prefix ratio aligned.

Instead of a fixed offset like wait-k, prefix-to-prefix commits the i-th target
word once ``source_read / source_len >= target_written / target_len`` (modulo a
lag ``k``). This adapts the lag to the relative lengths of the two languages,
which matters for language pairs with very different word rates (e.g. Chinese is
compact, English is wordy).
"""
from .base import Policy, Decision, READ, WRITE


class Prefix2PrefixPolicy(Policy):
    name = "prefix2prefix"

    def __init__(self, k=4):
        self.k = max(0, int(k))

    def decide(self, source_read, source_len, target_written, target_len,
               confidence):
        if target_written >= target_len:
            return Decision(READ)
        if target_len <= 0:
            return Decision(READ)
        ratio = source_len / target_len if target_len else 1.0
        needed = int(target_written * ratio) + self.k
        if source_read < min(needed, source_len):
            return Decision(READ, confidence=0.0)
        return Decision(WRITE, confidence=1.0)

    def describe(self):
        return "prefix-to-prefix(k=%d)" % self.k
