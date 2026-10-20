# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.tools.orchestrator import ToolOrchestrator
from taskforge.tools.registry import ToolRegistry


class TestTools(unittest.TestCase):
    def test_registry_seeded(self):
        reg = ToolRegistry()
        self.assertGreater(len(reg), 5)

    def test_orchestrator_executes(self):
        b = get_backend("mock", Config())
        b.skill = 1.0
        orch = ToolOrchestrator(b, Config().tools)
        step = orch.execute("search")
        self.assertIn("ok", step)


if __name__ == "__main__":
    unittest.main()
