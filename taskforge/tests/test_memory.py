# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.memory.working import WorkingMemory
from taskforge.memory.stall import StallDetector


class TestMemory(unittest.TestCase):
    def test_stall_triggers_recovery(self):
        d = StallDetector(threshold=3)
        self.assertFalse(d.register("x"))
        self.assertFalse(d.register("x"))
        self.assertTrue(d.register("x"))

    def test_working_memory_progress(self):
        m = WorkingMemory(Config().memory)
        m.mark_progress("search")
        m.mark_progress("open")
        self.assertEqual(m.done(), ["search", "open"])


if __name__ == "__main__":
    unittest.main()
