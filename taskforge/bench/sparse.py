# -*- coding: utf-8 -*-
"""Benchmark: sparse attention speedup + gold-block recall.

speedup = n_blocks / top_k (architectural, constant); recall = fraction of gold
blocks selected (skill-dependent: random baseline at skill = 0.5, perfect at 1.0).
"""
from __future__ import annotations

from ..sparse.router import BlockRouter
from ..utils.stable import stable_ints
from .registry import register_benchmark


@register_benchmark("sparse")
def run(cfg, backend) -> dict:
    seq_len = cfg.sparse.seq_len
    block_size = cfg.sparse.block_size
    top_k = cfg.sparse.top_k
    n_blocks = (seq_len + block_size - 1) // block_size
    speedup = n_blocks / top_k

    n_seqs = cfg.bench.n_tasks
    gold_count = min(3, n_blocks)
    total_hits = 0
    total_gold = 0
    router = BlockRouter(top_k=top_k)
    for i in range(n_seqs):
        seq_key = "seq-%d" % i
        gold = stable_ints("gold:" + seq_key, gold_count, 0, n_blocks - 1)
        gold = sorted(set(gold))
        selected = router.select(seq_key, n_blocks, gold, backend.skill)
        hits = sum(1 for b in gold if b in selected)
        total_hits += hits
        total_gold += len(gold)
    recall = total_hits / total_gold if total_gold else 0.0
    return {"name": "sparse", "speedup": speedup, "recall": recall,
            "n_blocks": n_blocks, "top_k": top_k}
