# -*- coding: utf-8 -*-
"""Mock direct S2S: speech in -> speech out (no explicit transcript)."""
from .base import MockModel
from ..oracle import speaker_embedding
from ..utils.random import stable_vector
from ..utils.metrics import cosine


class S2sModel(MockModel):
    def __init__(self, skill=0.5, vocab=2048, embed_dim=32):
        super().__init__(skill=skill, vocab=vocab)
        self.embed_dim = embed_dim

    def translate_speech(self, audio_id, speaker_id):
        speech = stable_vector("s2s:%s" % audio_id, 64, -1.0, 1.0)
        ref = speaker_embedding(speaker_id, self.embed_dim)
        noise = stable_vector("s2s-emb:%s" % audio_id, self.embed_dim, -1.0, 1.0)
        hyp = [self.b * r + (1.0 - self.b) * n for r, n in zip(ref, noise)]
        norm = (sum(x * x for x in hyp) ** 0.5) or 1.0
        hyp = [x / norm for x in hyp]
        similarity = cosine(ref, hyp)
        return {"speech": speech, "embed": hyp, "similarity": similarity,
                "transcript": None}
