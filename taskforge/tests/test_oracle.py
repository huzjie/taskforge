# -*- coding: utf-8 -*-
import unittest

from taskforge.oracle import (
    SUBGOALS, TOOLS, goal_subgoals, subgoal_tool, plan_correct,
    chain_correct, screen_elements, ground_correct,
)


class TestOracle(unittest.TestCase):
    def test_goal_subgoals_deterministic(self):
        a = goal_subgoals("goal-0")
        b = goal_subgoals("goal-0")
        self.assertEqual(a, b)
        self.assertTrue(3 <= len(a) <= 6)

    def test_plan_correct_perfect(self):
        req = goal_subgoals("goal-1")
        self.assertTrue(plan_correct("goal-1", req))

    def test_plan_correct_wrong_order(self):
        req = goal_subgoals("goal-1")
        self.assertFalse(plan_correct("goal-1", list(reversed(req))))

    def test_subgoal_tool(self):
        self.assertIn(subgoal_tool("search"), TOOLS)

    def test_chain_correct(self):
        s = "search"
        self.assertTrue(chain_correct(s, subgoal_tool(s), {"subgoal": s}))

    def test_ground_correct(self):
        elements = screen_elements("scr-0", 12)
        from taskforge.oracle import target_element
        tgt = target_element("scr-0", "intent-0", elements)
        self.assertTrue(ground_correct("scr-0", "intent-0", tgt["id"], "click"))
        self.assertFalse(ground_correct("scr-0", "intent-0", "nope", "click"))


if __name__ == "__main__":
    unittest.main()
