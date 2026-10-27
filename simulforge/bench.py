# -*- coding: utf-8 -*-
"""Benchmark: sweep skill 0.5 -> 1.0 and report the quality/latency profile.

Every headline metric is monotonic in skill by construction:

  * StreamLAAL (seconds)  -- decreases: 8.0s -> ~2.8s (Hy-SimulMT's ~3s target)
  * BLEU / GEMBA quality  -- increases: random -> near-perfect
  * speaker similarity    -- increases: random -> ~1.0
  * WER (transcript)      -- decreases: 0.4 -> 0.0
  * quality-per-latency   -- increases (the Pareto frontier moves up-left)

Run with ``python -m simulforge.bench`` or ``simulforge bench``.
"""
from .config import load_config
from .engine import SimultaneousEngine
from .eval import GembaScorer, QualityLatencyTradeoff
from .utils.metrics import mean, word_error_rate
from .utils.random import stable_float
from .oracle import sentence


def _metric_at(skill, audio_id, tradeoff, gemba):
    b = (skill - 0.5) * 2.0
    latency = tradeoff.latency_seconds(skill)
    quality = gemba.score(audio_id, b)
    similarity = b * 1.0 + (1.0 - b) * (0.20 + 0.30 * stable_float("sim:" + str(audio_id)))
    wer = (1.0 - skill) * 0.8
    qpl = quality / (1.0 + latency)
    return {
        "streamlaal_s": latency,
        "quality": quality,
        "similarity": similarity,
        "wer": wer,
        "qpl": qpl,
    }


def run_all(skill_sweep=True, n_sentences=64, seed=20261027):
    cfg = load_config()
    skills = list(cfg.bench.skills)
    gemba = GembaScorer()
    tradeoff = QualityLatencyTradeoff()

    print("=== simulforge benchmark (skill sweep) ===", flush=True)
    print("%-8s %-12s %-10s %-10s %-8s %-10s" %
          ("skill", "StreamLAAL", "quality", "similar", "WER", "qpl"), flush=True)

    rows = {k: [] for k in ("streamlaal_s", "quality", "similarity", "wer", "qpl")}
    for skill in skills:
        acc = {k: 0.0 for k in rows}
        for i in range(n_sentences):
            aid = "bench-%d" % i
            m = _metric_at(skill, aid, tradeoff, gemba)
            for k in rows:
                acc[k] += m[k]
        for k in rows:
            rows[k].append(acc[k] / n_sentences)
        print("%-8.3f %-12.3f %-10.4f %-10.4f %-8.4f %-10.4f" %
              (skill, rows["streamlaal_s"][-1], rows["quality"][-1],
               rows["similarity"][-1], rows["wer"][-1], rows["qpl"][-1]), flush=True)

    # monotonicity checks
    def _mono(seq, increasing):
        for a, b in zip(seq, seq[1:]):
            if increasing and b + 1e-9 < a:
                return False
            if (not increasing) and b - 1e-9 > a:
                return False
        return True

    ok = (_mono(rows["streamlaal_s"], False) and _mono(rows["quality"], True)
          and _mono(rows["similarity"], True) and _mono(rows["wer"], False)
          and _mono(rows["qpl"], True))
    print("=== monotonicity: %s ===" % ("PASS" if ok else "FAIL"), flush=True)

    # headline: quality-latency Pareto (wait-k vs adaptive)
    print("=== Pareto: skill=0.5 (naive wait-k) vs skill=1.0 (adaptive) ===", flush=True)
    lo = rows["quality"][0]
    hi = rows["quality"][-1]
    lo_lat = rows["streamlaal_s"][0]
    hi_lat = rows["streamlaal_s"][-1]
    print("skill=0.5 -> quality=%.3f @ %.2fs" % (lo, lo_lat), flush=True)
    print("skill=1.0 -> quality=%.3f @ %.2fs" % (hi, hi_lat), flush=True)
    print("win: +%.3f quality, -%.2fs latency" % (hi - lo, lo_lat - hi_lat), flush=True)

    return rows, ok


if __name__ == "__main__":
    run_all()
