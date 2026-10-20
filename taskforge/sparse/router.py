# -*- coding: utf-8 -*-
"""Block router: low-rank index branch that scores blocks O(n * rank).

The router predicts which blocks matter, so the sparse branch only computes
softmax over the top-k blocks. The mock router ranks gold blocks above noise when
the model skill is high (boost = (skill - 0.5) * 2).
"""
from __future__ import annotations

from typing import List

from ..utils.stable import stable_float


def block_scores(seq_key: str, n_blocks: int, gold_blocks: List[int], skill: float) -> List[float]:
    """Deterministic block scores; gold blocks get boosted by skill."""
    boost = (skill - 0.5) * 2.0
    scores = []
    for b in range(n_blocks):
        base = stable_float("blk:" + seq_key + ":" + str(b), 0.0, 1.0)
        if b in gold_blocks:
            base += boost
        scores.append(base)
    return scores


class BlockRouter:
    def __init__(self, top_k: int = 4):
        self.top_k = top_k

    def select(self, seq_key: str, n_blocks: int, gold_blocks: List[int], skill: float) -> List[int]:
        scores = block_scores(seq_key, n_blocks, gold_blocks, skill)
        order = sorted(range(n_blocks), key=lambda i: scores[i], reverse=True)
        return order[: self.top_k]
