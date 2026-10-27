# -*- coding: utf-8 -*-
"""Policy registry: map a policy name to a configured instance."""
from .waitk import WaitKPolicy
from .prefix2prefix import Prefix2PrefixPolicy
from .adaptive import AdaptivePolicy
from .mma import MonotonicAlignmentPolicy


def get_policy(name, cfg=None):
    """Return a policy instance by name, using ``cfg`` (PolicyConfig) if given."""
    name = (name or "adaptive").lower()
    cfg = cfg or _Dummy()
    waitk = getattr(cfg, "waitk", 4)
    thr = getattr(cfg, "confidence_threshold", 0.6)
    if name == "waitk":
        return WaitKPolicy(k=waitk)
    if name == "prefix2prefix":
        return Prefix2PrefixPolicy(k=waitk)
    if name == "mma":
        return MonotonicAlignmentPolicy(threshold=0.5)
    return AdaptivePolicy(threshold=thr)


def list_policies():
    return ["waitk", "prefix2prefix", "adaptive", "mma"]


class _Dummy:
    waitk = 4
    confidence_threshold = 0.6
