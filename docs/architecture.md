# Architecture

simulforge is organized as a small set of composable, pure-Python packages. Each
layer is deterministic and shares a single oracle, so every benchmark is
reproducible bit-for-bit.

```
audio chunks ──> VAD ──> streaming ASR ──> streaming MT ──> streaming TTS ──> speech
                              │                 │                 │
                              └─── policy (read/write) decides when to commit ───┘
                                                     │
                                              LatencyManager (AL / LAAL / StreamLAAL)
```

## Layers

| Layer       | Package      | Responsibility |
|-------------|--------------|----------------|
| Audio       | `audio`      | chunking, VAD, frame features, resampling |
| Policy      | `policy`     | wait-k / prefix-to-prefix / adaptive / MMA read-write decisions |
| Cascade     | `cascade`    | streaming ASR -> MT -> TTS pipeline |
| Direct S2S  | `s2s`        | speech-to-speech without an explicit transcript |
| Latency     | `latency`    | AL / LAAL / StreamLAAL, commit & revision bookkeeping |
| Evaluation  | `eval`       | BLEU, GEMBA-style quality, WER, quality-latency tradeoff |
| Models      | `model`      | deterministic trainable mock backends |
| Engine      | `engine.py`  | `SimultaneousEngine` integration point |

## Design principles

1. **Single oracle.** All mock backends and benchmarks score against one source
   of truth (`oracle.py`), so "cross-stage consistency" is a guarantee, not a hope.
2. **Deterministic randomness.** Every random value is md5-keyed, so a run is
   identical across machines and Python versions.
3. **Monotone training.** `skill += lr * (1 - skill)` climbs monotonically; every
   metric moves monotonically with skill (quality up, latency down).
4. **Zero dependencies.** Only the standard library is used, so the managed
   Python runtime stays self-contained.
