# -*- coding: utf-8 -*-
import unittest

from simulforge.audio import (FixedWindowChunker, AdaptiveChunker,
                              linear_resample, mel_spectrogram)
from simulforge.utils.audio import rms, energy, hz_to_mel, mel_to_hz, mel_filterbank


class TestChunking(unittest.TestCase):
    def test_fixed_window(self):
        samples = list(range(1000))
        c = FixedWindowChunker(window_ms=100, hop_ms=100, sample_rate=1000)
        chunks = list(c.iter_chunks(samples))
        # 1000 samples / (100 samples per chunk) = 10 chunks
        self.assertEqual(len(chunks), 10)
        self.assertEqual(chunks[0][0], list(range(100)))

    def test_adaptive_window(self):
        samples = [0.0] * 50 + [0.5] * 100 + [0.0] * 50
        c = AdaptiveChunker(base_ms=20, max_ms=100, hop_ms=20,
                            sample_rate=1000, energy_threshold=0.02)
        chunks = list(c.iter_chunks(samples))
        self.assertGreater(len(chunks), 0)
        total = sum(len(ch[0]) for ch in chunks)
        self.assertEqual(total, len(samples))


class TestResample(unittest.TestCase):
    def test_linear_resample_same_rate(self):
        s = [0.1, 0.2, 0.3]
        self.assertEqual(linear_resample(s, 16000, 16000), s)

    def test_linear_resample_down(self):
        s = [0.0, 0.5, 1.0, 0.5, 0.0]
        out = linear_resample(s, 1000, 500)
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out[0], s[0], places=6)


class TestFeatures(unittest.TestCase):
    def test_mel_roundtrip(self):
        self.assertAlmostEqual(mel_to_hz(hz_to_mel(1000)), 1000, places=0)

    def test_mel_filterbank(self):
        banks = mel_filterbank(40, 512, 16000)
        self.assertEqual(len(banks), 40)

    def test_mel_spectrogram(self):
        samples = [0.3] * 2048
        frames = mel_spectrogram(samples, sample_rate=16000, n_fft=512, n_mels=20)
        self.assertGreater(len(frames), 0)
        self.assertEqual(len(frames[0]), 20)


class TestAudioUtils(unittest.TestCase):
    def test_energy(self):
        self.assertAlmostEqual(energy([0.5, 0.5]), 0.25, places=6)

    def test_rms(self):
        self.assertAlmostEqual(rms([0.0, 0.0]), 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
