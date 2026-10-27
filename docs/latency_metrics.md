# Latency metrics

- **Average Lagging (AL)** = `(1/tau) sum_i (g_i - (i-1)/gamma)`, where `g_i` is
  the number of source words read when committing target word `i`, and `gamma` is
  the target/source length ratio. Lower is better.
- **Length-Adaptive AL (LAAL)** normalizes AL by target length.
- **StreamLAAL** is LAAL expressed in *seconds* (multiply by seconds-per-word).
  This is the metric Hy-SimulMT reports (~3s on the RealSI long-audio benchmark).

The `latency` package computes these from a policy's read/write trace via
`LatencyManager`.
