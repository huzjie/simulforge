# -*- coding: utf-8 -*-
"""Base class and shared decision enum for SimulMT policies.

A policy answers a single question at every step of streaming translation:
"given how much of the source I have read, how much of the target I have
written, and my current confidence, should I READ one more source word or WRITE
one more target word?"  That read/write sequence fully determines the latency.
"""

READ = "READ"
WRITE = "WRITE"


class Decision:
    def __init__(self, action, confidence=1.0):
        self.action = action
        self.confidence = confidence

    def __repr__(self):
        return "Decision(%s, conf=%.3f)" % (self.action, self.confidence)


class Policy:
    name = "base"

    def decide(self, source_read, source_len, target_written, target_len,
               confidence):
        raise NotImplementedError

    def describe(self):
        return self.name
