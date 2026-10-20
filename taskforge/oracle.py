# -*- coding: utf-8 -*-
"""Shared ground truth for the mock backend and every benchmark.

Both the mock backend and the benchmarks derive correctness from the SAME
deterministic functions, so a fully-trained skill (skill = 1.0) yields score 1.0
and a random skill (0.5) yields the random baseline. This single source of truth
keeps every reported number reproducible and monotonic.

Vocabulary (deterministic, seeded by md5):
  * subgoals - the generic steps of a business workflow (search/open/read/...).
  * tools    - the concrete tools an agent can chain (browser.*, sheet.*, ...).
  * actions  - the GUI primitives a computer-use agent can emit.
  * element types - the UI controls present on a synthetic screen.
"""
from __future__ import annotations

from typing import Dict, List

SUBGOALS = [
    "search", "open", "read", "extract", "transform",
    "fill", "submit", "verify", "close",
]

TOOLS = [
    "browser.open", "browser.search", "browser.click",
    "sheet.read", "sheet.write", "email.send",
    "slack.post", "code.run", "file.save", "api.call",
]

ACTIONS = ["click", "type", "scroll", "press", "drag", "hover"]

ELEMENT_TYPES = ["button", "input", "link", "menu", "checkbox", "dropdown"]


def _stable_ints(key: str, n: int, lo: int, hi: int) -> List[int]:
    from .utils.stable import stable_ints
    return stable_ints(key, n, lo, hi)


def goal_subgoals(goal_id: str) -> List[str]:
    """Deterministically derive the ordered subgoals a goal requires.

    The order matters: executing the subgoals in the correct order is what a
    correct plan does, which is exactly what the planner/benchmark checks.
    """
    n = 3 + (_stable_ints("goal:len:" + goal_id, 1, 0, 3)[0] % 4)   # 3..6
    idxs = _stable_ints("goal:subs:" + goal_id, n, 0, len(SUBGOALS) - 1)
    seen = set()
    out = []
    for i in idxs:
        if i not in seen:
            seen.add(i)
            out.append(SUBGOALS[i])
    return out


def subgoal_tool(subgoal: str) -> str:
    """Deterministic tool that realizes a given subgoal."""
    idx = SUBGOALS.index(subgoal) if subgoal in SUBGOALS else 0
    return TOOLS[idx % len(TOOLS)]


def tool_args(subgoal: str) -> Dict[str, str]:
    """Deterministic argument payload for a subgoal's tool call."""
    return {"subgoal": subgoal, "target": subgoal + "-resource", "mode": "auto"}


def plan_correct(goal_id: str, plan: List[str]) -> bool:
    """A plan is correct iff it performs ``goal_subgoals(goal_id)`` in order
    (extra steps are allowed as long as the required sequence is a subsequence)."""
    required = goal_subgoals(goal_id)
    if not required:
        return True
    it = iter(plan)
    return all(any(p == x for x in it) for p in required)


def chain_correct(subgoal: str, tool: str, args: Dict[str, str]) -> bool:
    """A tool chain step is correct iff the right tool is used with plausible args."""
    if tool != subgoal_tool(subgoal):
        return False
    return isinstance(args, dict) and args.get("subgoal") == subgoal


def screen_elements(screen_id: str, n: int = 12) -> List[Dict]:
    """Deterministically synthesize the UI element tree of a screen."""
    elems = []
    for i in range(n):
        etype = ELEMENT_TYPES[i % len(ELEMENT_TYPES)]
        x = _stable_ints("scr:x:" + screen_id, 1, 0, 1279)[0] if False else (i * 97 + 40) % 1240
        y = (i * 61 + 30) % 770
        elems.append({
            "id": "%s-e%d" % (screen_id, i),
            "type": etype,
            "label": "%s-%d" % (etype, i),
            "bbox": [x, y, x + 80, y + 28],
        })
    return elems


def target_element(screen_id: str, intent_id: str, elements: List[Dict]) -> Dict:
    """Deterministic target element an intent should act on."""
    idx = _stable_ints("intent:tgt:" + screen_id + ":" + intent_id, 1, 0, len(elements) - 1)[0]
    return elements[idx]


def ground_correct(screen_id: str, intent_id: str, element_id: str, action: str) -> bool:
    """A grounded action is correct iff it hits the target element with a legal action."""
    elements = screen_elements(screen_id)
    target = target_element(screen_id, intent_id, elements)
    return element_id == target["id"] and action in ACTIONS
