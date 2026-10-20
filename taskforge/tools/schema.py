# -*- coding: utf-8 -*-
"""JSON-schema binding for tools, so an agent can call them by name + typed args."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: Dict[str, str] = field(default_factory=dict)   # param -> json type
    required: List[str] = field(default_factory=list)

    def json_schema(self) -> Dict[str, Any]:
        props = {k: {"type": v} for k, v in self.parameters.items()}
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": self.required,
                },
            },
        }


def arg_schema(schema: ToolSchema) -> Dict[str, Any]:
    return schema.json_schema()
