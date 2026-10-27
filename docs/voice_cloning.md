# Voice cloning

Real-time voice cloning embeds the source speaker's voice, then conditions the
TTS on that embedding so the *translated* speech keeps the speaker's timbre.

The mock TTS blends the reference embedding with noise, weighted by skill:

```
hyp = boost * ref + (1 - boost) * noise
similarity = cosine(ref, hyp)
```

At `skill = 0.5` (`boost = 0`) the output is essentially random; at `skill = 1.0`
(`boost = 1`) it reproduces the reference embedding exactly (similarity = 1.0).
