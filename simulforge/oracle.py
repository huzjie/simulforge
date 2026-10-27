# -*- coding: utf-8 -*-
"""Single source of truth shared by the mock models and every benchmark.

The oracle answers deterministic questions:

  * ``sentence(audio_id)``      -- the true source sentence (list of word ids).
  * ``translation(audio_id)``   -- the true target translation (list of word ids).
  * ``speaker_embedding(spk)``  -- the true speaker embedding vector.
  * ``reference_audio(audio_id)`` -- deterministic PCM samples for a source sentence.
  * ``gold_waitk(audio_id)``    -- the optimal wait-k for a sentence.

Keeping the truth in one place is what makes "quality improves and latency drops
monotonically with skill" testable: every mock backend scores against the *same*
reference instead of re-deriving its own.
"""
from .utils.random import stable_int, stable_ints, stable_vector, stable_float


def sentence(audio_id):
    """Deterministic source sentence as a list of word tokens (int ids)."""
    n = stable_int("slen:" + str(audio_id), 6, 12)
    return stable_ints("src:" + str(audio_id), n, 0, 2048)


def translation(audio_id):
    """Reference translation as a list of word tokens (int ids)."""
    src = sentence(audio_id)
    m = max(1, int(len(src) * 0.9 + 0.5))
    return stable_ints("tgt:" + str(audio_id), m, 0, 2048)


def speaker_embedding(speaker_id, dim=32):
    """Deterministic reference speaker embedding (unit vector)."""
    v = stable_vector("spk:" + str(speaker_id), dim, -1.0, 1.0)
    norm = sum(x * x for x in v) ** 0.5 or 1.0
    return [x / norm for x in v]


def reference_audio(audio_id, sample_rate=16000, seconds=2.0):
    """Deterministic PCM waveform (list of floats) for a source utterance."""
    n = int(sample_rate * seconds)
    return stable_vector("audio:" + str(audio_id), n, -0.9, 0.9)


def gold_waitk(audio_id):
    """The optimal wait-k for a sentence (used by the policy benchmark)."""
    return stable_int("gold-k:" + str(audio_id), 1, 5)


def length_ratio(audio_id):
    """Target/source length ratio gamma (deterministic, near 1.0)."""
    return 0.85 + stable_float("gamma:" + str(audio_id), 0.0, 0.3)
