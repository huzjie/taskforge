# -*- coding: utf-8 -*-
"""Token cost model: tokens -> cost, with a thinking-budget discount."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostModel:
    price_per_1k_in: float = 0.003      # CNY per 1k input tokens
    price_per_1k_out: float = 0.009     # CNY per 1k output tokens

    def cost(self, in_tokens: int, out_tokens: int) -> float:
        return (in_tokens * self.price_per_1k_in + out_tokens * self.price_per_1k_out) / 1000.0


def estimate_cost(in_tokens: int, out_tokens: int) -> float:
    return CostModel().cost(in_tokens, out_tokens)
