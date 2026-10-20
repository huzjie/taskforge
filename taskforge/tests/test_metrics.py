# -*- coding: utf-8 -*-
import unittest

from taskforge.metrics.cost import estimate_cost
from taskforge.metrics.latency import estimate_latency


class TestMetrics(unittest.TestCase):
    def test_cost_positive(self):
        self.assertGreater(estimate_cost(1000, 1000), 0)

    def test_latency(self):
        self.assertAlmostEqual(estimate_latency(200), 1.0, places=3)


if __name__ == "__main__":
    unittest.main()
