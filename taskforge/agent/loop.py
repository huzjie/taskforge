# -*- coding: utf-8 -*-
"""High-level agent loop with metrics + security hooks over the engine."""
from __future__ import annotations

from typing import Dict

from ..config import Config
from ..engine import TaskforgeEngine
from ..metrics.cost import estimate_cost
from ..security.audit import audit_code


class Agent:
    def __init__(self, config: Config = None):
        self.cfg = config or Config()
        self.engine = TaskforgeEngine(self.cfg)

    def run(self, goal_id: str) -> Dict:
        res = self.engine.run(goal_id)
        cost = estimate_cost(res.tokens_used, res.tokens_used)
        return {
            "result": res.to_dict(),
            "cost_cny": round(cost, 4),
            "backend": self.cfg.model.backend,
        }


def run_agent(goal_id: str, config: Config = None) -> Dict:
    return Agent(config).run(goal_id)
