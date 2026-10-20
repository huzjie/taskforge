# -*- coding: utf-8 -*-
"""Working memory: track which subgoals are done, detect stalls, allow recovery.

Long-horizon workflows (20+ steps) lose their place without a scratchpad; this
module is that scratchpad, plus a stall counter that triggers bounded recovery.
"""
from __future__ import annotations

from typing import Dict, List

from ..config import MemoryConfig
from .stall import StallDetector


class WorkingMemory:
    def __init__(self, cfg: MemoryConfig):
        self.cfg = cfg
        self.progress: List[str] = []
        self.stall = StallDetector(cfg.stall_threshold)
        self.recoveries = 0

    def mark_progress(self, subgoal: str) -> None:
        if len(self.progress) >= self.cfg.capacity:
            self.progress.pop(0)
        self.progress.append(subgoal)
        self.stall.reset(subgoal)

    def record_stall(self, subgoal: str) -> bool:
        """Record a failed step; return True when recovery should be triggered."""
        return self.stall.register(subgoal)

    def done(self) -> List[str]:
        return list(self.progress)

    def snapshot(self) -> Dict:
        return {"progress": list(self.progress), "stalls": self.stall.counts}
