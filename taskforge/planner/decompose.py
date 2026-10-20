# -*- coding: utf-8 -*-
"""Goal decomposition: natural-language goal -> ordered subgoal sequence/DAG.

The mock backend emits a plan where each position is the gold subgoal with
probability ``p = 0.5 + 0.5*boost`` (boost = (skill - 0.5) * 2) and a wrong
subgoal otherwise. skill = 0.5 -> random baseline, skill = 1.0 -> perfect plan.
"""
from __future__ import annotations

from typing import List

from ..config import PlannerConfig
from ..oracle import SUBGOALS, goal_subgoals


def decompose(backend, goal_id: str, cfg: PlannerConfig) -> List[str]:
    if cfg.decompose_mode == "dag":
        return decompose_dag(backend, goal_id, cfg)
    return _linear(backend, goal_id, cfg)


def decompose_dag(backend, goal_id: str, cfg: PlannerConfig) -> List[str]:
    """DAG decomposition is linearized into an executable topological order here
    (the reference planner keeps it ordered; see docs for the DAG model)."""
    return _linear(backend, goal_id, cfg)


def _linear(backend, goal_id: str, cfg: PlannerConfig) -> List[str]:
    plan = backend.plan(goal_id)
    if len(plan) > cfg.max_steps:
        return plan[: cfg.max_steps]
    return plan


def required_subgoals(goal_id: str) -> List[str]:
    return goal_subgoals(goal_id)


def plan_matches(goal_id: str, plan: List[str]) -> bool:
    from ..oracle import plan_correct
    return plan_correct(goal_id, plan)
