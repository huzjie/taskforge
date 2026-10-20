# -*- coding: utf-8 -*-
"""Deterministic synthesis of workflow scenarios.

Every scenario (a goal + its subgoals + the screens/intents a GUI task touches)
is derived from an md5-seeded key so the mock backend and benchmarks agree.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..oracle import goal_subgoals, screen_elements
from ..utils.stable import stable_ints


@dataclass
class Scenario:
    goal_id: str
    subgoals: List[str] = field(default_factory=list)
    screens: List[str] = field(default_factory=list)
    intents: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "goal_id": self.goal_id,
            "subgoals": self.subgoals,
            "screens": self.screens,
            "intents": self.intents,
        }


def synthesize_goal(goal_id: str) -> Scenario:
    sub = goal_subgoals(goal_id)
    n = len(sub)
    screens = ["scr-%s-%d" % (goal_id, i) for i in range(n)]
    intents = ["intent-%s-%d" % (goal_id, i) for i in range(n)]
    return Scenario(goal_id=goal_id, subgoals=sub, screens=screens, intents=intents)


def synthesize_screen(screen_id: str, n: int = 12) -> List[Dict]:
    return screen_elements(screen_id, n)


def synthesize_intent(screen_id: str, intent_id: str) -> Dict:
    idx = stable_ints("synth:intent:" + screen_id + ":" + intent_id, 1, 0, 11)[0]
    return {"screen_id": screen_id, "intent_id": intent_id, "seed": idx}
