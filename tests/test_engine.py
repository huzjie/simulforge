# -*- coding: utf-8 -*-
import unittest

from simulforge.engine import SimultaneousEngine
from simulforge.oracle import sentence, translation


class TestEngine(unittest.TestCase):
    def test_interpret_cascade_perfect(self):
        e = SimultaneousEngine(skill=1.0)
        r = e.interpret("eng-1", speaker_id="spk-1", direct=False)
        self.assertEqual(r["transcript"], sentence("eng-1"))
        self.assertEqual(r["translation"], translation("eng-1"))
        self.assertAlmostEqual(r["bleu"], 1.0, places=6)
        self.assertAlmostEqual(r["similarity"], 1.0, places=6)
        self.assertIn("streamlaal_s", r["latency"])

    def test_interpret_direct(self):
        e = SimultaneousEngine(skill=0.5)
        r = e.interpret("eng-2", direct=True)
        self.assertTrue(r["direct"])
        self.assertIsNone(r["transcript"])

    def test_confidence_monotonic_in_skill(self):
        lo = SimultaneousEngine(skill=0.5)
        hi = SimultaneousEngine(skill=1.0)
        self.assertLess(lo.confidence("x", 1, 0), hi.confidence("x", 1, 0))
        self.assertEqual(lo.confidence("x", 0, 0), 0.0)

    def test_doctor(self):
        r = SimultaneousEngine(skill=0.5).doctor()
        self.assertIn("latency", r)


if __name__ == "__main__":
    unittest.main()
