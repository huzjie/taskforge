# -*- coding: utf-8 -*-
"""Train the mock backend: skill climbs monotonically 0.5 -> 1.0.

The training signal is intentionally simple and monotonic (the iron rule):
each step nudges skill up by a constant amount, and every benchmark metric that
depends on skill therefore climbs monotonically too. There is no "correct/incorrect"
random walk that could push skill back down.
"""
from __future__ import annotations

from typing import List, Tuple

from .config import Config
from .model.backends import get_backend


def train(backend, steps: int = 40, lr: float = 0.02) -> List[Tuple[int, float]]:
    history: List[Tuple[int, float]] = [(0, backend.skill)]
    for step in range(1, steps + 1):
        backend.skill = min(1.0, backend.skill + lr)
        history.append((step, backend.skill))
    return history


def train_and_report(cfg: Config = None):
    cfg = cfg or Config()
    backend = get_backend(cfg.model.backend, cfg)
    before = backend.skill
    history = train(backend)
    after = backend.skill
    print("[train] skill %.4f -> %.4f (%d steps)" % (before, after, len(history) - 1))
    return history
