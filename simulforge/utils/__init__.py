# -*- coding: utf-8 -*-
"""Utility helpers: deterministic randomness, a minimal YAML parser, metrics, DSP."""
from .random import (stable_float, stable_int, stable_ints, stable_vector,
                     stable_choice, stable_bool)
from .yamlish import parse as parse_yaml
from .metrics import (mean, variance, std, cosine, edit_distance,
                      word_error_rate, bleu)

__all__ = [
    "stable_float", "stable_int", "stable_ints", "stable_vector",
    "stable_choice", "stable_bool", "parse_yaml",
    "mean", "variance", "std", "cosine", "edit_distance",
    "word_error_rate", "bleu",
]
