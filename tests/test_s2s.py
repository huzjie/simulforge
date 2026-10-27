# -*- coding: utf-8 -*-
import unittest

from simulforge.s2s import speaker_embed, embed_similarity, DirectS2S, VoiceCloner
from simulforge.model import S2sModel


class TestS2S(unittest.TestCase):
    def test_embedding_unit(self):
        e = speaker_embed("s1", dim=32)
        self.assertEqual(len(e), 32)
        self.assertAlmostEqual(sum(x * x for x in e), 1.0, places=6)

    def test_similarity_self(self):
        e = speaker_embed("s1", dim=32)
        self.assertAlmostEqual(embed_similarity(e, e), 1.0, places=6)

    def test_direct(self):
        d = DirectS2S(S2sModel(skill=1.0))
        out = d.run("d1", speaker_id="spk")
        self.assertIn("speech", out)
        self.assertIsNone(out["transcript"])

    def test_cloner(self):
        c = VoiceCloner(dim=32)
        e = c.embed("spk")
        self.assertAlmostEqual(c.similarity("spk", e), 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
