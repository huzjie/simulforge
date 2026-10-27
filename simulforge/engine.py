# -*- coding: utf-8 -*-
"""The high-level ``SimultaneousEngine`` that ties policy + cascade + latency.

It exposes a single ``interpret`` method: feed an audio utterance id and get
back the transcript, translation, synthesized speech, and the full
quality/latency profile. The engine is the integration point the CLI and HTTP
server both drive.
"""
from .config import Config, load_config
from .oracle import sentence, translation
from .policy import get_policy
from .model import AsrModel, MtModel, TtsModel, S2sModel
from .cascade import StreamingASR, StreamingMT, StreamingTTS, CascadePipeline
from .s2s import DirectS2S
from .latency import LatencyManager
from .eval import GembaScorer, QualityLatencyTradeoff


class SimultaneousEngine:
    def __init__(self, skill=0.5, cfg=None):
        self.skill = skill
        self.cfg = cfg or load_config()
        self.asr = AsrModel(skill=skill, vocab=self.cfg.model.vocab)
        self.mt = MtModel(skill=skill, vocab=self.cfg.model.vocab)
        self.tts = TtsModel(skill=skill, vocab=self.cfg.model.vocab,
                            embed_dim=self.cfg.s2s.embed_dim)
        self.s2s = S2sModel(skill=skill, vocab=self.cfg.model.vocab,
                            embed_dim=self.cfg.s2s.embed_dim)
        self.policy = get_policy(self.cfg.policy.default_policy, self.cfg.policy)
        self.cascade_pipeline = CascadePipeline(
            StreamingASR(self.asr), StreamingMT(self.mt), StreamingTTS(self.tts))
        self.direct = DirectS2S(self.s2s)
        self.latency = LatencyManager(self.cfg.latency.word_seconds)
        self.gemba = GembaScorer()
        self.tradeoff = QualityLatencyTradeoff()

    # -- confidence model ------------------------------------------------
    def confidence(self, audio_id, source_read, target_written):
        """Deterministic confidence that rises with skill and read-ahead.

        A higher-skill model is confident sooner (higher baseline), so an
        adaptive policy writes earlier -> lower latency. Before any source word
        is heard the confidence is zero (you cannot translate what you have not
        heard yet).
        """
        if source_read <= 0:
            return 0.0
        base = 0.20 + 0.35 * self.skill
        slope = 0.06
        val = base + slope * (source_read - target_written)
        return max(0.0, min(1.0, val))

    # -- interpretation --------------------------------------------------
    def interpret(self, audio_id, speaker_id=None, direct=None):
        """Run a full streaming interpretation and return the profile."""
        speaker_id = speaker_id or audio_id
        if direct is None:
            direct = self.cfg.s2s.direct

        src = sentence(audio_id)
        tgt = translation(audio_id)
        source_len = len(src)
        target_len = len(tgt)

        read_times, _ = self.latency.build_read_times(
            source_len, target_len, self.policy,
            lambda sr, tw: self.confidence(audio_id, sr, tw))
        latency_profile = self.latency.measure(read_times, target_len, source_len)

        if direct:
            s2s_out = self.direct.run(audio_id, speaker_id)
            transcript = None
            hyp_translation = tgt  # reference, direct path has no explicit MT
            speech = s2s_out["speech"]
            similarity = s2s_out["similarity"]
        else:
            cascade_out = self.cascade_pipeline.run(audio_id, speaker_id)
            transcript = cascade_out["transcript"]
            hyp_translation = cascade_out["translation"]
            speech = cascade_out["speech"]["speech"]
            similarity = cascade_out["speech"]["similarity"]

        bleu = self._bleu(tgt, hyp_translation)
        quality = self.gemba.score(audio_id, (self.skill - 0.5) * 2.0)

        return {
            "audio_id": audio_id,
            "speaker_id": speaker_id,
            "source_len": source_len,
            "target_len": target_len,
            "transcript": transcript,
            "translation": hyp_translation,
            "speech": speech,
            "similarity": similarity,
            "latency": latency_profile,
            "bleu": bleu,
            "quality": quality,
            "direct": direct,
            "policy": self.policy.describe(),
            "skill": self.skill,
        }

    @staticmethod
    def _bleu(ref, hyp):
        from .utils.metrics import bleu
        return bleu([(ref, hyp)])

    # -- training --------------------------------------------------------
    def train_step(self, lr=None):
        lr = lr if lr is not None else self.cfg.train.learning_rate
        self.asr.train_step(lr)
        self.mt.train_step(lr)
        self.tts.train_step(lr)
        self.s2s.train_step(lr)
        self.skill = self.asr.skill
        return self.skill

    def doctor(self):
        """Quick self-check: run one interpretation and summarize."""
        r = self.interpret("doctor-sample", speaker_id="doctor-spk")
        return r


def build_engine(skill=0.5, config_path=None):
    return SimultaneousEngine(skill=skill, cfg=load_config(config_path))
