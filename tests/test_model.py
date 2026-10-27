# -*- coding: utf-8 -*-
import unittest

from simulforge.model import AsrModel, MtModel, TtsModel, S2sModel, boost
from simulforge.oracle import sentence, translation
from simulforge.utils.metrics import word_error_rate, mean


class TestModel(unittest.TestCase):
    def test_boost(self):
        self.assertEqual(boost(0.5), 0.0)
        self.assertEqual(boost(1.0), 1.0)

    def test_perfect_skill_is_exact(self):
        self.assertEqual(AsrModel(skill=1.0).transcribe("m1"), sentence("m1"))
        self.assertEqual(MtModel(skill=1.0).translate("m1"), translation("m1"))

    def test_wer_decreases_with_skill(self):
        aids = ["agg-%d" % i for i in range(50)]
        def avg_wer(skill):
            m = AsrModel(skill=skill)
            ws = [word_error_rate(sentence(a), m.transcribe(a)) for a in aids]
            return mean(ws)
        w0 = avg_wer(0.5)
        w1 = avg_wer(1.0)
        self.assertLess(w1, w0)
        self.assertLessEqual(avg_wer(0.75), w0 + 1e-9)

    def test_tts_similarity_monotonic(self):
        low = TtsModel(skill=0.5).synthesize("t1", "spk", [1, 2, 3])
        high = TtsModel(skill=1.0).synthesize("t1", "spk", [1, 2, 3])
        self.assertLess(low["similarity"], high["similarity"])
        self.assertAlmostEqual(high["similarity"], 1.0, places=6)

    def test_train_step(self):
        m = AsrModel(skill=0.5)
        prev = m.skill
        for _ in range(5):
            s = m.train_step(0.3)
            self.assertGreater(s, prev)
            prev = s


if __name__ == "__main__":
    unittest.main()
