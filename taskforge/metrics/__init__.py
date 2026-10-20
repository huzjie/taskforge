# -*- coding: utf-8 -*-
"""Cost / latency / throughput metrics for a flash-class model."""
from .cost import CostModel, estimate_cost
from .latency import LatencyModel, estimate_latency

__all__ = ["CostModel", "estimate_cost", "LatencyModel", "estimate_latency"]
