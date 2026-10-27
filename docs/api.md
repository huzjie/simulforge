# API

## Python

```python
from simulforge.engine import SimultaneousEngine

engine = SimultaneousEngine(skill=0.8)
result = engine.interpret("audio-id", speaker_id="speaker-id")
# result: transcript, translation, speech, bleu, quality, similarity, latency
```

## CLI

```
python -m simulforge.cli doctor
python -m simulforge.cli interpret my-audio --speaker-id spk-1
python -m simulforge.cli train --steps 24
python -m simulforge.cli bench
python -m simulforge.cli serve --host 0.0.0.0 --port 8432
```

## HTTP

- `GET  /health` -> `{"status": "ok"}`
- `GET  /v1/models`
- `POST /v1/interpret` `{"audio_id": ..., "speaker_id": ...}`
- `POST /v1/interpret/direct`
