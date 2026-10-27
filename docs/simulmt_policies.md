# SimulMT policies

A simultaneous-translation policy answers one question each step: **READ** one
more source word, or **WRITE** one more target word? That sequence fully
determines latency.

## wait-k

Read `k` source words, then alternate. Average lagging is essentially `k`.
Larger `k` = more context = higher quality but higher latency.

## prefix-to-prefix

Keep the source/target *prefix ratio* aligned (plus a lag `k`). Better for
language pairs with very different word rates (Chinese is compact, English is
wordy).

## confidence-adaptive

Write only when the model's confidence in the current hypothesis exceeds a
threshold. A better model is confident sooner, so it writes earlier — lower
latency *without* sacrificing quality. This is the mechanism behind
Hy-SimulMT's near-3-second StreamLAAL.

## monotonic multihead attention (MMA)

Learns a hard-monotonic alignment: emit a target word once attention energy for
the next source word exceeds a learned threshold.

## Why this matters

A policy is just a function `(source_read, target_written, confidence) -> action`.
Swapping policies changes only latency, not the model — which is what lets you
tune a deployment for latency-first or quality-first with a one-line config.
