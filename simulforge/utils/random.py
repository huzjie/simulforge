# -*- coding: utf-8 -*-
"""Deterministic pseudo-randomness keyed by string (md5-seeded).

Every helper derives an 8-byte seed from md5(key), so the same key always
produces the same value. This is what makes the mock backends, the oracle and
every benchmark agree bit-for-bit.
"""
import hashlib
import random


def _seed(key):
    h = hashlib.md5(str(key).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big")


def _rng(key):
    return random.Random(_seed(key))


def stable_float(key, lo=0.0, hi=1.0):
    return lo + (hi - lo) * _rng(key).random()


def stable_int(key, lo, hi):
    return _rng(key).randint(lo, hi - 1)


def stable_ints(key, n, lo, hi, distinct=False):
    r = _rng(key)
    if distinct:
        return r.sample(range(lo, hi), min(n, max(0, hi - lo)))
    return [r.randint(lo, hi - 1) for _ in range(n)]


def stable_vector(key, n, lo=-1.0, hi=1.0):
    r = _rng(key)
    return [lo + (hi - lo) * r.random() for _ in range(n)]


def stable_choice(key, items):
    r = _rng(key)
    return items[r.randrange(len(items))]


def stable_bool(key, p=0.5):
    return _rng(key).random() < p
