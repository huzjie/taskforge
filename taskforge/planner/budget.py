# -*- coding: utf-8 -*-
"""Thinking budget: allocate the limited reasoning tokens across steps.

A flash-class model wins on cost/efficiency by spending thinking tokens only
where they pay off. The budget is spent per step and shrinks for late steps.
"""
from __future__ import annotations

from typing import List


class ThinkingBudget:
    def __init__(self, total: int = 2048, decay: float = 0.85):
        self.total = total
        self.remaining = total
        self.decay = decay

    def allocate(self, n_steps: int) -> List[int]:
        """Split the remaining budget across ``n_steps`` with geometric decay."""
        out = []
        share = max(1, self.remaining // max(1, n_steps))
        for _ in range(n_steps):
            out.append(share)
            share = max(1, int(share * self.decay))
        self.remaining = max(0, self.remaining - sum(out))
        return out

    def tokens_used(self) -> int:
        return self.total - self.remaining
