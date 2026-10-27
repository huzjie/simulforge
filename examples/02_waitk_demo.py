# -*- coding: utf-8 -*-
"""Run standalone: python examples/02_waitk_demo.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.policy import WaitKPolicy, Prefix2PrefixPolicy
from simulforge.latency import LatencyManager


def main():
    source_len, target_len = 10, 9
    mgr = LatencyManager(word_seconds=0.5)
    print("%-16s %-10s %-10s" % ("policy", "AL(words)", "StreamLAAL(s)"))
    for k in (2, 4, 6, 8):
        p = WaitKPolicy(k=k)
        read_times, _ = mgr.build_read_times(
            source_len, target_len, p, lambda sr, tw: 1.0)
        m = mgr.measure(read_times, target_len, source_len)
        print("%-16s %-10.3f %-10.3f" % (p.describe(), m["al_words"], m["streamlaal_s"]))
    print()
    print("Larger wait-k -> more context -> higher latency (the core tradeoff).")


if __name__ == "__main__":
    main()
