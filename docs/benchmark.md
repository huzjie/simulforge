# Benchmark

Run `python -m simulforge.bench` to sweep skill 0.5 -> 1.0 across 64 sentences.

| metric | direction | range |
|--------|-----------|-------|
| StreamLAAL (s) | decreases | 8.0 -> ~2.8 |
| BLEU / quality | increases | ~0.25 -> ~0.9 |
| speaker similarity | increases | ~0.35 -> 1.0 |
| WER (transcript) | decreases | 0.4 -> 0.0 |
| quality-per-latency | increases | Pareto up-left |

Every metric is monotonic in skill by construction, which makes the "better
model = better on *both* axes" claim falsifiable instead of hand-waved.
