# -*- coding: utf-8 -*-
"""Run standalone: python examples/08_adaptive_policy.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.engine import SimultaneousEngine


def main():
    for skill in (0.5, 0.75, 1.0):
        e = SimultaneousEngine(skill=skill)
        r = e.interpret("adaptive-demo")
        print("skill=%.2f policy=%-22s StreamLAAL=%.3fs quality=%.4f" %
              (skill, r["policy"], r["latency"]["streamlaal_s"], r["quality"]))
    print()
    print("Confidence-adaptive policy writes earlier as skill rises -> lower latency.")


if __name__ == "__main__":
    main()
