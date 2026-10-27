# -*- coding: utf-8 -*-
"""Mock MT: translate the source sentence (full or prefix) with skill noise."""
from .base import MockModel
from ..oracle import translation


class MtModel(MockModel):
    def translate(self, audio_id):
        ref = translation(audio_id)
        return self._noisy_copy("mt:%s" % audio_id, ref)

    def translate_prefix(self, audio_id, n_words):
        ref = translation(audio_id)
        # map a source-prefix length to a proportional target-prefix length
        src_len = len(__import__("simulforge.oracle", fromlist=["sentence"]).sentence(audio_id))
        frac = min(1.0, n_words / src_len) if src_len else 0.0
        n = int(round(len(ref) * frac))
        return self._noisy_copy("mt:%s" % audio_id, ref[:n])
