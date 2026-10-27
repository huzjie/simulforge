# -*- coding: utf-8 -*-
"""Run standalone: python examples/06_s2s_direct.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.engine import SimultaneousEngine


def main():
    cascade = SimultaneousEngine(skill=1.0).interpret("s2s-demo", direct=False)
    direct = SimultaneousEngine(skill=1.0).interpret("s2s-demo", direct=True)
    print("cascade: bleu=%.4f sim=%.4f (has transcript)" %
          (cascade["bleu"], cascade["similarity"]))
    print("direct : bleu=%.4f sim=%.4f (no transcript, fewer cascaded errors)" %
          (direct["bleu"], direct["similarity"]))


if __name__ == "__main__":
    main()
