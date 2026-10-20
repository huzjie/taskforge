# -*- coding: utf-8 -*-
"""Benchmark: long-horizon workflow completion, with and without stall recovery.

Each step succeeds with p = 0.5 + 0.5*boost. Naive completion = product of per-step
success; recovery completion reruns failed steps (with the same p), which lifts the
effective per-step success to p + (1-p)*p. Demonstrates the memory/stall-recovery win.
"""
from __future__ import annotations

from ..utils.stable import stable_bool
from .registry import register_benchmark


def _step_ok(key: str, skill: float) -> bool:
    boost = (skill - 0.5) * 2.0
    return stable_bool(key, p=0.5 + 0.5 * boost)


@register_benchmark("longhorizon")
def run(cfg, backend) -> dict:
    horizon = cfg.bench.horizon
    n_episodes = cfg.bench.episodes * 4

    naive_ok = 0
    recover_ok = 0
    for e in range(n_episodes):
        naive = True
        recover = True
        for s in range(horizon):
            key = "lh:%d:%d" % (e, s)
            ok = _step_ok(key, backend.skill)
            naive = naive and ok
            if not ok:
                ok2 = _step_ok(key + ":r", backend.skill)
                recover = recover and ok2
            else:
                recover = recover and ok
        naive_ok += 1 if naive else 0
        recover_ok += 1 if recover else 0

    return {
        "name": "longhorizon",
        "naive_completion": naive_ok / n_episodes,
        "recovery_completion": recover_ok / n_episodes,
        "horizon": horizon,
        "episodes": n_episodes,
    }
