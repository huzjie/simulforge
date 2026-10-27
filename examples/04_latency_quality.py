# -*- coding: utf-8 -*-
"""Run standalone: python examples/04_latency_quality.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.eval import QualityLatencyTradeoff


def main():
    t = QualityLatencyTradeoff()
    print("%-6s %-12s %-10s" % ("skill", "latency(s)", "quality"))
    for skill in (0.5, 0.625, 0.75, 0.875, 1.0):
        print("%-6.3f %-12.2f %-10.3f" %
              (skill, t.latency_seconds(skill), t.quality("demo", skill)))
    print()
    print("The Pareto frontier: as the model improves, latency drops AND quality rises.")


if __name__ == "__main__":
    main()
