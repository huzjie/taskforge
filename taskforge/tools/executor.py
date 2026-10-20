# -*- coding: utf-8 -*-
"""Tool executor: a sandboxed, deterministic executor for the chained tools.

In this zero-dependency reference the "execution" is a deterministic mock that
returns a structured result, but the interface is exactly what a real executor
(subprocess / HTTP / SDK) would expose.
"""
from __future__ import annotations

from typing import Any, Dict


def execute_tool(tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic mock execution of ``tool`` with ``args``."""
    from ..utils.stable import stable_float
    ok = stable_float("exec:" + tool + ":" + str(sorted(args.items())), 0.0, 1.0) < 0.95
    return {
        "tool": tool,
        "args": args,
        "ok": ok,
        "result": {"status": "ok" if ok else "error", "echo": args},
    }


class ToolExecutor:
    def __init__(self, max_calls: int = 64):
        self.max_calls = max_calls
        self.calls = 0

    def run(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if self.calls >= self.max_calls:
            raise RuntimeError("tool call budget exceeded")
        self.calls += 1
        return execute_tool(tool, args)
