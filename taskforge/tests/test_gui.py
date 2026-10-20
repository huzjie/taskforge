# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.gui.agent import GuiAgent
from taskforge.gui.state_machine import AppStateMachine, AppState


class TestGui(unittest.TestCase):
    def test_agent_grounds(self):
        b = get_backend("mock", Config())
        b.skill = 1.0
        agent = GuiAgent(b)
        rec = agent.act("scr-0", "intent-0")
        self.assertTrue(rec["ok"])

    def test_state_machine_transition(self):
        sm = AppStateMachine()
        self.assertTrue(sm.transition(AppState.BROWSER))
        self.assertFalse(sm.transition(AppState.DONE))  # invalid from BROWSER


if __name__ == "__main__":
    unittest.main()
