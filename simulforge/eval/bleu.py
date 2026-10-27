# -*- coding: utf-8 -*-
"""Corpus BLEU scorer over token lists."""


class BleuScorer:
    def __init__(self, max_n=2):
        self.max_n = max_n

    def score(self, reference, hypothesis):
        """BLEU for a single (reference, hypothesis) pair."""
        from ..utils.metrics import bleu
        return bleu([(reference, hypothesis)], max_n=self.max_n)

    def corpus(self, pairs):
        from ..utils.metrics import bleu
        return bleu(pairs, max_n=self.max_n)
