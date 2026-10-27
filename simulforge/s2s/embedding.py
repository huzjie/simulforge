# -*- coding: utf-8 -*-
"""Speaker embeddings and similarity.

A reference speaker embedding is a unit vector from the oracle. The similarity
between a synthesized voice and the reference embedding is the cosine of their
vectors. A high-skill model reproduces the embedding almost exactly (similarity
~1.0); a low-skill model is essentially random (similarity ~noise).
"""
from ..utils.metrics import cosine
from ..oracle import speaker_embedding


def speaker_embed(speaker_id, dim=32):
    return speaker_embedding(speaker_id, dim)


def embed_similarity(vec_a, vec_b):
    return cosine(vec_a, vec_b)
