# -*- coding: utf-8 -*-
"""Mock TTS: synthesize translated text into speech features with a cloned voice.

Returns ``(speech_features, synthesized_embed, similarity)``. The speaker
similarity rises monotonically with skill: a high-skill synthesizer reproduces
the reference embedding almost exactly.
"""
from .base import MockModel
from ..oracle import speaker_embedding
from ..utils.random import stable_vector, stable_float
from ..utils.metrics import cosine


class TtsModel(MockModel):
    def __init__(self, skill=0.5, vocab=2048, embed_dim=32):
        super().__init__(skill=skill, vocab=vocab)
        self.embed_dim = embed_dim

    def synthesize(self, audio_id, speaker_id, text_tokens):
        n_feats = max(16, len(text_tokens) * 8)
        speech = stable_vector("tts:%s" % audio_id, n_feats, -1.0, 1.0)
        ref = speaker_embedding(speaker_id, self.embed_dim)
        # blend the reference embedding with noise; skill decides the mix
        noise = stable_vector("tts-emb:%s" % audio_id, self.embed_dim, -1.0, 1.0)
        hyp = [self.b * r + (1.0 - self.b) * n for r, n in zip(ref, noise)]
        norm = (sum(x * x for x in hyp) ** 0.5) or 1.0
        hyp = [x / norm for x in hyp]
        similarity = cosine(ref, hyp)
        return {"speech": speech, "embed": hyp, "similarity": similarity}
