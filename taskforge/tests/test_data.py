# -*- coding: utf-8 -*-
import unittest

from taskforge.data.synth import synthesize_goal
from taskforge.data.tasks import TASK_TEMPLATES, render_goal


class TestData(unittest.TestCase):
    def test_synthesize_goal(self):
        sc = synthesize_goal("goal-0")
        self.assertTrue(3 <= len(sc.subgoals) <= 6)
        self.assertEqual(len(sc.screens), len(sc.subgoals))

    def test_templates(self):
        self.assertGreater(len(TASK_TEMPLATES), 3)
        self.assertIn("整理", render_goal("sales_report"))
        self.assertEqual(render_goal("unknown_key"), TASK_TEMPLATES["sales_report"])


if __name__ == "__main__":
    unittest.main()
