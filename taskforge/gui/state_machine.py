# -*- coding: utf-8 -*-
"""Cross-app state machine: track which app/screen the agent is on.

Long-horizon computer-use tasks span multiple applications; the state machine
records the current app, last action and the allowed transitions.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class AppState(Enum):
    IDLE = "idle"
    BROWSER = "browser"
    SHEET = "sheet"
    MAIL = "mail"
    DONE = "done"


_TRANSITIONS: Dict[AppState, List[AppState]] = {
    AppState.IDLE: [AppState.BROWSER, AppState.SHEET, AppState.MAIL],
    AppState.BROWSER: [AppState.SHEET, AppState.MAIL, AppState.BROWSER],
    AppState.SHEET: [AppState.MAIL, AppState.SHEET, AppState.BROWSER],
    AppState.MAIL: [AppState.DONE, AppState.MAIL, AppState.SHEET],
    AppState.DONE: [AppState.DONE],
}


@dataclass
class AppStateMachine:
    state: AppState = AppState.IDLE
    history: List[AppState] = None

    def __post_init__(self):
        self.history = self.history or [self.state]

    def can_transition(self, target: AppState) -> bool:
        return target in _TRANSITIONS.get(self.state, [])

    def transition(self, target: AppState) -> bool:
        if not self.can_transition(target):
            return False
        self.state = target
        self.history.append(target)
        return True
