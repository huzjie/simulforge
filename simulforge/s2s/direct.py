# -*- coding: utf-8 -*-
"""Direct speech-to-speech (S2S) path.

Skips the explicit transcript/translation intermediate: audio in one language is
mapped straight to audio in the other. This removes two stages of cascaded error
and latency, at the cost of not having an inspectable transcript. The mock model
produces deterministic speech features plus a quality/similarity profile that
improves monotonically with skill.
"""


class DirectS2S:
    def __init__(self, model):
        self.model = model

    def run(self, audio_id, speaker_id=None):
        return self.model.translate_speech(audio_id, speaker_id or audio_id)
