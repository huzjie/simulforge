# -*- coding: utf-8 -*-
"""High-level evaluator that scores an interpretation result across all axes."""


class Evaluator:
    def __init__(self, cfg=None):
        self.cfg = cfg

    def score_transcript(self, reference, hypothesis):
        from ..utils.metrics import word_error_rate
        return 1.0 - word_error_rate(reference, hypothesis)

    def score_translation(self, reference, hypothesis):
        from ..utils.metrics import bleu
        return bleu([(reference, hypothesis)])

    def score_speaker(self, ref_embed, hyp_embed):
        from ..utils.metrics import cosine
        return cosine(ref_embed, hyp_embed)
