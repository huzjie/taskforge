# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.model.backends import get_backend
from taskforge.train import train


class TestTrain(unittest.TestCase):
    def test_skill_monotonic(self):
        b = get_backend("mock", Config())
        hist = train(b, steps=40)
        self.assertAlmostEqual(hist[0][1], 0.5, places=3)
        self.assertAlmostEqual(hist[-1][1], 1.0, places=3)
        for (_, a), (_, c) in zip(hist, hist[1:]):
            self.assertLessEqual(a, c)


if __name__ == "__main__":
    unittest.main()
