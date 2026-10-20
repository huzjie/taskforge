# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.bench.registry import run_all


class TestBench(unittest.TestCase):
    def test_run_all_five(self):
        cfg = Config()
        b = get_backend("mock", cfg)
        b.skill = 1.0
        results = run_all(cfg, b)
        self.assertEqual(len(results), 5)
        self.assertAlmostEqual(results["planning"]["success_rate"], 1.0, places=3)
        self.assertAlmostEqual(results["tools"]["chain_accuracy"], 1.0, places=3)


if __name__ == "__main__":
    unittest.main()
