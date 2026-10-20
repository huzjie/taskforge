# -*- coding: utf-8 -*-
"""Uniform backend interface + 5 registered backends.

Every backend exposes:
  * plan(goal_id) -> List[str]                 (goal decomposition)
  * choose_tool(subgoal, retry=False) -> str   (tool chaining)
  * ground(screen_id, intent_id, elements) -> (element_id, action)
  * think(goal_id, trace) -> dict|None         (ReAct thought)
  * next_token(ids) -> int                     (token generation)

The mock backend is deterministic: each decision hits the gold answer with
probability ``p = 0.5 + 0.5*boost`` where ``boost = (skill - 0.5) * 2``. This is the
iron rule that makes skill = 0.5 the random baseline and skill = 1.0 perfect.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from ..config import Config
from ..oracle import (
    ACTIONS, SUBGOALS, TOOLS, goal_subgoals, subgoal_tool,
    screen_elements, target_element,
)
from ..utils.stable import stable_bool, stable_float, stable_ints

_BACKENDS: Dict[str, type] = {}


def register_backend(name: str):
    def deco(cls):
        _BACKENDS[name] = cls
        return cls
    return deco


def list_backends() -> List[str]:
    return sorted(_BACKENDS.keys())


def _hit(key: str, skill: float) -> bool:
    """Core decision primitive: gold with p = 0.5 + 0.5*boost, boost=(skill-0.5)*2."""
    boost = (skill - 0.5) * 2.0
    return stable_bool(key, p=0.5 + 0.5 * boost)


class _BaseBackend:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.skill = 0.5

    def plan(self, goal_id: str) -> List[str]:
        raise NotImplementedError

    def choose_tool(self, subgoal: str, retry: bool = False) -> str:
        raise NotImplementedError

    def ground(self, screen_id: str, intent_id: str, elements: List[Dict]) -> Tuple[str, str]:
        raise NotImplementedError

    def think(self, goal_id: str, trace) -> Dict:
        return {"action": "stop"}

    def next_token(self, ids) -> int:
        return 0


@register_backend("mock")
class MockBackend(_BaseBackend):
    def __init__(self, cfg: Config):
        super().__init__(cfg)
        self.skill = 0.5

    def plan(self, goal_id: str) -> List[str]:
        required = goal_subgoals(goal_id)
        plan = []
        for i, gold in enumerate(required):
            key = "plan:%s:%d" % (goal_id, i)
            if _hit(key, self.skill):
                plan.append(gold)
            else:
                wrong = SUBGOALS[(SUBGOALS.index(gold) + 1 + i) % len(SUBGOALS)]
                plan.append(wrong)
        return plan

    def choose_tool(self, subgoal: str, retry: bool = False) -> str:
        key = "tool:%s:%s" % (subgoal, "r" if retry else "n")
        if _hit(key, self.skill):
            return subgoal_tool(subgoal)
        idx = TOOLS.index(subgoal_tool(subgoal)) if subgoal_tool(subgoal) in TOOLS else 0
        return TOOLS[(idx + 1) % len(TOOLS)]

    def ground(self, screen_id: str, intent_id: str, elements: List[Dict]) -> Tuple[str, str]:
        target = target_element(screen_id, intent_id, elements)
        key = "gnd:%s:%s" % (screen_id, intent_id)
        if _hit(key, self.skill):
            element_id = target["id"]
        else:
            others = [e for e in elements if e["id"] != target["id"]]
            element_id = others[stable_ints("gnd-alt:" + intent_id, 1, 0, len(others) - 1)[0]]["id"]
        action = ACTIONS[stable_ints("gnd-act:" + intent_id, 1, 0, len(ACTIONS) - 1)[0]]
        return element_id, action

    def next_token(self, ids) -> int:
        return stable_ints("tok:" + str(ids)[:40], 1, 0, 99)[0]


@register_backend("openai")
class OpenAIBackend(_BaseBackend):
    """Stub delegating to a mock core; swap in a real SDK by setting cfg.model.model_id."""
    def __init__(self, cfg: Config):
        super().__init__(cfg)
        self._mock = MockBackend(cfg)

    def plan(self, goal_id: str) -> List[str]:
        return self._mock.plan(goal_id)

    def choose_tool(self, subgoal: str, retry: bool = False) -> str:
        return self._mock.choose_tool(subgoal, retry)

    def ground(self, screen_id: str, intent_id: str, elements: List[Dict]) -> Tuple[str, str]:
        return self._mock.ground(screen_id, intent_id, elements)


@register_backend("vllm")
class VllmBackend(OpenAIBackend):
    pass


@register_backend("transformers")
class TransformersBackend(OpenAIBackend):
    pass


@register_backend("anthropic")
class AnthropicBackend(OpenAIBackend):
    pass


def get_backend(name: str, cfg: Config):
    if name not in _BACKENDS:
        raise ValueError("unknown backend %r (available: %s)" % (name, list_backends()))
    return _BACKENDS[name](cfg)
