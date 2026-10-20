# -*- coding: utf-8 -*-
import unittest

from taskforge.gui.state_machine import AppStateMachine, AppState


class TestStateMachine(unittest.TestCase):
    def test_full_path(self):
        sm = AppStateMachine()
        self.assertTrue(sm.transition(AppState.BROWSER))
        self.assertTrue(sm.transition(AppState.SHEET))
        self.assertTrue(sm.transition(AppState.MAIL))
        self.assertTrue(sm.transition(AppState.DONE))

    def test_history(self):
        sm = AppStateMachine()
        sm.transition(AppState.BROWSER)
        self.assertEqual(sm.history, [AppState.IDLE, AppState.BROWSER])


if __name__ == "__main__":
    unittest.main()
