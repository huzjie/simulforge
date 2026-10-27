# Cascade vs direct S2S

- **Cascade** (ASR -> MT -> TTS): inspectable transcript, but errors compound
  across stages and latency adds up.
- **Direct S2S**: speech in, speech out, no explicit transcript. Fewer stages
  means fewer cascaded errors and lower latency, at the cost of no transcript.

simulforge implements both paths; the engine switches on `config.s2s.direct`.
