# -*- coding: utf-8 -*-
"""Top-level orchestration engine: wires planner + tools + gui + memory + sparse."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import Config
from .model.backends import get_backend


@dataclass
class WorkflowResult:
    goal_id: str
    plan: List[str] = field(default_factory=list)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = False
    stall_recoveries: int = 0
    tokens_used: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "plan": self.plan,
            "steps": self.steps,
            "success": self.success,
            "stall_recoveries": self.stall_recoveries,
            "tokens_used": self.tokens_used,
        }


class TaskforgeEngine:
    """Runs a long-horizon workflow end to end for a single goal."""

    def __init__(self, config: Optional[Config] = None, backend_name: Optional[str] = None):
        self.cfg = config or Config()
        name = backend_name or self.cfg.model.backend
        self.backend = get_backend(name, self.cfg)

    def run(self, goal_id: str) -> WorkflowResult:
        from .planner.decompose import decompose
        from .tools.orchestrator import ToolOrchestrator
        from .memory.working import WorkingMemory

        res = WorkflowResult(goal_id=goal_id)
        plan = decompose(self.backend, goal_id, self.cfg.planner)
        res.plan = plan

        mem = WorkingMemory(self.cfg.memory)
        orch = ToolOrchestrator(self.backend, self.cfg.tools)
        for subgoal in plan:
            step = orch.execute(subgoal)
            res.steps.append(step)
            res.tokens_used += step.get("tokens", 0)
            if step.get("ok"):
                mem.mark_progress(subgoal)
            else:
                stall = mem.record_stall(subgoal)
                if stall and self.cfg.memory.recovery_budget > 0:
                    step = orch.execute(subgoal, force_retry=True)
                    res.steps.append(step)
                    res.stall_recoveries += 1
                    if step.get("ok"):
                        mem.mark_progress(subgoal)

        from .oracle import plan_correct, chain_correct
        res.success = plan_correct(goal_id, plan) and all(s.get("ok") for s in res.steps if "ok" in s)
        return res
