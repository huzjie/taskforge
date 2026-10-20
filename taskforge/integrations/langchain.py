# -*- coding: utf-8 -*-
"""Export the tool registry as LangChain-compatible tools (best-effort)."""
from __future__ import annotations

from typing import List

from ..tools.registry import ToolRegistry


def to_langchain_tools(registry: ToolRegistry = None) -> List[dict]:
    registry = registry or ToolRegistry()
    out = []
    for name in registry.names():
        schema = registry.get(name)
        out.append({
            "name": name,
            "description": schema.description,
            "parameters": schema.parameters,
        })
    return out
