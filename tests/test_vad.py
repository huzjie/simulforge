# -*- coding: utf-8 -*-
import unittest

from simulforge.audio.vad import EnergyVAD


class TestVAD(unittest.TestCase):
    def test_finds_speech(self):
        # 100ms silence + 200ms loud + 100ms silence @ 16kHz
        samples = [0.0] * 1600 + [0.5] * 3200 + [0.0] * 1600
        vad = EnergyVAD(sample_rate=16000, energy_threshold=0.02,
                        min_speech_ms=100, min_silence_ms=100)
        segs = vad.segment(samples)
        self.assertGreaterEqual(len(segs), 1)
        self.assertGreater(segs[0].n_samples, 0)

    def test_silence_returns_empty(self):
        samples = [0.0] * 3200
        vad = EnergyVAD(sample_rate=16000, energy_threshold=0.02,
                        min_speech_ms=100, min_silence_ms=100)
        self.assertEqual(vad.segment(samples), [])


if __name__ == "__main__":
    unittest.main()
