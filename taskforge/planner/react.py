# -*- coding: utf-8 -*-
"""ReAct loop: think -> act -> observe, bounded by a thinking budget."""
from __future__ import annotations

from typing import List, Tuple

from ..config import PlannerConfig


def react_loop(backend, goal_id: str, cfg: PlannerConfig,
               observe) -> List[Tuple[str, object]]:
    """Run a bounded ReAct loop.

    ``observe`` is a callable ``(action) -> observation`` supplied by the caller.
    Returns the list of (action, observation) trace.
    """
    trace: List[Tuple[str, object]] = []
    for _ in range(cfg.react_max_iters):
        thought = backend.think(goal_id, trace)
        if thought is None:
            break
        action = thought.get("action", "stop")
        if action == "stop":
            break
        obs = observe(action)
        trace.append((action, obs))
    return trace
