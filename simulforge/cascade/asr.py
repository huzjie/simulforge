# -*- coding: utf-8 -*-
"""Streaming automatic speech recognition wrapper.

As audio chunks stream in, the recognizer emits a *partial* transcript that
grows word-by-word. A low-skill recognizer hallucinates tokens; a high-skill one
converges to the reference transcription. The ``partial`` hypothesis is what
feeds the streaming MT stage downstream.
"""


class StreamingASR:
    def __init__(self, model):
        self.model = model
        self.partial = []

    def reset(self):
        self.partial = []

    def feed_chunk(self, audio_id, n_words_read):
        """Return the partial transcript after ``n_words_read`` source words."""
        self.partial = self.model.transcribe_prefix(audio_id, n_words_read)
        return self.partial

    def finalize(self, audio_id):
        self.partial = self.model.transcribe(audio_id)
        return self.partial
