# -*- coding: utf-8 -*-
"""Benchmark registry and runner."""
from __future__ import annotations

from typing import Callable, Dict, List


class _Registry:
    def __init__(self):
        self._items: Dict[str, Callable] = {}

    def register(self, name: str):
        def deco(fn):
            self._items[name] = fn
            return fn
        return deco

    def names(self) -> List[str]:
        return sorted(self._items.keys())

    def get(self, name: str) -> Callable:
        return self._items[name]


BENCHMARKS = _Registry()
register_benchmark = BENCHMARKS.register


def list_benchmarks() -> List[str]:
    return BENCHMARKS.names()


def run_all(cfg, backend, **kw) -> Dict[str, dict]:
    """Run every registered benchmark. Extra kwargs are dispatched per benchmark
    (each benchmark ignores kwargs it does not declare)."""
    results: Dict[str, dict] = {}
    for name in BENCHMARKS.names():
        fn = BENCHMARKS.get(name)
        results[name] = fn(cfg, backend)
    return results
