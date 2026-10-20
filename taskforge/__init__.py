# -*- coding: utf-8 -*-
"""taskforge - long-horizon agent workflow orchestration engine.

A zero-dependency Python reference implementation of the ideas behind MiniMax
M3.1 Flash "Space Bunny": a small-but-capable model that excels at complex,
long-horizon agent tasks via multi-step planning, continuous tool calling,
computer-use (GUI) action grounding, and a sparse-attention inference path that
trades a fraction of compute for large token-efficiency gains.

Core concepts (see docs/ARCHITECTURE.md):
  * planner - decompose a natural-language goal into an ordered subgoal DAG,
    then run a bounded ReAct think/act/observe loop with a thinking budget.
  * tools - schema-bound tool registry with continuous chaining, result
    validation, retry and rollback so a chain keeps moving toward the goal.
  * gui (computer-use) - perceive a synthetic screen (UI element tree), ground
    a natural-language intent to a concrete element + action (click/type/...),
    and track a cross-app state machine.
  * memory - long-horizon working memory: progress tracking, stall detection,
    and recovery so a 20-step workflow does not lose its place.
  * sparse - sparse attention (index branch picks blocks, sparse branch does
    top-k softmax) plus a token/thinking budget for low-latency inference.

Everything is deterministic (md5-seeded) and shares a single oracle so that the
mock backend and every benchmark agree: skill = 0.5 gives a random baseline and
skill = 1.0 gives perfect, reproducible scores.
"""

__version__ = "1.0.0"

from .config import Config, load_config
from .engine import TaskforgeEngine

__all__ = ["Config", "load_config", "TaskforgeEngine", "__version__"]
