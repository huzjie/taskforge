# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.planner.decompose import decompose
from taskforge.planner.budget import ThinkingBudget


class TestPlanner(unittest.TestCase):
    def test_decompose_returns_ordered(self):
        b = get_backend("mock", Config())
        plan = decompose(b, "goal-0", Config().planner)
        self.assertTrue(len(plan) >= 3)

    def test_budget_decays(self):
        tb = ThinkingBudget(total=2048)
        alloc = tb.allocate(8)
        self.assertEqual(len(alloc), 8)
        self.assertTrue(all(a > 0 for a in alloc))


if __name__ == "__main__":
    unittest.main()
