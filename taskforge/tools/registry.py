# -*- coding: utf-8 -*-
"""Tool registry: name -> ToolSchema, with a decorator-based registration API."""
from __future__ import annotations

from typing import Callable, Dict, List

from .schema import ToolSchema

_TOOLS: Dict[str, ToolSchema] = {}


def register_tool(schema: ToolSchema):
    _TOOLS[schema.name] = schema
    return schema


class ToolRegistry:
    def __init__(self, tools: List[ToolSchema] = None):
        self._tools: Dict[str, ToolSchema] = dict(_TOOLS)
        for t in (tools or []):
            self._tools[t.name] = t

    def get(self, name: str) -> ToolSchema:
        if name not in self._tools:
            raise KeyError("unknown tool: %s" % name)
        return self._tools[name]

    def names(self) -> List[str]:
        return sorted(self._tools.keys())

    def __len__(self) -> int:
        return len(self._tools)


# Seed the default tools (browser.*, sheet.*, email, slack, code, file, api) so
# the registry and the integrations are non-empty out of the box.
def _seed_default_tools():
    from ..oracle import TOOLS
    for t in TOOLS:
        if t not in _TOOLS:
            register_tool(ToolSchema(
                name=t,
                description="Deterministic mock execution of %s" % t,
                parameters={"subgoal": "string", "target": "string", "mode": "string"},
                required=["subgoal"],
            ))


_seed_default_tools()
