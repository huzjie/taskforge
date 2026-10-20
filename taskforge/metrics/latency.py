# -*- coding: utf-8 -*-
"""Latency / throughput model for sparse attention inference."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LatencyModel:
    tokens_per_second: int = 200          # P50 decode throughput
    prefill_tps: int = 1200

    def decode_time(self, n_tokens: int) -> float:
        return n_tokens / self.tokens_per_second

    def prefill_time(self, n_tokens: int) -> float:
        return n_tokens / self.prefill_tps


def estimate_latency(n_decode: int, n_prefill: int = 0) -> float:
    m = LatencyModel()
    return m.decode_time(n_decode) + m.prefill_time(n_prefill)
