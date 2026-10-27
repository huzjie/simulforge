# -*- coding: utf-8 -*-
"""One-shot train + benchmark: demonstrate the skill -> metrics climb end-to-end."""
from .train import train
from .bench import run_all
from .engine import SimultaneousEngine


def main():
    print("=== 1) train (skill 0.5 -> ~1.0) ===", flush=True)
    engine, trace = train(SimultaneousEngine(skill=0.5), max_steps=24, log_every=8)
    print("trained skill: %.4f" % engine.skill, flush=True)
    print()
    print("=== 2) benchmark skill sweep ===", flush=True)
    rows, ok = run_all()
    print()
    print("=== 3) sample interpretation @ trained skill ===", flush=True)
    r = engine.interpret("run-all-sample", speaker_id="speaker-1")
    print("policy=%s bleu=%.4f quality=%.4f similarity=%.4f StreamLAAL=%.3fs" %
          (r["policy"], r["bleu"], r["quality"], r["similarity"],
           r["latency"]["streamlaal_s"]), flush=True)
    print()
    print("ALL OK" if ok else "MONOTONICITY FAILED")


if __name__ == "__main__":
    main()
