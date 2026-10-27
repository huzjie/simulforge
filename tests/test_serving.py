# -*- coding: utf-8 -*-
import unittest

from simulforge.serving import _summary
from simulforge.engine import SimultaneousEngine


class TestServing(unittest.TestCase):
    def test_summary(self):
        e = SimultaneousEngine(skill=1.0)
        r = e.interpret("srv-1", speaker_id="spk", direct=False)
        s = _summary(r)
        self.assertEqual(s["audio_id"], "srv-1")
        self.assertIn("streamlaal_s", s)
        self.assertAlmostEqual(s["bleu"], 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
