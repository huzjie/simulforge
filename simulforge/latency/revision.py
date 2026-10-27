# -*- coding: utf-8 -*-
"""Commit / revision bookkeeping for streaming translation.

A streaming system often *revises* earlier output as more context arrives (it
guesses a word, then corrects it). A commit policy decides when a word becomes
final. Tracking revisions is what lets you trade "how early" against "how often
I flip-flopped".
"""


class CommitPolicy:
    GREEDY = "greedy"
    THRESHOLD = "threshold"

    @staticmethod
    def should_commit(name, confidence, threshold=0.9):
        if name == CommitPolicy.THRESHOLD:
            return confidence >= threshold
        return True  # greedy: commit immediately


class RevisionTracker:
    def __init__(self):
        self.history = []
        self.final = []

    def emit(self, tokens, committed):
        """Record one emitted hypothesis and the number of tokens committed."""
        self.history.append(list(tokens))
        self.final = list(committed)

    @property
    def n_revisions(self):
        """Count position flips between consecutive hypotheses."""
        revs = 0
        for a, b in zip(self.history[:-1], self.history[1:]):
            for i in range(min(len(a), len(b))):
                if a[i] != b[i]:
                    revs += 1
        return revs

    def revision_rate(self):
        if len(self.history) < 2:
            return 0.0
        return self.n_revisions / max(1, len(self.history) - 1)
