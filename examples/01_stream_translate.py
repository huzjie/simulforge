# -*- coding: utf-8 -*-
"""Run standalone: python examples/01_stream_translate.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulforge.engine import SimultaneousEngine


def main():
    engine = SimultaneousEngine(skill=1.0)
    r = engine.interpret("hello-world", speaker_id="speaker-alice")
    print("policy        :", r["policy"])
    print("source_len    :", r["source_len"])
    print("target_len    :", r["target_len"])
    print("bleu          : %.4f" % r["bleu"])
    print("quality       : %.4f" % r["quality"])
    print("speaker sim   : %.4f" % r["similarity"])
    print("StreamLAAL    : %.3f s" % r["latency"]["streamlaal_s"])
    print("AL            : %.3f words" % r["latency"]["al_words"])


if __name__ == "__main__":
    main()
