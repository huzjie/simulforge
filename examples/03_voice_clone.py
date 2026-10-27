# -*- coding: utf-8 -*-
"""Run standalone: python examples/03_voice_clone.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.model import TtsModel
from simulforge.oracle import translation


def main():
    for skill in (0.5, 0.75, 1.0):
        tts = TtsModel(skill=skill, embed_dim=32)
        out = tts.synthesize("clone-demo", "speaker-bob", translation("clone-demo"))
        print("skill=%.2f -> speaker similarity=%.4f" % (skill, out["similarity"]))
    print()
    print("Higher skill reproduces the speaker's timbre almost exactly.")


if __name__ == "__main__":
    main()
