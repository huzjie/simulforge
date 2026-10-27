# -*- coding: utf-8 -*-
import unittest

from simulforge.policy import (WaitKPolicy, Prefix2PrefixPolicy, AdaptivePolicy,
                               MonotonicAlignmentPolicy, get_policy, list_policies,
                               READ, WRITE)


class TestWaitK(unittest.TestCase):
    def test_reads_k_first(self):
        p = WaitKPolicy(k=3)
        self.assertEqual(p.decide(0, 10, 0, 5, 0.0).action, READ)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.0).action, READ)
        self.assertEqual(p.decide(3, 10, 0, 5, 0.0).action, WRITE)

    def test_alternates(self):
        p = WaitKPolicy(k=2)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.0).action, WRITE)
        self.assertEqual(p.decide(2, 10, 1, 5, 0.0).action, READ)


class TestPrefix2Prefix(unittest.TestCase):
    def test_reads_before_write(self):
        p = Prefix2PrefixPolicy(k=0)
        # source 10, target 5 -> ratio 2; target word 0 needs 0 source, but +0
        self.assertEqual(p.decide(0, 10, 0, 5, 0.0).action, WRITE)


class TestAdaptive(unittest.TestCase):
    def test_writes_when_confident(self):
        p = AdaptivePolicy(threshold=0.6)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.9).action, WRITE)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.1).action, READ)

    def test_no_livelock(self):
        p = AdaptivePolicy(threshold=0.99, patience=3)
        # always low confidence but patience forces a write on the 3rd stuck step
        self.assertEqual(p.decide(2, 10, 0, 5, 0.1).action, READ)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.1).action, READ)
        self.assertEqual(p.decide(2, 10, 0, 5, 0.1).action, WRITE)


class TestMMA(unittest.TestCase):
    def test_energy_writes_when_high(self):
        p = MonotonicAlignmentPolicy(threshold=0.5)
        # large read-ahead -> energy high -> WRITE
        self.assertEqual(p.decide(9, 10, 0, 5, 0.0).action, WRITE)
        # lagging behind (src < tgt) -> energy below threshold -> READ
        self.assertEqual(p.decide(0, 10, 3, 5, 0.0).action, READ)


class TestRegistry(unittest.TestCase):
    def test_get_policy(self):
        self.assertIsInstance(get_policy("waitk"), WaitKPolicy)
        self.assertIsInstance(get_policy("mma"), MonotonicAlignmentPolicy)
        self.assertIsInstance(get_policy("bogus"), AdaptivePolicy)

    def test_list_policies(self):
        self.assertIn("adaptive", list_policies())


if __name__ == "__main__":
    unittest.main()
