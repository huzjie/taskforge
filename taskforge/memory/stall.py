# -*- coding: utf-8 -*-
"""Stall detection: count consecutive failures per subgoal, flag recovery."""
from __future__ import annotations

from typing import Dict


class StallDetector:
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.counts: Dict[str, int] = {}

    def register(self, subgoal: str) -> bool:
        self.counts[subgoal] = self.counts.get(subgoal, 0) + 1
        return self.counts[subgoal] >= self.threshold

    def reset(self, subgoal: str) -> None:
        self.counts[subgoal] = 0
