# -*- coding: utf-8 -*-
"""Voice cloning: reproduce a speaker's timbre on translated speech.

Real-time voice cloning (as in Hy-SimulMT) embeds the source speaker's voice,
then conditions the TTS on that embedding so the *translated* speech keeps the
speaker's tone. The cloner here exposes the embedding and a similarity metric.
"""


class VoiceCloner:
    def __init__(self, dim=32):
        self.dim = dim

    def embed(self, speaker_id):
        from ..oracle import speaker_embedding
        return speaker_embedding(speaker_id, self.dim)

    def similarity(self, speaker_id, synthesized_embed):
        from ..utils.metrics import cosine
        return cosine(self.embed(speaker_id), synthesized_embed)
