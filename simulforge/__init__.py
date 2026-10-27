# -*- coding: utf-8 -*-
"""simulforge - an end-to-end streaming speech-to-speech simultaneous interpretation engine.

A pure-Python, zero-dependency reference implementation of the ideas behind
Tencent Hunyuan's open-sourced simultaneous interpretation model **Hy-SimulMT**
(30B-A3B, Apache-2.0, announced 2026-10-26): real-time speech-to-speech
translation between Chinese and English with near-3-second StreamLAAL latency and
real-time voice cloning that preserves the speaker's timbre.

The composable pieces:

  * audio      - streaming chunking, energy VAD, frame features (mel / ZCR).
  * policy     - SimulMT read/write policies: wait-k, prefix-to-prefix,
                 confidence-adaptive, monotonic-multihead-alignment (MMA).
  * cascade    - the classic 3-stage pipeline: streaming ASR -> streaming MT ->
                 streaming TTS (with speaker embedding).
  * s2s        - the direct speech-to-speech path and voice cloning.
  * latency    - average lagging (AL), length-adaptive AL, StreamLAAL, commit /
                 revision bookkeeping.
  * eval       - StreamLAAL latency, BLEU, GEMBA-style quality, WER, and the
                 quality-latency Pareto tradeoff.
  * model      - deterministic trainable mock backends (ASR/MT/TTS/S2S) whose
                 ``skill`` sweeps monotonically from random to perfect.
  * engine     - the high-level ``SimultaneousEngine`` tying it all together.

Everything is deterministic (md5-seeded) and shares a single oracle. ``skill =
0.5`` is an untrained configuration and ``skill = 1.0`` is the perfect one, so
every benchmark sweeps monotonically from a random baseline to the optimum.
"""

__version__ = "1.0.0"

from .config import Config, load_config

__all__ = ["Config", "load_config", "__version__"]
