# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend, list_backends


class TestBackends(unittest.TestCase):
    def test_five_backends(self):
        names = list_backends()
        for expected in ("mock", "openai", "vllm", "transformers", "anthropic"):
            self.assertIn(expected, names)

    def test_mock_plan_length(self):
        b = get_backend("mock", Config())
        plan = b.plan("goal-0")
        self.assertTrue(3 <= len(plan) <= 6)

    def test_mock_skill_perfect_plan(self):
        b = get_backend("mock", Config())
        b.skill = 1.0
        from taskforge.oracle import goal_subgoals, plan_correct
        self.assertTrue(plan_correct("goal-0", b.plan("goal-0")))

    def test_unknown_backend(self):
        with self.assertRaises(ValueError):
            get_backend("nope", Config())


if __name__ == "__main__":
    unittest.main()
