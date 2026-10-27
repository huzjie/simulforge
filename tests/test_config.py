# -*- coding: utf-8 -*-
import unittest

from simulforge.config import Config, load_config


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        cfg = Config()
        self.assertEqual(cfg.audio.sample_rate, 16000)
        self.assertEqual(cfg.policy.default_policy, "adaptive")
        self.assertEqual(cfg.declared.project, "Hy-SimulMT")

    def test_load_default_yaml(self):
        cfg = load_config()
        self.assertEqual(cfg.declared.vendor, "Tencent Hunyuan")
        self.assertAlmostEqual(cfg.declared.latency_seconds, 3.0)

    def test_load_direct_s2s(self):
        from pathlib import Path
        here = Path(__file__).resolve().parents[1]
        p = here / "simulforge" / "configs" / "direct_s2s.yaml"
        cfg = load_config(str(p))
        self.assertTrue(cfg.s2s.direct)
        self.assertFalse(cfg.cascade.use_cascade)

    def test_roundtrip(self):
        cfg = Config()
        d = cfg.to_dict()
        self.assertEqual(d["bench"]["skills"], [0.5, 0.625, 0.75, 0.875, 1.0])


if __name__ == "__main__":
    unittest.main()
