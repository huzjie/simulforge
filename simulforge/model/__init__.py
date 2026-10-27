# -*- coding: utf-8 -*-
"""Deterministic trainable mock backends (ASR / MT / TTS / S2S)."""
from .base import MockModel, boost
from .asr_model import AsrModel
from .mt_model import MtModel
from .tts_model import TtsModel
from .s2s_model import S2sModel

__all__ = ["MockModel", "boost", "AsrModel", "MtModel", "TtsModel", "S2sModel"]
