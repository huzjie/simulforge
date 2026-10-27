# -*- coding: utf-8 -*-
"""Direct speech-to-speech path and voice cloning."""
from .embedding import speaker_embed, embed_similarity
from .direct import DirectS2S
from .clone import VoiceCloner

__all__ = ["speaker_embed", "embed_similarity", "DirectS2S", "VoiceCloner"]
