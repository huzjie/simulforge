# -*- coding: utf-8 -*-
import unittest

from simulforge.latency.revision import RevisionTracker, CommitPolicy


class TestRevision(unittest.TestCase):
    def test_n_revisions(self):
        t = RevisionTracker()
        t.emit([1, 2, 3], [1, 2, 3])
        t.emit([1, 2, 4], [1, 2, 4])  # position 2 flipped
        t.emit([1, 2, 4], [1, 2, 4])
        self.assertEqual(t.n_revisions, 1)

    def test_revision_rate(self):
        t = RevisionTracker()
        t.emit([1, 2], [1, 2])
        t.emit([1, 3], [1, 3])
        self.assertAlmostEqual(t.revision_rate(), 1.0, places=6)

    def test_commit_policy(self):
        self.assertTrue(CommitPolicy.should_commit("greedy", 0.1))
        self.assertFalse(CommitPolicy.should_commit("threshold", 0.5, 0.9))
        self.assertTrue(CommitPolicy.should_commit("threshold", 0.95, 0.9))


if __name__ == "__main__":
    unittest.main()
