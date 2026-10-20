# -*- coding: utf-8 -*-
"""GUI agent: perceive -> ground -> act -> update state machine."""
from __future__ import annotations

from typing import Dict, List

from ..oracle import ground_correct
from .grounding import ground_intent
from .screen import screen_from_id
from .state_machine import AppStateMachine, AppState


class GuiAgent:
    def __init__(self, backend, n_elements: int = 12):
        self.backend = backend
        self.n_elements = n_elements
        self.sm = AppStateMachine()
        self.trace: List[Dict] = []

    def act(self, screen_id: str, intent_id: str) -> Dict:
        screen = screen_from_id(screen_id, self.n_elements)
        element_id, action = ground_intent(self.backend, screen_id, intent_id)
        ok = ground_correct(screen_id, intent_id, element_id, action)
        # heuristic app transition from action semantics
        if action in ("type", "click") and ok:
            self.sm.transition(AppState.SHEET if "sheet" in screen_id else AppState.BROWSER)
        record = {"screen": screen_id, "intent": intent_id, "element": element_id,
                  "action": action, "ok": ok}
        self.trace.append(record)
        return record
