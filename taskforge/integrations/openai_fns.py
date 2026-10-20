# -*- coding: utf-8 -*-
"""Export the tool registry as OpenAI function-calling JSON schemas."""
from __future__ import annotations

from typing import List

from ..tools.registry import ToolRegistry


def to_openai_functions(registry: ToolRegistry = None) -> List[dict]:
    registry = registry or ToolRegistry()
    return [registry.get(name).json_schema() for name in registry.names()]
