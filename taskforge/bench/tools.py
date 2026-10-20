# -*- coding: utf-8 -*-
"""Benchmark: continuous tool-chaining accuracy.

Each subgoal must select the correct tool; accuracy = fraction of correct choices.
"""
from __future__ import annotations

from ..oracle import SUBGOALS, chain_correct, tool_args
from .registry import register_benchmark


@register_benchmark("tools")
def run(cfg, backend) -> dict:
    ok = 0
    total = 0
    for subgoal in SUBGOALS:
        tool = backend.choose_tool(subgoal)
        if chain_correct(subgoal, tool, tool_args(subgoal)):
            ok += 1
        total += 1
    return {"name": "tools", "chain_accuracy": ok / total, "tools": total}
