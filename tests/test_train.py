# -*- coding: utf-8 -*-
import unittest

from simulforge.train import train
from simulforge.engine import SimultaneousEngine


class TestTrain(unittest.TestCase):
    def test_skill_climbs(self):
        e = SimultaneousEngine(skill=0.5)
        prev = e.skill
        for _ in range(10):
            s = e.train_step()
            self.assertGreater(s, prev)
            prev = s
        self.assertGreater(prev, 0.9)

    def test_train_loop(self):
        engine, trace = train(SimultaneousEngine(skill=0.5),
                              lr=0.3, max_steps=24, log_every=100)
        self.assertGreater(engine.skill, 0.99)
        self.assertEqual(len(trace), 25)
        for a, b in zip(trace, trace[1:]):
            self.assertGreater(b, a)


if __name__ == "__main__":
    unittest.main()
