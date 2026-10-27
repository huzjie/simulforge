# -*- coding: utf-8 -*-
import unittest

from simulforge.model import AsrModel, MtModel, TtsModel
from simulforge.cascade import (StreamingASR, StreamingMT, StreamingTTS,
                                CascadePipeline)
from simulforge.oracle import sentence, translation


class TestCascade(unittest.TestCase):
    def test_streaming_asr_prefix(self):
        asr = StreamingASR(AsrModel(skill=1.0))
        partial = asr.feed_chunk("c1", 3)
        self.assertEqual(len(partial), 3)
        self.assertEqual(partial, sentence("c1")[:3])

    def test_pipeline(self):
        pipe = CascadePipeline(StreamingASR(AsrModel(skill=1.0)),
                               StreamingMT(MtModel(skill=1.0)),
                               StreamingTTS(TtsModel(skill=1.0)))
        out = pipe.run("c2", speaker_id="spk")
        self.assertEqual(out["transcript"], sentence("c2"))
        self.assertEqual(out["translation"], translation("c2"))
        self.assertIn("speech", out["speech"])


if __name__ == "__main__":
    unittest.main()
