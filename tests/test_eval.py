# -*- coding: utf-8 -*-
import unittest

from simulforge.eval import (GembaScorer, BleuScorer,
                             QualityLatencyTradeoff, Evaluator)
from simulforge.utils.metrics import bleu, word_error_rate, edit_distance, cosine


class TestGemba(unittest.TestCase):
    def test_gold_above_noise(self):
        g = GembaScorer()
        for i in range(20):
            aid = "g-%d" % i
            self.assertGreater(g.gold(aid), g.noise(aid))

    def test_score_monotonic(self):
        g = GembaScorer()
        for i in range(20):
            aid = "g-%d" % i
            self.assertLess(g.score(aid, 0.0), g.score(aid, 1.0))


class TestBleu(unittest.TestCase):
    def test_perfect(self):
        self.assertAlmostEqual(BleuScorer().score([1, 2, 3], [1, 2, 3]), 1.0, places=6)

    def test_empty_hyp(self):
        self.assertAlmostEqual(BleuScorer().score([1, 2], []), 0.0, places=6)


class TestTradeoff(unittest.TestCase):
    def test_latency_monotonic(self):
        t = QualityLatencyTradeoff()
        self.assertGreater(t.latency_seconds(0.5), t.latency_seconds(1.0))

    def test_qpl_monotonic(self):
        t = QualityLatencyTradeoff()
        for i in range(20):
            aid = "t-%d" % i
            self.assertLess(t.quality_per_latency(aid, 0.5),
                            t.quality_per_latency(aid, 1.0))


class TestMetrics(unittest.TestCase):
    def test_edit_distance(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)

    def test_wer(self):
        self.assertAlmostEqual(word_error_rate([1, 2, 3], [1, 2, 3]), 0.0)
        self.assertAlmostEqual(word_error_rate([1, 2], [3, 4]), 1.0)

    def test_cosine(self):
        self.assertAlmostEqual(cosine([1, 0], [1, 0]), 1.0, places=6)
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
