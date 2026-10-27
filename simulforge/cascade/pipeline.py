# -*- coding: utf-8 -*-
"""The streaming cascade pipeline: ASR -> MT -> TTS.

Ties the three stages together and exposes a ``run`` method that, given an audio
utterance, returns the transcript, translation, and synthesized speech along
with the quality/latency profile used for evaluation.
"""


class CascadePipeline:
    def __init__(self, asr, mt, tts):
        self.asr = asr
        self.mt = mt
        self.tts = tts

    def run(self, audio_id, speaker_id=None):
        """Full cascade: transcribe -> translate -> synthesize."""
        transcript = self.asr.finalize(audio_id)
        translation = self.mt.finalize(audio_id)
        speech = self.tts.synthesize(audio_id, speaker_id or audio_id,
                                     translation)
        return {
            "audio_id": audio_id,
            "transcript": transcript,
            "translation": translation,
            "speech": speech,
        }
