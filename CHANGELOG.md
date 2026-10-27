# Changelog

All notable changes to simulforge are documented here.

## [1.0.0] - 2026-10-27

### Added

- Streaming audio front-end: fixed/adaptive chunking, energy VAD, frame features
  (mel filterbank + zero-crossing rate), linear resampler.
- SimulMT read/write policies: wait-k, prefix-to-prefix, confidence-adaptive, MMA.
- Cascade pipeline (streaming ASR -> MT -> TTS) and direct S2S path.
- Voice cloning via deterministic speaker embeddings.
- Latency metrics: Average Lagging, Length-Adaptive AL, StreamLAAL.
- Evaluation: BLEU, GEMBA-style quality, WER, quality-latency tradeoff.
- Deterministic trainable mock backends (ASR/MT/TTS/S2S) with monotone skill.
- Zero-dependency HTTP serving + CLI + 57 unit tests + 8 examples + docs + prompts.
