# -*- coding: utf-8 -*-
import unittest

from simulforge.latency.lag import (average_lagging,
                                    length_adaptive_lagging, streamlaal)


class TestLag(unittest.TestCase):
    def test_al_wait1(self):
        # wait-1 trace on equal lengths -> AL == 1.0
        read_times = [1, 2, 3, 4]
        al = average_lagging(read_times, target_len=4, source_len=4)
        self.assertAlmostEqual(al, 1.0, places=9)

    def test_laal(self):
        read_times = [1, 2, 3, 4]
        laal = length_adaptive_lagging(read_times, 4, 4)
        self.assertAlmostEqual(laal, 0.25, places=9)

    def test_streamlaal(self):
        read_times = [1, 2, 3, 4]
        s = streamlaal(read_times, 4, 4, word_seconds=0.5)
        self.assertAlmostEqual(s, 0.125, places=9)

    def test_empty(self):
        self.assertEqual(average_lagging([], 0, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
