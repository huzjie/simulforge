# -*- coding: utf-8 -*-
"""Run standalone: python examples/07_vad_demo.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.audio.vad import EnergyVAD
from simulforge.oracle import reference_audio


def main():
    samples = reference_audio("vad-demo", sample_rate=16000, seconds=2.0)
    vad = EnergyVAD(sample_rate=16000, energy_threshold=0.02,
                    min_speech_ms=100, min_silence_ms=100)
    segs = vad.segment(samples)
    print("voiced segments:", len(segs))
    for s in segs:
        print("  %s" % s)


if __name__ == "__main__":
    main()
