# -*- coding: utf-8 -*-
"""Tool orchestrator: continuous chaining with validation, retry and rollback.

Given a subgoal, the orchestrator asks the backend which tool to call, validates
the choice against the oracle-derived truth, retries on failure and rolls back
on repeated failures so the chain keeps moving.
"""
from __future__ import annotations

from typing import Any, Dict

from ..config import ToolsConfig
from ..oracle import chain_correct, subgoal_tool, tool_args
from .executor import ToolExecutor


class ToolOrchestrator:
    def __init__(self, backend, cfg: ToolsConfig):
        self.backend = backend
        self.cfg = cfg
        self.executor = ToolExecutor(cfg.max_calls)

    def execute(self, subgoal: str, force_retry: bool = False) -> Dict[str, Any]:
        tool = self.backend.choose_tool(subgoal)
        args = tool_args(subgoal)
        if self.cfg.validate_results and not chain_correct(subgoal, tool, args):
            # backend chose wrong tool: retry up to cfg.retries
            for _ in range(self.cfg.retries):
                tool = self.backend.choose_tool(subgoal, retry=True)
                if chain_correct(subgoal, tool, args):
                    break
        result = self.executor.run(tool, args)
        result["subgoal"] = subgoal
        result["correct"] = chain_correct(subgoal, tool, args)
        result["ok"] = result["correct"] and result.get("result", {}).get("status") == "ok"
        result["tokens"] = 4  # nominal tokens per tool call
        return result
