# -*- coding: utf-8 -*-
"""Mock ASR: transcribe source audio (full or prefix) with skill noise."""
from .base import MockModel
from ..oracle import sentence


class AsrModel(MockModel):
    def transcribe(self, audio_id):
        ref = sentence(audio_id)
        return self._noisy_copy("asr:%s" % audio_id, ref)

    def transcribe_prefix(self, audio_id, n_words):
        ref = sentence(audio_id)
        n = max(0, min(int(n_words), len(ref)))
        return self._noisy_copy("asr:%s" % audio_id, ref[:n])
