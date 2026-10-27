# -*- coding: utf-8 -*-
"""Configuration for simulforge.

A plain dataclass plus a minimal YAML loader (falling back to a tiny hand-rolled
parser ``utils/yamlish.py`` because the managed Python runtime has no pyyaml).
Declared scale numbers (30B-A3B, near-3-second StreamLAAL) are informational
only; the reference implementation instantiates tiny tensors so a full
chunk -> transcribe -> translate -> synthesize round-trip completes in
milliseconds of pure Python.
"""
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:  # pragma: no cover - optional
    import yaml as _pyyaml  # type: ignore
except Exception:  # pragma: no cover
    _pyyaml = None


@dataclass
class AudioConfig:
    sample_rate: int = 16000
    frame_ms: int = 25
    hop_ms: int = 10
    chunk_ms: int = 100          # streaming chunk length
    n_mels: int = 40
    n_fft: int = 512


@dataclass
class VadConfig:
    energy_threshold: float = 0.02
    min_speech_ms: int = 300
    min_silence_ms: int = 200


@dataclass
class PolicyConfig:
    default_policy: str = "adaptive"   # waitk | prefix2prefix | adaptive | mma
    waitk: int = 4
    confidence_threshold: float = 0.6
    gamma: float = 1.0                 # target/source length ratio


@dataclass
class CascadeConfig:
    use_cascade: bool = True
    language_pair: str = "zh-en"       # zh-en | en-zh


@dataclass
class S2SConfig:
    direct: bool = False
    embed_dim: int = 32


@dataclass
class LatencyConfig:
    word_seconds: float = 0.5          # nominal seconds per spoken word
    commit_policy: str = "greedy"      # greedy | threshold


@dataclass
class EvalConfig:
    n_sentences: int = 64
    seed: int = 20261027


@dataclass
class ModelConfig:
    dim: int = 32
    vocab: int = 2048
    embed_dim: int = 32
    # declared scale (informational)
    declared_params_b: float = 30.0
    declared_active_b: float = 3.0


@dataclass
class ServingConfig:
    host: str = "127.0.0.1"
    port: int = 8432


@dataclass
class TrainConfig:
    learning_rate: float = 0.3
    max_steps: int = 24
    seed: int = 20261027


@dataclass
class BenchConfig:
    n_sentences: int = 64
    seed: int = 20261027
    skills: tuple = (0.5, 0.625, 0.75, 0.875, 1.0)


@dataclass
class DeclaredConfig:
    project: str = "Hy-SimulMT"
    vendor: str = "Tencent Hunyuan"
    announcement: str = "2026-10-26"
    model: str = "30B-A3B"
    latency_seconds: float = 3.0
    language_pair: str = "Chinese <-> English"
    license: str = "Apache-2.0"

    def to_dict(self):
        return asdict(self)


@dataclass
class Config:
    audio: AudioConfig = field(default_factory=AudioConfig)
    vad: VadConfig = field(default_factory=VadConfig)
    policy: PolicyConfig = field(default_factory=PolicyConfig)
    cascade: CascadeConfig = field(default_factory=CascadeConfig)
    s2s: S2SConfig = field(default_factory=S2SConfig)
    latency: LatencyConfig = field(default_factory=LatencyConfig)
    eval: EvalConfig = field(default_factory=EvalConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    bench: BenchConfig = field(default_factory=BenchConfig)
    declared: DeclaredConfig = field(default_factory=DeclaredConfig)

    @classmethod
    def from_dict(cls, d):
        d = d or {}
        factories = {
            "audio": AudioConfig, "vad": VadConfig, "policy": PolicyConfig,
            "cascade": CascadeConfig, "s2s": S2SConfig, "latency": LatencyConfig,
            "eval": EvalConfig, "model": ModelConfig, "serving": ServingConfig,
            "train": TrainConfig, "bench": BenchConfig, "declared": DeclaredConfig,
        }
        kw = {}
        for key, factory in factories.items():
            sub = d.get(key) or {}
            if key == "bench" and "skills" in sub and not isinstance(sub["skills"], tuple):
                sub = dict(sub)
                sub["skills"] = tuple(x for x in (sub["skills"] or [0.5, 0.625, 0.75, 0.875, 1.0]))
            kw[key] = factory(**{k: v for k, v in sub.items()})
        return cls(**kw)

    def to_dict(self):
        d = asdict(self)
        d["bench"]["skills"] = list(d["bench"]["skills"])
        return d


def load_config(path=None):
    if path is None:
        here = Path(__file__).parent
        path = here / "configs" / "default.yaml"
        if not path.exists():
            path = here.parent / "configs" / "default.yaml"
    p = Path(path)
    if not p.exists():
        return Config()
    text = p.read_text(encoding="utf-8")
    data = None
    if _pyyaml is not None:
        try:
            data = _pyyaml.safe_load(text)
        except Exception:
            data = None
    if data is None:
        from .utils.yamlish import parse
        data = parse(text)
    return Config.from_dict(data)
