# -*- coding: utf-8 -*-
"""SimulMT read/write policies that decide when to emit a target word."""
from .base import Policy, Decision, READ, WRITE
from .waitk import WaitKPolicy
from .prefix2prefix import Prefix2PrefixPolicy
from .adaptive import AdaptivePolicy
from .mma import MonotonicAlignmentPolicy
from .registry import get_policy, list_policies

__all__ = [
    "Policy", "Decision", "READ", "WRITE",
    "WaitKPolicy", "Prefix2PrefixPolicy", "AdaptivePolicy",
    "MonotonicAlignmentPolicy", "get_policy", "list_policies",
]
