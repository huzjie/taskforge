# -*- coding: utf-8 -*-
"""Sparse attention: index branch + sparse branch.

full_attention computes O(n^2) attention over the whole sequence; sparse_attention
splits the sequence into blocks, selects top-k blocks via the router, and computes
softmax only over those blocks. The speedup is ~ n_blocks / top_k.
"""
from __future__ import annotations

import math
from typing import List

from ..utils.stable import stable_vector


def _softmax(xs: List[float]) -> List[float]:
    m = max(xs)
    ex = [math.exp(x - m) for x in xs]
    s = sum(ex)
    return [e / s for e in ex]


def full_attention(q: List[float], keys: List[List[float]]) -> List[float]:
    scores = [sum(a * b for a, b in zip(q, k)) for k in keys]
    return _softmax(scores)


def sparse_attention(q: List[float], keys: List[List[float]],
                     block_size: int, top_k: int, gold_blocks: List[int],
                     skill: float, seq_key: str = "seq") -> List[float]:
    n = len(keys)
    n_blocks = (n + block_size - 1) // block_size
    from .router import BlockRouter
    router = BlockRouter(top_k=top_k)
    selected = router.select(seq_key, n_blocks, gold_blocks, skill)
    # gather selected blocks
    gathered: List[float] = []
    for b in selected:
        start = b * block_size
        end = min(start + block_size, n)
        for k in keys[start:end]:
            gathered.append(sum(a * bb for a, bb in zip(q, k)))
    if not gathered:
        return []
    return _softmax(gathered)
