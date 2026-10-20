# -*- coding: utf-8 -*-
import unittest

from taskforge.planner.budget import ThinkingBudget


class TestBudget(unittest.TestCase):
    def test_alloc_sum_le_total(self):
        tb = ThinkingBudget(total=2048)
        alloc = tb.allocate(10)
        self.assertLessEqual(sum(alloc), 2048)

    def test_tokens_used(self):
        tb = ThinkingBudget(total=1000)
        tb.allocate(5)
        self.assertEqual(tb.tokens_used(), 1000 - tb.remaining)


if __name__ == "__main__":
    unittest.main()
