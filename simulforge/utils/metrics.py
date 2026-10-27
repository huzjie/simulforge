# -*- coding: utf-8 -*-
"""Numeric helpers: statistics, cosine, edit distance (WER), BLEU."""
import math


def mean(xs):
    if not xs:
        return 0.0
    return sum(xs) / len(xs)


def variance(xs):
    if not xs:
        return 0.0
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def std(xs):
    return math.sqrt(variance(xs))


def cosine(a, b, eps=1e-9):
    if not a or not b:
        return 0.0
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(x * x for x in b))
    if da < eps or db < eps:
        return 0.0
    return num / (da * db)


def edit_distance(a, b):
    """Levenshtein distance between two sequences (of hashable items)."""
    la, lb = len(a), len(b)
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def word_error_rate(ref, hyp):
    """Word error rate in [0, 1]; 0 == perfect, 1 == totally wrong."""
    if not ref:
        return 0.0 if not hyp else 1.0
    return min(1.0, edit_distance(ref, hyp) / len(ref))


def _ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def bleu(pairs, max_n=2):
    """Corpus BLEU over a list of (reference, hypothesis) token lists.

    Uses n-gram precision for n in 1..max_n with a simple brevity penalty.
    Returns a float in [0, 1].
    """
    if not pairs:
        return 0.0
    precisions = []
    for n in range(1, max_n + 1):
        matched = 0
        total = 0
        for r, h in pairs:
            rn = _ngrams(r, n)
            hn = _ngrams(h, n)
            if not hn:
                continue
            total += len(hn)
            counts = {}
            for g in rn:
                counts[g] = counts.get(g, 0) + 1
            for g in hn:
                if counts.get(g, 0) > 0:
                    matched += 1
                    counts[g] -= 1
        precisions.append(matched / total if total else 0.0)
    geo = 1.0
    for p in precisions:
        geo *= (p if p > 0 else 1e-9)
    geo = geo ** (1.0 / max_n)
    ref_len = sum(len(r) for r, _ in pairs)
    hyp_len = sum(len(h) for _, h in pairs)
    bp = 1.0 if hyp_len >= ref_len else math.exp(1.0 - ref_len / max(1, hyp_len))
    return bp * geo
