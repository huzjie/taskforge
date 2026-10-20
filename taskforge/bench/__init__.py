# -*- coding: utf-8 -*-
"""Benchmarks: planning / tools / gui / sparse / longhorizon.

Importing this package triggers registration of all benchmarks via the
@BENCHMARKS.register decorators in the submodules below.
"""
from .registry import BENCHMARKS, register_benchmark, list_benchmarks, run_all
from . import planning, tools, gui, sparse, longhorizon  # noqa: F401

__all__ = ["BENCHMARKS", "register_benchmark", "list_benchmarks", "run_all"]
