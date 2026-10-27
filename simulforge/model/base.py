# -*- coding: utf-8 -*-
"""Base mock model with a trainable ``skill`` in [0.5, 1.0].

``skill = 0.5`` means untrained (outputs are essentially random); ``skill =
1.0`` means perfect. The ``boost`` transform maps skill to [0, 1] so that
``boost = (skill - 0.5) * 2`` is 0 at the random baseline and 1 at the optimum.
Training nudges skill upward with ``skill += lr * (1 - skill)`` (geometric
climb), so every downstream metric moves monotonically toward the optimum.
"""
from ..utils.random import stable_float, stable_int


def boost(skill):
    return (skill - 0.5) * 2.0


class MockModel:
    def __init__(self, skill=0.5, vocab=2048):
        self.skill = skill
        self.vocab = vocab

    @property
    def b(self):
        return boost(self.skill)

    def _noisy_copy(self, tag, ref):
        """Copy ``ref`` token-by-token; each token is correct with probability
        ``0.5 + 0.5 * b`` (so skill=0.5 is random, skill=1.0 is exact)."""
        out = []
        for i, t in enumerate(ref):
            p_correct = 0.5 + 0.5 * self.b
            key = "%s:%d" % (tag, i)
            if stable_float(key) < p_correct:
                out.append(t)
            else:
                out.append(stable_int("hall:" + key, 0, self.vocab))
        return out

    def train_step(self, lr=0.3):
        """Geometric climb toward 1.0 (delta always positive)."""
        self.skill += lr * (1.0 - self.skill)
        return self.skill
