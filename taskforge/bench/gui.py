# -*- coding: utf-8 -*-
"""Benchmark: GUI action grounding accuracy (OSWorld-style).

For each (screen, intent) the agent must hit the target element with a legal
action. Accuracy = fraction of correctly grounded intents.
"""
from __future__ import annotations

from ..oracle import ground_correct
from .registry import register_benchmark


@register_benchmark("gui")
def run(cfg, backend) -> dict:
    n = cfg.bench.n_tasks
    ok = 0
    for i in range(n):
        screen_id = "scr-%d" % i
        intent_id = "intent-%d" % i
        from ..oracle import screen_elements
        elements = screen_elements(screen_id, cfg.gui.n_elements)
        element_id, action = backend.ground(screen_id, intent_id, elements)
        if ground_correct(screen_id, intent_id, element_id, action):
            ok += 1
    return {"name": "gui", "grounding_accuracy": ok / n, "intents": n}
