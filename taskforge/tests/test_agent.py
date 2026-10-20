# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.agent.loop import Agent


class TestAgent(unittest.TestCase):
    def test_run(self):
        cfg = Config()
        a = Agent(cfg)
        a.engine.backend.skill = 1.0
        out = a.run("goal-0")
        self.assertTrue(out["result"]["success"])

    def test_run_agent_fn(self):
        from taskforge.agent.loop import run_agent
        cfg = Config()
        out = run_agent("goal-1", cfg)
        self.assertIn("cost_cny", out)


if __name__ == "__main__":
    unittest.main()
