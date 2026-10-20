# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.engine import TaskforgeEngine


class TestEngine(unittest.TestCase):
    def test_run_perfect_skill(self):
        cfg = Config()
        eng = TaskforgeEngine(cfg)
        eng.backend.skill = 1.0
        res = eng.run("goal-0")
        self.assertTrue(res.success)

    def test_run_returns_result(self):
        cfg = Config()
        eng = TaskforgeEngine(cfg)
        res = eng.run("goal-3")
        self.assertIsNotNone(res.plan)
        self.assertGreaterEqual(len(res.steps), 0)


if __name__ == "__main__":
    unittest.main()
