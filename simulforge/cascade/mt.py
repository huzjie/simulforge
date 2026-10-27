# -*- coding: utf-8 -*-
"""Streaming machine translation wrapper.

Takes the (possibly partial, noisy) transcript and emits a partial translation.
The reference translation is keyed by the same ``audio_id``, so quality can be
scored against a single source of truth downstream.
"""


class StreamingMT:
    def __init__(self, model):
        self.model = model
        self.partial = []

    def reset(self):
        self.partial = []

    def feed(self, audio_id, transcript_tokens):
        """Return a partial translation for the given partial transcript."""
        self.partial = self.model.translate_prefix(audio_id, len(transcript_tokens))
        return self.partial

    def finalize(self, audio_id):
        self.partial = self.model.translate(audio_id)
        return self.partial
