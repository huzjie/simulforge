# -*- coding: utf-8 -*-
"""Streaming text-to-speech wrapper with speaker identity.

Synthesizes translated text into speech features while preserving the original
speaker's timbre (voice cloning). Returns deterministic speech features plus a
speaker-similarity score that rises monotonically with skill.
"""


class StreamingTTS:
    def __init__(self, model):
        self.model = model

    def synthesize(self, audio_id, speaker_id, text_tokens):
        return self.model.synthesize(audio_id, speaker_id, text_tokens)
