# -*- coding: utf-8 -*-
"""Screen model: a synthetic UI element tree the agent perceives."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..oracle import screen_elements


@dataclass
class Screen:
    screen_id: str
    elements: List[Dict] = field(default_factory=list)

    def element(self, element_id: str) -> Dict:
        for e in self.elements:
            if e["id"] == element_id:
                return e
        raise KeyError("element not found: %s" % element_id)

    def to_dict(self) -> Dict:
        return {"screen_id": self.screen_id, "elements": self.elements}


def screen_from_id(screen_id: str, n: int = 12) -> Screen:
    return Screen(screen_id=screen_id, elements=screen_elements(screen_id, n))
