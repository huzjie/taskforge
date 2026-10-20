# -*- coding: utf-8 -*-
"""Benchmark: multi-step planning success rate.

A goal is "planned correctly" iff the produced plan contains the oracle-required
subgoals in order. At skill = 0.5 each subgoal is gold with p = 0.5, so an
n-step plan succeeds with ~0.5^n; at skill = 1.0 it always succeeds.
"""
from __future__ import annotations

from ..oracle import plan_correct
from .registry import register_benchmark


@register_benchmark("planning")
def run(cfg, backend) -> dict:
    n = cfg.bench.n_tasks
    ok = 0
    for i in range(n):
        goal_id = "goal-%d" % i
        plan = backend.plan(goal_id)
        if plan_correct(goal_id, plan):
            ok += 1
    return {"name": "planning", "success_rate": ok / n, "tasks": n}
